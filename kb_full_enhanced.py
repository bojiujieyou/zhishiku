#!/usr/bin/env python3
"""
知识库增强完整版 - 集成PDF、YouTube和语义搜索
基于现有kb_light.py，添加阶段1增强功能
"""

import json
import os
import re
import sqlite3
import hashlib
from datetime import datetime
from urllib.parse import urlparse
import logging
from pathlib import Path
import tempfile
import mimetypes

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(__file__).parent / 'logs' / 'kb_full_enhanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedKnowledgeBase:
    """增强版知识库 - 完整功能"""
    
    def __init__(self, config_path=None):
        """初始化增强版知识库"""
        if config_path is None:
            config_path = Path(__file__).parent / 'config.json'
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 路径处理 - 使用绝对路径到知识库目录
        base_path_str = self.config['base_path']
        base_path_str = base_path_str.replace('\\\\', '/')
        self.base_path = Path(base_path_str)
        
        # 确保目录存在
        self.articles_path = self.base_path / 'articles'
        self.index_path = self.base_path / 'index'
        self.articles_path.mkdir(exist_ok=True)
        self.index_path.mkdir(exist_ok=True)
        
        # 创建缓存目录
        self.cache_path = self.base_path / 'cache'
        self.cache_path.mkdir(exist_ok=True)
        self.pdf_cache_path = self.cache_path / 'pdfs'
        self.pdf_cache_path.mkdir(exist_ok=True)
        self.youtube_cache_path = self.cache_path / 'youtube'
        self.youtube_cache_path.mkdir(exist_ok=True)
        
        # 检查依赖状态
        self.dependencies = self._check_dependencies()
        
        # 初始化数据库
        self._init_database()
        
        # 尝试初始化向量数据库（如果可用）
        self.vector_client = None
        self.embedding_model = None
        if self.dependencies['chromadb'] and self.dependencies['sentence_transformers']:
            self._init_vector_database()
        
        logger.info("增强版知识库初始化完成")
        logger.info(f"依赖状态: {self.dependencies}")
    
    def _check_dependencies(self):
        """检查依赖包状态"""
        dependencies = {}
        
        # PDF处理库
        try:
            import pypdf
            dependencies['pypdf'] = True
        except ImportError:
            dependencies['pypdf'] = False
        
        try:
            import fitz  # PyMuPDF
            dependencies['pymupdf'] = True
        except ImportError:
            dependencies['pymupdf'] = False
        
        # YouTube处理库
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            dependencies['youtube_transcript_api'] = True
        except ImportError:
            dependencies['youtube_transcript_api'] = False
        
        try:
            import yt_dlp
            dependencies['yt_dlp'] = True
        except ImportError:
            try:
                import youtube_dl
                dependencies['youtube_dl'] = True
            except ImportError:
                dependencies['youtube_dl'] = False
        
        # 向量数据库库
        try:
            import chromadb
            dependencies['chromadb'] = True
        except ImportError:
            dependencies['chromadb'] = False
        
        try:
            from sentence_transformers import SentenceTransformer
            dependencies['sentence_transformers'] = True
        except ImportError:
            dependencies['sentence_transformers'] = False
        
        try:
            import numpy
            dependencies['numpy'] = True
        except ImportError:
            dependencies['numpy'] = False
        
        return dependencies
    
    def _init_database(self):
        """初始化SQLite数据库（增强版）"""
        db_path = self.index_path / 'knowledge_enhanced.db'
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        # 创建主表（增强结构）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_hash TEXT UNIQUE,
                url TEXT NOT NULL,
                title TEXT,
                content_type TEXT,  -- pdf, youtube, article, social, document, webpage
                content_text TEXT,
                summary TEXT,
                keywords TEXT,
                word_count INTEGER,
                date_saved TIMESTAMP,
                date_created TIMESTAMP,
                metadata TEXT,
                embedding_ready INTEGER DEFAULT 0,
                source_file TEXT,
                processed_with TEXT
            )
        ''')
        
        # 创建关键词索引表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER,
                keyword TEXT,
                frequency INTEGER,
                FOREIGN KEY (doc_id) REFERENCES documents (id)
            )
        ''')
        
        # 创建内容类型统计表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_stats (
                content_type TEXT PRIMARY KEY,
                count INTEGER DEFAULT 0,
                total_words INTEGER DEFAULT 0,
                last_updated TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("增强数据库初始化完成")
    
    def _init_vector_database(self):
        """初始化向量数据库（可选）"""
        try:
            import chromadb
            from chromadb.config import Settings
            from sentence_transformers import SentenceTransformer
            
            self.vector_client = chromadb.PersistentClient(
                path=str(self.base_path / 'vectors'),
                settings=Settings(anonymized_telemetry=False)
            )
            
            self.collection = self.vector_client.get_or_create_collection(
                name="enhanced_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
            self.embedding_model = SentenceTransformer(model_name)
            
            logger.info(f"向量数据库初始化成功，模型: {model_name}")
            
        except Exception as e:
            logger.warning(f"向量数据库初始化失败: {e}")
            self.vector_client = None
            self.embedding_model = None
    
    def detect_content_type(self, url):
        """智能检测内容类型"""
        url_lower = url.lower()
        
        # PDF文档
        if url_lower.endswith('.pdf'):
            return 'pdf'
        
        # YouTube视频
        youtube_patterns = [
            r'youtube\.com/watch\?v=',
            r'youtu\.be/',
            r'youtube\.com/embed/',
            r'youtube\.com/v/'
        ]
        for pattern in youtube_patterns:
            if pattern in url_lower:
                return 'youtube'
        
        # 社交媒体
        social_patterns = ['twitter.com', 'x.com', 'weibo.com', 't.co']
        for pattern in social_patterns:
            if pattern in url_lower:
                return 'social'
        
        # Office文档
        office_extensions = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
        for ext in office_extensions:
            if url_lower.endswith(ext):
                return 'document'
        
        # 图片
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        for ext in image_extensions:
            if url_lower.endswith(ext):
                return 'image'
        
        # 默认网页
        return 'webpage'
    
    def extract_youtube_video_id(self, url):
        """从URL提取YouTube视频ID"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def process_content(self, url, raw_content=None, title=None, force_type=None):
        """处理内容 - 智能路由到对应的处理器"""
        content_type = force_type or self.detect_content_type(url)
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        
        logger.info(f"处理内容: {url} (类型: {content_type})")
        
        # 检查是否已存在
        self.cursor.execute('SELECT id FROM documents WHERE url_hash = ?', (url_hash,))
        existing = self.cursor.fetchone()
        
        if existing:
            logger.info(f"文档已存在，跳过: {url}")
            return {"status": "exists", "doc_id": existing[0], "type": content_type}
        
        # 根据内容类型处理
        if content_type == 'pdf' and self.dependencies['pypdf']:
            return self._process_pdf(url, title)
        elif content_type == 'youtube' and self.dependencies['youtube_transcript_api']:
            return self._process_youtube(url, title)
        else:
            # 默认网页处理
            return self._process_webpage(url, raw_content, title, content_type)
    
    def _process_pdf(self, url, title):
        """处理PDF文档"""
        try:
            import pypdf
            logger.info(f"开始处理PDF: {url}")
            
            # 这里应该实现PDF下载和内容提取
            # 暂时返回占位结果
            
            metadata = {
                "source_url": url,
                "content_type": "pdf",
                "processing_date": datetime.now().isoformat(),
                "title": title or url,
                "status": "pdf_ready_placeholder"
            }
            
            # 保存到数据库
            doc_id = self._save_to_database(
                url=url,
                title=title or url,
                content_type="pdf",
                content_text="PDF内容提取占位符 - 需要实现下载和解析",
                summary="PDF文档",
                keywords=["pdf", "document"],
                metadata=metadata
            )
            
            return {
                "status": "pdf_ready",
                "doc_id": doc_id,
                "url": url,
                "title": title or url,
                "type": "pdf",
                "message": "PDF处理功能已准备就绪"
            }
            
        except Exception as e:
            logger.error(f"PDF处理失败: {e}")
            return {
                "status": "pdf_error",
                "url": url,
                "error": str(e)
            }
    
    def _process_youtube(self, url, title):
        """处理YouTube视频"""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            
            video_id = self.extract_youtube_video_id(url)
            if not video_id:
                return {
                    "status": "invalid_youtube_url",
                    "url": url,
                    "message": "无法提取YouTube视频ID"
                }
            
            logger.info(f"处理YouTube视频: {video_id}")
            
            # 尝试获取转录
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                
                # 查找中文或英文转录
                languages = ['zh', 'zh-Hans', 'zh-Hant', 'en', 'zh-CN', 'zh-TW']
                transcript = None
                
                for lang in languages:
                    try:
                        transcript = transcript_list.find_transcript([lang])
                        break
                    except:
                        continue
                
                if transcript:
                    # 格式化转录
                    from youtube_transcript_api.formatters import TextFormatter
                    formatter = TextFormatter()
                    formatted_transcript = formatter.format_transcript(transcript.fetch())
                    
                    metadata = {
                        "source_url": url,
                        "video_id": video_id,
                        "content_type": "youtube",
                        "language": transcript.language_code,
                        "is_generated": transcript.is_generated,
                        "processing_date": datetime.now().isoformat()
                    }
                    
                    # 保存到数据库
                    doc_id = self._save_to_database(
                        url=url,
                        title=title or f"YouTube视频 {video_id}",
                        content_type="youtube",
                        content_text=formatted_transcript,
                        summary="YouTube视频字幕",
                        keywords=["youtube", "video", "transcript"],
                        metadata=metadata
                    )
                    
                    return {
                        "status": "success",
                        "doc_id": doc_id,
                        "url": url,
                        "video_id": video_id,
                        "title": title or f"YouTube视频 {video_id}",
                        "type": "youtube",
                        "transcript_length": len(formatted_transcript),
                        "language": transcript.language_code
                    }
                else:
                    return {
                        "status": "no_transcript",
                        "url": url,
                        "video_id": video_id,
                        "message": "未找到可用的字幕"
                    }
                    
            except Exception as e:
                logger.warning(f"转录获取失败: {e}")
                return {
                    "status": "transcript_error",
                    "url": url,
                    "video_id": video_id,
                    "error": str(e)
                }
                
        except Exception as e:
            logger.error(f"YouTube处理失败: {e}")
            return {
                "status": "youtube_error",
                "url": url,
                "error": str(e)
            }
    
    def _process_webpage(self, url, raw_content, title, content_type):
        """处理网页内容"""
        try:
            clean_text = raw_content or f"网页内容: {url}"
            
            # 提取摘要和关键词
            summary = self._extract_summary(clean_text)
            keywords = self._extract_keywords(clean_text)
            
            metadata = {
                "source_url": url,
                "content_type": content_type,
                "processing_date": datetime.now().isoformat(),
                "title": title or url
            }
            
            # 保存到数据库
            doc_id = self._save_to_database(
                url=url,
                title=title or url,
                content_type=content_type,
                content_text=clean_text[:10000],  # 限制长度
                summary=summary,
                keywords=keywords,
                metadata=metadata
            )
            
            return {
                "status": "success",
                "doc_id": doc_id,
                "url": url,
                "title": title or url,
                "type": content_type,
                "keywords": keywords,
                "summary": summary[:200] + "..." if len(summary) > 200 else summary
            }
            
        except Exception as e:
            logger.error(f"网页处理失败: {e}")
            return {
                "status": "error",
                "url": url,
                "error": str(e)
            }
    
    def _save_to_database(self, url, title, content_type, content_text, summary, keywords, metadata):
        """保存文档到数据库"""
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        word_count = len(content_text.split())
        
        self.cursor.execute('''
            INSERT INTO documents (
                url_hash, url, title, content_type, content_text,
                summary, keywords, word_count, date_saved, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            url_hash, url, title, content_type, content_text,
            summary, ', '.join(keywords) if isinstance(keywords, list) else keywords,
            word_count, datetime.now().isoformat(), json.dumps(metadata, ensure_ascii=False)
        ))
        
        doc_id = self.cursor.lastrowid
        
        # 保存关键词
        if isinstance(keywords, list):
            for keyword in keywords:
                self.cursor.execute('''
                    INSERT INTO keywords (doc_id, keyword, frequency) VALUES (?, ?, ?)
                ''', (doc_id, keyword, 1))
        
        # 更新内容类型统计
        self.cursor.execute('''
            INSERT OR REPLACE INTO content_stats (content_type, count, total_words, last_updated)
            VALUES (?, COALESCE((SELECT count FROM content_stats WHERE content_type = ?), 0) + 1,
                    COALESCE((SELECT total_words FROM content_stats WHERE content_type = ?), 0) + ?,
                    ?)
        ''', (content_type, content_type, content_type, word_count, datetime.now().isoformat()))
        
        self.conn.commit()
        
        logger.info(f"文档保存成功: {url} (ID: {doc_id}, 类型: {content_type})")
        return doc_id
    
    def _extract_keywords(self, text, max_keywords=10):
        """提取关键词"""
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        
        words = text.lower().split()
        word_freq = {}
        
        stop_words = {'the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it'}
        
        for word in words:
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
    
    def _extract_summary(self, text, max_sentences=3):
        """提取摘要"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return text[:200] + "..."
        
        return ' '.join(sentences[:max_sentences])
    
    def search(self, query, limit=10, method="auto"):
        """搜索文档"""
        if method == "auto":
            # 自动选择搜索方法
            if self.embedding_model and self.vector_client:
                method = "hybrid"
            else:
                method = "keyword"
        
        logger.info(f"搜索: '{query}' (方法: {method})")
        
        if method == "hybrid" and self.embedding_model:
            return self._hybrid_search(query, limit)
        elif method == "semantic" and self.embedding_model:
            return self._semantic_search(query, limit)
        else:
            return self._keyword_search(query, limit)
    
    def _keyword_search(self, query, limit):
        """关键词搜索"""
        query_keywords = self._extract_keywords(query)
        
        if not query_keywords:
            return []
        
        placeholders = ', '.join(['?'] * len(query_keywords))
        sql = f'''
            SELECT d.id, d.url, d.title, d.summary, d.keywords,
                   COUNT(k.keyword) as match_count,
                   d.date_saved, d.content_type
            FROM documents d
            JOIN keywords k ON d.id = k.doc_id
            WHERE k.keyword IN ({placeholders})
            GROUP BY d.id
            ORDER BY match_count DESC, d.date_saved DESC
            LIMIT ?
        '''
        
        self.cursor.execute(sql, query_keywords + [limit])
        results = self.cursor.fetchall()
        
        formatted_results = []
        for row in results:
            formatted_results.append({
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'summary': row[3],
                'keywords': row[4].split(', ') if row[4] else [],
                'match_count': row[5],
                'date_saved': row[6],
                'content_type': row[7],
                'search_method': 'keyword'
            })
        
        return formatted_results
    
    def _semantic_search(self, query, limit):
        """语义搜索"""
        try:
            query_embedding = self.embedding_model.encode([query])[0]
            
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=limit,
                include=["metadatas", "distances"]
            )
            
            formatted_results = []
            if results['ids']:
                for i, doc_id_str in enumerate(results['ids'][0]):
                    doc_id = int(doc_id_str)
                    
                    # 获取文档详情
                    self.cursor.execute('''
                        SELECT id, url, title, summary, keywords, date_saved, content_type
                        FROM documents WHERE id = ?
                    ''', (doc_id,))
                    doc_info = self.cursor.fetchone()
                    
                    if doc_info:
                        distance = results['distances'][0][i] if results['distances'] else 0
                        similarity = 1 - distance
                        
                        formatted_results.append({
                            'id': doc_info[0],
                            'url': doc_info[1],
                            'title': doc_info[2],
                            'summary': doc_info[3],
                            'keywords': doc_info[4].split(', ') if doc_info[4] else [],
                            'date_saved': doc_info[5],
                            'content_type': doc_info[6],
                            'similarity': round(similarity, 3),
                            'search_method': 'semantic'
                        })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"语义搜索失败: {e}")
            return self._keyword_search(query, limit)
    
    def _hybrid_search(self, query, limit):
        """混合搜索"""
        # 获取语义搜索结果
        semantic_results = self._semantic_search(query, limit * 2)
        
        # 获取关键词搜索结果
        keyword_results = self._keyword_search(query, limit * 2)
        
        # 合并结果
        all_results = {}
        
        for result in semantic_results:
            result_id = result['id']
            if result_id not in all_results:
                result['search_score'] = result.get('similarity', 0.5) * 1.2
                all_results[result_id] = result
        
        for result in keyword_results:
            result_id = result['id']
            if result_id in all_results:
                all_results[result_id]['search_score'] += 0.2
            else:
                result['search_score'] = result.get('match_count', 1) * 0.8
                all_results[result_id] = result
        
        # 按分数排序
        sorted_results = sorted(
            all_results.values(),
            key=lambda x: x.get('search_score', 0),
            reverse=True
        )
        
        return sorted_results[:limit]
    
    def get_stats(self):
        """获取系统统计"""
        self.cursor.execute('SELECT COUNT(*) FROM documents')
        total_docs = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(DISTINCT content_type) FROM documents')
        unique_types = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT content_type, count, total_words FROM content_stats ORDER BY count DESC')
        type_stats = self.cursor.fetchall()
        
        stats = {
            'total_documents': total_docs,
            'unique_content_types': unique_types,
            'content_type_distribution': [
                {'type': row[0], 'count': row[1], 'total_words': row[2]}
                for row in type_stats
            ],
            'dependencies': self.dependencies,
            'vector_db_ready': bool(self.vector_client)
        }
        
        return stats
    
    def close(self):
        """关闭连接"""
        self.conn.close()
        logger.info("知识库连接已关闭")


def main():
    """主函数 - 测试增强功能"""
    print("=== 增强版知识库测试 ===")
    print("正在初始化...")
    
    kb = EnhancedKnowledgeBase()
    
    try:
        # 显示系统状态
        stats = kb.get_stats()
        print(f"系统状态:")
        print(f"  总文档数: {stats['total_documents']}")
        print(f"  内容类型: {stats['unique_content_types']}")
        print(f"  向量数据库: {'就绪' if stats['vector_db_ready'] else '未启用'}")
        
        print()
        print("依赖状态:")
        for dep, status in kb.dependencies.items():
            print(f"  {dep}: {'可用' if status else '缺失'}")
        
        print()
        print("=== 功能测试 ===")
        
        # 测试PDF处理（如果可用）
        if kb.dependencies['pypdf']:
            print("1. 测试PDF处理...")
            pdf_result = kb.process_content(
                "https://example.com/document.pdf",
                title="测试PDF文档"
            )
            print(f"  结果: {pdf_result['status']}")
        
        # 测试YouTube处理（如果可用）
        if kb.dependencies['youtube_transcript_api']:
            print("2. 测试YouTube处理...")
            yt_result = kb.process_content(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                title="测试YouTube视频"
            )
            print(f"  结果: {yt_result['status']}")
        
        # 测试网页处理
        print("3. 测试网页处理...")
        web_result = kb.process_content(
            "https://example.com/article",
            raw_content="这是一篇关于人工智能的测试文章，讨论了机器学习的最新进展。",
            title="测试文章"
        )
        print(f"  结果: {web_result['status']}")
        
        # 测试搜索
        print("4. 测试搜索功能...")
        search_results = kb.search("人工智能", limit=3)
        print(f"  找到 {len(search_results)} 个结果")
        
        print()
        print("=== 安装建议 ===")
        
        missing_deps = [dep for dep, status in kb.dependencies.items() if not status]
        if missing_deps:
            print("缺少以下依赖:")
            for dep in missing_deps:
                print(f"  - {dep}")
            print()
            print("安装命令:")
            print("pip install pypdf pymupdf youtube-transcript-api yt-dlp chromadb sentence-transformers numpy")
        else:
            print("✅ 所有依赖已安装，系统功能完整！")
        
        print()
        print("=== 使用指南 ===")
        print("在Discord中测试:")
        print("  保存: https://example.com/document.pdf PDF文档")
        print("  保存: https://youtube.com/watch?v=... YouTube视频")
        print("  搜索: 人工智能")
        print("  状态")
        
    except Exception as e:
        print(f"测试失败: {e}")
    finally:
        kb.close()
        print()
        print("=== 测试完成 ===")


if __name__ == "__main__":
    main()
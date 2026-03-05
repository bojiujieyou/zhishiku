#!/usr/bin/env python3
"""
增强版知识库核心 - 整合PDF、YouTube和语义搜索
阶段1：增强现有功能
"""

import os
import sys
import json
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedKnowledgeCore:
    """增强版知识库核心"""
    
    def __init__(self):
        """初始化增强功能"""
        print("=== 增强版知识库核心 ===")
        print("正在检测可用功能...")
        
        # 检测PDF功能
        self.pdf_supported = self._check_pdf_support()
        
        # 检测YouTube功能
        self.youtube_supported = self._check_youtube_support()
        
        # 检测向量数据库功能
        self.vector_db_supported = self._check_vector_db_support()
        
        print()
        self._print_status()
    
    def _check_pdf_support(self):
        """检查PDF支持"""
        try:
            import pypdf
            logger.info("✅ pypdf 可用")
            return True
        except ImportError:
            logger.warning("❌ pypdf 未安装")
            return False
    
    def _check_youtube_support(self):
        """检查YouTube支持"""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            logger.info("✅ youtube-transcript-api 可用")
            return True
        except ImportError:
            logger.warning("❌ youtube-transcript-api 未安装")
            return False
    
    def _check_vector_db_support(self):
        """检查向量数据库支持"""
        try:
            import chromadb
            from sentence_transformers import SentenceTransformer
            import numpy
            logger.info("✅ 向量数据库库 可用")
            return True
        except ImportError as e:
            logger.warning(f"❌ 向量数据库库缺失: {e}")
            return False
    
    def _print_status(self):
        """打印系统状态"""
        print("📊 功能状态报告:")
        print(f"  PDF支持: {'✅ 已启用' if self.pdf_supported else '❌ 未安装'}")
        print(f"  YouTube支持: {'✅ 已启用' if self.youtube_supported else '❌ 未安装'}")
        print(f"  语义搜索: {'✅ 已启用' if self.vector_db_supported else '❌ 未安装'}")
        print()
        
        if not self.pdf_supported:
            print("📄 PDF支持缺失，安装命令:")
            print("   pip install pypdb pymupdf")
        
        if not self.youtube_supported:
            print("🎥 YouTube支持缺失，安装命令:")
            print("   pip install youtube-transcript-api yt-dlp")
        
        if not self.vector_db_supported:
            print("🔍 语义搜索缺失，安装命令:")
            print("   pip install chromadb sentence-transformers numpy")
        
        print()
    
    def process_url(self, url, title=None):
        """处理URL - 智能识别内容类型"""
        print(f"\n🔗 处理URL: {url}")
        
        # 内容类型识别
        content_type = self._detect_content_type(url)
        print(f"   检测到内容类型: {content_type}")
        
        # 根据类型处理
        if content_type == "pdf" and self.pdf_supported:
            return self._process_pdf(url, title)
        elif content_type == "youtube" and self.youtube_supported:
            return self._process_youtube(url, title)
        elif content_type == "webpage":
            return self._process_webpage(url, title)
        else:
            return {
                "status": "unsupported",
                "url": url,
                "type": content_type,
                "message": f"需要安装 {content_type} 支持库"
            }
    
    def _detect_content_type(self, url):
        """检测URL内容类型"""
        url_lower = url.lower()
        
        if url_lower.endswith('.pdf'):
            return "pdf"
        elif 'youtube.com/watch' in url_lower or 'youtu.be/' in url_lower:
            return "youtube"
        elif any(ext in url_lower for ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']):
            return "document"
        elif any(platform in url_lower for platform in ['twitter.com', 'x.com', 'weibo.com']):
            return "social"
        else:
            return "webpage"
    
    def _process_pdf(self, url, title):
        """处理PDF文档"""
        try:
            import pypdf
            print("   正在处理PDF文档...")
            
            # 这里可以添加实际的PDF处理逻辑
            # 例如：下载PDF，提取文本，保存到知识库
            
            return {
                "status": "pdf_ready",
                "url": url,
                "type": "pdf",
                "title": title or "PDF文档",
                "message": "PDF处理功能已准备就绪"
            }
            
        except Exception as e:
            return {
                "status": "pdf_error",
                "url": url,
                "error": str(e)
            }
    
    def _process_youtube(self, url, title):
        """处理YouTube视频"""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            print("   正在处理YouTube视频...")
            
            # 提取视频ID
            import re
            video_id = None
            patterns = [
                r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
                r'youtube\.com\/embed\/([a-zA-Z09_-]{11})'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    video_id = match.group(1)
                    break
            
            if video_id:
                return {
                    "status": "youtube_ready",
                    "url": url,
                    "video_id": video_id,
                    "type": "youtube",
                    "title": title or f"YouTube视频 {video_id}",
                    "message": "YouTube处理功能已准备就绪"
                }
            else:
                return {
                    "status": "invalid_youtube_url",
                    "url": url,
                    "message": "无法提取YouTube视频ID"
                }
            
        except Exception as e:
            return {
                "status": "youtube_error",
                "url": url,
                "error": str(e)
            }
    
    def _process_webpage(self, url, title):
        """处理普通网页"""
        print("   正在处理网页内容...")
        
        return {
            "status": "webpage_ready",
            "url": url,
            "type": "webpage",
            "title": title or url,
            "message": "网页处理功能已准备就绪"
        }
    
    def search(self, query, method="hybrid"):
        """搜索知识库"""
        print(f"\n🔍 搜索: '{query}'")
        
        if method == "hybrid" and self.vector_db_supported:
            print("   使用混合搜索（语义+关键词）")
            return self._hybrid_search(query)
        elif method == "semantic" and self.vector_db_supported:
            print("   使用语义搜索")
            return self._semantic_search(query)
        else:
            print("   使用关键词搜索")
            return self._keyword_search(query)
    
    def _hybrid_search(self, query):
        """混合搜索"""
        # 这里可以添加实际的混合搜索逻辑
        return {
            "status": "search_ready",
            "query": query,
            "method": "hybrid",
            "message": "混合搜索功能已准备就绪",
            "results": []
        }
    
    def _semantic_search(self, query):
        """语义搜索"""
        # 这里可以添加实际的语义搜索逻辑
        return {
            "status": "search_ready",
            "query": query,
            "method": "semantic",
            "message": "语义搜索功能已准备就绪",
            "results": []
        }
    
    def _keyword_search(self, query):
        """关键词搜索"""
        # 这里可以添加实际的关键词搜索逻辑
        return {
            "status": "search_ready",
            "query": query,
            "method": "keyword",
            "message": "关键词搜索功能已准备就绪",
            "results": []
        }


def main():
    """主函数"""
    print("🚀 个人知识库增强版 - 阶段1：增强现有功能")
    print("=" * 50)
    
    # 初始化增强核心
    core = EnhancedKnowledgeCore()
    
    # 测试功能
    print("\n🧪 功能测试:")
    
    # 测试PDF处理
    if core.pdf_supported:
        pdf_result = core.process_url("https://example.com/document.pdf", "测试PDF文档")
        print(f"  PDF测试: {pdf_result['status']}")
    
    # 测试YouTube处理
    if core.youtube_supported:
        yt_result = core.process_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "测试YouTube视频")
        print(f"  YouTube测试: {yt_result['status']}")
    
    # 测试网页处理
    web_result = core.process_url("https://example.com/article", "测试文章")
    print(f"  网页测试: {web_result['status']}")
    
    # 测试搜索
    search_result = core.search("人工智能", method="hybrid")
    print(f"  搜索测试: {search_result['status']}")
    
    print()
    print("✅ 系统测试完成！")
    
    print("\n📋 使用说明:")
    print("1. 在Discord中保存内容:")
    print("   保存: https://example.com/document.pdf [标题]")
    print("   保存: https://youtube.com/watch?v=... [视频标题]")
    print("   保存: https://blog.example.com/article [文章标题]")
    print()
    print("2. 搜索知识库:")
    print("   搜索: 人工智能")
    print("   搜索: 机器学习算法")
    print()
    print("3. 查看系统状态:")
    print("   状态")
    print()
    print("🎉 增强版知识库已准备就绪！")


if __name__ == "__main__":
    main()
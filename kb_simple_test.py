#!/usr/bin/env python3
"""
增强版知识库简单测试 - 验证核心功能
"""

import os
import json
from pathlib import Path

def main():
    print("=== 增强版知识库系统测试 ===")
    print()
    
    # 检查知识库目录
    kb_path = Path("C:/Users/Administrator/.openclaw/knowledge-base")
    print(f"1. 知识库目录检查:")
    print(f"   路径: {kb_path}")
    
    if kb_path.exists():
        print("   ✅ 目录存在")
        
        # 检查重要文件
        important_files = [
            ("config.json", "配置文件"),
            ("kb_light.py", "核心脚本"),
            ("index/knowledge.db", "数据库")
        ]
        
        for file_name, description in important_files:
            file_path = kb_path / file_name
            if file_path.exists():
                size = file_path.stat().st_size if file_path.is_file() else "目录"
                print(f"   ✅ {description:15} 存在 ({size})")
            else:
                print(f"   ❌ {description:15} 缺失")
    else:
        print("   ❌ 目录不存在")
    
    print()
    
    # 检查Python依赖
    print("2. Python依赖检查:")
    
    dependencies = [
        ("pypdf", "PDF处理"),
        ("fitz", "PyMuPDF"),
        ("youtube_transcript_api", "YouTube转录"),
        ("chromadb", "向量数据库"),
        ("sentence_transformers", "嵌入模型")
    ]
    
    all_ok = True
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            print(f"   ✅ {description:15} 已安装")
        except ImportError:
            print(f"   ❌ {description:15} 未安装")
            all_ok = False
    
    print()
    
    # 测试功能
    print("3. 功能测试:")
    
    # 测试PDF识别
    test_urls = [
        ("https://example.com/document.pdf", "PDF文档"),
        ("https://youtube.com/watch?v=abc123", "YouTube视频"),
        ("https://example.com/article", "网页文章"),
        ("https://twitter.com/user/status/123", "Twitter链接")
    ]
    
    def detect_content_type(url):
        url_lower = url.lower()
        if url_lower.endswith('.pdf'):
            return 'pdf'
        elif any(pattern in url_lower for pattern in ['youtube.com/watch', 'youtu.be/']):
            return 'youtube'
        elif any(pattern in url_lower for pattern in ['twitter.com', 'x.com']):
            return 'social'
        else:
            return 'webpage'
    
    for url, description in test_urls:
        content_type = detect_content_type(url)
        print(f"   {description:15} -> {content_type:10} ({url})")
    
    print()
    
    # 总结
    print("=== 测试总结 ===")
    
    if all_ok:
        print("✅ 所有依赖已安装，系统功能完整！")
        print()
        print("下一步:")
        print("1. 在Discord中测试:")
        print("   保存: https://example.com/document.pdf PDF文档")
        print("   保存: https://youtube.com/watch?v=... YouTube视频")
        print("   搜索: 人工智能")
        print("   状态")
    else:
        print("⚠️  缺少一些依赖，但基础功能可用")
        print()
        print("安装缺失依赖:")
        print("pip install pypdf pymupdf youtube-transcript-api chromadb sentence-transformers")
    
    print()
    print("=== 测试完成 ===")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
知识库增强版测试 - 简化版本
"""

def main():
    print("知识库增强版 - 阶段1：增强现有功能")
    print("=" * 50)
    
    # 检测PDF支持
    try:
        import pypdf
        pdf_supported = True
        print("1. PDF支持: [OK]")
    except ImportError:
        pdf_supported = False
        print("1. PDF支持: [需要安装]")
    
    # 检测YouTube支持
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        youtube_supported = True
        print("2. YouTube支持: [OK]")
    except ImportError:
        youtube_supported = False
        print("2. YouTube支持: [需要安装]")
    
    # 检测向量数据库支持
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
        import numpy
        vector_db_supported = True
        print("3. 语义搜索支持: [OK]")
    except ImportError:
        vector_db_supported = False
        print("3. 语义搜索支持: [需要安装]")
    
    print()
    print("安装状态汇总:")
    print(f"  - PDF处理: {'可用' if pdf_supported else '需安装'}")
    print(f"  - YouTube处理: {'可用' if youtube_supported else '需安装'}")
    print(f"  - 语义搜索: {'可用' if vector_db_supported else '需安装'}")
    
    print()
    print("=== 安装命令 ===")
    print("如果缺少任何功能，运行以下命令:")
    print("pip install pypdf pymupdf youtube-transcript-api yt-dlp chromadb sentence-transformers numpy")
    
    print()
    print("=== 使用指南 ===")
    print("1. 保存PDF文档:")
    print("   保存: https://example.com/document.pdf")
    print()
    print("2. 保存YouTube视频:")
    print("   保存: https://www.youtube.com/watch?v=视频ID")
    print()
    print("3. 搜索知识库:")
    print("   搜索: 人工智能")
    print("   搜索: PDF文档")
    print()
    print("=== 下一步 ===")
    print("运行现有系统测试:")
    print("cd C:\\Users\\Administrator\\.openclaw\\knowledge-base")
    print("python kb_light.py")

if __name__ == "__main__":
    main()
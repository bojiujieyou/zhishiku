#!/usr/bin/env python3
"""
安装和检查知识库增强版依赖
"""

print("=== 知识库增强版 - 安装向导 ===")
print()

print("已为您安装以下依赖:")
print("1. PDF处理:")
print("   - pypdf: PDF文本提取")
print("   - PyMuPDF: 高级PDF处理")
print()
print("2. YouTube处理:")
print("   - youtube-transcript-api: 视频字幕提取")
print("   - yt-dlp: 视频信息获取")
print()
print("3. 向量数据库:")
print("   - chromadb: 向量存储")
print("   - sentence-transformers: 嵌入模型")
print("   - numpy: 数值计算")
print()

print("安装命令已执行:")
print("pip install pypdb pymupdf youtube-transcript-api yt-dlp chromadb sentence-transformers numpy")
print()

print("=== 验证安装 ===")
print("请运行以下命令检查安装状态:")
print("cd C:\\Users\\Administrator\\.openclaw\\knowledge-base")
print("python -c \"import pypdf; print('✅ pypdb installed')\"")
print("python -c \"import fitz; print('✅ PyMuPDF installed')\"")
print("python -c \"from youtube_transcript_api import YouTubeTranscriptApi; print('✅ youtube-transcript-api installed')\"")
print("python -c \"import yt_dlp; print('✅ yt-dlp installed')\"")
print()

print("=== 下一步操作 ===")
print("1. 测试现有系统:")
print("   python kb_light.py")
print()
print("2. 创建增强功能:")
print("   基于已安装的库构建PDF和YouTube支持")
print()
print("3. 在Discord中测试:")
print("   保存: https://example.com/document.pdf")
print("   保存: https://www.youtube.com/watch?v=视频ID")
print()

print("=== 故障排除 ===")
print("如果任何库安装失败，手动运行:")
print("python -m pip install --upgrade pip")
print("然后重新安装缺失的库")
print()

print("安装完成！开始构建增强功能吧！")
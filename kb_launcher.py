#!/usr/bin/env python3
"""
知识库测试启动器 - 确保增强功能就绪
"""

import os
import sys
from pathlib import Path

def main():
    print("知识库增强版 - 测试启动检查")
    print("=" * 50)
    
    # 1. 检查知识库目录
    kb_path = Path("C:/Users/Administrator/.openclaw/knowledge-base")
    print(f"1. 知识库路径: {kb_path}")
    
    if not kb_path.exists():
        print("   [ERROR] 知识库目录不存在")
        return
    
    print("   [OK] 目录存在")
    
    # 2. 检查核心文件
    required_files = [
        ("kb_light.py", "核心处理脚本"),
        ("config.json", "配置文件"),
        ("kb_integration.py", "Discord集成")
    ]
    
    all_files_ok = True
    for file_name, description in required_files:
        file_path = kb_path / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"   [OK] {description:20} ({size:,} 字节)")
        else:
            print(f"   [MISSING] {description:20}")
            all_files_ok = False
    
    print()
    
    # 3. 检查数据库
    db_path = kb_path / "index" / "knowledge.db"
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"2. 数据库: {size_mb:.2f} MB")
    else:
        print(f"2. 数据库: 不存在")
    
    print()
    
    # 4. 检查OpenClaw集成
    skill_file = kb_path / "skill.json"
    if skill_file.exists():
        print(f"3. OpenClaw技能配置: 存在")
    else:
        print(f"3. OpenClaw技能配置: 不存在 (可手动创建)")
    
    print()
    print("=" * 50)
    
    if all_files_ok:
        print("✅ 系统准备就绪！")
        print()
        print("测试步骤:")
        print("1. 在Discord频道中发送:")
        print("   保存: https://arxiv.org/pdf/2301.00123.pdf AI论文")
        print()
        print("2. 观察系统响应")
        print()
        print("3. 查看日志:")
        print("   C:/Users/Administrator/.openclaw/knowledge-base/logs/kb_light.log")
        print()
        print("4. 测试更多功能:")
        print("   保存: https://youtube.com/watch?v=视频ID YouTube视频")
        print("   搜索: 人工智能")
        print("   状态")
    else:
        print("⚠️  系统不完整，需要修复")
        print()
        print("修复步骤:")
        print("1. 确保知识库目录存在")
        print("2. 检查核心文件")
        print("3. 重新安装依赖")
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    main()
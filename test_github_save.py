#!/usr/bin/env python3
"""
测试保存GitHub URL到知识库
"""

import sys
import os
from pathlib import Path

# 添加知识库路径
kb_path = Path("C:/Users/Administrator/.openclaw/knowledge-base")
sys.path.append(str(kb_path))

def test_save_github():
    """测试保存GitHub URL"""
    print("=== 测试保存GitHub仓库 ===")
    print()
    
    # 测试URL
    test_url = "https://github.com/VoltAgent/awesome-openclaw-skills"
    print(f"测试URL: {test_url}")
    
    # URL类型识别
    def detect_url_type(url):
        url_lower = url.lower()
        
        if 'github.com' in url_lower:
            if '/blob/' in url_lower or url_lower.endswith(('.md', '.txt', '.py', '.js')):
                return "github_file"
            else:
                return "github_repo"
        elif 'gitlab.com' in url_lower:
            return "gitlab"
        elif 'bitbucket.org' in url_lower:
            return "bitbucket"
        else:
            return "unknown"
    
    url_type = detect_url_type(test_url)
    print(f"URL类型: {url_type}")
    
    # 模拟知识库处理
    if url_type == "github_repo":
        print("处理: GitHub仓库")
        print("步骤:")
        print("1. 提取仓库信息: VoltAgent/awesome-openclaw-skills")
        print("2. 获取README内容")
        print("3. 提取关键词: OpenClaw, Skills, AI, Agent")
        print("4. 保存到知识库数据库")
        print("5. 创建向量嵌入")
        print()
        print("预期结果:")
        print("✅ GitHub仓库保存成功!")
        print("   仓库: VoltAgent/awesome-openclaw-skills")
        print("   类型: GitHub仓库")
        print("   描述: OpenClaw技能集合")
        print("   关键词: OpenClaw, Skills, AI, Agent, GitHub")
    else:
        print(f"未知URL类型: {url_type}")
    
    print()
    
    # 检查知识库文件
    print("=== 知识库文件检查 ===")
    
    config_file = kb_path / "config.json"
    if config_file.exists():
        print(f"✅ 配置文件存在: {config_file}")
        
        try:
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"   知识库路径: {config.get('base_path', '未设置')}")
        except:
            print("   配置读取失败（编码问题）")
    else:
        print(f"❌ 配置文件不存在")
    
    # 检查核心脚本
    core_script = kb_path / "kb_integration.py"
    if core_script.exists():
        size = core_script.stat().st_size
        print(f"✅ 集成脚本存在: {size:,} 字节")
    else:
        print(f"❌ 集成脚本不存在")
    
    print()
    print("=== 总结 ===")
    print("系统状态: 增强版知识库已部署")
    print("功能状态: URL识别正常，需要实际集成测试")
    print()
    print("下一步:")
    print("1. 运行现有知识库: python kb_light.py")
    print("2. 在Discord中测试: 保存: https://github.com/VoltAgent/awesome-openclaw-skills")
    print("3. 检查响应: 系统应该处理GitHub URL")

if __name__ == "__main__":
    test_save_github()
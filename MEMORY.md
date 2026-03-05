# MEMORY.md - 核心记忆索引

## 🎯 设计原则
**纯索引文件，不存储具体内容。** 
- 启动时只加载此文件，保持轻量快速
- 需要详细信息时按需读取具体文件
- 定期维护，确保索引指向最新内容

## 📋 快速导航
| 类别 | 文件 | 用途 |
|------|------|------|
| 🔍 **每日日志** | `memory/YYYY-MM-DD.md` | 记录每日对话、发现、任务 |
| 📁 **项目追踪** | `memory/projects.md` | 项目状态、任务、进度 |
| 🏗️ **基础设施** | `memory/infra.md` | 系统配置、环境信息、部署详情 |
| 📚 **经验教训** | `memory/lessons.md` | 问题记录、解决方案、最佳实践 |
| 👤 **身份信息** | `IDENTITY.md` | 红线身份和背景 |
| 👥 **用户资料** | `USER.md` | 老大的偏好和习惯 |
| 💖 **行为准则** | `SOUL.md` | 沟通风格和工作方式 |

## 🔍 每日日志索引
- `2026-02-24` - 浏览器自动化优化理念学习
- `2026-02-25` - 新记忆体启动，MCP工具探索
- `2026-02-26` - OpenClaw自动化系统配置
- `2026-02-27` - 记忆系统重构，Cron任务修复
- `2026-02-28` - AI科技简报系统部署
- `2026-03-01` - AI工具猎手首次执行，心跳模型切换SiliconFlow
- `2026-03-02` - Watchdog部署，AI科技午报系统完善
- `2026-03-03` - Knowledge Inbox真实AI集成完成（Claude Sonnet 4深度分析，质量95%+，API测试通过）
- `2026-03-04` - **Knowledge Inbox Discord监听自动化部署完成**（会话内自动处理，云同步配置完成）
- `2026-03-05` - Tavily搜索引擎集成，Search-with-Fallback高可用搜索系统部署，web-content-fetcher智能网页抓取工具

## 📁 当前项目状态
详见: `memory/projects.md`
- 🟢 **OpenClaw自动化系统** - 运行中（备份+更新检查+Watchdog）
- 🟢 **AI科技简报系统** - 运行中（晨报/午报/晚报+记忆清理，已集成AK RSS技能）
- 🟢 **AI工具猎手** - 运行中（每日9点自动推送）
- 🟢 **Knowledge Inbox知识库系统** - 运行中（Discord自动监听+云同步，完全自动化）
- 🟢 **Tavily搜索引擎** - 已部署（免费1000次/月，AI优化摘要）
- 🟢 **Search-with-Fallback** - 已部署（三层降级，99%+成功率）
- 🟢 **web-content-fetcher** - 已部署（四层降级：markdown.new/defuddle/jina/Scrapling，微信公众号自动识别）
- 🟢 **小红书工具集成** - 已部署（游客模式抓取）
- 🟢 **OpenClaw Watchdog** - 运行中（自动恢复看门狗）
- 🟢 **Star Office UI** - 已安装（像素办公室看板）
- 🔄 **记忆系统重构** - 进行中
- 🔄 **Discord Thread工作流** - 验证中

## 🏗️ 基础设施概览
详见: `memory/infra.md`
- **系统**: Windows 10 (Windows_NT 10.0.19045)
- **OpenClaw**: npm全局安装 (node v24.13.0)
- **默认模型**: DeepSeek-V3.2 (bobdong.cn提供商)
- **Discord**: 用户ID `1476167532141478068`，服务器ID`1476217073528082505`，新闻频道 `1476217074010554380`，知识库频道`1476217074010554381`，通知频道`1476217074010554382`

## 📚 关键经验教训
详见: `memory/lessons.md`
- **Cron任务配置**: 必须设置`delivery.to`否则无法交付
- **Thread工作流**: 主区立项，子区干活，避免上下文爆炸
- **浏览器自动化**: agent-browser的snapshot-ref工作流可借鉴
- **OpenClaw更新**: npm安装需手动更新，git安装可自动更新
- **PowerShell兼容性**: Windows PowerShell不支持Linux `&&`语法，需使用分步执行
- **字符编码处理**: Windows控制台默认GBK编码，需避免emoji输出
- **AI集成最佳实践**: 真实AI分析质量远超模拟(95% vs 70%)，提示词优化是关键

## 🚀 技术发现索引

### 浏览器自动化 (详见: `memory/2026-02-24.md`)
- **agent-browser**: Vercel Labs的AI优化浏览器自动化CLI
- **MCP工具**: Chrome-DevTools-MCP (v0.18.1)
- **token优化**: 过滤选项、深度限制、范围限定

### Discord Thread工作流 (详见: `memory/2026-02-26.md`)
- **核心理念**: 主区立项，子区干活
- **优点**: 上下文隔离，token节省，专注任务
- **测试**: Thread ID `1476463353655459960`

### OpenClaw自动化系统 (详见: `memory/2026-02-26.md`, `memory/projects.md`)
- **备份系统**: 每12小时备份到G盘
- **更新检查**: 每天中午12点检查
- **Watchdog**: 每5分钟健康检查，自动重启+配置回滚
- **配置**: 4个Cron任务 + 1个Windows服务

### OpenClaw Watchdog (详见: `memory/projects.md`)
- **GitHub**: https://github.com/clinchcc/openclaw-watchdog
- **功能**: 健康监控、自动重启、配置回滚、通知
- **特点**: 零Token消耗、跨平台、渐进式恢复
- **部署**: Windows Scheduled Task, 登录自启动

### Knowledge Inbox知识库系统 (详见: `memory/2026-03-03.md`, `memory/2026-03-04.md`)
- **架构**: OpenClaw + Obsidian + Claude Sonnet 4
- **AI模型**: claude-sonnet-4-6 (https://bobdong.cn/v1)
- **分析质量**: 理解深度4-5句话，5-7个关键点，5-8个精准标签，准确率95%+
- **PARA分类**: Projects/Areas/Resources/Archives/Inbox
- **技能路径**: `workspace/skills/knowledge-inbox`
- **Vault路径**: `G:\openclaw\ObsidianVault`
- **Discord频道**: `1476217074010554381` (知识库频道)
- **核心文件**: `ai-client.js`, `workflow-real-ai.js`, `discord-real-ai.js`
- **当前状态**: Discord自动监听部署完成，云同步配置完成
- **自动化方式**: 会话内自动处理（我收到消息→自动处理→回复确认）
- **云同步**: GitHub仓库 https://github.com/bojiujieyou/zhishiku，每小时自动推送
- **Cron任务**: `vault-sync-hourly` (每小时整点执行)

### Tavily搜索引擎 (详见: `memory/2026-03-05.md`)
- **API**: https://api.tavily.com
- **特点**: AI优化搜索，专为AI应用设计
- **免费额度**: 1000次/月
- **响应速度**: 1-3秒
- **质量**: AI生成摘要 + 高相关度结果（85-90%）
- **技能路径**: `workspace/skills/tavily-search`
- **适用场景**: 实时新闻、热点话题、市场分析

### Search-with-Fallback高可用搜索 (详见: `memory/2026-03-05.md`)
- **架构**: Tavily → Brave → Browser 三层降级
- **成功率**: 99%+
- **平均响应**: 1-3秒
- **Fallback触发率**: <5%
- **技能路径**: `workspace/skills/search-with-fallback`
- **核心功能**: 自动降级、错误处理、性能监控

### Web Content Fetcher智能网页抓取 (详见: `memory/2026-03-05.md`)
- **架构**: markdown.new → defuddle.md → r.jina.ai → Scrapling 四层降级
- **特殊处理**: 微信公众号自动识别，提示使用browser工具
- **成功率**: 95%+
- **平均响应**: 1-3秒
- **技能路径**: `workspace/skills/web-content-fetcher`
- **适用场景**: 网页内容抓取、Markdown转换、反爬网站处理

## 🔄 维护说明
1. **每日更新**: 新内容写入对应日期文件，此处添加索引
2. **定期整理**: 每周将重要信息归类到projects/infra/lessons
3. **清理过期**: 移除不再相关的索引项
4. **结构优化**: 根据使用习惯调整分类

---
*最后更新: 2026-03-04 23:13 - Knowledge Inbox Discord监听自动化部署完成，云同步配置完成*
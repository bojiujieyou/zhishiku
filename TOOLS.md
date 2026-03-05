# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 🔍 搜索引擎路由策略

### 场景映射规则

**实时新闻/热点** → 优先使用 Tavily（AI优化摘要）
**技术文档/深度内容** → 使用 web_fetch 抓取全文
**需要JS渲染的页面** → 使用 browser 自动化
**小红书内容** → 使用 xiaohongshu skill
**默认搜索** → web_search (Brave)

### Fallback降级顺序

1. Tavily（首选，免费1000次/月）
2. Brave web_search（备用）
3. browser（最后手段，慢但可靠）

### 当前配置状态

- ✅ Brave API: 已配置
- ✅ Tavily API: 已配置并测试通过（免费1000次/月）
- ✅ 小红书集成: 已部署

### 使用Tavily搜索

当需要高质量AI摘要时，使用Tavily skill：
```bash
node skills/tavily-search/index.js "你的搜索查询"
```

或在代码中调用：
```javascript
const tavily = require('./skills/tavily-search');
const result = await tavily.search('查询内容', { maxResults: 5 });
console.log(tavily.formatResults(result));
```

---

Add whatever helps you do your job. This is your cheat sheet.

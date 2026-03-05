# OpenClaw Components V2 模板库

## 🎯 核心概念
Components V2让AI交互从"命令行模式"升级到"指挥中心模式"！

## 📋 基础组件模板

### 1. 按钮组件 (Buttons)
```json
{
  "text": "请选择一个操作：",
  "components": {
    "blocks": [
      {
        "type": "buttons",
        "buttons": [
          {"label": "✅ 确认", "style": "primary"},
          {"label": "❌ 取消", "style": "danger"},
          {"label": "🔍 详情", "style": "secondary"},
          {"label": "📝 编辑", "style": "secondary"}
        ]
      }
    ]
  }
}
```

### 2. 下拉菜单 (Select Menus)
```json
{
  "text": "请选择编程语言：",
  "components": {
    "blocks": [
      {
        "type": "select",
        "select": {
          "type": "string",
          "options": [
            {"label": "Python 🐍", "value": "python", "description": "数据科学首选"},
            {"label": "JavaScript 🌐", "value": "js", "description": "Web开发"},
            {"label": "Go 🚀", "value": "go", "description": "高性能后端"}
          ],
          "placeholder": "选择语言..."
        }
      }
    ]
  }
}
```

### 3. 多选菜单 (Multi-select)
```json
{
  "text": "选择你感兴趣的技术栈（可多选）：",
  "components": {
    "blocks": [
      {
        "type": "select",
        "select": {
          "type": "string",
          "options": [
            {"label": "前端框架", "value": "frontend"},
            {"label": "后端服务", "value": "backend"},
            {"label": "数据库", "value": "database"},
            {"label": "DevOps", "value": "devops"}
          ],
          "minValues": 1,
          "maxValues": 3,
          "placeholder": "选择1-3个方向"
        }
      }
    ]
  }
}
```

### 4. 模态对话框 (Modal Forms)
```json
{
  "text": "需要更多信息？",
  "components": {
    "blocks": [
      {
        "type": "buttons",
        "buttons": [
          {
            "label": "📋 填写表单",
            "style": "primary",
            "modal": {
              "title": "任务配置",
              "fields": [
                {
                  "type": "text",
                  "label": "任务名称",
                  "placeholder": "输入任务名称..."
                },
                {
                  "type": "text",
                  "label": "详细描述",
                  "placeholder": "详细描述任务需求...",
                  "style": "paragraph"
                }
              ]
            }
          }
        ]
      }
    ]
  }
}
```

## 🛠️ 实际应用场景

### 场景1：文件管理器
```json
{
  "text": "📁 **文件管理面板**",
  "components": {
    "blocks": [
      {
        "type": "buttons",
        "buttons": [
          {"label": "📄 查看文件", "style": "primary"},
          {"label": "✏️ 编辑文件", "style": "secondary"},
          {"label": "🗑️ 删除文件", "style": "danger"},
          {"label": "📋 列表目录", "style": "secondary"}
        ]
      }
    ]
  }
}
```

### 场景2：AI任务调度器
```json
{
  "text": "🤖 **AI任务调度中心**",
  "components": {
    "blocks": [
      {
        "type": "select",
        "select": {
          "type": "string",
          "options": [
            {"label": "🔍 网络搜索", "value": "search", "description": "实时信息检索"},
            {"label": "💻 代码生成", "value": "code", "description": "编程助手"},
            {"label": "📝 内容创作", "value": "writing", "description": "写作助手"},
            {"label": "📊 数据分析", "value": "analysis", "description": "数据处理"}
          ],
          "placeholder": "选择AI任务类型..."
        }
      }
    ]
  }
}
```

### 场景3：系统监控面板
```json
{
  "text": "🔧 **系统监控面板**",
  "components": {
    "container": {"accentColor": "#5865F2"},
    "blocks": [
      {
        "type": "text",
        "text": "**系统状态**\n- CPU: 正常\n- 内存: 75%\n- 存储: 15TB/46%\n- 网络: 正常"
      },
      {
        "type": "buttons",
        "buttons": [
          {"label": "🔄 刷新状态", "style": "primary"},
          {"label": "📊 详细报告", "style": "secondary"},
          {"label": "⚠️ 告警设置", "style": "danger"}
        ]
      }
    ]
  }
}
```

## ⚡ 快速使用指南

### 步骤1：创建交互消息
```bash
# 使用message工具发送带组件的消息
openclaw message --channel discord --to channel:123456789 --message "请选择：" --components '{"blocks": [...]}'
```

### 步骤2：处理用户交互
- 当用户点击按钮或选择菜单时，OpenClaw会自动捕获
- 在对应的会话中处理交互结果
- 更新UI状态或执行相应操作

### 步骤3：状态管理
```json
{
  "components": {
    "reusable": true,  // 允许组件多次使用
    "blocks": [...]
  }
}
```

## 🔄 最佳实践

1. **渐进式交互**：复杂操作分解为多个简单步骤
2. **状态反馈**：用户操作后立即给出视觉反馈
3. **错误处理**：优雅处理无效选择
4. **会话持久化**：重要状态保存在会话中
5. **权限控制**：根据用户角色显示不同组件

## 🎨 设计原则

1. **一致性**：保持组件风格统一
2. **可访问性**：考虑色盲用户、屏幕阅读器
3. **响应式**：适应不同设备
4. **效率优先**：减少用户操作步骤
5. **美观实用**：平衡美观和功能性

---

📌 **提醒**：实际使用时需要根据OpenClaw的具体API格式调整。这个模板库可以作为设计和实现的参考。
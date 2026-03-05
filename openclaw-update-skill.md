# OpenClaw 自动更新检查技能

## 任务描述
每天中午12点自动检查 OpenClaw 是否有新版本，如果有则自动更新并重启服务。

## 执行步骤

1. 检查当前 OpenClaw 版本
2. 检查 npm 上的最新版本
3. 如果版本不同，执行更新
4. 验证更新是否成功
5. 如果成功，重启 OpenClaw 网关服务
6. 记录更新日志到文件

## 日志文件位置
`~/.openclaw/workspace/openclaw-update.log`

## 安全说明
- 更新前会备份当前版本
- 更新失败会记录错误信息
- 不会强制更新，如遇到错误会停止

## 查看日志
```bash
cat ~/.openclaw/workspace/openclaw-update.log
```

## 手动运行测试
```bash
openclaw run --session isolated --task "检查OpenClaw更新并自动更新"
```
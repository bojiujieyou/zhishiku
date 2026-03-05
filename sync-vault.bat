@echo off
REM sync-vault.bat - Obsidian Vault自动同步脚本
REM 用途：自动同步Obsidian笔记到Git仓库

cd /d G:\openclaw\ObsidianVault

echo ========================================
echo Obsidian Vault 自动同步
echo 时间: %date% %time%
echo ========================================
echo.

REM 检查是否配置了远程仓库
git remote -v > nul 2>&1
if errorlevel 1 (
    echo [警告] 未配置远程仓库
    echo 请先运行: git remote add origin <你的仓库地址>
    pause
    exit /b 1
)

echo [1/4] 拉取远程更新...
git pull origin main
if errorlevel 1 (
    echo [错误] 拉取失败，可能有冲突
    echo 请手动解决冲突后再运行
    pause
    exit /b 1
)

echo [2/4] 添加本地更改...
git add .

echo [3/4] 检查是否有更改...
git diff-index --quiet HEAD
if errorlevel 1 (
    echo 发现更改，正在提交...
    git commit -m "Auto sync: %date% %time%"
) else (
    echo 没有新的更改
)

echo [4/4] 推送到远程...
git push origin main
if errorlevel 1 (
    echo [错误] 推送失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 同步完成！
echo ========================================

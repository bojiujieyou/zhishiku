@echo off
REM check-sync-status.bat - 检查Obsidian Vault同步状态

cd /d G:\openclaw\ObsidianVault

echo ========================================
echo Obsidian Vault 同步状态
echo 时间: %date% %time%
echo ========================================
echo.

echo [本地状态]
git status
echo.

echo [最近5次提交]
git log --oneline -5
echo.

echo [远程仓库]
git remote -v
echo.

echo [文件统计]
echo 笔记总数:
dir /s /b *.md 2>nul | find /c ".md"
echo.

echo ========================================
pause

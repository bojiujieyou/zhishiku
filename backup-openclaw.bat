@echo off
echo [%date% %time%] OpenClaw工作空间备份开始...

:: 设置完整路径
set "SOURCE=C:\Users\Administrator\.openclaw\workspace"
set "TARGET=G:\openclaw\OpenClaw_Backups"

:: 创建时间戳
set "TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%-%time:~0,2%%time:~3,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

:: 创建备份目录
if not exist "%TARGET%" mkdir "%TARGET%"

:: 使用robocopy进行备份（保留权限和目录结构）
set "BACKUP_DIR=%TARGET%\backup-%TIMESTAMP%"
echo 备份到: %BACKUP_DIR%
robocopy "%SOURCE%" "%BACKUP_DIR%" /E /COPY:DAT /R:2 /W:5 /NP /LOG+:"%TARGET%\backup-log.txt" /TEE

if %ERRORLEVEL% LEQ 7 (
    echo [%date% %time%] 备份成功: %BACKUP_DIR%
) else (
    echo [%date% %time%] 备份失败，错误码: %ERRORLEVEL%
)

:: 清理10天前的旧备份
forfiles /p "%TARGET%" /m "backup-*" /d -10 /c "cmd /c if @isdir==TRUE rmdir /s /q @path"

echo [%date% %time%] 备份任务完成
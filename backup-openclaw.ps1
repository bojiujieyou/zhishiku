$source = 'C:\Users\Administrator\.openclaw\workspace'
$target = 'G:\openclaw\OpenClaw_Backups'
$timestamp = Get-Date -Format 'yyyyMMdd-HHmm'
$backupDir = Join-Path $target "backup-$timestamp"

Write-Host "[$(Get-Date)] OpenClaw Backup Started..."
Write-Host "Source: $source"
Write-Host "Target: $backupDir"

if (-not (Test-Path $target)) {
    New-Item -ItemType Directory -Path $target -Force | Out-Null
}

$logFile = Join-Path $target 'backup-log.txt'
robocopy $source $backupDir /E /COPY:DAT /R:2 /W:5 /NP /LOG+:$logFile /TEE

$exitCode = $LASTEXITCODE
if ($exitCode -le 7) {
    Write-Host "[$(Get-Date)] Backup Successful"
    
    $size = (Get-ChildItem $backupDir -Recurse | Measure-Object -Property Length -Sum).Sum
    $sizeMB = [math]::Round($size / 1MB, 2)
    
    Write-Host "Backup Directory: $backupDir"
    Write-Host "Backup Size: $sizeMB MB"
    
    Get-ChildItem $target -Directory -Filter 'backup-*' | 
        Where-Object { $_.CreationTime -lt (Get-Date).AddDays(-10) } | 
        ForEach-Object { 
            Write-Host "Cleaning old backup: $($_.Name)"
            Remove-Item $_.FullName -Recurse -Force 
        }
    
    Write-Output "SUCCESS|$backupDir|$sizeMB"
} else {
    Write-Host "[$(Get-Date)] Backup Failed, Error Code: $exitCode"
    Write-Output "FAILED|$exitCode"
}

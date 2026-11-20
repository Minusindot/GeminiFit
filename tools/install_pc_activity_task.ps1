<#
.SYNOPSIS
  GeminiFit PC 활동 자동 동기화 작업 스케줄러 1회 설치 스크립트
  - 실행 시 GitHub PAT(GeminiFit 앱에서 쓰는 토큰과 동일)를 한 번만 입력받아
    %APPDATA%\GeminiFit\sync.json 에 안전하게 저장합니다.
  - Windows 작업 스케줄러에 로그인 시 + 30분마다 백그라운드 실행을 등록합니다.
#>
$ErrorActionPreference = "Stop"

$appDir = Join-Path $env:APPDATA "GeminiFit"
if (-not (Test-Path $appDir)) { New-Item -ItemType Directory -Path $appDir -Force | Out-Null }
$configPath = Join-Path $appDir "sync.json"

Write-Host "=== GeminiFit PC 활동 자동 동기화 설치 ===" -ForegroundColor Cyan
$token = Read-Host "GitHub Personal Access Token (ghp_... 또는 github_pat_...)"
if (-not $token) {
  Write-Host "토큰이 비어 있어 취소합니다." -ForegroundColor Yellow
  exit 1
}

$cfg = @{
  repo  = "Minusindot/GeminiFit"
  path  = "state.json"
  token = $token.Trim()
} | ConvertTo-Json
Set-Content -Path $configPath -Value $cfg -Encoding UTF8
Write-Host "설정 저장 완료: $configPath" -ForegroundColor Green

$scriptPath = Join-Path $PSScriptRoot "pc_activity_sync.ps1"
$taskName = "GeminiFit-PC-Activity-Sync"

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`" -EventType heartbeat"
$triggerLogon = New-ScheduledTaskTrigger -AtLogOn
$triggerRepeat = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger @($triggerLogon, $triggerRepeat) -Settings $settings -Description "GeminiFit PC 사용 시간대 자동 동기화 (state.json)" -Force | Out-Null

Write-Host "작업 스케줄러 등록 완료: $taskName (로그인 시 + 30분 간격 백그라운드 실행)" -ForegroundColor Green
Write-Host "지금 즉시 1회 테스트 실행합니다..." -ForegroundColor Cyan
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $scriptPath -EventType install_test

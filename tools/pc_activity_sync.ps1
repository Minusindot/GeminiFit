<#
.SYNOPSIS
  GeminiFit PC 활동 시간 자동 동기화 스크립트 (Windows)
  - PC 로그인/사용 중 주기적으로 GitHub state.json의 deviceActivity[오늘]을 업데이트합니다.
  - 토큰은 %APPDATA%\GeminiFit\sync.json 에만 저장되며 Git 저장소에 포함되지 않습니다.
#>
param(
  [string]$EventType = "heartbeat"
)

$ErrorActionPreference = "Stop"

$configPath = Join-Path $env:APPDATA "GeminiFit\sync.json"
if (-not (Test-Path $configPath)) {
  Write-Host "[GeminiFit] 설정 파일이 없습니다: $configPath"
  Write-Host "먼저 tools\install_pc_activity_task.ps1 를 실행해 GitHub 토큰을 등록해 주세요."
  exit 1
}

$cfg = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
$repo = if ($cfg.repo) { $cfg.repo } else { "Minusindot/GeminiFit" }
$path = if ($cfg.path) { $cfg.path } else { "state.json" }
$token = $cfg.token
if (-not $token) { exit 1 }

$headers = @{
  "Authorization" = "token $token"
  "Accept"        = "application/vnd.github.v3+json"
  "User-Agent"    = "GeminiFit-PC-Sync"
}

$now = Get-Date
$todayStr = $now.ToString("yyyy-MM-dd")
$timeStr  = $now.ToString("HH:mm")
$hour     = $now.Hour

$apiUrl = "https://api.github.com/repos/$repo/contents/$path"
$res = Invoke-RestMethod -Uri $apiUrl -Headers $headers -Method Get
$sha = $res.sha
$rawBytes = [System.Convert]::FromBase64String(($res.content -replace "\s", ""))
$jsonText = [System.Text.Encoding]::UTF8.GetString($rawBytes)
$state = $jsonText | ConvertFrom-Json

# Ensure deviceActivity object exists
if (-not ($state.PSObject.Properties.Name -contains "deviceActivity") -or $null -eq $state.deviceActivity) {
  $state | Add-Member -NotePropertyName "deviceActivity" -NotePropertyValue ([PSCustomObject]@{}) -Force
}

if (-not ($state.deviceActivity.PSObject.Properties.Name -contains $todayStr) -or $null -eq $state.deviceActivity.$todayStr) {
  $dayObj = [PSCustomObject]@{
    pcFirstSeen    = $timeStr
    pcLastSeen     = $timeStr
    pcHeartbeats   = 0
    phoneFirstSeen = $null
    phoneLastSeen  = $null
    lateNightPc    = $false
    lateNightLast  = $null
  }
  $state.deviceActivity | Add-Member -NotePropertyName $todayStr -NotePropertyValue $dayObj -Force
}

$todayAct = $state.deviceActivity.$todayStr
if (-not $todayAct.pcFirstSeen -or $timeStr -lt $todayAct.pcFirstSeen) {
  $todayAct.pcFirstSeen = $timeStr
}
if (-not $todayAct.pcLastSeen -or $timeStr -gt $todayAct.pcLastSeen) {
  $todayAct.pcLastSeen = $timeStr
}
$todayAct.pcHeartbeats = [int]($todayAct.pcHeartbeats) + 1

# 새벽 00:00 ~ 04:59 활동 감지 (야간 작업/수면 방해 패턴)
if ($hour -ge 0 -and $hour -lt 5) {
  $todayAct.lateNightPc = $true
  if (-not $todayAct.lateNightLast -or $timeStr -gt $todayAct.lateNightLast) {
    $todayAct.lateNightLast = $timeStr
  }
}

# Keep only last 35 days of deviceActivity to keep state.json lightweight
$allKeys = @($state.deviceActivity.PSObject.Properties.Name | Sort-Object)
if ($allKeys.Count -gt 35) {
  $toRemove = $allKeys[0..($allKeys.Count - 36)]
  foreach ($k in $toRemove) {
    $state.deviceActivity.PSObject.Properties.Remove($k)
  }
}

$updatedJson = $state | ConvertTo-Json -Depth 12
$updatedBytes = [System.Text.Encoding]::UTF8.GetBytes($updatedJson)
$updatedB64 = [System.Convert]::ToBase64String($updatedBytes)

$body = @{
  message = "PC activity sync ($todayStr $timeStr, $EventType)"
  content = $updatedB64
  sha     = $sha
} | ConvertTo-Json -Depth 5

try {
  Invoke-RestMethod -Uri $apiUrl -Headers $headers -Method Put -Body $body -ContentType "application/json; charset=utf-8" | Out-Null
  Write-Host "[GeminiFit] PC 활동 동기화 완료: $todayStr $timeStr ($EventType)"
} catch {
  # 409 conflict is harmless if phone pushed at the exact same second
  Write-Host "[GeminiFit] 동기화 건너뜀 (충돌/네트워크): $($_.Exception.Message)"
}

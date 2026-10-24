$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
if (-not (Test-Path -LiteralPath (Join-Path $taskRoot 'local-generated/EBS.zh-CN.ui.data')) -or -not (Test-Path -LiteralPath (Join-Path $taskRoot 'local-generated/EBS.sandbox.ui.data'))) {
    throw '缺少本地生成文件，请先按 README_LOCAL.md 重建补丁。'
}
$python = (Get-Command python).Source
try { $response = Invoke-WebRequest 'http://127.0.0.1:8765/local.html' -TimeoutSec 2 } catch { $response = $null }
if ($response -and $response.Headers['X-EBS-Local'] -ne '0.1.0') { throw '8765 端口被其他服务占用；请先停止该服务，不要换端口。' }
if (-not $response) {
    $server = Join-Path $taskRoot 'tools/serve_local.py'
    Start-Process -FilePath $python -ArgumentList @('"' + $server + '"') -WindowStyle Hidden
    Start-Sleep -Seconds 1
    $response = Invoke-WebRequest 'http://127.0.0.1:8765/local.html' -TimeoutSec 5
    if ($response.Headers['X-EBS-Local'] -ne '0.1.0') { throw '本地服务未正确启动。' }
}
$browserCandidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
)
$browser = $browserCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $browser) {
    $browser = Get-ChildItem -LiteralPath "$env:LOCALAPPDATA\ms-playwright" -Filter chrome.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
}
if (-not $browser) { throw '未找到 Chromium 浏览器；服务已启动，请使用独立浏览器配置打开固定地址。' }
$profile = Join-Path (Split-Path $taskRoot -Parent) 'player-profile'
# Visible window is intentional: this is the user's interactive local game.
Start-Process -FilePath $browser -ArgumentList @('--user-data-dir="' + $profile + '"','--no-first-run','http://127.0.0.1:8765/local.html')

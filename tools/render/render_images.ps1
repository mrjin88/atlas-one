param(
    [string]$ProjectPath = "E:\atlas-one\projects\lost-archive\content\LA-0001-roman-concrete"
)

Write-Host "Atlas ONE - Render Image Queue" -ForegroundColor Cyan
Write-Host "Project: $ProjectPath"

if (!(Test-Path $ProjectPath)) {
    Write-Host "Project path not found." -ForegroundColor Red
    exit 1
}

Set-Location $ProjectPath

$ShotsFile = Join-Path $ProjectPath "shots.yaml"
$ImagesDir = Join-Path $ProjectPath "assets\images"
$QueueFile = Join-Path $ProjectPath "generated\image_render_queue.csv"

if (!(Test-Path $ShotsFile)) {
    Write-Host "Missing shots.yaml" -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Force -Path $ImagesDir | Out-Null
New-Item -ItemType Directory -Force -Path "generated" | Out-Null

@"
shot_id,image_path,status,notes
RC-001,assets/images/RC-001.png,pending,Master Frame candidate
RC-002,assets/images/RC-002.png,pending,
RC-003,assets/images/RC-003.png,pending,
RC-004,assets/images/RC-004.png,pending,
RC-005,assets/images/RC-005.png,pending,
RC-006,assets/images/RC-006.png,pending,
RC-007,assets/images/RC-007.png,pending,
RC-008,assets/images/RC-008.png,pending,
RC-009,assets/images/RC-009.png,pending,
RC-010,assets/images/RC-010.png,pending,Style test
RC-011,assets/images/RC-011.png,pending,
RC-012,assets/images/RC-012.png,pending,
RC-013,assets/images/RC-013.png,pending,
RC-014,assets/images/RC-014.png,pending,
RC-015,assets/images/RC-015.png,pending,
RC-016,assets/images/RC-016.png,pending,
RC-017,assets/images/RC-017.png,pending,
RC-018,assets/images/RC-018.png,pending,
RC-019,assets/images/RC-019.png,pending,
RC-020,assets/images/RC-020.png,pending,
RC-021,assets/images/RC-021.png,pending,
RC-022,assets/images/RC-022.png,pending,
RC-023,assets/images/RC-023.png,pending,Style test
RC-024,assets/images/RC-024.png,pending,
"@ | Set-Content -Encoding UTF8 $QueueFile

Write-Host "Image render queue created:" -ForegroundColor Green
Write-Host $QueueFile
Write-Host ""
Write-Host "Next action:" -ForegroundColor Yellow
Write-Host "Render RC-001 first, save as assets\images\RC-001.png, then send it for QA."

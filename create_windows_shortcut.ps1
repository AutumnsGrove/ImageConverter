# PowerShell Script to Create ImageConverter Desktop Shortcut
# Run this script once to create a desktop shortcut for ImageConverter
# Usage: Right-click this file and select "Run with PowerShell"

Write-Host "ImageConverter - Desktop Shortcut Creator" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the current directory (where this script is located)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BatchFile = Join-Path $ScriptDir "ImageConverter.bat"

# Check if the batch file exists
if (-not (Test-Path $BatchFile)) {
    Write-Host "ERROR: ImageConverter.bat not found!" -ForegroundColor Red
    Write-Host "Expected location: $BatchFile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Get the desktop path
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "ImageConverter.lnk"

# Create the shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $BatchFile
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.Description = "ImageConverter - Batch Image Conversion Tool"
$Shortcut.WindowStyle = 1  # Normal window

# Optional: Set icon if you have one
# Uncomment the line below if you add an icon file (e.g., icon.ico)
# $Shortcut.IconLocation = Join-Path $ScriptDir "icon.ico"

$Shortcut.Save()

Write-Host "SUCCESS! Desktop shortcut created." -ForegroundColor Green
Write-Host ""
Write-Host "Shortcut location: $ShortcutPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "You can now double-click 'ImageConverter' on your desktop to launch the app." -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

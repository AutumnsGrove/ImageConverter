# Windows Setup Guide - ImageConverter

## Quick Start for Windows Users

You have **two easy options** to launch ImageConverter on Windows:

---

## Option 1: Double-Click the Batch File (Simplest)

Just double-click **`ImageConverter.bat`** in this folder to launch the GUI!

- No setup required
- Works immediately
- Can be placed anywhere (desktop, taskbar, etc.)

---

## Option 2: Create a Desktop Shortcut (Recommended)

For a proper Windows desktop shortcut with icon support:

1. **Right-click** on `create_windows_shortcut.ps1`
2. Select **"Run with PowerShell"**
3. A shortcut will appear on your desktop!

> **Note**: If PowerShell execution is blocked, you can enable it by running PowerShell as Administrator and executing:
> ```powershell
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## Adding a Custom Icon (Optional)

To give your shortcut a custom icon:

1. Find or create an `.ico` file (Windows icon format)
2. Place it in this folder and name it `icon.ico`
3. Edit `create_windows_shortcut.ps1`:
   - Find the line that says `# $Shortcut.IconLocation = ...`
   - Remove the `#` at the beginning to uncomment it
4. Run the PowerShell script again

---

## Troubleshooting

### "UV package manager not found"

If you see this error, you need to install UV:

1. Download UV from: https://github.com/astral-sh/uv
2. Or install via PowerShell:
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
3. Restart your terminal/batch file

### "Script cannot be loaded" (PowerShell error)

Run this in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### GUI doesn't appear

Make sure you've installed the dependencies:
```bash
uv sync
```

---

## Alternative: Pin to Taskbar/Start Menu

You can also:
- **Right-click** `ImageConverter.bat` → **Send to** → **Desktop (create shortcut)**
- **Right-click** the shortcut → **Pin to taskbar**
- **Right-click** the shortcut → **Pin to Start**

---

## Need Help?

See the main [README.md](README.md) for full documentation.

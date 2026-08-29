![RedeeMODLogo](./RedeeMODLogo.svg)

# RedeeMOD

[![Python code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Supported Python version](https://img.shields.io/badge/python-3.12%2B-green?style=flat-square)](https://github.com/domasles/redeemod)
[![License](https://img.shields.io/github/license/domasles/redeemod?color=red&style=flat-square)](https://github.com/domasles/redeemod/blob/main/LICENSE)
[![Build status](https://img.shields.io/github/actions/workflow/status/domasles/redeemod/build-app.yml?color=blue&style=flat-square)](https://github.com/domasles/redeemod/actions)

A custom mod launcher for games.

## Features

1. **Automatic** discovery of game installations
2. **Easy** mod management
3. **Modular** architecture for future game adaptations
4. **Cross-platform** support

## Supported Games

- **Unreal Tournament 99** and **Unreal Gold**
- **Unreal Tournament 2004**
- **IOQuake 3** (modern fork of Quake 3 engine)

## Requirements to Run

These only apply if you want to run RedeeMOD from downloaded source. If not, see [releases](https://github.com/domasles/redeemod/releases).

- **Python 3.12** or higher
- **PySide6** (Qt6 framework)

## Requirements for a Build

- **PyInstaller** (Python app packager)
- **act** (Local GitHub actions runner) (optional)

## Build Instructions

RedeeMOD supports **2 methods** of building.

To build, clone the repo:
```bash
git clone https://github.com/domasles/redeemod.git
cd redeemod
```

### Method 1 (Python and PyInstaller, Default for Most)

1. **Create a virtual environment (recommended)**:

Linux:
```bash
python -m venv venv
source ./venv/bin/activate
```

Windows CMD:
```bash
python -m venv venv
.\venv\Scripts\activate.bat
```

PowerShell:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. **Either install the package and run directly**:
```bash
pip install -e .
redeemod
```

3. **OR build a standalone binary**:

Linux:
```bash
python -m PyInstaller \
    -F -p . -n redeemod \
    -i frontend/assets/logo.ico \
    --add-data "frontend:frontend" \
    --add-data "backend:backend" \
    frontend/app.py
```

Windows CMD:
```bash
python -m PyInstaller ^
    -w -F -p . -n redeemod ^
    -i frontend/assets/logo.ico ^
    --add-data "frontend;frontend" ^
    --add-data "backend;backend" ^
    frontend/app.py
```

Powershell:
```bash
python -m PyInstaller `
    -w -F -p . -n redeemod `
    -i frontend/assets/logo.ico `
    --add-data "frontend;frontend" `
    --add-data "backend;backend" `
    frontend/app.py
```

> NOTE: You'll find the executable in `dist` directory

### Method 2 (act) (Linux builds only)

**act** allows running an isolated build environment.

Simply run `act` inside of your terminal after installing it. Necessary flags for building will be handled by the `.actrc` file.

**act** in this project is NOT meant for anything else other than testing CI/CD **builds** locally.

> NOTE: You'll find the executable in `build` directory

## Known Issues

1. **Some mods not working**<br>
    If you're on **Linux**, this might be due to the Linux nature of case sensitivity and the mod files must be either:
    1. Renamed (a common fix)
    2. Patched/modified (especially some .int and .ini files)

    If it happens across both platforms on some older Unreal Tournament '99 mods, the mod itself might be broken.

2. **Unreal Tournament 2004 mods load, but don't fully work in-game**<br>
    Mods with heavy hardcoding or GUI customizations might not work. Luckily, this game has an internal way of triggering standalone mods by visiting `Community` tab in the main menu.

    Some mods might also be conflicting, as Unreal Tournament 2004 was designed to support at most 1 mod loaded.

3. **IOQuake 3 non-standalone mods not working**<br>
    Due to no 100% accurate way of detecting if a mod requires Quake 3 Arena files, some mods might not work. Such mods include a `default.cfg` file which conflicts with detection.

    If you found such a mod, open an issue on GitHub. This might get fixed in future releases.

## Support

If you found a bug, have an idea or want to add a new game, open an issue or pull request on GitHub!

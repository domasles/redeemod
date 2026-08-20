![RedeeMODLogo](./RedeeMODLogo.svg)

# RedeeMOD

A custom and easily extensible game launcher with modding capabilities.

## What is It?

RedeeMOD is a custom mod launcher that keeps your mods organized, per game. Not only does it find your game installations, but also launches with mods applied automatically.

As of today, RedeeMOD supports **Unreal Tournament 99** and **Unreal Tournament 2004**, with a modular adapter system that makes adding more games painless.

## Features

- **Automatic Game Discovery** - Finds your UT installations on Linux and Windows without any manual setup
- **Mod Management** - Add, track, and remove mods per game. Everything continues where you left off
- **Custom Path Overrides** - Games installed somewhere unexpected? Point them to the right place!
- **Modular Adapter System** - Each game gets its own adapter, so everything stays clean, isolated, and enables every game to use its native modding capabilities
- **Cross-Platform** - Runs natively on Linux and Windows
- **Standalone Builds** - Single-file executables built with PyInstaller, along with automated CI via GitHub Actions

## Supported Games

- **Unreal Tournament 99** - Mod loading through INI patching
- **Unreal Tournament 2004** - Mod "stitching" and loading using methods native to this game

## Requirements to Run

These only apply if you want to run RedeeMOD from downloaded source. If not, look [here](https://github.com/domasles/redeemod/releases)!

- **Python 3.12** or higher
- **PySide6** - The Qt framework powering the interface

## Requirements for a Build

- **Python 3.12+**
- **PyInstaller** - To compile everything into a single binary
- **act** - To run the local GitHub actions runner (optional)

## Build Instructions

RedeeMOD supports **2 methods** for building after cloning:
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

> NOTE: Omit -e flag if you are not planning to edit the source files

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

### Method 2 (act)

**act** lets you run a local isolated environment for building that leaves nothing behind:
```bash
act workflow_dispatch
```

> NOTE: You'll find the executable in `build` directory

## Architecture

Pretty straightforward and easily maintainable:

```
redeemod/
├── backend/
│   ├── config/
│   │   └── config.json    # Default game-specific paths per platform
│   │
│   ├── games/
│   │   ├── base.py        # Abstract BaseGameAdapter class
│   │   ├── ut99/          # Unreal Tournament 99 adapter
│   │   └── ut2k4/         # Unreal Tournament 2004 adapter
│   │
│   ├── discovery.py       # Game installation path discovery
│   ├── manager.py         # Persistent user settings and mod tracking
│   ├── models.py          # Data models for configuration
│   └── constants.py       # Application-wide constants
│
├── frontend/
│   ├── app.py             # Application entry point and main window
│   ├── components/
│   │   ├── cards/         # UI cards for games and mods
│   │   ├── modals/        # Dialog windows
│   │   ├── sidebar.py     # Navigation sidebar
│   │   └── ...
│   │
│   ├── views/
│   │   ├── library.py     # Mod library view
│   │   └── games.py       # Game browser/selection view
│   │
│   └── styles/            # QSS stylesheets
│
├── .github/
│   └── workflows/
│       └── build-app.yml  # CI pipeline for Linux/Windows builds
│
├── LICENSING/
│   └── Epic.txt           # Epic Games fan content disclaimer
│
└── pyproject.toml         # Project metadata and dependencies
```

## Known issues

This project isn't without its flaws, and they could get pretty irritating:

1. **Some mods not working**<br>
    If you're on **Linux**, this might be due to the Linux nature of case sensitivity and the mod files must be either:
    1. Renamed (a common fix)
    2. Patched/modified (especially some .int and .ini files)

    If it happens across both platforms on some older Unreal Tournament '99 mods, the mod itself might be broken. During testing, a small amount of mods needed modifications to get running, thus it's not RedeeMOD's responsibility.

2. **Unreal Tournament 2004 mods load, but don't fully work in-game**<br>
    Mods with heavy hardcoding or GUI customizations might not work. Luckily, this game has an internal way of triggering standalone mods by visiting `Community` tab in the main menu.

    Some mods might also be conflicting, as Unreal Tournament 2004 was designed to support at most 1 mod loaded at a time, however such cases didn't appear while testing.

## Support

Found a bug, have an idea or want to add a game adapter? Open an issue or pull request on GitHub.

---

Built with love for the gaming community. _Open source, as intended._

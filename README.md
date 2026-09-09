# RedeeMOD

A custom mod launcher for supported games! (To find out what they are, check [this](#supported-games))

The whole idea is to make game modding as easy and as native as possible, relying on built-in modding features for games.

## Development Journey

Everything started from the frustration of trashing Unreal Tournament '99 directory with mod files. Most mods change the fundamental way of how the game works, making the original unplayable!

By researching a lot about how the .ini structure of UT works I managed to put together a simple PoC that could discover the game files and add more contents to a specific section. From then on it was only a matter of choosing the correct technologies for the frontend (nobody wants to play around with CLI!), for which I chose the Qt framework.

This project was never actually supposed to also have a nice adapter making API (see [contributing guide](./CONTRIBUTING.md) to learn more), however evaluating the potential of modding more and more games I had to implement that. Working examples prove that RedeeMOD functions (and quite well actually), but I also want to encourage the community to create more adapters and grow this launcher!

## Features

1. Auto-discovery of games
3. Modular architecture for future game adaptations
4. It's cross-platform!

## Supported Games

- Unreal Tournament 1999 and Unreal Gold
- Unreal Tournament 2004
- IOQuake 3 engine (requires running from source (oops))

## Running the Launcher!

All you have to do is:
- Download from [releases](https://github.com/domasles/redeemod/releases/latest) for your platform
- Run the executable
- Add your game (pro tip: install first so the launcher discovers games automatically!)
- Navigate to library and add mod folders
- Click the launch button and enjoy!

## Requirements to Run (from Source)

These only apply if you want to run RedeeMOD from downloaded Python source.

- Python 3.12+
- PySide6

## Requirements for a Build

- PyInstaller
- That's it!

## Build Instructions

Linux:
```bash
python -m PyInstaller -F -p . -n redeemod -i frontend/assets/logo.ico --add-data "frontend:frontend" --add-data "backend:backend" frontend/app.py
```

Powershell:
```bash
python -m PyInstaller -w -F -p . -n redeemod -i frontend/assets/logo.ico --add-data "frontend;frontend" --add-data "backend;backend" frontend/app.py
```

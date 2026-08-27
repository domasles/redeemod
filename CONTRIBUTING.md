![RedeeMODLogo](./RedeeMODLogo.svg)

# RedeeMOD Contributing Guide

[![Python code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Supported Python version](https://img.shields.io/badge/python-3.12%2B-green?style=flat-square)](https://github.com/domasles/redeemod)
[![License](https://img.shields.io/github/license/domasles/redeemod?color=red&style=flat-square)](https://github.com/domasles/redeemod/blob/main/LICENSE)
[![Build status](https://img.shields.io/github/actions/workflow/status/domasles/redeemod/build-app.yml?color=blue&style=flat-square)](https://github.com/domasles/redeemod/actions)

Welcome! If you wish to add any new game adapter, improve the interface or anyhow add to the development of RedeeMOD, you've come to the right place!

## Setup

RedeeMOD has dependencies and follows strict development rules:
1. It's **Python-exclusive**
2. Everything must be modularized
3. Do NOT modify anything that's unnecessary for the planned improvement
4. As this is both a fully-built application and a framework, coding style and file architecture must remain intact

This repository utilizes the [_Black_ formatter](https://github.com/psf/black) that you must set up by running:
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

To get started and make your first build, ensure you're using **Python 3.12** or later. Then you can either:
- Install this repo as an editable package (recommended):
```bash
pip install -e .
redeemod
```

- Or run it as a Python module:
```bash
pip install pyside6     # The only required dependency
python -m frontend.app  # From the project's root directory
```

> NOTE: Using a Python virtual environment (venv) is highly advised

## Case 1. You Want to Add a New Game Adapter

Adding a new game adapter is very simple. You'll need to do 3 things:
1. Create a directory within `backend/games` named using an ID you'll be referencing your game as in this codebase
2. Create a file called `adapter.py` - this will serve as the entry point for the adapter you'll be doing everything in (though imports are supported, so you can modularize your adapter freely)
3. Copy over the contents of `backend/games/adapter_template.py` and get started!

Adapters are discovered automatically: every directory under `backend/games` containing an `adapter.py` is imported at startup, and each class inheriting from `BaseGameAdapter` found within gets registered. No system files need to be touched to make your game appear!

### How to Use The Framework

Everything revolves around `BaseGameAdapter` (`backend/games/base.py`) - a small abstract class that handles configuration loading, path resolution and mod scanning for you. Your adapter only describes your game and how to launch it.

> NOTE: Name your directory exactly as your `game_id`. Configuration lookups and asset resolution rely on the ID, so keeping them identical is necessary

#### Properties

Override the following properties on your adapter class:

- `game_id` (**required**) - unique string used as a short identifier
- `display_name` (**required**) - the user-friendly name shown on game cards in the UI
- `logo` (**optional**) - path to your game's logo image, displayed on its card in the UI
- `file_extensions` (**optional**) - set of extensions RedeeMOD treats as mod files when scanning mod directories. Without it, every file in a selected directory will be added as a mod file. Useful when you want to restrict which files can be treated as mod files and which not
- `allowed_mod_amount` (**optional**) - caps how many mods may be selected simultaneously when launching. When unset, selection is unlimited
- `setup_message` (**optional**) - returning a non-empty string opts your game into a first-run setup flow: right after your game is added, users are shown this text, and upon confirming, your optional `setup()` override runs. Closing the prompt instead rolls back the addition. Implement `setup()` only alongside this message

Alongside these, you inherit several helpers:

- `self.adapter_assets_path` - resolves to `backend/games/<game_id>/assets`, whether or not it exists yet. You can put your file assets there, later to be used by the RedeeMOD app (for example, a logo)
- `self.scan_mod_directory(target_dir)` - recursively collects files matching `file_extensions`, returning `(file_path, lowercase_extension)` tuples
- `self.all_configured_data` - every path group defined for your game in `config.json`, resolved for the current platform (as of now, only **Linux** and **Windows** are supported)
- `self.get_missing_paths()` - names of paths within `config.json` that couldn't be resolved on a machine (the interface uses this to warn users before launching)
- And more useful methods from across the backend!

You are not **required** to use any of these, but they can speed up development significantly!

#### Game Setup

If your game requires some form of setup before being added to RedeeMOD, instead of prompting users for manual work, any game can be set up automatically!

By implementing the `setup_message` property and `setup` method you can control what happens the exact moment a user adds the game.

#### Configuration (config.json)

All required filesystem locations must live in `backend/games/<game_id>/config/config.json`:

```json
{
    "executable_paths": {
        "linux": ["~/.local/share/MyGame/Binaries/mygame"],
        "windows": ["C:\\MyGame\\Binaries\\mygame.exe"]
    },

    "config_paths": {
        "linux": ["~/.mygame/mygame.ini"],
        "windows": ["C:\\MyGame\\MyGame.ini"]
    }
}
```

> NOTE: Leaving any `*_paths` object empty will make it required for user to input without automatic discovery. This is useful if your game does NOT have a standard install path (as seen in `backend/games/ioq3/`)

Rules of the format:

- Any key ending in `_paths` defines a path group, holding a `linux` and/or `windows` list of candidate locations - the first one that exists on disk wins
- Each group becomes a singular attribute on your adapter automatically: `executable_paths` gives you `self.executable_path`, `config_paths` gives you `self.config_path`, and so on
- Paths support `~` and environment variables, they are later expanded
- Users may override any group through the interface and their custom paths are merged in. Custom paths take priority over pre-configured ones
- Only define groups your adapter actually references - don't configure things you'll never read

#### Launching the Game

The heart of every adapter is `launch(selected_mod_paths)`, receiving the list of selected mod directories. Game processes are spawned through `subprocess.Popen()`, so the game runs independently without freezing the launcher:

```python
subprocess.Popen(cmd, cwd=str(self.executable_path.parent))
```

What happens beforehand depends entirely on your game's modding mechanics. Both bundled adapters follow the same pattern - point the game at selected mods and pass them to game's executable as a command-line argument. However, if your game does not support dedicated modding capabilities, any other implementation is fine! No game is like the others, thus why extensible adapter system of RedeeMOD exists!

See existing `backend/games/<game_id>/adapter.py` files for complete working examples!

> NOTE: Validate that your executable exists and fail early if it doesn't (`raise FileNotFoundError(...)`), exactly like the bundled adapters do

> NOTE: Raising any other error on launch will notify users on frontend. This is useful if you want to validate game asset presence or handle edge cases

#### Adding a Logo

Create an `assets` directory next to your `adapter.py` and drop your logo in:

```
backend/games/<game_id>/assets/logo.svg
```

> NOTE: Many image formats are supported, but using `.svg` is recommended

Then override the property:

```python
@property
def logo(self) -> Path | None:
    return self.adapter_assets_path / "logo.svg"
```

## Case 2. You Want to Modify Frontend

The interface is built with **PySide6** (Qt 6) and kept deliberately thin - it renders whatever adapters provide and never references concrete games directly:

- `frontend/app.py` - the entry point. Assembles the main window: a `Sidebar` for navigation and a stacked widget holding the screens
- `frontend/views/` - the screens themselves: `games.py` (game grid, adding/removing games) and `library.py` (browsing mods of a chosen game)
- `frontend/components/` - reusable widgets: card variants (`cards/`), modal dialogs (`modals/`), banners, dropdowns, labels, etc.
- `frontend/styles/style.qss` - all styling lives here, written as Qt Style Sheets
- `backend/manager.py` - the bridge between both halves. A `QObject` exposing signals (e.g. `games_changed`) and persisting user choices into `user_settings.json` in the application data directory

> NOTE: If you ever find yourself importing a specific game adapter inside `frontend/`, stop and keep the layers separate!

---

Thank you for checking out RedeeMOD! A maintainer will review your Pull Request as soon as possible.

*Stay creative, smart and open!*

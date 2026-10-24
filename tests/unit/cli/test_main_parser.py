from cli.app import build_parser


def test_parser_list_games_defaults_to_added():
    args = build_parser().parse_args(["list-games"])

    assert args.command == "list-games"
    assert args.available is False


def test_parser_list_games_available_flag():
    args = build_parser().parse_args(["list-games", "--available"])

    assert args.command == "list-games"
    assert args.available is True


def test_parser_add_game_defaults():
    args = build_parser().parse_args(["add-game", "ut99"])

    assert args.command == "add-game"
    assert args.game_id == "ut99"
    assert args.set_path == []


def test_parser_add_game_set_path():
    args = build_parser().parse_args(["add-game", "ut99", "--set-path", "executable_path=/games/ut99/ut-bin"])

    assert args.command == "add-game"
    assert args.game_id == "ut99"
    assert args.set_path == ["executable_path=/games/ut99/ut-bin"]


def test_parser_remove_game():
    args = build_parser().parse_args(["remove-game", "ut99"])

    assert args.command == "remove-game"
    assert args.game_id == "ut99"


def test_parser_launch_game_with_mods():
    args = build_parser().parse_args(["launch", "ut99", "/tmp/mod-1", "/tmp/mod-2"])

    assert args.command == "launch"
    assert args.game_id == "ut99"
    assert args.mod_refs == ["/tmp/mod-1", "/tmp/mod-2"]


def test_parser_launch_game_standalone():
    args = build_parser().parse_args(["launch", "ut99"])

    assert args.command == "launch"
    assert args.game_id == "ut99"
    assert args.mod_refs == []


def test_parser_list_mods():
    args = build_parser().parse_args(["list-mods", "ut99"])

    assert args.command == "list-mods"
    assert args.game_id == "ut99"


def test_parser_add_mods():
    args = build_parser().parse_args(["add-mods", "ut99", "/tmp/mod-1", "/tmp/mod-2"])

    assert args.command == "add-mods"
    assert args.game_id == "ut99"
    assert args.mod_paths == ["/tmp/mod-1", "/tmp/mod-2"]


def test_parser_remove_mods():
    args = build_parser().parse_args(["remove-mods", "ut99", "mod-1", "/tmp/mod-2"])

    assert args.command == "remove-mods"
    assert args.game_id == "ut99"
    assert args.mod_refs == ["mod-1", "/tmp/mod-2"]

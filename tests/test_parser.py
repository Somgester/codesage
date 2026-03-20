
from pathlib import Path

import pytest
from tree_sitter import Language, Node, Parser

from codesage.parser.tree_sitter_parser import (
    detect_language,
    get_parser,
    load_language,
    parse_file,
)


def test_detect_language():
    py_path = Path("test.py")
    assert detect_language(py_path) == "python"

    txt_path = Path("test.txt")
    assert detect_language(txt_path) is None

    no_ext_path = Path("test")
    assert detect_language(no_ext_path) is None

def test_load_language():
    python_lang = load_language("python")
    assert isinstance(python_lang, Language)
    with pytest.raises(ValueError):
        load_language("unsupported_lang")

def test_get_parser():
    python_parser = get_parser("python")
    assert isinstance(python_parser, Parser)
    assert python_parser.language is not None

def test_parse_file(tmp_path: Path):
    py_file = tmp_path / "test_script.py"
    py_file.write_text("def hello():\n    print('Hello, world!')")

    root_node = parse_file(py_file)
    assert isinstance(root_node, Node)
    assert root_node.type == "module"

    unsupported_file = tmp_path / "test_script.txt"
    unsupported_file.write_text("some text")

    with pytest.raises(ValueError):
        parse_file(unsupported_file)

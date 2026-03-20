from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Node, Parser

# supported languages and their file extensions
language_extensions: dict[str, tuple[str]] = {
    "python": (".py",)
}

# mapping from langauge names to their tree-sitter language loader functions
language_loaders: dict[str, Callable[[], Language]] = {
    "python": lambda: Language(tspython.language())
}

def detect_language(path: Path) -> str | None:
    ext=path.suffix.lower()
    for lang, exts in language_extensions.items():
        if ext in exts:
            return lang
    return None

def load_language(lang: str) -> Language:
    loader = language_loaders.get(lang)
    if loader:
        return loader()
    raise ValueError(f"Unsupported language, wait for future updates...: {lang}")

def get_parser(lang: str) -> Parser:
    language = load_language(lang)
    parser = Parser()
    parser.language = language

    return parser

def parse_file(path: Path) -> Node:
    lang = detect_language(path)
    if not lang:
        raise ValueError(f"No supported language found for file: {path}")

    source = path.read_bytes()
    tree = get_parser(lang).parse(source)
    return tree.root_node

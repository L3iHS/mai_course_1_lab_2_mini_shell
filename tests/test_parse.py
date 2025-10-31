from src.main import parse
import pytest

def test_parse_basic():
    name, args = parse("ls src")
    assert name == "ls"
    assert args == ["src"]

def test_parse_with_quotes():
    name, args = parse('cat "file name.txt"')
    assert args == ["file name.txt"]

def test_parse_unclosed_quotes():
    with pytest.raises(ValueError):
        parse('cat "oops.txt')
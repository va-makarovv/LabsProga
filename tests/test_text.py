import pytest

from src.lib.text import normalize, tokenize, count_freq, top_n


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
        ("", ""),
    ],
)
def test_normalize_basic(source: str, expected: str) -> None:
    """Базовые случаи нормализации."""
    assert normalize(source) == expected


def test_normalize_yo2e_flag() -> None:
    """Проверяем флаг yo2e — замена ё/Ё на е/Е."""
    text = "ёжик ёлка"
    # по умолчанию yo2e=True → буква "ё" заменяется на "е"
    assert normalize(text) == "ежик елка"
    assert normalize(text, yo2e=True) == "ежик елка"
    # если yo2e выключен — буква "ё" сохраняется
    assert normalize(text, yo2e=False) == "ёжик ёлка"


@pytest.mark.parametrize(
    "source, expected_tokens",
    [
        ("привет мир", ["привет", "мир"]),
        ("hello.txt,world!!!", ["hello", "txt", "world"]),
        ("по-настоящему круто", ["по-настоящему", "круто"]),
        ("2025 год", ["2025", "год"]),
        ("emoji 😀 не слово", ["emoji", "не", "слово"]),
        ("", []),
    ],
)
def test_tokenize_basic(source: str, expected_tokens: list[str]) -> None:
    """Тесты токенизации (после normalize)."""
    tokens = tokenize(normalize(source))
    assert tokens == expected_tokens


def test_count_freq_and_top_n() -> None:
    """Связка count_freq + top_n на базовом примере и граничных значениях."""
    tokens = ["a", "b", "a", "c", "b", "a"]
    freq = count_freq(tokens)

    # частоты считаются корректно
    assert freq == {"a": 3, "b": 2, "c": 1}

    # top_n с n=2
    top2 = top_n(freq, n=2)
    assert top2 == [("a", 3), ("b", 2)]

    # пустой словарь → пустой список
    assert top_n({}, n=5) == []


def test_top_n_tie_breaker() -> None:
    """
    При одинаковой частоте слова должны сортироваться по алфавиту.
    """
    tokens = ["bb", "aa", "bb", "aa", "cc"]
    freq = count_freq(tokens)

    # "aa" и "bb" встречаются по 2 раза,
    # сортировка: сначала по убыванию частоты, потом по слову
    top2 = top_n(freq, n=2)
    assert top2 == [("aa", 2), ("bb", 2)]

    # если n больше числа уникальных слов — возвращаем все
    top_all = top_n(freq, n=10)
    assert top_all == [("aa", 2), ("bb", 2), ("cc", 1)]
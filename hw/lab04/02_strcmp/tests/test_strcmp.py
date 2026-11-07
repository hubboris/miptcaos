import os
import re
import random
import subprocess
import pytest

# Директория самой задачи (на уровень выше директории tests)
TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BINARY = os.path.join(TASK_DIR, "solution")
SOURCE = os.path.join(TASK_DIR, "my_strcmp.c")


def strip_comments_and_literals(code: str) -> str:
    """Убирает комментарии, строковые и символьные литералы."""
    pattern = re.compile(
        r"""//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'""", re.S
    )
    return pattern.sub(" ", code)


@pytest.fixture(scope="module", autouse=True)
def build():
    """Сборка решения через make до тестов и очистка после."""
    subprocess.run(["make", "clean"], cwd=TASK_DIR, capture_output=True)
    res = subprocess.run(["make"], cwd=TASK_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"Команда make завершилась с ошибкой:\n{res.stderr}"
    assert os.path.exists(BINARY), "Исполняемый файл solution не найден в корне задачи"
    yield
    subprocess.run(["make", "clean"], cwd=TASK_DIR, capture_output=True)


def run(pairs):
    data = str(len(pairs)).encode() + b"\n"
    for a, b in pairs:
        data += a + b"\n" + b + b"\n"
    res = subprocess.run([BINARY], input=data, capture_output=True, timeout=10)
    assert res.returncode == 0, "Программа вернула ненулевой код"
    return res.stdout.decode().split()


def expected(pairs):
    out = []
    for a, b in pairs:
        out.append("less" if a < b else "greater" if a > b else "equal")
    return out


# ---------- проверки исходного кода ----------

def test_no_square_brackets():
    code = strip_comments_and_literals(open(SOURCE, encoding="utf-8").read())
    assert "[" not in code and "]" not in code, (
        "В my_strcmp.c нельзя использовать квадратные скобки: только арифметика указателей"
    )


def test_no_string_h_functions():
    code = strip_comments_and_literals(open(SOURCE, encoding="utf-8").read())
    assert "string.h" not in open(SOURCE, encoding="utf-8").read(), "Нельзя подключать <string.h>"
    assert not re.search(r"(?<![A-Za-z0-9_])(strcmp|strncmp|memcmp|strcoll)\s*\(", code), (
        "Нельзя использовать стандартные функции сравнения"
    )


# ---------- проверки работы ----------

BASIC = [
    (b"apple", b"apple"),
    (b"apple", b"banana"),
    (b"banana", b"apple"),
    (b"b", b"a"),
    (b"a", b"b"),
    (b"abc", b"ab"),
    (b"ab", b"abc"),
    (b"", b""),
    (b"", b"a"),
    (b"a", b""),
    (b"abc", b"abd"),
    (b"abd", b"abc"),
    (b"Hello", b"hello"),
    (b"hello", b"Hello"),
    (b"Z", b"a"),
    (b"hello world", b"hello world"),
    (b"hello world", b"hello  world"),
    (b" a", b"a"),
    (b"a ", b"a"),
    (b"123", b"1234"),
    (b"10", b"9"),
    (b"~", b"!"),
]


def test_example():
    pairs = [(b"apple", b"apple"), (b"apple", b"banana"), (b"b", b"a"), (b"abc", b"ab")]
    assert run(pairs) == ["equal", "less", "greater", "greater"]


@pytest.mark.parametrize("pair", BASIC, ids=[f"{a!r}-{b!r}" for a, b in BASIC])
def test_basic_pairs(pair):
    assert run([pair]) == expected([pair])


def test_all_basic_in_one_run():
    assert run(BASIC) == expected(BASIC)


def test_non_ascii_bytes_compared_as_unsigned():
    pairs = [
        ("я".encode(), b"a"),
        (b"a", "я".encode()),
        ("привет".encode(), "приветик".encode()),
        ("мир".encode(), "мир".encode()),
        ("Я".encode(), "я".encode()),
        (b"\x7f", b"\x80"),
        (b"\xff", b"\x01"),
        (b"\x80a", b"\x80b"),
    ]
    assert run(pairs) == expected(pairs)


def test_long_strings():
    base = b"x" * 1000
    pairs = [
        (base, base),
        (base[:-1] + b"y", base),
        (base, base[:-1] + b"w"),
        (base, base[:-1]),
        (b"a" * 500 + b"b" + b"a" * 499, b"a" * 500 + b"c" + b"a" * 499),
    ]
    assert run(pairs) == expected(pairs)


def test_zero_pairs():
    assert run([]) == []


@pytest.mark.parametrize("seed", range(5))
def test_random(seed):
    rnd = random.Random(seed)
    alphabet = b"abcAB 01"
    pairs = []
    for _ in range(100):
        la, lb = rnd.randint(0, 8), rnd.randint(0, 8)
        a = bytes(rnd.choice(alphabet) for _ in range(la))
        b = a[: rnd.randint(0, la)] + bytes(rnd.choice(alphabet) for _ in range(rnd.randint(0, 3))) \
            if rnd.random() < 0.5 else bytes(rnd.choice(alphabet) for _ in range(lb))
        pairs.append((a, b))
    assert run(pairs) == expected(pairs)

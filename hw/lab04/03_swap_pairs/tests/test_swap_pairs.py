import os
import re
import random
import subprocess
import pytest

# Директория самой задачи (на уровень выше директории tests)
TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BINARY = os.path.join(TASK_DIR, "solution")
SOURCE = os.path.join(TASK_DIR, "swap_pairs.c")

INT_MIN = -(2**31)
INT_MAX = 2**31 - 1


def read_source():
    return open(SOURCE, encoding="utf-8").read()


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


def run(arr, sep=" "):
    text = f"{len(arr)}\n" + sep.join(map(str, arr)) + "\n"
    res = subprocess.run(
        [BINARY], input=text, capture_output=True, text=True, timeout=10
    )
    assert res.returncode == 0, (
        f"Код возврата {res.returncode}. stderr: {res.stderr.strip()}"
    )
    return res.stdout


def expected(arr):
    a = list(arr)
    for i in range(0, len(a) - 1, 2):
        a[i], a[i + 1] = a[i + 1], a[i]
    return " ".join(map(str, a))


# ---------- проверки исходного кода ----------

def test_no_square_brackets():
    code = strip_comments_and_literals(read_source())
    assert "[" not in code and "]" not in code, (
        "В swap_pairs.c нельзя использовать квадратные скобки: только указатели"
    )


def test_no_extra_memory():
    code = strip_comments_and_literals(read_source())
    assert not re.search(
        r"(?<![A-Za-z0-9_])(malloc|calloc|realloc|alloca|memcpy|memmove|memset)\s*\(", code
    ), "Нельзя выделять память и копировать массив: решение должно работать на месте"
    raw = read_source()
    assert "string.h" not in raw and "stdlib.h" not in raw, (
        "Нельзя подключать <string.h> и <stdlib.h>"
    )


# ---------- проверки работы ----------

def test_example_even():
    assert run([1, 2, 3, 4, 5, 6]).strip() == "2 1 4 3 6 5"


def test_example_odd():
    assert run([10, 20, 30, 40, 50]).strip() == "20 10 40 30 50"


def test_empty():
    assert run([]).strip() == ""


def test_single():
    assert run([42]).strip() == "42"


def test_two():
    assert run([1, 2]).strip() == "2 1"


def test_three():
    assert run([1, 2, 3]).strip() == "2 1 3"


@pytest.mark.parametrize("n", list(range(0, 21)))
def test_sizes(n):
    arr = list(range(1, n + 1))
    assert run(arr).strip() == expected(arr)


def test_extreme_values():
    arr = [INT_MAX, INT_MIN, 0, -1, INT_MIN, INT_MAX, 7]
    assert run(arr).strip() == expected(arr)


def test_equal_elements():
    arr = [5, 5, 5, 5, 5]
    assert run(arr).strip() == "5 5 5 5 5"


def test_negative_numbers():
    arr = [-1, -2, -3, -4]
    assert run(arr).strip() == "-2 -1 -4 -3"


def test_input_on_separate_lines():
    arr = [1, 2, 3, 4, 5]
    assert run(arr, sep="\n").strip() == "2 1 4 3 5"


@pytest.mark.parametrize("n", [999, 1000])
def test_max_sizes(n):
    arr = list(range(n))
    assert run(arr).strip() == expected(arr)


@pytest.mark.parametrize("seed", range(10))
def test_random(seed):
    rnd = random.Random(seed)
    n = rnd.randint(0, 1000)
    arr = [rnd.randint(INT_MIN, INT_MAX) for _ in range(n)]
    assert run(arr).strip() == expected(arr)

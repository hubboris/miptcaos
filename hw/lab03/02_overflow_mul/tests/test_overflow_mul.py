import os
import subprocess
import pytest

# Директория самой задачи (на уровень выше директории tests)
TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BINARY = os.path.join(TASK_DIR, "solution")

INT_MIN = -(2**31)
INT_MAX = 2**31 - 1


@pytest.fixture(scope="module", autouse=True)
def build():
    """Сборка решения через make до тестов и очистка после."""
    subprocess.run(["make", "clean"], cwd=TASK_DIR, capture_output=True)
    res = subprocess.run(["make"], cwd=TASK_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"Команда make завершилась с ошибкой:\n{res.stderr}"
    assert os.path.exists(BINARY), "Исполняемый файл solution не найден в корне задачи"
    yield
    subprocess.run(["make", "clean"], cwd=TASK_DIR, capture_output=True)


def run(a, b):
    res = subprocess.run(
        [BINARY], input=f"{a} {b}\n", capture_output=True, text=True, timeout=5
    )
    assert res.returncode == 0, "Программа вернула ненулевой код"
    return res.stdout


def expected(a, b):
    p = a * b
    if p < INT_MIN or p > INT_MAX:
        return "Overflow"
    return f"Product: {p}"


@pytest.mark.parametrize(
    "a, b",
    [
        (0, 0),
        (0, INT_MAX),
        (INT_MIN, 0),
        (1, 1),
        (1000, 1000),
        (-1000, 1000),
        (-1000, -1000),
        (46340, 46340),
        (46341, 46341),
        (-46341, 46341),
        (65536, 32768),
        (65536, 32767),
        (-65536, 32768),
        (-65536, 32769),
        (100000, 100000),
        (INT_MAX, 1),
        (INT_MAX, -1),
        (INT_MAX, 2),
        (INT_MAX, -2),
        (INT_MIN, 1),
        (INT_MIN, -1),
        (INT_MIN, 2),
        (-1, INT_MIN),
        (INT_MIN, INT_MIN),
        (INT_MAX, INT_MAX),
        (2, 1073741823),
        (2, 1073741824),
        (-2, 1073741824),
        (-2, 1073741825),
    ],
)
def test_multiplication(a, b):
    out = run(a, b)
    assert out.strip() == expected(a, b), (
        f"Ввод: {a} {b}\nОжидалось: {expected(a, b)}\nПолучено: {out}"
    )

import os
import subprocess
import pytest

# Директория самой задачи (на уровень выше директории tests)
TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BINARY = os.path.join(TASK_DIR, "solution")


@pytest.fixture(scope="module", autouse=True)
def build():
    """Сборка решения через make до тестов и очистка после."""
    subprocess.run(["make", "clean"], cwd=TASK_DIR, capture_output=True)
    res = subprocess.run(["make"], cwd=TASK_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"Команда make завершилась с ошибкой:\n{res.stderr}"
    assert os.path.exists(BINARY), "Исполняемый файл solution не найден в корне задачи"
    yield
    subprocess.run(["make", "clean"], cwd=TASK_DIR, capture_output=True)


def run(x):
    res = subprocess.run(
        [BINARY], input=f"{x}\n", capture_output=True, text=True, timeout=5
    )
    assert res.returncode == 0, "Программа вернула ненулевой код"
    return res.stdout


def swap(x):
    return int.from_bytes(x.to_bytes(4, "big"), "little")


def expected(x):
    y = swap(x)
    return f"Decimal: {y}\nHex: 0x{y:08X}"


@pytest.mark.parametrize(
    "x",
    [
        0,
        1,
        255,
        256,
        0x12345678,
        0x78563412,
        0xDEADBEEF,
        0xAABBCCDD,
        0x000000FF,
        0xFF000000,
        0x00FF00FF,
        0x01020304,
        0x80000000,
        0x7FFFFFFF,
        0xFFFFFFFF,
        305419896,
        4294967295,
        123456789,
    ],
)
def test_byte_swap(x):
    out = run(x)
    assert out.strip() == expected(x), (
        f"Ввод: {x}\nОжидалось:\n{expected(x)}\nПолучено:\n{out}"
    )


def test_double_swap_is_identity():
    """Двойное применение даёт исходное число."""
    x = 0xCAFEBABE
    first = int(run(x).splitlines()[0].split(": ")[1])
    second = int(run(first).splitlines()[0].split(": ")[1])
    assert second == x

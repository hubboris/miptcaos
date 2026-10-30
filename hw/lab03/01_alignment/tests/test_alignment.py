import os
import subprocess
import pytest

# Директория самой задачи (на уровень выше директории tests)
TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(TASK_DIR, "solution.c")
BINARY = os.path.join(TASK_DIR, "solution")


@pytest.fixture(scope="module", autouse=True)
def build():
    """Компиляция решения до тестов и удаление бинарного файла после."""
    if os.path.exists(BINARY):
        os.remove(BINARY)
    res = subprocess.run(
        ["gcc", "-Wall", "-Wextra", "-o", BINARY, SOURCE],
        cwd=TASK_DIR,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"Компиляция solution.c не удалась:\n{res.stderr}"
    yield
    if os.path.exists(BINARY):
        os.remove(BINARY)


def run(addr, align):
    res = subprocess.run(
        [BINARY], input=f"{addr} {align}\n", capture_output=True, text=True, timeout=5
    )
    assert res.returncode == 0, "Программа вернула ненулевой код"
    return res.stdout


def expected(addr, align):
    aligned = "yes" if addr % align == 0 else "no"
    down = addr // align * align
    up = (addr + align - 1) // align * align
    return f"Aligned: {aligned}\nDown: {down}\nUp: {up}\n"


@pytest.mark.parametrize(
    "addr, align",
    [
        (13, 8),
        (24, 8),
        (0, 8),
        (1, 1),
        (7, 1),
        (1, 16),
        (15, 16),
        (16, 16),
        (17, 16),
        (100, 7),
        (4096, 4096),
        (4097, 4096),
        (123456789, 64),
        (4294967296, 4096),
        (4294967297, 4096),
    ],
)
def test_alignment(addr, align):
    out = run(addr, align)
    assert out.split() == expected(addr, align).split(), (
        f"Ввод: {addr} {align}\nОжидалось:\n{expected(addr, align)}Получено:\n{out}"
    )


def test_output_format():
    """Проверка точного формата вывода (три строки)."""
    out = run(13, 8)
    assert out.strip().splitlines() == ["Aligned: no", "Down: 8", "Up: 16"]

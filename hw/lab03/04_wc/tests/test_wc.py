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


def run(data: bytes):
    res = subprocess.run([BINARY], input=data, capture_output=True, timeout=10)
    assert res.returncode == 0, "Программа вернула ненулевой код"
    return res.stdout.decode()


def expected(data: bytes):
    chars = len(data)
    lines = data.count(b"\n")
    words = len(data.replace(b"\t", b" ").replace(b"\n", b" ").split())
    return f"Chars: {chars}\nWords: {words}\nLines: {lines}"


CASES = [
    b"",
    b"\n",
    b" ",
    b"   \t  \n\n \t",
    b"hello",
    b"hello\n",
    b"hello world\nfoo\n",
    b"hello world\nfoo",
    b"  leading and trailing  \n",
    b"many     spaces    between\twords\t\tand tabs\n",
    b"one\ntwo\nthree\nfour\n",
    b"\n\n\nword\n\n\n",
    b"a b c d e f g h i j\n",
    b"line without newline at the end",
    b"punctuation, is: part-of; words! (yes?)\n",
    "Привет, мир!\nвторая строка\n".encode("utf-8"),
    b"a" * 100000 + b"\n",
    (b"word " * 20000) + b"\n",
    b"x\ty\nz \n",
]


@pytest.mark.parametrize("data", CASES, ids=[f"case{i}" for i in range(len(CASES))])
def test_wc(data):
    out = run(data)
    assert out.strip() == expected(data), (
        f"Ввод: {data[:80]!r}\nОжидалось:\n{expected(data)}\nПолучено:\n{out}"
    )


def test_example():
    out = run(b"hello world\nfoo\n")
    assert out.strip().splitlines() == ["Chars: 16", "Words: 3", "Lines: 2"]

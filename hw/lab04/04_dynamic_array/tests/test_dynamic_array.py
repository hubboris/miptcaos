import os
import re
import random
import subprocess
import pytest

# Директория самой задачи (на уровень выше директории tests)
TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BINARY = os.path.join(TASK_DIR, "solution")
BINARY_ASAN = os.path.join(TASK_DIR, "solution_asan")
SOURCE = os.path.join(TASK_DIR, "int_vec.c")

INT_MAX = 2**31 - 1
INT_MIN = -(2**31)


def strip_comments_and_literals(code: str) -> str:
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


def run(numbers, binary=BINARY, sep=" "):
    text = sep.join(map(str, numbers)) + "\n"
    res = subprocess.run(
        [binary], input=text, capture_output=True, text=True, timeout=30
    )
    return res


def capacity_for(count):
    cap = 4
    while cap < count:
        cap *= 2
    return cap


def expected(numbers):
    kept = []
    for x in numbers:
        if x < 0:
            break
        if x % 2 == 0:
            kept.append(x)
    return (
        " ".join(map(str, kept)) + "\n"
        f"Count: {len(kept)}\n"
        f"Capacity: {capacity_for(len(kept))}\n"
    )


def check(numbers, **kw):
    res = run(numbers, **kw)
    assert res.returncode == 0, f"Код возврата {res.returncode}. stderr: {res.stderr}"
    assert res.stdout == expected(numbers), (
        f"Ввод: {numbers[:30]}{'...' if len(numbers) > 30 else ''}\n"
        f"Ожидалось:\n{expected(numbers)[:300]}\nПолучено:\n{res.stdout[:300]}"
    )


# ---------- проверки исходного кода ----------

def test_uses_realloc():
    code = strip_comments_and_literals(open(SOURCE, encoding="utf-8").read())
    assert re.search(r"(?<![A-Za-z0-9_])realloc\s*\(", code), (
        "Увеличение ёмкости должно выполняться через realloc"
    )


def test_frees_memory():
    code = strip_comments_and_literals(open(SOURCE, encoding="utf-8").read())
    assert re.search(r"(?<![A-Za-z0-9_])free\s*\(", code), "Память нужно освобождать через free"


# ---------- проверки работы ----------

def test_example_1():
    res = run([3, 8, 15, 4, 0, 7, 10, -1, 6])
    assert res.returncode == 0
    assert res.stdout == "8 4 0 10\nCount: 4\nCapacity: 4\n"


def test_example_2():
    res = run([2, 4, 6, 8, 10, 12, -5])
    assert res.returncode == 0
    assert res.stdout == "2 4 6 8 10 12\nCount: 6\nCapacity: 8\n"


def test_example_empty():
    res = run([-1])
    assert res.returncode == 0
    assert res.stdout == "\nCount: 0\nCapacity: 4\n"


def test_empty_input_without_terminator():
    res = subprocess.run([BINARY], input="", capture_output=True, text=True, timeout=10)
    assert res.returncode == 0
    assert res.stdout == "\nCount: 0\nCapacity: 4\n"


def test_no_terminator_reads_until_eof():
    check([2, 4, 5, 6])


def test_zero_is_even():
    check([0, 0, 0, -1])


def test_only_odd_numbers():
    check([1, 3, 5, 7, 9, 11, -2])


def test_terminator_stops_reading():
    check([2, -1, 4, 6, 8, 10, 12, 14])


def test_first_number_negative():
    check([-4, 2, 4])


def test_extreme_values():
    check([INT_MAX - 1, 0, 2, INT_MAX, 4, 6, 8, INT_MIN])


def test_input_on_separate_lines():
    check([2, 4, 6, 8, 10, 12, 14, 16, 18, -1], sep="\n")


@pytest.mark.parametrize("count", list(range(0, 70)))
def test_capacity_growth(count):
    """Ёмкость после count чётных чисел: 4, затем удваивается при заполнении."""
    nums = [2 * i for i in range(count)] + [-1]
    res = run(nums)
    assert res.returncode == 0
    lines = res.stdout.splitlines()
    assert lines[1] == f"Count: {count}"
    assert lines[2] == f"Capacity: {capacity_for(count)}", (
        f"Для {count} чётных чисел ёмкость должна быть {capacity_for(count)}"
    )


def test_capacity_boundary_values():
    for count, cap in [(4, 4), (5, 8), (8, 8), (9, 16), (16, 16), (17, 32)]:
        nums = [2] * count + [-1]
        res = run(nums)
        assert f"Capacity: {cap}" in res.stdout, f"count={count}: ожидалась ёмкость {cap}"


def test_odd_numbers_do_not_grow_capacity():
    nums = [1] * 100 + [2, 4, -1]
    res = run(nums)
    assert res.stdout == "2 4\nCount: 2\nCapacity: 4\n"


def test_large_input():
    rnd = random.Random(1)
    nums = [rnd.randint(0, INT_MAX) for _ in range(200000)] + [-1]
    check(nums)


def test_large_all_even():
    nums = [2 * i for i in range(100000)] + [-1]
    res = run(nums)
    assert res.returncode == 0
    assert res.stdout.splitlines()[1:] == ["Count: 100000", "Capacity: 131072"]


@pytest.mark.parametrize("seed", range(10))
def test_random(seed):
    rnd = random.Random(seed)
    nums = [rnd.randint(0, 1000) for _ in range(rnd.randint(0, 200))]
    if rnd.random() < 0.7:
        nums.append(-rnd.randint(1, 100))
        nums += [rnd.randint(0, 1000) for _ in range(rnd.randint(0, 20))]
    check(nums)


# ---------- проверка памяти (AddressSanitizer + LeakSanitizer) ----------

@pytest.fixture(scope="module")
def asan_binary():
    res = subprocess.run(["make", "asan"], cwd=TASK_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        pytest.skip(f"Сборка с санитайзерами недоступна:\n{res.stderr}")
    return BINARY_ASAN


@pytest.mark.parametrize(
    "nums",
    [
        [-1],
        [2, 4, -1],
        [2, 4, 6, 8, 10, -1],
        [2 * i for i in range(33)] + [-1],
        [2 * i for i in range(1000)] + [-1],
        [1, 3, 5],
    ],
    ids=["empty", "two", "grow-once", "grow-to-64", "thousand", "no-evens-eof"],
)
def test_no_memory_errors(asan_binary, nums):
    env = dict(os.environ, ASAN_OPTIONS="detect_leaks=1:abort_on_error=0")
    res = subprocess.run(
        [asan_binary],
        input=" ".join(map(str, nums)) + "\n",
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
    )
    assert res.returncode == 0, (
        f"Санитайзер обнаружил проблему с памятью (код {res.returncode}):\n{res.stderr[:1500]}"
    )

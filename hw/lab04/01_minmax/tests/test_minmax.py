import os
import random
import subprocess
import pytest

# Директория самой задачи (на уровень выше директории tests)
TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BINARY = os.path.join(TASK_DIR, "solution")

LL_MIN = -(2**63)
LL_MAX = 2**63 - 1


@pytest.fixture(scope="module", autouse=True)
def build():
    """Сборка решения через make до тестов и очистка после."""
    subprocess.run(["make", "clean"], cwd=TASK_DIR, capture_output=True)
    res = subprocess.run(["make"], cwd=TASK_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"Команда make завершилась с ошибкой:\n{res.stderr}"
    assert os.path.exists(BINARY), "Исполняемый файл solution не найден в корне задачи"
    yield
    subprocess.run(["make", "clean"], cwd=TASK_DIR, capture_output=True)


def run(*args):
    res = subprocess.run(
        [BINARY, *map(str, args)], capture_output=True, text=True, timeout=10
    )
    assert res.returncode == 0, f"Код возврата {res.returncode}, ожидался 0"
    return res


def warnings(res):
    return [l for l in res.stderr.splitlines() if l.strip()]


@pytest.mark.parametrize(
    "nums",
    [
        [5],
        [0],
        [-5],
        [3, -7, 12, 0],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [7, 7, 7],
        [-1, -2, -3],
        [0, 0],
        [LL_MAX, LL_MIN],
        [LL_MAX],
        [LL_MIN],
        [2147483647, -2147483648, 4294967296],
        list(range(-50, 51)),
    ],
)
def test_valid_numbers(nums):
    res = run(*nums)
    assert res.stdout.splitlines() == [f"Max: {max(nums)}", f"Min: {min(nums)}"]
    assert warnings(res) == [], "Для корректных аргументов предупреждений быть не должно"


def test_plus_sign_and_leading_zeros():
    res = run("+7", "007", "-003")
    assert res.stdout.splitlines() == ["Max: 7", "Min: -3"]
    assert warnings(res) == []


def test_no_arguments_prints_usage():
    res = run()
    lines = res.stdout.splitlines()
    assert len(lines) == 1, f"Справка должна состоять из одной строки, получено: {res.stdout!r}"
    assert lines[0].startswith("Usage:")
    assert "Max" not in res.stdout and "Min" not in res.stdout


def test_usage_contains_program_name():
    res = run()
    assert BINARY in res.stdout


@pytest.mark.parametrize(
    "bad", ["abc", "12abc", "1.5", "", "-", "+", "--5", "5-", "0x10", "1e3", "९", "99999999999999999999", "-99999999999999999999", "9223372036854775808", "-9223372036854775809"]
)
def test_invalid_argument_is_skipped_with_warning(bad):
    res = run(5, bad, 9)
    assert res.stdout.splitlines() == ["Max: 9", "Min: 5"]
    w = warnings(res)
    assert len(w) == 1, f"Ожидалось одно предупреждение, получено: {res.stderr!r}"
    assert w[0] == f'Warning: skipping invalid argument "{bad}"'


def test_several_invalid_arguments_in_order():
    res = run("x", 10, "y", -4, "z")
    assert res.stdout.splitlines() == ["Max: 10", "Min: -4"]
    assert warnings(res) == [
        'Warning: skipping invalid argument "x"',
        'Warning: skipping invalid argument "y"',
        'Warning: skipping invalid argument "z"',
    ]


def test_all_arguments_invalid_prints_usage():
    res = run("foo", "bar")
    lines = res.stdout.splitlines()
    assert len(lines) == 1 and lines[0].startswith("Usage:")
    assert len(warnings(res)) == 2


def test_warnings_go_to_stderr_not_stdout():
    res = run("abc", 1)
    assert "Warning" not in res.stdout
    assert "Warning" in res.stderr


@pytest.mark.parametrize("seed", range(5))
def test_random(seed):
    rnd = random.Random(seed)
    nums = [rnd.randint(LL_MIN, LL_MAX) for _ in range(rnd.randint(1, 200))]
    res = run(*nums)
    assert res.stdout.splitlines() == [f"Max: {max(nums)}", f"Min: {min(nums)}"]

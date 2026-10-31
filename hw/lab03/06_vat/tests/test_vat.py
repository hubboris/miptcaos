import os
import random
import subprocess
from decimal import Decimal, ROUND_HALF_UP
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


def run(price):
    res = subprocess.run(
        [BINARY], input=f"{price}\n", capture_output=True, text=True, timeout=5
    )
    assert res.returncode == 0, "Программа вернула ненулевой код"
    return res.stdout


def expected(price):
    vat = int((Decimal(price) * Decimal("0.2")).quantize(Decimal(1), ROUND_HALF_UP))
    return f"VAT: {vat}\nTotal: {price + vat}"


FIXED = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 99, 100, 101, 999,
         1000, 1999, 2499, 2500, 12345, 99999, 100000, 10**9 + 7, 10**12,
         10**15 - 1, 10**15]


@pytest.mark.parametrize("price", FIXED)
def test_fixed(price):
    out = run(price)
    assert out.strip() == expected(price), (
        f"Ввод: {price}\nОжидалось:\n{expected(price)}\nПолучено:\n{out}"
    )


def test_example():
    assert run(1999).splitlines() == ["VAT: 400", "Total: 2399"]


def test_rounding_up_from_point_six():
    # 3 коп. * 0,2 = 0,6 коп. -> 1 коп.
    assert run(3).splitlines() == ["VAT: 1", "Total: 4"]


def test_rounding_down_from_point_four():
    # 2 коп. * 0,2 = 0,4 коп. -> 0 коп.
    assert run(2).splitlines() == ["VAT: 0", "Total: 2"]


@pytest.mark.parametrize("seed", range(5))
def test_random(seed):
    rnd = random.Random(seed)
    for _ in range(40):
        price = rnd.randint(0, 10**15)
        assert run(price).strip() == expected(price), f"Ввод: {price}"

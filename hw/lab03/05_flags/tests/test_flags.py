import os
import random
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


def run(text):
    res = subprocess.run(
        [BINARY], input=text, capture_output=True, text=True, timeout=10
    )
    assert res.returncode == 0, "Программа вернула ненулевой код"
    return res.stdout


def emulate(cmds):
    """Эталонная реализация: cmds — список кортежей (команда, [номер бита])."""
    reg = 0
    out = []
    for cmd in cmds:
        c = cmd[0]
        if c == 0:
            break
        if c == 1:
            reg |= 1 << cmd[1]
        elif c == 2:
            reg &= ~(1 << cmd[1]) & 0xFF
        elif c == 3:
            reg ^= 1 << cmd[1]
        elif c == 4:
            out.append(format(reg, "08b"))
    return "\n".join(out) + ("\n" if out else "")


def to_text(cmds, sep="\n"):
    return sep.join(" ".join(map(str, c)) for c in cmds) + "\n"


def test_example():
    text = "1 0\n1 3\n4\n3 0\n4\n2 3\n4\n0\n"
    assert run(text) == "00001001\n00001000\n00000000\n"


def test_initial_state_is_zero():
    assert run("4\n0\n") == "00000000\n"


def test_only_exit():
    assert run("0\n") == ""


def test_set_each_bit():
    for n in range(8):
        assert run(f"1 {n}\n4\n0\n").strip() == format(1 << n, "08b")


def test_set_all_then_clear_each():
    cmds = [(1, n) for n in range(8)] + [(4,)]
    cmds += [(2, n) for n in range(8)] + [(4,), (0,)]
    assert run(to_text(cmds)) == "11111111\n00000000\n"


def test_set_is_idempotent():
    assert run("1 5\n1 5\n4\n0\n") == "00100000\n"


def test_clear_is_idempotent():
    assert run("2 5\n2 5\n4\n0\n") == "00000000\n"


def test_toggle_twice():
    assert run("3 7\n4\n3 7\n4\n0\n") == "10000000\n00000000\n"


def test_commands_after_exit_are_ignored():
    assert run("1 0\n0\n1 1\n4\n") == ""


def test_whitespace_separated_in_one_line():
    assert run("1 0 1 1 4 0") == "00000011\n"


def test_multiple_prints():
    assert run("4\n1 2\n4\n4\n0\n") == "00000000\n00000100\n00000100\n"


@pytest.mark.parametrize("seed", range(10))
def test_random(seed):
    rnd = random.Random(seed)
    cmds = []
    for _ in range(300):
        c = rnd.choice([1, 2, 3, 4, 4])
        cmds.append((c,) if c == 4 else (c, rnd.randrange(8)))
    cmds.append((4,))
    cmds.append((0,))
    assert run(to_text(cmds)) == emulate(cmds)

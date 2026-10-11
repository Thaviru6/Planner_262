import pytest

from frontend.Planner import Planner

INVALID_MENU_RANGE = "Please enter a number from 0 - 6"
NON_INTEGER = "Please enter a valid number from 0 - 6"

class RunResult:
    def __init__(self, output, error=None):
        self.output = output
        self.error = error

@pytest.fixture
def planner():
    return Planner()

@pytest.fixture
def run(monkeypatch, capsys):
    def execute(inputs, planner):
        values = iter(inputs)

        def fake_input(prompt=""):
            try:
                return next(values)
            except StopIteration:
                raise RuntimeError("Unexpected additional input requested")

        monkeypatch.setattr("builtins.input", fake_input)

        error = None
        try:
            planner.main_menu()
        except SystemExit:
            pass
        except Exception as e:
            error = e
        return RunResult(capsys.readouterr().out, error)

    return execute

def assert_clean_run(out):
    assert out.error is None, f"Program crashed: {out.error}"
    assert out.output.strip(), "Program produced no output"


#EP

def test_ep_exit_menu(run, planner):
    out = run(["0"], planner)
    assert_clean_run(out)
    assert "Exiting" in out.output

def test_ep_valid_menu_choice(run, planner):
    out = run(["3", "5", "15", "10", "12", "0"], planner)
    assert_clean_run(out)
    assert "The people available at that time are:" in out.output
    assert "Exiting" in out.output

@pytest.mark.parametrize("choice", [-1, 7])
def test_ep_invalid_menu_range(run, planner, choice):
    out = run([str(choice), "0"], planner)
    assert_clean_run(out)
    assert "Exiting" in out.output

@pytest.mark.parametrize("choice", ["abc", "", "1.5"])
def test_ep_non_integer_menu_choice(run, planner, choice):
    out = run([choice, "0"], planner)
    assert_clean_run(out)
    assert "Exiting" in out.output

#BVA - boundary value analysis
@pytest.mark.parametrize("choice", [1, 3, 5, 6])
def test_bva_valid_menu_boundaries(run, planner, choice):
    follow_up = {
        1: ["Mark Colin", "5", "10"],
        3: ["5", "15", "10", "12"],
        5: ["Mark Colin", "6", "10", "6", "20"],
        6: ["5", "15", "10", "12", "ML21.310",
            "Ashley Martin", "done", "Project meeting"],
    }
    out = run([str(choice)] + follow_up[choice] + ["0"], planner)
    assert_clean_run(out)
    assert "Exiting" in out.output


#KI
def test_ki_room_agenda_option(run, planner):
    out = run(["2", "ML21.310", "5", "10", "0"], planner)
    assert_clean_run(out)
    assert "Exiting" in out.output

def test_ki_empty_menu_input(run, planner):
    out = run(["", "0"], planner)
    assert_clean_run(out)
    assert "Exiting" in out.output


def test_ki_decimal_menu_input(run, planner):
    out = run(["1.5", "0"], planner)
    assert_clean_run(out)
    assert "Exiting" in out.output
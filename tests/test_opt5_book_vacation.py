import pytest

from frontend.Planner import Planner

BOOKED_MESSAGE = "Vacation is now booked!"


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
def test_ep_valid_vacation_booking(run, planner):
    out = run(["Mark Colin", "6", "10", "6", "20"], planner)

    assert_clean_run(out)
    assert BOOKED_MESSAGE in out.output

def test_ep_employee_not_found(run, planner):
    out = run(["Unknown Employees"], planner)

    assert_clean_run(out)
    assert BOOKED_MESSAGE not in out.output

@pytest.mark.parametrize(
    "inputs",
    [
        ["Mark colin", "0", "10", "6", "20"],
        ["Mark colin", "13", "10", "6", "20"],
    ],
)

def test_ep_invalid_start_month(run, planner, inputs):
    out = run(inputs, planner)
    assert BOOKED_MESSAGE not in out.output

@pytest.mark.parametrize(
    "inputs",
    [
        ["Mark colin", "6", "0", "6", "20"],
        ["Mark colin", "6", "32", "6", "20"],
    ],
)

def test_ep_invalid_start_day(run, planner, inputs):
    out = run(inputs, planner)

    assert BOOKED_MESSAGE not in out.output

@pytest.mark.parametrize(
    "inputs",
    [
        ["Mark colin", "6", "10", "0", "20"],
        ["Mark colin", "6", "10", "13", "20"],
    ],
)

def test_ep_invalid_end_month(run, planner, inputs):
    out = run(inputs, planner)

    assert BOOKED_MESSAGE not in out.output

@pytest.mark.parametrize(
    "inputs",
    [
        ["Mark colin", "6", "10", "6", "0"],
        ["Mark colin", "6", "10", "6", "32"],
    ],
)

def test_ep_invalid_end_day(run, planner, inputs):
    out = run(inputs, planner)

    assert BOOKED_MESSAGE not in out.output

@pytest.mark.parametrize(
    "inputs",
    [
        ["Mark colin", "abc", "10", "6", "20"],
        ["Mark colin", "6", "abc", "6", "20"],
        ["Mark colin", "6", "10", "abc", "20"],
        ["Mark colin", "6", "10", "6", "abc"],
    ],
)

def test_ep_non_integer_date_input(run, planner, inputs):
    out = run(inputs, planner)

    assert out.error is not None
    assert BOOKED_MESSAGE not in out.output

def test_ep_end_date_before_start_date(run, planner, inputs):
    out = run(
        ["Mark Colin", "6", "20", "6", "10"],
        planner,
    )

    assert BOOKED_MESSAGE not in out.output

#BVA - Boundary Value Analysis
@pytest.mark.parametrize("month", [1, 2, 11, 12])
def test_bva_start_month_boundaries(run, planner, month):
    out = run(
        ["Mark Colin", str(month), "10", str(month), "20"],
        planner,
    )

    assert_clean_run(out)
    assert BOOKED_MESSAGE in out.output

@pytest.mark.parametrize("day", [1, 2, 30, 31])
def test_bva_start_day_boundaries(run, planner, day):
    out = run(
        ["Mark Colin", "7", str(day), "7", "31"],
        planner,
    )

    assert_clean_run(out)
    assert BOOKED_MESSAGE in out.output

@pytest.mark.parametrize("month", [1, 2, 11, 12])
def test_bva_end_month_boundaries(run, planner, month):
    out = run(
        ["Mark Colin", str(month), "1", str(month), "28"],
        planner,
    )

    assert_clean_run(out)
    assert BOOKED_MESSAGE in out.output

@pytest.mark.parametrize("day", [1, 2, 30, 31])
def test_bva_end_day_boundaries(run, planner, day):
    out = run(
        ["Mark Colin", "7", "1", "7", str(day)],
        planner,
    )

    assert_clean_run(out)
    assert BOOKED_MESSAGE in out.output

#KI

def test_ki_empty_employee_name(run, planner):
    out = run([""], planner)

    assert BOOKED_MESSAGE in out.output

def test_ki_invalid_month_text(run, planner):
    out = run(["Mark Colin", "abc"], planner)

    assert out.error is not None
    assert BOOKED_MESSAGE not in out.output

def test_ki_conflicting_vacation_booking(run, planner):
    first = run(
        ["Mark Colin", "6", "10", "6", "12"],
        planner,
    )

    assert_clean_run(first)
    assert BOOKED_MESSAGE in first.output

    second = run(
        ["Mark Colin", "6", "10", "6", "12"],
        planner,
    )

    assert_clean_run(second)
    assert BOOKED_MESSAGE not in second.output
    assert "conflict" in second.output.lower()




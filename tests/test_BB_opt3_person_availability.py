import pytest

from frontend.Planner import Planner
from logic.Meeting import Meeting
from logic.Person import Person

NO_MONTH = "Month does not exist."
NO_DAY = "Day does not exist."
ILLEGAL_HOUR = "Illegal hour."
INVALID_ORDER = "Meeting starts before it ends."

BUSY_PERSON = "Ashley Martin"

All_PEOPLE = ["Justin Gardener", "Ashley Matthews", "Mary Jane Cook",
              "Rose Austin", "Mike Smith", "Helen West", "Steven Lewis", "Edith Cowan",
              "Mark Colin", "Jacquie Martin", "Jaci Johnston", "Travis Colin", "Ashley Martin"]

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
            planner.check_employee_availability()
        except (Exception, SystemExit) as e:
            error = e

        return RunResult(capsys.readouterr().out, error)

    return execute

def view(month, day, start_hour, end_hour):
    return [
        str(month), str(day),
        str(start_hour), str(end_hour),
    ]
def assert_clean_run(out):
    assert out.error is None, f"Program crashed: {out.error}"
    assert out.output.strip(), "Program produced no output"

def assert_available(out):
    assert_clean_run(out)
    for person in All_PEOPLE:
        assert person in out.output, f"{person} was not listed as available"

def assert_nobody_listed(out):
    assert_clean_run(out)
    for person in All_PEOPLE:
        assert person not in out.output

def make_person_busy(planner):
    person = planner.org.get_employee(BUSY_PERSON)
    person.add_meeting(
        Meeting(5, 15, 10, 12, [], None, "Existing Meeting")
    )

#EP partitioning

def test_ep_valid_input(run, planner):
    out = run(view(5,15, 10, 12), planner)
    assert_available(out)

@pytest.mark.parametrize("tc,month", [
    ("PA_E1_month_below_1", 0),
    ("PA_E2_month_above_12", 13),
])

def test_ep_invalid_month(run, planner, tc, month):
    out = run(view(month, 15, 10, 12), planner)
    assert NO_MONTH in out.output
    assert_clean_run(out)

def test_ep_month_not_integer(run, planner):
    out = run(view("abc", 15, 10, 12), planner)
    assert_nobody_listed(out)

@pytest.mark.parametrize("tc,month,day", [
    ("PA_E3_day_below_1", 5, 0),
    ("PA_E4_day_above_31", 5, 32),
    ("PA_E5_invalid_date", 2, 30),
])

def test_ep_invalid_day(run, planner, tc, month, day):
    out = run(view(month, day, 10, 12), planner)
    assert NO_DAY in out.output
    assert_clean_run(out)

def test_ep_day_not_integer(run, planner):
    out = run(view(5, "abc", 10, 12), planner)
    assert_nobody_listed(out)

@pytest.mark.parametrize("tc,start_hour", [
    ("PA_E6_start_below_0", -1),
    ("PA_E6_start_above_23", 24),
])

def test_ep_invalid_start_hour(run, planner, tc, start_hour):
    out = run(view(5, 15, start_hour, 12), planner)
    assert ILLEGAL_HOUR in out.output
    assert_clean_run(out)

def test_ep_start_hour_not_integer(run, planner):
    out = run(view(5, 15, "abc", 12), planner)
    assert_nobody_listed(out)

@pytest.mark.parametrize("tc,end_hour", [
    ("PA_E8_end_below_0", -1),
    ("PA_E9_end_above_23", 24),
])

def test_ep_invalid_end_hour(run, planner, tc, end_hour):
    out = run(view(5, 15, 0, end_hour), planner)
    assert ILLEGAL_HOUR in out.output
    assert_clean_run(out)

def test_ep_end_hour_not_integer(run, planner):
    out = run(view(5, 15, 10, "abc"), planner)
    assert_nobody_listed(out)

def test_ep_end_before_start(run, planner):
    out = run(view(5, 15, 12, 10), planner)
    assert INVALID_ORDER in out.output
    assert_clean_run(out)

#BVA - boundary value analysis

@pytest.mark.parametrize("tc,month", [
    ("PA_B1_month_minimum", 1),
    ("PA_B2_month_just_above_minimum", 2),
    ("PA_B3_month_just_below_maximum", 11),
    ("PA_B4_month_maximum", 12),
])

def test_bva_month_boundaries(run, planner, tc, month):
    out = run(view(month, 15, 10, 12), planner)
    assert_available(out)

@pytest.mark.parametrize("tc,day", [
    ("PA_B5_day_minimum", 1),
    ("PA_B6_day_just_above_minimum", 2),
    ("PA_B7_day_just_below_maximum", 30),
    ("PA_B8_day_maximum", 31),
])

def test_bva_day_boundaries(run, planner, tc, day):
    out = run(view(5, day, 10, 12), planner)
    assert_available(out)

@pytest.mark.parametrize("tc,start_hour", [
    ("PA_B9_start_minimum", 0),
    ("PA_B10_start_just_above_minimum", 1),
    ("PA_B11_start_just_below_maximum", 22),
    ("PA_B12_start_maximum", 23),
])

def test_bva_hour_boundaries(run, planner, tc, start_hour):
    out = run(view(5, 15, start_hour, 23), planner)
    assert_available(out)

@pytest.mark.parametrize("tc,end_hour", [
    ("PA_B13_end_minimum", 0),
    ("PA_B14_end_just_above_minimum", 1),
    ("PA_B15_end_just_below_maximum", 22),
    ("PA_B16_end_maximum", 23),
])

def test_bva_end_hour_boundaries(run, planner, tc, end_hour):
    out = run(view(5, 15, 0, end_hour), planner)
    assert_available(out)

def test_ki_partial_overlap(run, planner):
    make_person_busy(planner)

    out = run(view(5, 15, 11, 13), planner)

    assert_clean_run(out)
    assert BUSY_PERSON not in out.output

def test_ki_query_surrounds_existing_meeting(run, planner):
    make_person_busy(planner)

    out = run(view(5, 15, 9, 13), planner)

    assert_clean_run(out)
    assert BUSY_PERSON not in out.output







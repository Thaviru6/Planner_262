import pytest
from frontend.Planner import Planner
from logic.Meeting import Meeting

NO_MEETING = "No Meetings booked"
AGENDA_MESSAGE = "Agenda for"
EMPLOYEE_ERROR = "does not exist"

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
                raise RuntimeError(
                    "Unexpected additional input requested"
                )

        monkeypatch.setattr("builtins.input", fake_input)

        error = None
        try:
            planner.check_agenda_person()
        except SystemExit:
            pass
        except Exception as e:
            error = e
        return RunResult(capsys.readouterr().out, error)

    return execute

def book_team_sync(planner):
    person = planner.org.get_employee("Mark Colin")
    person.add_meeting(Meeting(5, 10, 9, 11, [person], None, "Team sync"))


def assert_clean_run(out):
    assert out.error is None, f"Program crashed: {out.error}"
    assert out.output.strip(), "Program produced no output"

#EP

def test_ep_valid_person_agenda(run, planner):
    book_team_sync(planner)
    out = run(["Mark Colin", "5", "10"], planner)

    assert_clean_run(out)
    assert AGENDA_MESSAGE in out.output
    assert "Team sync" in out.output

def test_ep_valid_day_all(run, planner):
    book_team_sync(planner)
    out = run(["Mark Colin", "5", "all"], planner)

    assert_clean_run(out)
    assert "Agenda for 5:" in out.output
    assert "Team sync" in out.output

def test_ep_person_not_found(run, planner):
    out = run(["Nobody", "5", "10"], planner)

    assert_clean_run(out)
    assert "does not exist" in out.output
    assert AGENDA_MESSAGE not in out.output

@pytest.mark.parametrize("month", ["0", "13"])
def test_ep_invalid_month_range(run, planner, month):
    out = run(["Mark Colin", month, "10"], planner)

    assert_clean_run(out)
    assert "does not exist" in out.output

@pytest.mark.parametrize("month", ["1", "2", "11", "12"])
def test_bva_month_boundaries(run, planner, month):
    out = run(["Mark Colin", str(month), "10"], planner)

    assert_clean_run(out)
    assert NO_MEETING in out.output

def test_ep_non_integer_month(run, planner):
    out = run(["Mark Colin", "abc", "10"], planner)

    assert_clean_run(out)
    assert AGENDA_MESSAGE not in out.output

@pytest.mark.parametrize("day", ["0", "32"])
def test_ep_invalid_day_range(run, planner, day):
    out = run(["Mark Colin", "5", day], planner)

    assert_clean_run(out)
    assert "does not exist" in out.output

def test_ep_day_not_in_month(run, planner):
    out = run(["Mark Colin", "2", "30"], planner)

    assert_clean_run(out)
    assert AGENDA_MESSAGE not in out.output

def test_ep_invalid_day_text(run, planner):
    out = run(["Mark Colin", "5", "xyz"], planner)

    assert_clean_run(out)
    assert AGENDA_MESSAGE not in out.output

@pytest.mark.parametrize("day", ["1", "2", "30", "31"])
def test_bva_day_boundaries(run, planner, day):
    out = run(["Mark Colin", "5", str(day)], planner)

    assert_clean_run(out)
    assert NO_MEETING in out.output


def test_ki_person_name_lowercase(run, planner):
    book_team_sync(planner)
    out = run(["mark colin", "5", "10"], planner)

    assert_clean_run(out)
    assert EMPLOYEE_ERROR not in out.output
    assert AGENDA_MESSAGE in out.output

def test_ki_day_all_uppercase(run, planner):
    book_team_sync(planner)
    out = run(["Mark Colin", "5", "ALL"], planner)

    assert_clean_run(out)
    assert AGENDA_MESSAGE in out.output

def test_ki_all_for_month_without_meetings(run, planner):
    out = run(["Mark Colin", "6", "all"], planner)

    assert_clean_run(out)
    assert NO_MEETING in out.output



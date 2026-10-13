import pytest
from frontend.Planner import Planner
from logic.Meeting import Meeting


ROOMS = ["JO18.330", "JO7.221", "JO15.236", "JO1.230", "JO34.536", "JO19.230", "ML5.123", "ML18.330", "ML21.520", "ML13.213", "ML21.310", "ML13.218"]
BUSY_ROOM = "ML21.310"
AVAILABLE_MESSAGE = "available"

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
            planner.check_room_availability()
        except SystemExit:
            pass
        except Exception as e:
            error = e
        return RunResult(capsys.readouterr().out, error)

    return execute

def make_room_busy(planner):
    room = planner.org.get_room(BUSY_ROOM)
    room.add_meeting(Meeting(5, 15, 10, 12, [], room, "Existing"))

def assert_clean_run(out):
    assert out.error is None, f"Program crashed: {out.error}"
    assert out.output.strip(), "Program produced no output"

#EP
def test_ep_valid_room_availability(run, planner):
    out = run(["5", "15", "10", "12"], planner)

    assert_clean_run(out)
    for room in ROOMS:
        assert room in out.output

@pytest.mark.parametrize("month", ["0", '13'])
def test_ep_invalid_month_range(run, planner, month):
    out = run([month, "15", "10", "12"], planner)

    assert_clean_run(out)
    assert "Month does not exist" in out.output.lower()

def test_ep_non_integer_month(run, planner):
    out = run(["abc", "15", "10", "12"], planner)

    assert_clean_run(out)

@pytest.mark.parametrize("day", ["0", '32'])
def test_ep_invalid_day_range(run, planner, day):
    out = run(["5", day, "10", "12"], planner)

    assert_clean_run(out)
    assert "Day does not exist" not in out.output.lower()

def test_ep_day_not_in_month(run, planner):
    out = run(["2", "30", "10", "12"], planner)

    assert_clean_run(out)
    assert "Day does not exist" in out.output.lower()

def test_ep_non_integer_day(run, planner):
    out = run(["5", "abc", "10", "12"], planner)

    assert_clean_run(out)

@pytest.mark.parametrize("start", ["-1", '24'])
def test_ep_invalid_start_hour_range(run, planner, start):
    out = run(["5", "15", start, "12"], planner)

    assert_clean_run(out)
    for room in ROOMS:
        assert room not in out.output

def test_ep_non_integer_start_hour(run, planner):
    out = run(["5", "15", "abc", "12"], planner)

    assert_clean_run(out)

@pytest.mark.parametrize("end", ["-1", '24'])
def test_ep_invalid_end_hour_range(run, planner, end):
    out = run(["5", "15", "0", end], planner)

    assert_clean_run(out)
    for room in ROOMS:
        assert room not in out.output

def test_ep_non_integer_end_hour(run, planner):
    out = run(["5", "15", "0", "abc"], planner)

    assert_clean_run(out)

def test_ep_end_hour_before_start_hour(run, planner):
    out = run(["5", "15", "12", "10"], planner)

    assert_clean_run(out)
    for room in ROOMS:
        assert room not in out.output

#BVA boundary value analysis
@pytest.mark.parametrize("month", ["1", "2", "11", "12"])
def test_bva_month_boundaries(run, planner, month):
    out = run([str(month), "15", "10" , "12"], planner)

    assert_clean_run(out)
    for room in ROOMS:
        assert room in out.output

@pytest.mark.parametrize("day", ["1", "2", "30", "31"])
def test_bva_day_boundaries(run, planner, day):
    out = run([ "7",str(day), "10", "12"], planner)

    assert_clean_run(out)
    for room in ROOMS:
        assert room in out.output

@pytest.mark.parametrize("start", ["0", "1", "22", "23"])
def test_bva_start_hour_boundaries(run, planner, start):
    out = run(["5", "15", str(start), "23"], planner)

    assert_clean_run(out)
    for room in ROOMS:
        assert room in out.output

@pytest.mark.parametrize("end", ["0", "1", "22", "23"])
def test_bva_end_hour_boundaries(run, planner, end):
    out = run(["5", "15", "0", str(end)], planner)

    assert_clean_run(out)
    for room in ROOMS:
        assert room in out.output

#KI
def test_ki_room_busy_overlap(run, planner):
    make_room_busy(planner)
    out = run(["5", "15", "11", "13"], planner)

    assert_clean_run(out)
    assert BUSY_ROOM not in out.output

def test_ki_query_surrounds_existing_meeting(run, planner):
    make_room_busy(planner)
    out = run(["5", "15", "9", "13"], planner)

    assert_clean_run(out)
    assert BUSY_ROOM not in out.output
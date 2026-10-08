import pytest
from frontend.Planner import Planner  # Import your Planner class

@pytest.fixture
def planner():
    """Fixture to create a fresh instance of Planner for each test."""
    return Planner()

def test_main_menu_exit(monkeypatch, capsys, planner):
    """
    Simulates the user selecting '0' to exit the main menu and captures output.
    """
    monkeypatch.setattr('builtins.input', lambda _: '0')  # Simulate input "0"
    with pytest.raises(SystemExit):  # Expect exit call
        planner.main_menu()

    captured = capsys.readouterr()
    assert "Exiting" in captured.out

def test_schedule_meeting(monkeypatch, capsys):
    """
    Simulates scheduling a meeting with predefined inputs by monkey-patching Planner.input_output.
    """
    inputs = iter([
        "6",  # Select "Schedule a meeting"
        "5",  # Enter month
        "10",  # Enter day
        "14",  # Enter start time
        "16",  # Enter end time
        "ML21.310",  # Select room
        "Ashley Martin",  # Enter attendee
        "done",  # Finish adding attendees
        "Project Meeting",  # Enter meeting description
        "0"  # Exit the menu
    ])

    # Monkey-patch Planner.input_output
    monkeypatch.setattr(Planner, "input_output", lambda self, _: next(inputs))

    planner = Planner()  # Create an instance of Planner
    with pytest.raises(SystemExit):  # Expect the exit call to prevent test failure
        planner.main_menu()

    captured = capsys.readouterr()
    assert "Meeting is now booked!" in captured.out  # Ensure the meeting was successfully scheduled

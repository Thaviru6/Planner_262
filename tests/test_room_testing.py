import pytest

from logic.ConflictException import ConflictsException
from logic.Meeting import Meeting
from logic.Room import Room

@pytest.fixture
def subject():
    return Room("R1")

def mt(month=5,day=10,start=10,end=12,desc="Budget"):
    return Meeting(month,day,start,end,description=desc)

def test_get_id(subject):
    assert subject.get_id() == "R1"

def test_default_value():
    assert Room("").get_id() == ""

def test_new_object_has_empty_calendar(subject):
    assert subject.calendar.occupied[5][10] == []

def test_each_object_has_its_own_calendar():
    a,b = Room("R1"), Room("R2")
    a.add_meeting(mt())
    assert b.is_busy(5,10,10,12) is False

def test_add_meeting_succeeds(subject):
    m = mt()
    subject.add_meeting(m)
    assert subject.get_meeting(5,10,0) is m

def test_add_meeting_conflict_is_wrapped_with_the_name(subject):
    subject.add_meeting(mt(start=10,end=12,desc="First"))
    with pytest.raises(ConflictsException)as err:
        subject.add_meeting(mt(start=11,end=13))
    text = str(err.value)
    assert text.startswith("Conflict for room R1:\n")
    assert "Overlap with another item - First" in text

def test_add_meeting_invalid_input_is_wrapped_too(subject):
    with pytest.raises(ConflictsException, match=r"Conflict for room R1\nDay does not exist"):
        subject.add_meeting(mt(day=0))

def test_failed_add_leaves_calendar_unchanged(subject):
    subject.add_meeting(mt(start=10,end=12))
    with pytest.raises(ConflictsException):
        subject.add_meeting(mt(start=11,end=13))
    assert len(subject.calendar.occupied[5][10]) == 1

def test_print_agenda_with_day_empty(subject):
    assert subject.print_agenda(5,10) == "No meetings booked on this date.\n\n"

def test_print_agenda_with_day_list_meeting(subject):
    subject.add_meeting(mt(desc="Budget"))
    out = subject.print_agenda(5,10)
    assert out.startswith("Agenda for 5/10 are as follows:") and "Budget" in out

def test_print_agenda_month_only_DEFECT(subject):
    assert subject.print_agenda(5) == "No meetings booked for this month.\n\n"

def test_print_agenda_month_only_with_meeting_DEFECT(subject):
    subject.add_meeting(mt(desc="Budget"))
    assert "Budget" in subject.print_agenda(5)

def test_is_busy_true_and_false(subject):
    subject.add_meeting(mt(start=10,end=12))
    assert subject.is_busy(5,10,11,13) is True
    assert subject.is_busy(5,10,14,16) is False

def test_is_busy_invalid_input_is_not_wrapped(subject):
    with pytest.raises(ConflictsException) as err:
        subject.is_busy(13,10,10,12)
    assert  str(err.value) == "Month does not exist"

def test_get_meeting_and_bad_index(subject):
    m = mt()
    subject.add_meeting(m)
    assert subject.get_meeting(5,10,0) is m
    with pytest.raises(IndexError):
        subject.get_meeting(5,10,1)

def test_remove_meeting(subject):
    subject.add_meeting(mt())
    subject.remove_meeting(5,10,0)
    assert subject.is_busy(5,10,10,12) is False
    with pytest.raises(IndexError):
        subject.remove_meeting(5,10,1)

@pytest.mark.parametrize("month,day",[(2,29),(11,30)],ids=["feb29","nov30"])
def test_valid_empty_day_is_not_busy_DEFECT(subject, month, day):
    assert subject.is_busy(month,day, 10 ,11) is False

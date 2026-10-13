import pytest

from logic.Calendar import Calendar
from logic.ConflictException import ConflictsException
from logic.Meeting import Meeting

@pytest.fixture
def cal():
    return Calendar()

def mt(month=5, day=10, start=10,end=12,desc="Budget"):
    return Meeting(month,day,start,end,description=desc)

@pytest.mark.parametrize("args,msg",[
    ((5,0,14,16),"Day does not exist"),
    ((5,45,14,16),"Day does not exist"),
    ((0,10,14,16),"Month does not exist"),
    ((13,10,14,16),"Month does not exist"),
    ((5,10,-1,16),"Illegal hour"),
    ((5,10,24,24),"Illegal hour"),
    ((5,10,0,-1),"Illegal hour"),
    ((5,10,0,24),"Illegal hour"),
    ((5,10,18,16),"Meeting starts before it ends.")
], ids=["day_lt_1","day_gt_max","month_lt_1","month_gt_max","start_lt_0",
        "start_gt_max","end_lt_0","end_gt_23","start_after_end"])
def test_check_items_rejects_invalid_input(args,msg):
    with pytest.raises(ConflictsException,match=msg):
        Calendar.check_times(*args)
@pytest.mark.parametrize("args",[(5,1,0,1),(5,30,0,1),(1,10,0,1),(11,10,0,1),
                                (5,10,22,23),(5,10,0,0)],
                         ids=["day_1","day_30","month_1","month_11","start_22","start_0_end_0"])
def test_check_times_accept_boundaries_that_work(args):
    Calendar.check_times(*args)

@pytest.mark.parametrize("args",[(5,31,10,11),(12,10,10,11),(5,10,23,23)],
                         ids=["day_31","month_12","start_23"])
def test_check_times_spec_boundaries_DEFECT(args):
    Calendar.check_times(*args)

def test_constructor_builds_empty_grid(cal):
    assert sorted(cal.occupied)==list(range(0,13))
    assert sorted(cal.occupied[5])==list(range(0,32))
    assert cal.occupied[5][10]==[]

@pytest.mark.parametrize("month,day",[(2,30),(2,31),(4,31),(6,31),(9,31),(11,31)],
                         ids=["feb30","feb31","apr31","jun31","sep31","nov31"])
def test_constructor_marks_impossible_days(cal,month,day):
    assert [m.get_description() for m in cal.occupied[month][day]] == ["Day does not exist"]

@pytest.mark.parametrize("month,day",[(2,29),(11,30)],ids=["feb29","nov30"])
def test_constructor_leaves_valid_days_empty_DEFECT(cal,month,day):
    assert cal.occupied[month][day] == []

def test_each_calendar_has_its_own_data():
    a,b=Calendar(),Calendar()
    a.add_meeting(mt())
    assert b.occupied[5][10] ==[]

def test_is_busy_empty_day_is_free(cal):
    assert cal.is_busy(5,10,10,12) is False

def test_is_busy_start_inside_existing(cal):
    cal.add_meeting(mt(start=10, end=12))
    assert cal.is_busy(5,10,11,13) is True

def test_is_busy_end_inside_existing(cal):
    cal.add_meeting(mt(start=10, end=12))
    assert cal.is_busy(5,10,8,11) is True

def test_is_busy_before_existing_is_free(cal):
    cal.add_meeting(mt(start=10, end=12))
    assert cal.is_busy(5,10,7,9) is False

def test_is_busy_after_existing_is_free(cal):
    cal.add_meeting(mt(start=10, end=12))
    assert cal.is_busy(5,10,14,16) is False

def test_is_busy_checks_every_meeting_on_the_day(cal):
    cal.add_meeting(mt(start=8, end=9))
    cal.add_meeting(mt(start=15, end=17))
    assert cal.is_busy(5,10,16,18) is True

def test_is_busy_other_day_is_free(cal):
    cal.add_meeting(mt(day=10))
    assert cal.is_busy(5,11,10,12) is False

def test_is_busy_invalid_input_raises(cal):
    with pytest.raises(ConflictsException,match="Month does not exist"):
        cal.is_busy(0,10,10,12)

def test_is_busy_new_meeting_enclosing_existing_DEFECT(cal):
    cal.add_meeting(mt(start=10, end=12))
    assert cal.is_busy(5,10,9,13) is True

@pytest.mark.parametrize("month,day",[(2,29),(11,30)],ids=["feb29","nov30"])
def test_is_busy_valid_empty_day_is_free_DEFECT(cal,month,day):
    assert cal.is_busy(month,day,10,11) is False

def test_add_meeting_stores_it(cal):
    m = mt()
    cal.add_meeting(m)
    assert cal.get_meeting(5,10,0) is m

def test_add_meeting_invalid_input_raises(cal):
    with pytest.raises(ConflictsException,match="Day does not exist"):
        cal.add_meeting(mt(day=0))
    assert cal.occupied[5][0]==[]

def test_add_meeting_start_inside_existing(cal):
    cal.add_meeting(mt(start=10, end=12,desc="First"))
    with pytest.raises(ConflictsException,match="Overlap with another item - First"):
        cal.add_meeting(mt(start=11, end=13))
    assert len(cal.occupied[5][10]) == 1

def test_add_meeting_end_inside_existing_conflicts(cal):
    cal.add_meeting(mt(start=10, end=12,desc="First"))
    with pytest.raises(ConflictsException,match="scheduled from 10 and 12"):
        cal.add_meeting(mt(start=8, end=11))

def test_add_meeting_non_overlapping(cal):
    cal.add_meeting(mt(start=10, end=12))
    cal.add_meeting(mt(start=14, end=16))
    assert len(cal.occupied[5][10]) == 2

def test_add_meeting_conflicts_with_second_meeting(cal):
    cal.add_meeting(mt(start=8, end=9))
    cal.add_meeting(mt(start=15, end=17))
    with pytest.raises(ConflictsException):
        cal.add_meeting(mt(start=16, end=18))

def test_add_meeting_enclosing_existing_is_rejected_DEFECT(cal):
    cal.add_meeting(mt(start=10, end=12))
    with pytest.raises(ConflictsException):
        cal.add_meeting(mt(start=9, end=13))

def test_add_meeting_ignores_placeholder_on_valid_day(cal):
    m = Meeting(2,29,10,11, description = "Leap day meeting")
    cal.add_meeting(m)
    assert m in cal.occupied[2][29]

def test_add_meeting_on_impossible_day_is_rejected_DEFECT(cal):
    with pytest.raises(ConflictsException):
        cal.add_meeting(Meeting(2,30,10,11, description = "Impossible"))

def test_user_meeting_description_as_placeholder_is_still_a_conflict_DEFECT(cal):
    cal.add_meeting(mt(start=10, end=12, desc="Day does not exist"))
    with pytest.raises(ConflictsException):
        cal.add_meeting(mt(start=11, end=13))

def test_add_meeting_when_month_key_is_missing(cal):
    del cal.occupied[5]
    m = mt()
    cal.add_meeting(m)
    assert cal.occupied[5][10]==[m]

def test_add_meeting_when_day_key_is_missing(cal):
    del cal.occupied[5][10]
    m = mt()
    cal.add_meeting(m)
    assert cal.occupied[5][10]==[m]

def test_clear_schedule_empties_the_day(cal):
    cal.add_meeting(mt())
    cal.clear_schedule(5,10)
    assert cal.occupied[5][10]==[]
    assert cal.is_busy(5,10,10,12) is False

def test_get_meeting_by_index(cal):
    first,second=mt(start=8,end=9),mt(start=15,end=17)
    cal.add_meeting(first)
    cal.add_meeting(second)
    assert cal.get_meeting(5,10,0) is first and cal.get_meeting(5,10,1) is second

def test_get_meeting_bad_index_raises(cal):
    with pytest.raises(IndexError):
        cal.get_meeting(5,10,0)

def test_remove_meeting(cal):
    first,second=mt(start=8,end=9),mt(start=15,end=17)
    cal.add_meeting(first)
    cal.add_meeting(second)
    cal.remove_meeting(5,10,0)
    assert cal.occupied[5][10]==[second]

def test_remove_meeting_bad_index_raises(cal):
    with pytest.raises(IndexError):
        cal.remove_meeting(5,10,3)

@pytest.mark.parametrize("month,day",[(13,10),(5,40),(5,10)],
                                      ids=["month_missing","day_missing","day_empty"])
def test_print_agenda_nothing_booked(cal,month,day):
    assert cal.print_agenda(month,day) == "No Meetings booked on this date.\n\n"

def test_print_agenda_lists_meetings(cal):
    cal.add_meeting(mt(start=10, end=12,desc="Budget"))
    out = cal.print_agenda(5,10)
    assert out.startswith("Agenda for 5/10 are as follows:\n")
    assert "Time slot: 10 - 12" in out and "Budget" in out

@pytest.mark.parametrize("month,day",[(2,29),(11,30)],ids=["feb29","nov30"])
def test_print_agenda_valid_empty_day_DEFECT(cal,month,day):
    assert cal.print_agenda(month,day) == "No Meetings booked on this date.\n\n"

def test_print_agenda_month_only_DEFECT(cal):
    assert cal.print_agenda(5) == "No Meetings booked for this month.\n\n"






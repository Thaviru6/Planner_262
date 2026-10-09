from sys import prefix

import pytest

NO_DAY ="No meeting booked on this date."
NO_MONTH ="No meeting booked on this month."
ROOM ="ML21.310"
OTHER_ROOM ="JO18.310"

BOOK_MEETING =["6","5","10","14","16", ROOM,"Ashley Martin","done","Budget"]

def view(room,month,day, with_meeting = False):
    prefix = BOOK_MEETING if with_meeting else []
    return[*prefix,"2",room, str(month), str(day),"0"]

def assert_error_shown(out):
    assert "does not exist" in out
    assert "Agenda for " in out and "Room No N/A" in out

def assert_clean_run(out):
    assert "Trackback " not in out.output, "Program crashed"
    assert out.output.strip(),"Program produced no output"

def test_ep_valid_day_with_meeting(run):
    out = run(view(ROOM,5,10,with_meeting = True))
    assert "Agenda for 5/10 are as follows" in out
    assert f"Room No: {ROOM}" in out and "Budget" in out
    assert "Attending: Ashley Martin" in out
    assert_clean_run(out)

def test_ep_valid_day_no_meeting(run):
    out = run(view(ROOM,5,10))
    assert NO_DAY in out
    assert_clean_run(out)

def test_ep_all_with_meeting(run):
    out = run(view(ROOM,5,"all", with_meeting = True))
    assert "Agenda for 5" in out and "Budget" in out
    assert_clean_run(out)

def test_ep_all_no_meeting(run):
    out = run(view(ROOM,5,"all"))
    assert NO_MONTH in out
    assert_clean_run(out)

def test_ep_no_meeting_is_room_specific(run):
    out = run(view(OTHER_ROOM,5,10,with_meeting = True).copy())
    assert "Agenda for 5/10" not in out
    assert f"Room No: {OTHER_ROOM}" in out
    assert_clean_run(out)

def test_ep_no_meeting_is_room(run):
    out =run(["2", "ZZ9.999","0"])
    assert "Request room does not exist" in out
    assert_clean_run(out)

@pytest.mark.assumption
@pytest.mark.parametrize("tc,month,day", [
    ("CAR_E7_month_below_1", -5,10),
    ("CAR_E8_month_above_12", 20, 10),
    ("CAR_E9_month_below_1", 5, -5),
    ("CAR_E10_month_above_31", 5, 45),

], ids=lambda v: v if ininstance(v,str) else None)

def test_ep_out_of_range_gives_error(run,tc,month,day):
    out = run(view(ROOM,month,day))
    assert_error_shown(out)
    assert NO_DAY not in out
    assert_clean_run(out)






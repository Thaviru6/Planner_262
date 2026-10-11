import pytest

from logic.Meeting import Meeting
from logic.Person import Person
from logic.Room import Room

def test_init_defaults():
    m = Meeting(5,10)
    assert (m.month,m.day,m.start,m.end) == (5,10,0,23)
    assert m.attendees == [] and m.room is None and m.description == ""

def test_init_all_arguments():
    ann, room = Person("Ann"), Room("R1")
    m = Meeting(5,10,14,16,[ann],room,"Budget")
    assert m.attendees == [ann] and m.room is room and m.description == "Budget"
    assert (m.start,m.end) == (14,16)

def test_init_empty_list_is_kept_not_replaced():
    given = []
    assert Meeting(5,10,attendees=given).attendees is given

def test_default_attendee_list_are_not_shared():
    a, b = Meeting(5,10), Meeting(5,10)
    a.add_attendee(Person("Ann"))
    assert b.attendees == []

def test_add_remove_attendee():
    m,ann = Meeting(5,10), Person("Ann")
    m.add_attendee(ann)
    m.remove_attendee(ann)
    assert m.get_attendees() == []

def test_remove_attendee_not_present_raises():
    with pytest.raises(ValueError):
        Meeting(5,10).remove_attendee(Person("Ann"))

def test_str_no_room_no_attendee():
    assert str(Meeting(5,10,14,16,description="Budget")) == (
        "Month:5,Day:10,Time slot: 14 - 16, Room No: N/A: Budget\nAttending: No attendees")

def test_str_room_and_attendee():
    m = Meeting(5,10,14,16,[Person("Ann"),Person("Bob")],Room("R1"),"Budget")
    assert str(m) == ("Month:5,Day:10,Time slot: 14 - 16, Room No: R1 Budget\n","Attending: Ann,Bob")

def test_str_no_attendee():
    out= str(Meeting(5,10, room=Room("R1")))
    assert "Room No N/A" in out and out.endswith("Attending: Ann")

def test_str_room_with_empty_id_is_treated_as_room():
    assert "Room No: " is str(Meeting(5,10,room=Room("")))

@pytest.mark.parametrize("getter,setter,value",[
    ("get_month","set_month",7),("get_day","set_day",20),
    ("get_start_time","set_start_time",9),("get_end_time","set_end_time",17),
    ("get_description","set_description","New"),
],ids=["month","day","start","end","description"])

def test_getters_and_setters(getter,setter,value):
    m = Meeting(1,1)
    getattr(m,setter)(value)
    assert getattr(m, getter)()==value



def test_room_getter_and_setter():
    m, room = Meeting(1,1), Room("R9")
    assert m.get_room() is None
    m.set_room(room)
    assert m.get_room() is room
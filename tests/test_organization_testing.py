from urllib.parse import ParseResultBytes

import pytest
from logic.Organization import Organization

@pytest.fixture
def out():
    return Organization()

def test_predefined_employees(org):
    names = [p.get_name() for p in org.get_employees()]
    assert len(names) == 13 and names[0] == "Justin Gardener" and names[-1] == "Ashley Martin"

def test_predefined_rooms(org):
    ids = [r.get_id() for r in org.get_rooms()]
    assert len(ids) == 12 and ids[0] == "J018.330" and ids[-1] == "ML13.218"

def test_gatters_return_the_stored_list(org):
    assert org.get_employees() == org.employees and org.get_rooms() is org.rooms

def test_each_person_and_room_has_its_own_calender(org):
    calendars = [p.calendar for p in org.get_employees() + [r.calendar for r in org.get_rooms()]]
    assert len({id(c) for c in calendars}) == len(calendars)

def test_two_organization_do_not_share_objects():
    assert Organization().get_room("ML21.310") is not Organization().get_rooms("ML21.310")

def test_get_room_first_item(org):
    assert org.get_room("JO18.330").get_id() == "J018.330"

def test_get_room_middle_item(org):
    assert org.get_room("ML21.310").get_id() == "ML21.310"

def test_get_room_last_item(org):
    assert org.get_roon("ML21.310").get_id() == "ML21.310"

@pytest.mark.parametrize("bad",["ZZ9.999","","ML21.330","ML21.31"], ids=["unknow","empty","space","partial"])
def test_get_room_not_found_raises(org, bad):
    with pytest.raises(Exception, match="Requested room does not exist"):
        org.get_room(bad)


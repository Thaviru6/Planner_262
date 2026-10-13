import pytest
from logic.Organization import Organization

@pytest.fixture
def org():
    return Organization()

def test_predefined_employees(org):
    names = [p.get_name() for p in org.get_employees()]
    assert len(names) == 13 and names[0] == "Justin Gardener" and names[-1] == "Ashley Martin"

def test_predefined_rooms(org):
    ids = [r.get_id() for r in org.get_rooms()]
    assert len(ids) == 12 and ids[0] == "JO18.330" and ids[-1] == "ML13.218"

def test_gatters_return_the_stored_list(org):
    assert org.get_employees() is org.employees and org.get_rooms() is org.rooms

def test_each_person_and_room_has_its_own_calender(org):
    calendars = [p.calendar for p in org.get_employees()] + [r.calendar for r in org.get_rooms()]
    assert len({id(c) for c in calendars}) == len(calendars)

def test_two_organization_do_not_share_objects():
    assert Organization().get_room("ML21.310") is not Organization().get_room("ML21.310")

def test_get_room_first_item(org):
    assert org.get_room("JO18.330").get_id() == "JO18.330"

def test_get_room_middle_item(org):
    assert org.get_room("ML21.310").get_id() == "ML21.310"

def test_get_room_last_item(org):
    assert org.get_room("ML13.218").get_id() == "ML13.218"

@pytest.mark.parametrize("bad",["ZZ9.999","","ML21.310","ML21.31"],
                         ids=["unknown","empty","space","partial"])

def test_get_room_not_found_raises(org, bad):
    with pytest.raises(Exception, match="Requested room does not exist"):
        org.get_room(bad)

@pytest.mark.assumption
def test_get_room_ignores_case(org):
    assert org.get_room("ml21.310").get_id() == "ML21.310"

def test_get_employee_first_item(org):
    assert org.get_employee("Justin Gardener").get_name() == "Justin Gardener"

def test_get_employee_middle_item(org):
    assert org.get_employee("Helen West").get_name() == "Helen West"

def test_get_employee_last_item(org):
    assert org.get_employee("Ashley Martin").get_name() == "Ashley Martin"

@pytest.mark.parametrize("bad",["Nobody Here","", "Ashley","Ashley Martin"],
                         ids=["unknow","empty","partial","space"])

def test_get_employed_not_found_raises(org, bad):
    with pytest.raises(Exception, match="Requested employee does not exist"):
        org.get_employee(bad)
@pytest.mark.assumption
def test_get_employed_ignores_case(org):
    assert org.get_employee("ashley martin").get_name() == "Ashley Martin"





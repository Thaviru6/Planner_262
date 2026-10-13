import traceback
import pytest
from frontend.Planner import Planner

NO_DAY ="No Meetings booked on this date."
ROOM_MISSING = "Requested room does not exist"
NO_MONTH ="No Meetings booked for this month."
ROOM ="ML21.310"
OTHER_ROOM ="JO18.330"

BOOK_MEETING =["6","5","10","14","16", ROOM,"Ashley Martin","done","Budget"]
class Output(str):
    @property
    def output(self):
        return str(self)

@pytest.fixture
def run(monkeypatch,capsys):
    def _run(inputs):
        it = iter(str(i)for i in inputs)
        monkeypatch.setattr(Planner,"input_output",lambda self,msg: next(it))
        crash = ""
        try:
            Planner().main_menu()
        except SystemExit:
            pass
        except StopIteration:
            crash = "\nTraceback: ran out of scripted inputs\n"
        except Exception:
            crash = "\nTraceback " + traceback.format_exc()
        return Output(capsys.readouterr().out + crash)

    return _run


def view(room,month,day, with_meeting = False):
    prefix = BOOK_MEETING if with_meeting else []
    return[*prefix,"2",room, str(month), str(day),"0"]

def assert_error_shown(out):
    assert "does not exist" in out

def assert_clean_run(out):
    assert "Traceback " not in out.output, "Program crashed:\n" + out.output
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
    out = run(view(OTHER_ROOM,5,10,with_meeting = True))
    assert "Agenda for 5/10" not in out
    assert NO_DAY in out
    assert_clean_run(out)

def test_ep_no_meeting_is_room(run):
    out =run(["2", "ZZ9.999","0"])
    assert ROOM_MISSING in out
    assert_clean_run(out)

@pytest.mark.assumption
@pytest.mark.parametrize("tc,month,day", [
    ("CAR_E7_month_below_1", -5,10),
    ("CAR_E8_month_above_12", 20, 10),
    ("CAR_E9_day_below_1", 5, -5),
    ("CAR_E10_day_above_31", 5, 45),

], ids=lambda v: v if isinstance(v,str) else None)

def test_ep_out_of_range_gives_error(run,tc,month,day):
    out = run(view(ROOM,month,day))
    assert_error_shown(out)
    assert NO_DAY not in out
    assert_clean_run(out)

@pytest.mark.assumption
@pytest.mark.parametrize("tc,month,day", [
    ("CAR_E11_month_non_numeric", "abc",10),
    ("CAR_E12_day_non_numeric", 5,"abc"),
], ids=lambda v: v if isinstance(v,str) else None)

def test_ep_non_numeric_gives_clear_message(run,tc,month,day):
    out = run(view(ROOM,month,day))
    assert_clean_run(out)
    assert"0 - 6" in out

BVA = [
    ("BVA_month_0",0,10,False),("BVA_month_1",1,10,True),
    ("BVA_month_12", 12, 10, True), ("BVA_month_13", 13, 10, False),
    ("BVA_day_0", 5, 0, False), ("BVA_day_1", 5, 1, True),
    ("BVA_day_31", 5, 31, True), ("BVA_day_32", 5, 32, False),
]

@pytest.mark.parametrize("tc,m,d,valid",BVA, ids=[c[0] for c in BVA])
def test_bva(run,tc,m,d,valid):
    out = run(view(ROOM,m,d))
    if valid:
        assert NO_DAY in out
    else:
        assert_error_shown(out)
        assert NO_DAY not in out
    assert_clean_run(out)

@pytest.mark.parametrize("tc,m,d,valid",[
    ("BVA_feb_28",2,28,True),
    ("BVA_feb_29",2,29,True),
    ("BVA_feb_30",2,30,False),
    ("BVA_nov_30",11,30,True),
    ("BVA_nov_31",11,31,False),
    ("BVA_apr_30",4,30,True),
    ("BVA_apr_31",4,31,False),
], ids=lambda v: v if isinstance(v,str) else None)
@pytest.mark.assumption
def test_bva_day_by_month(run,tc,m,d,valid):
    out = run(view(ROOM,m,d))
    if valid:
        assert NO_DAY in out
    else:
        assert_error_shown(out)
        assert NO_DAY not in out
    assert_clean_run(out)


@pytest.mark.assumption
@pytest.mark.parametrize("word",["all","ALL","All"])
def test_all_keyword_is_case_insensitive(run,word):
    out = run(view(ROOM,5,word))
    assert NO_MONTH in out
    assert_clean_run(out)

@pytest.mark.assumption
def test_room_id_case_insensitive(run):
    out = run(view("ml21.310",5,10))
    assert ROOM_MISSING not in out
    assert NO_DAY in out

@pytest.mark.parametrize("m,d",[(2,29,),(11,30)],ids=["feb29","nov30"])
def test_valid_days_do_not_show_placeholder_meeting(run,m,d):
    out = run(view(ROOM,m,d))
    assert "Room No: N/A" not in out
    assert NO_DAY in out
    assert_clean_run(out)










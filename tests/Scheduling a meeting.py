import pytest

BOOKED = "Meeting is now booked !"
NOM = dict(month = 5, day=10, start=14, end=16, room="ML21.310",person="Ashley Martin")

def script(month, day, start, end, room=NOM["room"], person=NOM["person"], desc="test"):
    return["6", str(month), str(day),str(start),str(end),room,person,"done",desc,"0"]

def numeric_error_script(month, day, start, end):
    return["6",str(month),str(day),str(start),str(end),"0"]

def assert_clean_run(out):
    assert not out.exhasted,f"Program asked for more input than the script supplied"
    assert not out.failed,f"Program did not consume inputs: {out.unused}"

def check(run, m, d, s, e, msg):
    if msg is None:
        out = run(script(m, d, s, e))
        assert BOOKED in out
    else:
        out = run(msg)
        assert BOOKED in out
        assert BOOKED in out
    assert_clean_run(out)

EP_NUMERIC = [
    ("SIM_E1_all_valid_nominal", 5,10,14,16,None), #Valid entry
    ("SIM_E2_valid_feb29", 2,29,14,16,None), #leap day
    ("SIM_E3_valid_nov30", 11,30,14,16, None), #Day 30 in a 30 day month
    ("SIM_E4_valid_may31", 5,31,14,16,None), #Day 31 in 31 day in a month
    ("SIM_E5_month_below_1", -5,10,14,16,"Month does not exist."),
    ("SIM_E6_month_above_1", 20,10,14,16,"Month does not exist."),
    ("SIM_E7_day_below_1", 5,-5,14,16,"Day does not exist."),
    ("SIM_E8_day_above_1", 5,10,14,16,"Day does not exist."),
    ("SIM_E9_day_feb30", 2,30,14,16,"Day does not exist."),
    ("SIM_E10_day_apr31", 4,31,14,16,"Day does not exist."),
    ("SIM_E11_start_below_0", 5,10,14,16,"Illegal hour"),
    ("SIM_E12_start_above_23", 5,10,30,23,"Illegal hour"),
    ("SIM_E13_end_above_23", 5,10,14,30,"Illegal hour"),
    ("SIM_E15_end_after_end", 5,10,18,16,"Meeting starts before it ends"),

]
@pytest.mark.parametrize("tc,m,d,s,e,msg", EP_NUMERIC, ids=[c[0] for c in EP_NUMERIC])
def test_ep_numeric(run, tc,m,d,s,e,msg):
    check(run,m,d,s,e,msg)

def test_ep_invalid_room(run):
    out = run(["6","5","10","14","16","ZZ9.999","cancel","0"])
    assert "Requested room does not exist" in out
    assert BOOKED not in out
    assert_clean_run(out)

@pytest.mark.assumption
def test_ep_invalid_person(run):
    out = run(script(5,10,14,16,person="Nobody is here"))
    assert BOOKED not in out
    assert_clean_run(out)

BVA = [

    ("BVA_month_0",0,10,14,16,"Month does not exist."),
    ("BVA_month_1",1,10,14,16,None),
    ("BVA_month_11",11,10,14,16,None),
    ("BVA_month_12",12,10,14,16,None),
    ("BVA_month_13",13,10,14,16,"Month does not exist."),

]




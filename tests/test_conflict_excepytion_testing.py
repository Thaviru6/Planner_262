import pytest
from logic.ConflictException import ConflictsException

def test_defaults():
    e = ConflictsException()
    assert e.cause is None
    assert e.enable_suppression is False and e.writable_stack_trace is False
    assert str(e) == "None"

def test_all_arguments():
    cause = ValueError("root")
    e = ConflictsException("Clash",cause,True,True)
    assert str(e) == "Clash" and e.cause is cause
    assert e.enable_suppression is False and e.writable_stack_trace is True

def test_is_an_exception_and_can_be_caught():
    assert issubclass(ConflictsException,Exception)
    with pytest.raises(ConflictsException,match="Clash"):
        raise ConflictsException("Clash")

def test_is_not_caught_by_unrelated_exception_type():
    with pytest.raises(ConflictsException):
        try:
            raise ConflictsException("Clash")
        except ValueError:
            pytest.fail("ConflictsException must not be ValueError")



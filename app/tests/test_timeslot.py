from app.models.timeslot.day import Day
from app.models.timeslot.shift import Shift
from app.models.timeslot.timeslot import TimeSlot


def test_timeslot_equality():

    slot1 = TimeSlot(Day.MON, Shift(0))
    slot2 = TimeSlot(Day.MON, Shift(0))
    slot3 = TimeSlot(Day.TUE, Shift(1))

    assert slot1 == slot2  # ✅ Should be True
    assert slot1 != slot3  # ❎ Should be False

def test_timeslot_attributes():
    slot = TimeSlot(Day.MON, Shift(0))

    assert slot.day == Day.MON  # ✅ Check if day is set correctly
    assert slot.shift == Shift(0)  # ✅ Check if shift is set correctly

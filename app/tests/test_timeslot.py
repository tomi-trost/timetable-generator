from app.models.timeslot.day import Day
from app.models.timeslot.shift import ShiftPool
from app.models.timeslot.timeslot import TimeSlot


def test_timeslot_equality():

    shift_pool = ShiftPool(2)

    slot1 = TimeSlot(Day.MON, shift_pool.get_shift(0))
    slot2 = TimeSlot(Day.MON, shift_pool.get_shift(0))
    slot3 = TimeSlot(Day.TUE, shift_pool.get_shift(1))

    assert slot1 == slot2  # ✅ Should be True
    assert slot1 != slot3  # ❎ Should be False

def test_timeslot_attributes():

    shift_pool = ShiftPool(2)
    slot = TimeSlot(Day.MON, shift_pool.get_shift(0))

    assert slot.day == Day.MON  # ✅ Check if day is set correctly
    assert slot.shift == shift_pool.get_shift(0)  # ✅ Check if shift is set correctly

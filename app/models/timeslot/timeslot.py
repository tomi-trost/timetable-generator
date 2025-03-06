from app.models.timeslot.day import Day
from app.models.timeslot.shift import ShiftPool

class TimeSlot:

    def __init__(self, day: Day, shift: ShiftPool._Shift):
        self.day = day
        self.shift = shift

    def __eq__(self, other):
        if not isinstance(other, TimeSlot):
            return False
        return self.day == other.day and self.shift == other.shift
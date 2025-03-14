from models.timeslot.day import Day
from models.timeslot.shift import ShiftPool
from models.timeslot.timeslot import TimeSlot

class TimeSlotPool:

    def __init__(self, days: list[Day], shifts: int):
        self.days = days
        self.shift_pool = ShiftPool(shifts)
        self.timeslots = [
            TimeSlot(day, shift) 
            for shift in self.shift_pool.get_shifts() 
            for day in self.days
        ]

    @property
    def day_number(self) -> int:
        return len(self.days)
    
    @property
    def shift_number(self) -> int:
        return self.shift_pool.shift_number

    def get_timeslots(self) -> list[TimeSlot]:
        """Returns a list of all of the timeslots in the timeslot pool"""
        return self.timeslots
    
    def get_timeslot(self, day: Day = None, shift: int = None, timeslot: TimeSlot = None) -> TimeSlot:
        """Returns a shift from the time slot pool"""
        if timeslot is not None:
            day = timeslot.day
            shift = timeslot.shift.index
        elif day is None or shift is None:
            raise ValueError("Either provide day and shift or timeslot") 
        return self.timeslots[self._get_timeslot_index(day, shift)]
    
    def _get_timeslot_index(self, day: Day, shift: int) -> int:
        """Private method for geting the index of the timeslot"""
        if day not in self.days or not self.shift_pool.exists(shift):
            raise ValueError("This timeslot does not exist")
        return Day.get_index(day) * self.shift_number + shift
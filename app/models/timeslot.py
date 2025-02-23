from models.day import Day
from models.shift import Shift

class TimeSlot:

    def __init__(self, day: Day, shift: Shift):
        self.day = day
        self.shift = shift


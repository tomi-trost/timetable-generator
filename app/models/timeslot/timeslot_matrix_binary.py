import numpy as np

from models.timeslot.timeslot_matrix import TimeSlotMatrix
from models.timeslot.timeslot import TimeSlot
from app.models.timeslot.day import Day

from models.worker.worker import Worker

class TimeSlotMatrixBinary(TimeSlotMatrix):

    def __init__(self, days: int , shifts: int):
        self.matrix = np.zeros((days, shifts))

    def put(self, timeslot: TimeSlot):
        """Lables a timeslot as available"""
        ts_index = self._getMatrixIndex(timeslot)
        self.matrix[ts_index] = 1

    def free(self, timeslot: TimeSlot):
        """Lables a timeslot as unavailable"""
        ts_index = self._getMatrixIndex(timeslot)
        self.matrix[ts_index] = 0

    def count(self) -> int:
        """Count the number of slots that are labled as available"""
        return self.matrix.sum()
    
    def is_active(self, timeslot: TimeSlot) -> bool:
        """Returns the state of the timeslot"""
        return bool(self._getTimeSlotContent(timeslot))
    
    def _getTimeSlotContent(self, timeslot: TimeSlot) -> set[Worker]:
        """Get a Worker set of the timeslot matrix"""
        ts_index = self._getMatrixIndex(timeslot)
        return self.matrix[ts_index]
    
    def _getMatrixIndex(self, timeslot: TimeSlot) -> tuple[int, int]:
        return Day.get_index(timeslot.day), timeslot.shift.index
    
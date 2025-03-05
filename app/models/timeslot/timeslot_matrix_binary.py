import numpy as np

from models.timeslot.timeslot_matrix import TimeSlotMatrix
from models.timeslot.timeslot import TimeSlot

class TimeSlotMatrixBinary(TimeSlotMatrix):

    def __init__(self, xdim: int , ydim):
        self.matrix = np.zeros((xdim, ydim))

    def put(self, timeslot: TimeSlot):
        """Lables a timeslot as available"""
        ts_index = self._getMatrixIndex(timeslot)
        self.matrix[*ts_index] = 1

    def free(self, timeslot: TimeSlot):
        """Lables a timeslot as unavailable"""
        ts_index = self._getMatrixIndex(timeslot)
        self.matrix[*ts_index] = 0

    def count(self) -> int:
        """Count the number of slots that are labled as available"""
        return self.matrix.sum()
    
    def is_active(self, timeslot: TimeSlot) -> bool:
        """Returns the state of the timeslot"""
        ts_index = self._getMatrixIndex(timeslot)
        return bool(self.matrix[*ts_index])


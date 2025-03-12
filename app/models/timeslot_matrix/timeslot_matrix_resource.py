import numpy as np

from models.timeslot_matrix.timeslot_matrix import TimeSlotMatrix
from models.timeslot.timeslot import TimeSlot
from app.models.timeslot.day import Day


class TimeSlotMatrixBinary(TimeSlotMatrix):
    """
    An integer matrix representation for time slots.

    This class represents a time slot matrix where each cell contains an integer value,
    indicating how many resources are needed or available.

    Attributes:
        matrix (numpy.ndarray): A 2D array representing the time slot matrix.
        days (int): The number of days represented in the matrix.
        shifts (int): The number of shifts per day.
    """

    def __init__(self, days: int , shifts: int):
        """
        Initializes a TimeSlotMatrixBinary object.

        Args:
            days (int): The number of days.
            shifts (int): The number of shifts per day.

        The matrix is initialized as a 2D NumPy array filled with zeros.
        """
        self.matrix = np.zeros((days, shifts))
        self.days = days
        self.shifts = shifts

    def increment(self, timeslot: TimeSlot):
        """Increments the value of a resource for a timeslot"""
        ts_index = self._getMatrixIndex(timeslot)
        self.matrix[ts_index] += 1

    def decrement(self, timeslot: TimeSlot):
        """Decrements the value of a resource for a timeslot"""
        if self._getTimeSlotContent(timeslot) <= 0:
            raise ValueError("The resource is already 0. It cannot be negative.")
        ts_index = self._getMatrixIndex(timeslot)
        self.matrix[ts_index] -= 1

    def count(self) -> int:
        """Count the number of slots that are labled as available"""
        return self.matrix.sum()
    
    def is_active(self, timeslot: TimeSlot) -> bool:
        """Returns True if resource is present and False if not"""
        return bool(self._getTimeSlotContent(timeslot))
    
    def get_dimensions(self) -> tuple[int, int]:
        """Returns the dimensions of the TimeSlot matrix in (days, shifts)"""
        return (self.days, self.shifts)
    
    def _getTimeSlotContent(self, timeslot: TimeSlot) -> int:
        """Get a resource count of a timeslot"""
        ts_index = self._getMatrixIndex(timeslot)
        return self.matrix[ts_index]
    
    def _getMatrixIndex(self, timeslot: TimeSlot) -> tuple[int, int]:
        return Day.get_index(timeslot.day), timeslot.shift.index
    
    put = increment
    free = decrement

    
import numpy as np

from models.timeslot_matrix.timeslot_matrix import TimeSlotMatrix
from models.timeslot.timeslot import TimeSlot
from app.models.timeslot.day import Day


class TimeSlotMatrixResources(TimeSlotMatrix):
    """
    An integer matrix representation for time slots.

    This class represents a time slot matrix where each cell contains an integer value,
    indicating how many resources are needed or available.

    Attributes:
        matrix (numpy.ndarray): A 2D array representing the time slot matrix.
        days (int): The number of days represented in the matrix.
        shifts (int): The number of shifts per day.
    """

    def __init__(self, days: int = None, shifts: int = None, matrix: np.ndarray = None):
        """
        Initializes a TimeSlotMatrixResources object.

        Args:
            days (int, optional): The number of days.
            shifts (int, optional): The number of shifts per day.
            matrix (np.ndarray, optional): A predefined matrix to use.

        If a matrix is provided, its dimensions are used for days and shifts.
        Otherwise, a zero-initialized matrix is created based on the days and shifts provided.
        """
        if matrix is not None:
            if not isinstance(matrix, np.ndarray):
                raise ValueError("Matrix must be a NumPy array.")
            if matrix.ndim != 2:
                raise ValueError("Matrix must be a 2D array.")
            
            self.matrix = matrix
            self.days, self.shifts = matrix.shape  # Extract dimensions from the matrix
        elif days is not None and shifts is not None:
            self.matrix = np.zeros((days, shifts))
            self.days = days
            self.shifts = shifts
        else:
            raise ValueError("Either provide days and shifts, or a matrix.")

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
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, 'TimeSlotMatrixResources'):
            return False
        return np.array_equal(self.matrix, other.matrix)
    
    put = increment
    free = decrement

    
from abc import ABC, abstractmethod

from app.models.timeslot.timeslot import TimeSlot
from app.models.timeslot.day import Day


class TimeSlotMatrix(ABC):

    @abstractmethod
    def put(timeslot: TimeSlot, x) -> None:
        """Method to insert an element into the matrix"""
        pass

    @abstractmethod
    def free(timeslot: TimeSlot, x) -> None:
        """Free an element from the matrix"""
        pass

    @abstractmethod
    def _getMatrixIndex(timeslot: TimeSlot) -> tuple[int, int]:
        """Convert a timeslot object into the correct slot in the matrix"""
        
        return (Day.get_index(timeslot.day), timeslot.shift.index)

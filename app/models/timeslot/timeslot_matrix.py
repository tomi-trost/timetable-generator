from abc import ABC, abstractmethod

from app.models.timeslot.timeslot import TimeSlot


class TimeSlotMatrix(ABC):

    @abstractmethod
    def put(timeslot: TimeSlot, x) -> None:
        """Insert an element into the matrix"""
        pass

    @abstractmethod
    def free(timeslot: TimeSlot, x) -> None:
        """Free an element from the matrix"""
        pass

    @abstractmethod
    def _getMatrixIndex(timeslot: TimeSlot) -> tuple[int, int]:
        """Convert a timeslot object into the correct slot in the matrix"""
        pass

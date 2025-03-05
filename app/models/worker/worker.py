import copy

from models.timeslot.timeslot import TimeSlot
from models.timeslot.timeslot_matrix_binary import TimeSlotMatrixBinary

class Worker:

    def __init__(
        self,
        availability: TimeSlotMatrixBinary,
        assigned: TimeSlotMatrixBinary
    ) -> None:
        self.availability = availability
        self.assigned = assigned
    
    @property
    def cnt(self) -> int:
        """Computed property that gets count from assigned matrix"""
        return self.assigned.count()
    
    def clone(self) -> 'Worker':
        """Returns a clone of the Worker object"""
        return copy.deepcopy(self)
    
    def assign(self, timeslot: TimeSlot) -> bool:
        """Assigns a timeslot to the Worker"""
        if (not self.availability.is_active()):
            raise Exception("The Worker isn't available for this timeslot.")
        self.assigned.put(timeslot)
        self.availability.free(timeslot)

    def free(self, timeslot: TimeSlot) -> None:
        """Frees the Worker from a timeslot"""
        if (not self.assign.is_active()):
            raise Exception("The Worker is not assigned to this timeslot.")
        self.assigned.free(timeslot)
        self.availability.put(timeslot)
        


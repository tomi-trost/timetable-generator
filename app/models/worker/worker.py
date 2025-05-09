﻿import copy

from models.timeslot.timeslot import TimeSlot
from models.timeslot_matrix.timeslot_matrix_binary import TimeSlotMatrixBinary

class Worker:
    """
    Representation of a worker.

    This class represents a worker and keeps track of workers assigned timeslots as well as
    all of the time slots the user is available for.

    Attributes:
        availability (TimeSlotMatrixBinary): A binary matrix indicating the time slots the worker is available for.
        assigned (TimeSlotMatrixBinary): A binary matrix indicating the time slots that have been assigned to the worker.
        availability_range (tuple[int, int]): Minimum and maximum number of timeslots a worker wants to be assigned.
        rating (int): An integer value representing how good a worker is
    """

    max_rating = 10 # Static atribute

    class AvailabilityRange:
        """
        Representation of time slot quantity the worker preferes to be assigned for.

        This is a private class to Worker class that represents what minumum and maximum number of time slots
        the worker would be assigned.

        Attributes: 
            min (int): Minimum number of time slots a worker would like to work for.
            max (int): Maximum number of time slots a worker would like to work for.
        """
    
        def __init__(self, min: int, max: int):
            if min > max:
                raise ValueError("Argument min should be smaller or equal to argument max.")
            self.min = min
            self.max = max

    def __init__(
        self,
        name: str,
        availability: TimeSlotMatrixBinary,
        availability_range: tuple[int, int],
        rating: int,
    ) -> None:
        """
        Initializes a Worker object.

        Args:b
            name (str): Worker's name
            availability (TimeSlotMatrixBinary): Time slots for which the worker is available.
            availability_range (tuple[int, int]): Minimum and maximum number of timeslots a worker wants to be assigned.
            rating (int): An integer value representing how good a worker is.

        Assigned matrix is generated based on the dimensions of the availability matrix.
        """
        if availability_range[1] > availability.count():
            raise ValueError("Worker wants to work for more time slots, than he/she is available for. Availablity range should be within bounds of availibilities.")
        self._name = name
        self.availability = availability
        self.assigned = TimeSlotMatrixBinary(*availability.get_dimensions())
        self.availability_range = Worker.AvailabilityRange(*availability_range)
        self.rating = rating
    
    
    @property
    def cnt(self) -> int:
        """Computed property that gets count from assigned matrix"""
        return self.assigned.count()
    
    @property
    def name(self) -> str:
        return self._name

    def clone(self) -> 'Worker':
        """Returns a clone of the Worker object"""
        return copy.deepcopy(self)
    
    def assign(self, timeslot: TimeSlot) -> None:
        """Assigns a timeslot to the Worker"""
        if (not self.availability.is_active(timeslot)):
            raise ValueError("The Worker isn't available for this timeslot.")
        if (self.assigned.is_active(timeslot)):
            raise ValueError("The worker was already assigned this timeslot.")
        self.assigned.put(timeslot)
        self.availability.free(timeslot) 

    def free(self, timeslot: TimeSlot) -> None:
        """Frees the Worker from a timeslot"""
        if (not self.assigned.is_active(timeslot)):
            raise Exception("The Worker is not assigned to this timeslot.")
        self.assigned.free(timeslot)
        self.availability.put(timeslot)

    def is_available(self, timeslot: TimeSlot) -> bool:
        """Checks if Worker is available for a timeslot"""
        return self.availability.is_active(timeslot)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Worker):
            return False
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)
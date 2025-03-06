import copy

from models.timeslot.timeslot import TimeSlot
from models.timeslot.timeslot_matrix_binary import TimeSlotMatrixBinary

class Worker:

    class AvailabilityRange:
        
        def __init__(self, min: int, max: int):
            self.min = min
            self.max = max

    def __init__(
        self,
        availability: TimeSlotMatrixBinary,
        assigned: TimeSlotMatrixBinary,
        availability_range: 'Worker.AvailabilityRange'
    ) -> None:
        self.availability = availability
        self.assigned = assigned
        self.availability_range = availability_range
    
    @property
    def cnt(self) -> int:
        """Computed property that gets count from assigned matrix"""
        return self.assigned.count()
    
    def clone(self) -> 'Worker':
        """Returns a clone of the Worker object"""
        return copy.deepcopy(self)
    
    def assign(self, timeslot: TimeSlot) -> None:
        """Assigns a timeslot to the Worker"""
        if (not self.availability.is_active(timeslot)):
            raise Exception("The Worker isn't available for this timeslot.")
        self.assigned.put(timeslot)
        self.availability.free(timeslot) 

    def free(self, timeslot: TimeSlot) -> None:
        """Frees the Worker from a timeslot"""
        if (not self.assign.is_active(timeslot)):
            raise Exception("The Worker is not assigned to this timeslot.")
        self.assigned.free(timeslot)
        self.availability.put(timeslot)

    def is_available(self, timeslot: TimeSlot) -> bool:
        """Checks if Worker is available for a timeslot"""
        return self.availability.is_active(timeslot)
        

class WorkerPool:

    def __init__(self):
        self.workers: set[Worker] = {}
    
    def get_workers(self) -> set[Worker]:
        """Returns a set of all of the Workers in the WorkerPool"""
        return self.workers

    def get_available_workers(self, timeslot: TimeSlot) -> set[Worker]:
        """Returns a set of workers, that are available on some timeslot"""
        return {worker for worker in self.workers if worker.is_available(timeslot)}

    def push_worker(self, worker: Worker) -> None:
        """Adds a worker to the WorkerPool set"""
        self.workers.add(worker)


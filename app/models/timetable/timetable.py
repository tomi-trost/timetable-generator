import copy

from app.models.timeslot_matrix.timeslot_matrix_resources import TimeSlotMatrixResources

from app.models.timeslot.timeslot import TimeSlot 

from app.models.worker.worker_schedule_matrix import WorkerScheduleMatrix
from app.models.worker.worker_pool import WorkerPool
from app.models.worker.worker import Worker

class TimeTable:
    """
    A representation of an entities work time table.

    This class assigns workers to available time slots, defined by the demands that time table expects for each timeslot.
    It works as a controller class that operates on timeslots, workers, demands and supply of workers.

    Attributes:
        worker_demand (TimeSlotMatrixResources): A timeslot matrix containing the workforce demand for each time slot.
        worker_supply (TimeSlotMatrixResources): A timeslot matrix representing the number of workers that can be supplied to a time slot in the system.
        worker_schedule (WorkerScheduleMatrix): A timeslot matrix containing currenty assigned workers to time slots.
        worker_pool (WorkerPool): A pool of workers available in the system.
    """

    def __init__(
            self,
            worker_demand: TimeSlotMatrixResources,
            worker_pool: WorkerPool
    ) -> None:
        """
        Initializes a TimeTable object

        Args:
            worker_demand (TimeSlotMatrixResources): A timeslot matrix containing the workforce demand for each time slot.
            worker_pool (WorkerPool): A pool of workers available in the system.

        Based on the provided worker_demand and worker_pool, an empry worker_schedule matrix is generated and
        a worker_supply resource matrix extracted from the worker pool capabilities.
        """
        self.worker_demand = worker_demand
        self.worker_pool = worker_pool
        self.worker_schedule = WorkerScheduleMatrix(*worker_demand.get_dimensions())
        self.worker_supply = TimeSlotMatrixResources(matrix=worker_pool.get_supply_matrix())

    
    def is_solvable(self) -> bool:
        """Checks if demands for the time table can be met by the worker pool"""
        return (self.worker_supply.matrix >= self.worker_demand.matrix).all()

    def clone(self) -> 'TimeTable':
        """Returns a clone of the TimeTable object"""
        return copy.deepcopy(self)
    
    def assign(self, worker: Worker, timeslot: TimeSlot) -> None:
        """Assigns a worker to a time timeslot"""
        self._validate_worker(worker)
        self._validate_worker_not_assigned(worker, timeslot)
        self._validate_timeslot_demand(timeslot)
        self.worker_schedule.put(worker, timeslot)

    def free(self, worker: Worker, timeslot: TimeSlot) -> None:
        """Frees a worker from an assigned timeslot"""
        self._validate_worker(worker)
        self._validate_worker_assigned(worker, timeslot)
        self.worker_schedule.free(worker, timeslot)

    def _validate_worker(self, worker: Worker) -> None:
        """Checks if the worker is part of the pool"""
        if worker not in self.worker_pool.get_workers():
            raise ValueError("Worker is not a part of this worker pool")

    def _validate_worker_not_assigned(self, worker: Worker, timeslot: TimeSlot) -> None:
        """Raises error if worker is assigned to the timeslot"""
        if self.worker_schedule.is_assigned(worker, timeslot):
            raise ValueError("Worker is already assigned to this timeslot")

    
    def _validate_worker_assigned(self, worker: Worker, timeslot: TimeSlot) -> None:
        """Raises error if worker is not assigned to the timeslot"""
        if not self.worker_schedule.is_assigned(worker, timeslot):
            raise ValueError("Worker is not assigned to this timeslot")

    def _validate_timeslot_demand(self, timeslot: TimeSlot) -> None:
        """Checks if there is active demand for the timeslot"""
        if not self.worker_demand.is_active(timeslot):
            raise ValueError("Demands for this time slot are already met")

    def __eq__(self, other) -> bool:
        if not isinstance(other, TimeTable):
            return False
        return (
            self.worker_schedule == other.worker_schedule and
            self.worker_pool == other.worker_pool and
            self.worker_demand == other.worker_demand
        )


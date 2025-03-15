import numpy as np

from models.worker.worker import Worker
from models.timeslot.timeslot import TimeSlot
from models.timeslot_matrix.timeslot_matrix_resources import TimeSlotMatrixResources

class WorkerPool:
    """
    A Controller class for Worker objects.

    This controller class is tasked with oversight of all of the workers in the system and
    facilitates the means for searching for workers by availability

    Attributes:
        workers (set[Workers]): A set of workers present in the pool.
    """
    def __init__(self):
        """
        Initializes a WorkerPool object.

        Args:
            
        
        Creates an empry set for worker objects.
        """
        self.workers: set[Worker] = set()
    
    def get_workers(self) -> set[Worker]:
        """Returns a set of all of the Workers in the WorkerPool"""
        return self.workers

    def get_available_workers(self, timeslot: TimeSlot) -> list[Worker]:
        """Returns a set of workers, that are available on some timeslot"""
        return [worker for worker in self.workers if worker.is_available(timeslot)]

    def add_worker(self, worker: Worker) -> None:
        """Adds a worker to the WorkerPool set"""
        if worker in self.workers:
            raise ValueError("A worker is already in the worker pool.")
        self.workers.add(worker)

    def add_workers(self, workers: list[Worker]) -> None:
        """Adds a list of worker to the WorkerPool set"""
        new_workers = set(workers)
        existing_workers = self.workers

        if existing_workers & new_workers:  # Check if any worker already exists
            raise ValueError("One or more workers are already in the worker pool.")
        
        existing_workers.update(new_workers)

    def get_supply_matrix(self) -> np.ndarray:
        """Returns a resource matrix for all of the workers"""
        worker_availabilities = [worker.availability.matrix for worker in self.workers]
        return np.sum(worker_availabilities, axis=0)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, WorkerPool):
            return False
        return self.workers == other.workers

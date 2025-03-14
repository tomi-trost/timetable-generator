import numpy as np

from models.worker.worker import Worker
from models.timeslot.timeslot import TimeSlot
from models.timeslot_matrix.timeslot_matrix_resources import TimeSlotMatrixResources

class WorkerPool:

    def __init__(self):
        self.workers: set[Worker] = {}
    
    def get_workers(self) -> set[Worker]:
        """Returns a set of all of the Workers in the WorkerPool"""
        return self.workers

    def get_available_workers(self, timeslot: TimeSlot) -> set[Worker]:
        """Returns a set of workers, that are available on some timeslot"""
        return {worker for worker in self.workers if worker.is_available(timeslot)}

    def add_worker(self, worker: Worker) -> None:
        """Adds a worker to the WorkerPool set"""
        if worker in self.workers:
            raise ValueError("A worker is already in the worker pool.")
        self.workers.add(worker)

    def get_supply_matrix(self) -> np.ndarray:
        """Returns a resource matrix for all of the workers"""
        worker_availabilities = [worker.availability for worker in self.workers]
        return np.sum(worker_availabilities, axis=0)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, WorkerPool):
            return False
        return self.workers == other.workers

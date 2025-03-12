from models.worker.worker import Worker
from models.timeslot.timeslot import TimeSlot

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


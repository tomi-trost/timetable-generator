import numpy as np

from app.models.worker.worker import Worker
from app.models.timeslot_matrix.timeslot_matrix_resources import TimeSlotMatrixResources

class Heuristics:

        
    def worker_heuristic(worker: Worker, worker_supply: TimeSlotMatrixResources, worker_demand: TimeSlotMatrixResources) -> int:
        """Returns a heuristic value for a worker"""
        worker_assigned_count = worker.assigned.count()

        # Computes the probability of a worker being assigned to a timeslot
        # Formula: Takes into acount already assigned timeslots and uses worker.availability.count() for normalization
        assign_probability = (worker_assigned_count + np.sum((worker_demand.matrix * worker.availability.matrix) / worker_supply.matrix)) / worker.availability.count() 
        # Computes the users rating from maximum rating
        worker_rating = worker.rating / Worker.max_rating
        # Computes satisfaction factor based on the prefered number of timeslots it wants to be assigned
        worker_satisfaction = worker_assigned_count / worker.availability_range.min

        heuristics = [1/worker_rating, assign_probability, worker_satisfaction]
        weights = [1/2, 1/4, 1/4]
        return sum([heuristic * weight for heuristic, weight in zip(heuristics, weights)])
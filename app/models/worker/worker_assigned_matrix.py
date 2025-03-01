import numpy as np

from models.timeslot.timeslot_matrix import TimeSlotMatrix
from models.worker.worker import Worker

class WorkerAssignedMatrix(TimeSlotMatrix):

    def __init__(self, xdim: int, ydim: int):
        self.matrix = np.full((xdim, ydim), None, dtype=object)
    
    def put(timeslot, x: Worker):
        ...

    def free(timeslot, x):
        return super().free(x)
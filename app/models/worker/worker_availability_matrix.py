import numpy as np

from models.timeslot.timeslot_matrix import TimeSlotMatrix

class WorkerAvailabilityMatrix(TimeSlotMatrix):

    def __init__(self, xdim: int , ydim):
        self.matrix = np.zeros((xdim, ydim))

    def put(timeslot: TimeSlot):
        """Lables a timeslot as available"""
        
    def _getMatrixIndex(timeslot: TimeSlot):
        return (timeslot.day)
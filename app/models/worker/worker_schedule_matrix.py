import numpy as np

from models.timeslot.timeslot_matrix import TimeSlotMatrix
from models.timeslot.timeslot import TimeSlot
from models.timeslot.day import Day

from models.worker.worker import Worker

class WorkerScheduleMatrix(TimeSlotMatrix):

    def __init__(self, days: int, shifts: int):
        self.matrix: list[list[set]] = np.array(
            [[set() for _ in range(shifts)] for _ in range(days)],
            dtype=object
        )
    
    def put(self, worker: Worker, timeslot: TimeSlot) -> None:
        """Assigns a Worker to a timeslot in the matrix"""
        matrix_timeslot = self._getTimeSlotContent(timeslot)
        matrix_timeslot.add(worker)

    def free(self, worker: Worker, timeslot: TimeSlot) -> None:
        """Frees a Worker from a timeslot"""
        matrix_timeslot = self._getTimeSlotContent(timeslot)
        matrix_timeslot.remove(worker)

    def count(self, timeslot: TimeSlot) -> int:
        """Count the number of Workers assigned to a TimeSlot"""
        matrix_timeslot = self._getTimeSlotContent(timeslot)
        return len(matrix_timeslot)
    
    def is_assigned(self, worker: Worker, timeslot: TimeSlot) -> bool:
        """Checks if a Worker is assigned to a timeslot"""
        matrix_timeslot = self._getTimeSlotContent(timeslot)
        return worker in matrix_timeslot
    
    def _getMatrixIndex(self, timeslot: TimeSlot) -> tuple[int, int]:
        return Day.get_index(timeslot.day), timeslot.shift.index
    
    def _getTimeSlotContent(self, timeslot: TimeSlot) -> set[Worker]:
        """Get a Worker set of the timeslot matrix"""
        ts_index = self._getMatrixIndex(timeslot)
        return self.matrix[ts_index]
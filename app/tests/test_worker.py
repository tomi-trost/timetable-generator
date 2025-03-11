import pytest

from models.worker.worker import Worker
from models.worker.worker_schedule_matrix import WorkerScheduleMatrix

from models.timeslot.timeslot_matrix_binary import TimeSlotMatrixBinary
from models.timeslot.timeslot import TimeSlot
from models.timeslot.day import Day
from models.timeslot.shift import ShiftPool


def test_timeslot_matrix_binary():

    shift_pool = ShiftPool(2)

    timeslot1 = TimeSlot(Day.MON, shift_pool.get_shift(0))
    timeslot2 = TimeSlot(Day.MON, shift_pool.get_shift(1))

    matrix1 = TimeSlotMatrixBinary(7, 2)
    matrix1.put(timeslot1)

    assert matrix1.count() == 1            
    assert matrix1.is_active(timeslot1)   

    matrix1.free(timeslot1)

    assert matrix1.count() == 0            
    assert matrix1.is_active(timeslot2) == False


def test_worker_schedule_matrix():

    TIMESLOT_MATRIX_DIMENSIONS = (7, 2)

    availability_matrix, shift_pool, timeslots = generate_availability_matrix(*TIMESLOT_MATRIX_DIMENSIONS)
    worker = Worker(availability_matrix, availability_range=(1, 2))

    worker.assign(timeslots[0])
    
    worker_schedule_matrix = WorkerScheduleMatrix(*TIMESLOT_MATRIX_DIMENSIONS)
    worker_schedule_matrix.put(worker, timeslots[0])

    assert worker_schedule_matrix.count(timeslots[0]) == 1  # Checks that number of assigned workers to the timeslot is 1
    assert worker_schedule_matrix.is_assigned(worker, timeslots[0]) # Check that timeslot was loged


def test_worker():

    availability_matrix, shift_pool, timeslots = generate_availability_matrix(7, 2)

    worker1 = Worker(availability=availability_matrix, availability_range=(1, 2))

    worker1.assign(timeslot=timeslots[0])
    worker1.assign(timeslot=timeslots[1])

    assert worker1.cnt == 2

    with pytest.raises(ValueError, match="The Worker isn't available for this timeslot."):
        worker1.assign(timeslot=TimeSlot(Day.FRI, shift_pool.get_shift(1)))
    

def generate_availability_matrix(days: int, shifts: int) -> TimeSlotMatrixBinary:
    
    shift_pool = ShiftPool(shifts)
    timeslots: list[TimeSlot] = []

    timeslots.append(TimeSlot(Day.TUE, shift_pool.get_shift(1)))
    timeslots.append(TimeSlot(Day.THU, shift_pool.get_shift(1)))
    timeslots.append(TimeSlot(Day.WED, shift_pool.get_shift(0)))


    availability_matrix = TimeSlotMatrixBinary(days=days, shifts=shifts)

    availability_matrix.put(timeslots[0])
    availability_matrix.put(timeslots[1])
    availability_matrix.put(timeslots[2])

    return availability_matrix, shift_pool, timeslots
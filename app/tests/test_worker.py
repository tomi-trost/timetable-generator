from models.worker.worker import Worker
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


def test_worker():

    shift_pool = ShiftPool(2)

    timeslot1 = TimeSlot(Day.TUE, shift_pool.get_shift(1))
    timeslot2 = TimeSlot(Day.THU, shift_pool.get_shift(1))
    timeslot3 = TimeSlot(Day.WED, shift_pool.get_shift(0))

    availability_matrix = TimeSlotMatrixBinary(days=7, shifts=2)
    assigned_matrix = TimeSlotMatrixBinary(days=7, shifts=2)

    availability_matrix.put(timeslot1)
    availability_matrix.put(timeslot2)
    availability_matrix.put(timeslot3)

    worker1 = Worker(availability=availability_matrix, assigned=assigned_matrix)

    worker1.assign(timeslot=timeslot1)
    worker1.assign(timeslot=timeslot2)

    assert worker1.cnt == 2

    assert worker1.assign(timeslot=TimeSlot(Day.FRI, shift_pool.get_shift(1))) 
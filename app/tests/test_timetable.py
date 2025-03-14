from app.models.timetable.timetable import TimeTable
from app.models.timeslot_matrix.timeslot_matrix_resources import TimeSlotMatrixResources
from app.models.timeslot_matrix.timeslot_matrix_binary import TimeSlotMatrixBinary
from app.models.timeslot.timeslot_pool import TimeSlotPool
from app.models.timeslot.timeslot import TimeSlot
from app.models.timeslot.day import Day
from app.models.worker.worker_pool import WorkerPool
from app.models.worker.worker import Worker


def test_timetable():

    timeslot_pool = TimeSlotPool(list(Day), 2)
    worker_demand = generate_demand_matrix(timeslot_pool) 
    worker_pool = generate_worker_pool(timeslot_pool)

    timetable = TimeTable(worker_demand=worker_demand, worker_pool=worker_pool)
    timeslot = timeslot_pool.get_timeslot(Day.MON, 0)
    available_workers: Worker = worker_pool.get_available_workers(timeslot)
    if available_workers is []:
        raise ValueError(f"No workers available on: {timeslot}")
    timetable.assign(available_workers[0], timeslot)

    timetable_clone = timetable.clone()

    assert timetable.worker_schedule.count(timeslot) == 1 # Was the worker assigned
    assert timetable == timetable_clone 
    assert timetable.is_solvable() == True

    timetable.free(available_workers[0], timeslot)
    assert timetable.worker_schedule.count(timeslot) == 0 # Was the worker freed 
    assert (timetable == timetable_clone) == False


def generate_demand_matrix(timeslot_pool: TimeSlotPool) -> TimeSlotMatrixResources:
    
    demand = TimeSlotMatrixResources(days=timeslot_pool.day_number, shifts=timeslot_pool.shift_number)

    demands = [1, 0, 1] + [0] * 11
    for ts_demand, timeslot in zip(demands, timeslot_pool.get_timeslots(), strict=True):
        for _ in range(ts_demand):
            demand.increment(timeslot)

    return demand
    

def generate_worker_pool(timeslot_pool: TimeSlotPool) -> WorkerPool:

    days = timeslot_pool.day_number
    shifts = timeslot_pool.shift_number

    worker_pool = WorkerPool()

    supply = {
        "Janez Novak": timeslot_pool.get_timeslot(day=Day.SUN, shift=0),
        "Pipa Pana": timeslot_pool.get_timeslot(day=Day.MON, shift=0),
        "Kuli Mana": timeslot_pool.get_timeslot(day=Day.FRI, shift=1),
    }

    for worker_name, timeslot in supply.items():
        if timeslot not in timeslot_pool.get_timeslots():
            raise ValueError("This time slot is not in the timeslot pool")
        availability = TimeSlotMatrixBinary(days=days, shifts=shifts)
        availability.put(timeslot)
        worker = Worker(name=worker_name, availability=availability, availability_range=(1, 1))
        worker_pool.add_worker(worker)

    return worker_pool

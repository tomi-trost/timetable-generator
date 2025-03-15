import json
import numpy as np

from app.models.timetable.timetable import TimeTable
from app.models.timeslot_matrix.timeslot_matrix_resources import TimeSlotMatrixResources
from app.models.timeslot_matrix.timeslot_matrix_binary import TimeSlotMatrixBinary
from app.models.worker.worker_pool import WorkerPool
from app.models.worker.worker_pool import Worker

class FileManager:

    def read_timetable(file_path: str = "app/data/timetable.json") -> TimeTable:
        
        try: 
            with open(file_path, "r") as file:
                timetable_data = json.load(file)
            print("JSON loaded successfully:", timetable_data)
        except FileNotFoundError:
            print("Error: File not found.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format.")

        # Read time table demand
        demand = np.array(timetable_data["demand"])
        worker_demand = TimeSlotMatrixResources(matrix=demand)

        # Read worker availabilities
        worker_pool = WorkerPool()
        worker_pool.add_workers([
            Worker(
                name=worker["name"],
                availability=TimeSlotMatrixBinary(matrix=np.array(worker["availability"])),
                availability_range=(worker["availability_range"]["min"], worker["availability_range"]["max"]),
                rating=worker["rating"]
            )
            for worker in timetable_data["workers"]
        ])

        return TimeTable(worker_demand=worker_demand, worker_pool=worker_pool)

        

from app.models.file_manager.file_manager import FileManager
from app.models.timetable.timetable import TimeTable

def test_file_manager():

    timetable: TimeTable = FileManager.read_timetable("app/data/timetable.json")

    assert timetable.is_solvable() == True
    shortage = timetable.get_shortage()
    assert shortage.sum() == 0
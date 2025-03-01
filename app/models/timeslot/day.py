from enum import Enum

class Day(str, Enum):
    SUN = "sun"
    MON = "mon"
    TUE = "tue"
    WED = "wed"
    THU = "thu"
    FRI = "fri"
    SAT = "sat"

    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def get_index(cls, day: 'Day') -> int:
        """Returns the index based on the day of the week"""
        # Mapping each enum member to an index starting from 0
        return list(cls).index(day)
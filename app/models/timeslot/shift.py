from typing import Generator

class ShiftPool():
    
    class _Shift():

        def __init__(self, index: int):
            """Index starts with 0 and ends with number of shifts minus 1"""
            self.index = index

        def __eq__(self, other):
            if not isinstance(other, ShiftPool._Shift):
                return False
            return other.index == self.index

    def __init__(self, shift_number: int = 2):
        self.shift_number = shift_number

    def get_shifts(self) -> Generator['ShiftPool._Shift', None, None]:
        """Generator method that yields all shifts from shift indexes"""
        for i in range(self.shift_number):
            yield self._Shift(i)

    def get_shift(self, index: int):
        """Returns a Shift object if index is within bounds of the ShiftPool"""
        if index not in range(self.shift_number):
            raise Exception(f"Shift with index value={index} does not exist.")
        return self._Shift(index)
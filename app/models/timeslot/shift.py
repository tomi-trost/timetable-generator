class Shift():

    def __init__(self, index: int):
        """Index starts with 0 and ends with number of shifts minus 1"""
        self.index = index

    def __eq__(self, other):
        if not isinstance(other, Shift):
            return False
        return other.index == self.index
    
    

class ShiftPool():
    
    def __init__(self, shift_number: int = 2):
        self.shift_number = shift_number

    def get_shifts(self):
        """Generator method that yields shifts from shift indexes"""
        for i in range(self.shift_number):
            yield Shift(i)
class Shift():

    def __init__(self, index):
        self.index = index

    def getIndex(self):
        """Getter method for the shift index"""
        return self.index
    

class ShiftPool():
    
    def __init__(self, shift_number: int = 2):
        self.shift_number = shift_number

    def get_shifts(self):
        """Generator method that yields shifts from shift indexes"""
        for i in range(self.shift_number):
            yield Shift(i)
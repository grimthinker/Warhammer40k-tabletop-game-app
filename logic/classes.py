import random


class DInt:
    def __init__(self, number, add):
        self.number = number
        self.add = add

    @property
    def rand(self):
        return random.randint(1, self.number) + self.add

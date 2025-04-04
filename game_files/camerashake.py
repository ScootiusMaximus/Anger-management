import random

class Camerashake:
    val = 0
    def __init__(self,decay=0.9):
        self.decay = decay

    def tick(self):
        self.val = self.val * self.decay
        if self.val < 0.01:
            self.val = 0

    def get(self):
        return (random.randint(-int(self.val),int(self.val)),
                random.randint(-int(self.val), int(self.val)))

    def set(self,val):
        self.val = val

    def add(self,val):
        self.val += val
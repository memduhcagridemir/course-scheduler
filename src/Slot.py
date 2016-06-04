import itertools    # generate unique ids for objects in case we need

""" Slot class represents timeslots in a week """
class Slot:
    autoIncrementalID = itertools.count().next

    def __init__(self, dow, time):
        self.id = Slot.autoIncrementalID()
        self.dow = dow      # day of week of slot
        self.time = time    # starting time of slot

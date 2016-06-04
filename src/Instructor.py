import itertools    # generate unique ids for objects in case we need

""" Instructor class represents faculty staff """
class Instructor:
    autoIncrementalID = itertools.count().next

    def __init__(self, name, capacity):
        self.id = Room.autoIncrementalID()
        self.name = name
        self.capacity = capacity

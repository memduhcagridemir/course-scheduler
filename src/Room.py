import itertools    # generate unique ids for objects in case we need

""" Room class represents Classrooms """
class Room:
    autoIncrementalID = itertools.count().next

    def __init__(self, name, capacity):
        self.id = Room.autoIncrementalID()
        self.name = name
        self.capacity = capacity

from src.Room import Room
from src.Course import Course
from src.Instructor import Instructor

class CourseClass:
    def __init__(self, course, instructor):
        self.course = course
        self.instructor = instructor

    def roomHasEnoughCapacity(self, room):
        capacity = {
            "Large": 3,
            "Medium": 2,
            "Small": 1
        }

        if capacity[room.capacity] >= capacity[self.course.capacity]:
            return True

        return False

    def printObject(self):
        self.course.printObject()
        self.instructor.printObject()

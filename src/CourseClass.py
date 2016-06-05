from src.Room import Room
from src.Course import Course
from src.Instructor import Instructor

class CourseClass:
    def __init__(self, course, instructor):
        self.course = course
        self.instructor = instructor

    def roomHasEnoughCapacity(self, room):
        roomCapacity = 0
        if room.capacity == 'Large':
            roomCapacity = 60
        elif room.capacity == 'Medium':
            roomCapacity = 30
        else:
            roomCapacity = 10

        courseCapacity = 0
        if self.course.capacity == 'Large':
            courseCapacity = 60
        elif self.course.capacity == 'Medium':
            courseCapacity = 30
        else:
            courseCapacity = 10

        if roomCapacity >= courseCapacity:
            return True

        return False

    def printObject(self):
        print "Class"
        self.course.printObject()

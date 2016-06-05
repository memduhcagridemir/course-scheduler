from CourseClass import CourseClass

import random

class Schedule:
    def __init__(self, slots, rooms, courses):
        self.classes = []
        self.slots = []
        for i in range(0, len(slots) * len(rooms)):
            self.slots.append([])

        self.rooms = rooms
        self.fitness = 0.
        self.satisfactory = False
        self.numberOfCrossoverPoints = 1

        self.courses = courses
        self.timeSlots = slots

    def createSchedule(self, instructors):
        for course in self.courses:
            courseClass = CourseClass(course, instructors[course.instructorIndex - 1])

            slotIndex = random.randint(0, len(self.slots) - 3)

            self.slots[slotIndex].append(courseClass)
            self.slots[slotIndex + 1].append(courseClass)
            self.slots[slotIndex + 2].append(courseClass) # assuming all courses are A3

            self.classes.append({"class": courseClass, "slotIndex": slotIndex})

    def instructorAvailable(self, instructor, timeSlot):
        checkSlot = timeSlot - len(self.slots)

        while checkSlot > 0:
            if self.slots[checkSlot] != [] and self.slots[checkSlot][0].instructor.id == instructor.id: # two class may occur at same time
                return False

            checkSlot -= len(self.slots)

        checkSlot = timeSlot + len(self.slots)

        while checkSlot < len(self.slots):
            if self.slots[checkSlot] != [] and self.slots[checkSlot].instructor.id == instructor.id:
                return False

            checkSlot += len(self.slots)

        return True

    def calculateFitness(self):
        self.satisfactory = False
        coursesToAdd = []
        extraCourses = []
        for course in self.courses:
            coursesToAdd.append(course.id)

        classPoints = []
        for someClass in self.classes:
            classIndex = someClass["slotIndex"]

            classPoint = 0
            if len(self.slots[classIndex]) == 1 and len(self.slots[classIndex + 1]) == 1 and len(self.slots[classIndex + 2]) == 1:
                # class is using a spare room
                classPoint += 1

                room = classIndex / len(self.slots)
                room = self.rooms[room]

                if self.slots[classIndex][0].roomHasEnoughCapacity(room):
                    classPoint += 1

                if self.instructorAvailable(self.slots[classIndex][0].instructor, classIndex):
                    classPoint += 1

            classPoints.append(classPoint)

            if someClass["class"].course.id in coursesToAdd:
                coursesToAdd.remove(someClass["class"].course.id)
            else:
                extraCourses.append(someClass["class"].course.id)

        if len(self.classes):
            self.fitness = (sum(classPoints) * 1.0) / (len(self.classes) * 3)
        else:
            self.fitness = 0

        if len(coursesToAdd) or len(extraCourses):
            self.satisfactory = False
        else:
            self.satisfactory = True

        return self.fitness

    def rebuildSlots(self):
        slotsLen = len(self.slots)

        self.slots = []
        for i in range(0, slotsLen):
            self.slots.append([])

        for someClass in self.classes:
            self.slots[someClass["slotIndex"]].append(someClass["class"])
            self.slots[someClass["slotIndex"] + 1].append(someClass["class"])
            self.slots[someClass["slotIndex"] + 2].append(someClass["class"]) # assuming all courses are A3

    def crossover(self, p2, p3):
        firstParentCrossoverIndex = random.randint(0, len(self.classes))
        secondParentCrossoverIndex = random.randint(0, len(p2.classes))

        p3.classes = self.classes[0:firstParentCrossoverIndex] + p2.classes[secondParentCrossoverIndex:]
        p3.rebuildSlots()

        return p3

    def printObject(self):
        for i in range(0, len(self.slots)):
            if i % len(self.timeSlots) == 0:
                self.rooms[i / len(self.timeSlots)].printObject()

            scheduledClasses = self.slots[i]
            for scheduledClass in scheduledClasses:
                if scheduledClass is not None:
                    scheduledClass.printObject()
                    print ""

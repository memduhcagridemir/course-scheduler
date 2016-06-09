from CourseClass import CourseClass

import random

class Schedule:
    def __init__(self, slots, rooms, courses, instructors):
        self.classes = []
        self.slots = []
        for i in range(0, len(slots) * len(rooms)):
            self.slots.append([])

        self.rooms = rooms
        self.fitness = 0.0
        self.satisfactory = False
        self.numberOfCrossoverPoints = 1

        self.courses = courses
        self.timeSlots = slots
        self.instructors = instructors
        self.generation = 1

    def createSchedule(self):
        for course in self.courses:
            courseClass = CourseClass(course, self.instructors[course.instructorIndex - 1])

            if course.arrangement == "A3":
                slotIndex = random.randint(0, len(self.slots) - 3)

                self.slots[slotIndex].append(courseClass)
                self.slots[slotIndex + 1].append(courseClass)
                self.slots[slotIndex + 2].append(courseClass) # assuming all courses are A3

                self.classes.append({"class": courseClass, "slotIndex": slotIndex, "length": 3})
            else:
                slotIndex = random.randint(0, len(self.slots) - 2)

                self.slots[slotIndex].append(courseClass)
                self.slots[slotIndex + 1].append(courseClass)

                self.classes.append({"class": courseClass, "slotIndex": slotIndex, "length": 2})

                slotIndex = random.randint(0, len(self.slots) - 1)

                self.slots[slotIndex].append(courseClass)

                self.classes.append({"class": courseClass, "slotIndex": slotIndex, "length": 1})

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
        coursesToAdd = []
        extraCourses = []
        for course in self.courses:
            coursesToAdd.append(course.id)
            if course.arrangement == 'A21':
                coursesToAdd.append(course.id)

        self.satisfactory = None

        classPoints = []
        for someClass in self.classes:
            classIndex = someClass["slotIndex"]

            spareRoom = False
            if someClass["length"] == 3:
                if len(self.slots[classIndex]) == 1 and len(self.slots[classIndex + 1]) == 1 and len(self.slots[classIndex + 2]) == 1:
                    spareRoom = True
            elif someClass["length"] == 2:
                if len(self.slots[classIndex]) == 1 and len(self.slots[classIndex + 1]) == 1:
                    spareRoom = True
            elif someClass["length"] == 1:
                if len(self.slots[classIndex]) == 1:
                    spareRoom = True
            else:
                raise ValueError(someClass)

            classPoint = 0
            if spareRoom:
                # class is using a spare room
                classPoint += 1

                room = classIndex / len(self.timeSlots)
                room = self.rooms[room]

                if self.slots[classIndex][0].roomHasEnoughCapacity(room):
                    classPoint += 1
                else:
                    self.satisfactory = False

                if self.instructorAvailable(self.slots[classIndex][0].instructor, classIndex):
                    classPoint += 1
                else:
                    self.satisfactory = False

                if self.slots[classIndex][0].instructor.wantsSlot((classIndex % len(self.timeSlots)) + 1):
                    classPoint += 1
                else:
                    self.satisfactory = False

                if self.slots[classIndex][0].instructor.prefersSlot((classIndex % len(self.timeSlots)) + 1):
                    classPoint += 1

                dayIndex = (classIndex % len(self.timeSlots)) / (len(self.timeSlots) / 5)
                if dayIndex != ((classIndex + someClass["length"] - 1) % len(self.timeSlots)) / (len(self.timeSlots) / 5):
                    self.satisfactory = False

            else:
                self.satisfactory = False

            classPoints.append(classPoint)

            if someClass["class"].course.id in coursesToAdd:
                coursesToAdd.remove(someClass["class"].course.id)
            else:
                extraCourses.append(someClass["class"].course.id)

        if len(self.classes):
            self.fitness = (sum(classPoints) * 1.0) / (len(self.classes) * 5)
        else:
            self.fitness = 0

        if self.satisfactory is None:
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
            if someClass["length"] == 3:
                self.slots[someClass["slotIndex"]].append(someClass["class"])
                self.slots[someClass["slotIndex"] + 1].append(someClass["class"])
                self.slots[someClass["slotIndex"] + 2].append(someClass["class"])
            elif someClass["length"] == 2:
                self.slots[someClass["slotIndex"]].append(someClass["class"])
                self.slots[someClass["slotIndex"] + 1].append(someClass["class"])
            elif someClass["length"] == 1:
                self.slots[someClass["slotIndex"]].append(someClass["class"])
            else:
                print "Hata"

    def crossover(self, p2, p3):
        firstCrossoverIndex = random.randint(0, len(self.classes) - 1)
        secondCrossoverIndex = random.randint(firstCrossoverIndex, len(self.classes) - 1)

        p3.classes = self.classes[0:firstCrossoverIndex] + p2.classes[firstCrossoverIndex:secondCrossoverIndex] + self.classes[secondCrossoverIndex:]
        p3.generation = max(self.generation, p2.generation) + 1

        return p3

    def mutation(self):
        classIndex = random.randint(0, len(self.classes) - 1)
        self.classes[classIndex]["slotIndex"] = random.randint(0, len(self.slots) - 1)
        self.rebuildSlots()

    def printObject(self):
        print "Generation: " + str(self.generation)
        for i in range(0, len(self.slots)):
            roomIndex = i / len(self.timeSlots)
            timeIndex = i % len(self.timeSlots)

            if i % len(self.timeSlots) == 0:
                print "----- &&& -----"
                self.rooms[roomIndex].printObject()
                print ""

            scheduledClasses = self.slots[i]
            if len(scheduledClasses):
                self.timeSlots[timeIndex].printObject()

            for scheduledClass in scheduledClasses:
                if scheduledClass is not None:
                    scheduledClass.printObject()
                    print ""

""" Course class represents courses offered by department """
class Course:
    def __init__(self, inputString):
        stringParts = inputString.split(",")
        cursorPosition = 0

        self.id = stringParts[cursorPosition].strip()
        cursorPosition += 1

        self.name = stringParts[cursorPosition].strip()
        cursorPosition += 1

        self.capacity = stringParts[cursorPosition].strip()
        cursorPosition += 1

        self.arrangement = stringParts[cursorPosition].strip()
        cursorPosition += 1

        self.instructorIndex = int(stringParts[cursorPosition].strip())
        cursorPosition += 1

    def printObject(self):
        print "Course Name: " + str(self.name) + str(" | ") + "Capacity: " + str(self.capacity)
        print "Arrangement: " + str(self.arrangement)

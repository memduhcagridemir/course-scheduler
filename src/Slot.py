""" Slot class represents timeslots in a week """
class Slot:
    def __init__(self, inputString):
        stringParts = inputString.split(",")
        cursorPosition = 0

        self.id = stringParts[cursorPosition].strip()
        cursorPosition += 1

        self.dow = stringParts[cursorPosition].strip()
        cursorPosition += 1

        self.time = stringParts[cursorPosition].strip()
        cursorPosition += 1

    def printObject(self):
        print str(self.dow) + ", " + str(self.time)

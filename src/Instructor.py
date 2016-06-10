""" Instructor class represents faculty staff """
class Instructor:
    def __init__(self, inputString):
        stringParts = inputString.split(",")
        cursorPosition = 0

        self.id = stringParts[cursorPosition].strip()
        cursorPosition += 1

        self.name = stringParts[cursorPosition].strip()
        cursorPosition += 1

        self.unwanteds = []
        self.unpreferreds = []

        numberOfUnwanteds = int(stringParts[cursorPosition].strip())
        cursorPosition += 1

        for i in range(cursorPosition, cursorPosition + numberOfUnwanteds):
            self.unwanteds.append(int(stringParts[i]))

        cursorPosition += numberOfUnwanteds

        numberOfUnpreferreds = int(stringParts[cursorPosition].strip())
        for i in range(cursorPosition, cursorPosition + numberOfUnpreferreds):
            self.unpreferreds.append(int(stringParts[i]))

    def wantsSlot(self, slotId):
        if slotId in self.unwanteds:
            return False

        return True

    def prefersSlot(self, slotId):
        if slotId in self.unpreferreds:
            return False

        return True

    def printObject(self):
        print "Instructor Name: " + str(self.name)

    def getInitials(self):
        return '.'.join(name[0].upper() for name in self.name.split())

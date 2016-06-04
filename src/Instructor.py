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

    def printObject(self):
        print "Instructor: " + str(self.id)
        print "Name: " + str(self.name)
        print "Unwanteds: " + str(self.unwanteds)
        print "Unpreferreds: " + str(self.unpreferreds)

import random
from operator import itemgetter

from Slot import Slot
from Room import Room
from Course import Course
from Instructor import Instructor
from Schedule import Schedule

class GeneticAlgorithm:
    def __init__(self, slots, rooms, courses, instructors):
        self.slots = slots
        self.rooms = rooms
        self.courses = courses
        self.instructors = instructors

        self.chromosomes = []

        self.newChromosomes = []
        self.newChromosomeCount = 3

    def initChromosomes(self, numberOfChromosomes):
        for i in range(0, numberOfChromosomes):
            chromosome = Schedule(self.slots, self.rooms, self.courses)
            chromosome.createSchedule(self.instructors)

            self.chromosomes.append({"chromosome": chromosome, "fitness": chromosome.calculateFitness()})

    def continueIteration(self):
        for chromosome in self.chromosomes:
            if chromosome["fitness"] == 1.0 and chromosome["chromosome"].satisfactory:
                chromosome["chromosome"].printObject()
                return False

        return True


    def execute(self):
        while self.continueIteration():
            selectedPairs = [] # [(3, 5)]
            while len(selectedPairs) < self.newChromosomeCount:
                pair = (random.randint(0, len(self.chromosomes) - 1), random.randint(0, len(self.chromosomes) - 1))
                if pair[0] != pair[1]:
                    selectedPairs.append(pair)

            for pair in selectedPairs:
                nc = self.chromosomes[pair[0]]["chromosome"].crossover(self.chromosomes[pair[1]]["chromosome"], Schedule(self.slots, self.rooms, self.courses))
                nc.rebuildSlots()
                self.newChromosomes.append({"chromosome": nc, "fitness": nc.calculateFitness()})

            self.chromosomes = sorted(self.chromosomes, key=itemgetter('fitness'))

            for chromosome in self.newChromosomes:
                changeIndex = random.randint(0, len(self.chromosomes) - 3) # dont change best three chromosomes
                self.chromosomes[changeIndex] = chromosome

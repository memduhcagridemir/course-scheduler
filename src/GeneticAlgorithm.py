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

        # possible solutions
        self.chromosomes = []

        # new generations generated on every turn
        self.newChromosomes = []
        self.newChromosomeCount = 4000

    def initChromosomes(self, numberOfChromosomes):
        for i in range(0, numberOfChromosomes):
            chromosome = Schedule(self.slots, self.rooms, self.courses, self.instructors)
            chromosome.createSchedule()

            self.chromosomes.append({"chromosome": chromosome, "fitness": chromosome.calculateFitness()})

    def continueIteration(self):
        for chromosome in self.chromosomes:
            if chromosome["fitness"] >= 0.70 and chromosome["chromosome"].satisfactory:
                chromosome["chromosome"].printObject()
                return False

        return True

    def execute(self):
        while self.continueIteration():
            # select random pair as parent for new generation
            selectedPairs = []
            while len(selectedPairs) < self.newChromosomeCount:
                pair = (random.randint(0, len(self.chromosomes) - 1), random.randint(0, len(self.chromosomes) - 1))
                if pair[0] != pair[1]:
                    selectedPairs.append(pair)

            # new generation of solutions
            self.newChromosomes = []
            for pair in selectedPairs:
                nc = self.chromosomes[pair[0]]["chromosome"].crossover(self.chromosomes[pair[1]]["chromosome"], Schedule(self.slots, self.rooms, self.courses, self.instructors))
                nc.rebuildSlots()
                self.newChromosomes.append({"chromosome": nc, "fitness": nc.calculateFitness()})

            self.chromosomes = sorted(self.chromosomes, key=itemgetter('fitness'))

            for chromosome in self.newChromosomes:
                changeIndex = random.randint(0, len(self.chromosomes) - int(len(self.chromosomes) * 0.05) - 1) # dont change best 5% chromosomes
                self.chromosomes[changeIndex] = chromosome

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
        self.newChromosomeCount = 80

        self.lastFitness = 0
        self.fitnessConstantSince = 0

    def initChromosomes(self, numberOfChromosomes):
        for i in range(0, numberOfChromosomes):
            chromosome = Schedule(self.slots, self.rooms, self.courses, self.instructors)
            chromosome.createSchedule()

            self.chromosomes.append({"chromosome": chromosome, "fitness": chromosome.calculateFitness()})

    def continueIteration(self):
        for chromosome in self.chromosomes:
            if chromosome["fitness"] >= 0.90 and chromosome["chromosome"].satisfactory:
                chromosome["chromosome"].printObject()
                chromosome["chromosome"].saveHtml('schedule_output.html')
                return False

        print "Best Fitness in Generation: " + str(self.chromosomes[len(self.chromosomes) - 1]["fitness"])
        if self.lastFitness == self.chromosomes[len(self.chromosomes) - 1]["fitness"]:
            self.fitnessConstantSince += 1
            if self.fitnessConstantSince >= 100:
                self.chromosomes[len(self.chromosomes) - 1]["chromosome"].printObject()
                self.chromosomes[len(self.chromosomes) - 1]["chromosome"].saveHtml('schedule_output.html')
                print "Fitness score does not seem improve anymore. This schedule may not satify some requirements but a \"significant\" time is passed, so it is returned. Please try again with (smaller) inputs"
                return False
        else:
            self.lastFitness = self.chromosomes[len(self.chromosomes) - 1]["fitness"]
            self.fitnessConstantSince = 0

        return True

    def execute(self):
        while self.continueIteration():
            # new generation of solutions
            self.newChromosomes = []

            for mutationIndex in range(len(self.chromosomes) / 2, len(self.chromosomes)):
                if random.randint(0, 5) == 4: # mutation probablity 20%
                    p4 = self.chromosomes[mutationIndex]["chromosome"].mutation()
                    self.newChromosomes.append({"chromosome": p4, "fitness": p4.calculateFitness()})

            # select random pair as parent for new generation
            selectedPairs = []
            while len(selectedPairs) < (self.newChromosomeCount - len(self.newChromosomes)) / 2:
                pair = (random.randint(0, len(self.chromosomes) - 1), random.randint(len(self.chromosomes) * 0.90, len(self.chromosomes) - 1))
                if pair[0] != pair[1]:
                    selectedPairs.append(pair)

            for pair in selectedPairs:
                if random.randint(0, 5) == 4: # mutation probablity 20%
                    children = self.chromosomes[pair[0]]["chromosome"].crossover(self.chromosomes[pair[1]]["chromosome"])
                    for nc in children:
                        nc.rebuildSlots()
                        self.newChromosomes.append({"chromosome": nc, "fitness": nc.calculateFitness()})

            self.chromosomes = sorted(self.chromosomes, key=itemgetter('fitness'))

            for i in range(0, min(len(self.newChromosomes), int(len(self.chromosomes) * 0.80))): # dont change best 20% chromosomes
                self.chromosomes[i] = self.newChromosomes[i]

import sys
import random

from src.Slot import Slot
from src.Room import Room
from src.Course import Course
from src.Instructor import Instructor

from src.GeneticAlgorithm import GeneticAlgorithm

def main(cmdArguments):
    if len(cmdArguments) <= 0:
        raise ValueError("Usage: python main.py <inputfile>")

    slots = []
    rooms = []
    courses = []
    instructors = []

    with open(cmdArguments[0]) as fp:
        for line in fp:
            if line.startswith("#"):
                # ignore comments in input file
                continue

            lineSections = line.split("=")
            if lineSections[0].strip() == "Slot":
                slots.append(Slot(lineSections[1]))
            elif lineSections[0].strip() == "Room":
                rooms.append(Room(lineSections[1]))
            elif lineSections[0].strip() == "Course":
                courses.append(Course(lineSections[1]))
            elif lineSections[0].strip() == "Instructor":
                instructors.append(Instructor(lineSections[1]))

    algo = GeneticAlgorithm(slots, rooms, courses, instructors)
    algo.initChromosomes(10000)
    algo.execute()

"""
    for course in courses:
        course.printObject()

    for room in rooms:
        room.printObject()

    for slot in slots:
        slot.printObject()

    for ins in instructors:
        ins.printObject()
"""

if __name__ == '__main__':
    main(sys.argv[1:])

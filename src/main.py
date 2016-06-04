from Slot import Slot
from Room import Room

s = Slot("ad", "asd")
print s.id
print s.dow
print s.time

s = Slot("asd", "asd")
print s.id

s = Room("bmb-1", "medim")
print s.id
print s.name

print s.capacity

### Logic layer (backend classes)
"""
PawPal — pet care planning system.

Class skeleton generated from diagrams/uml.mmd.
Attributes are set up in each __init__; method bodies are left as stubs
(marked with TODO) for you to implement.
"""


class Pet:
    def __init__(self, name, weight, age, owner_name, on_medication):
        self.name = name
        self.weight = weight
        self.age = age
        self.owner_name = owner_name
        self.on_medication = on_medication

    def is_walking(self):
        # TODO: return True if the pet is currently on a walk
        pass

    def is_eating(self):
        # TODO: return True if the pet is currently eating
        pass

    def is_playing(self):
        # TODO: return True if the pet is currently playing
        pass

    def took_medicine(self):
        # TODO: return True if the pet has taken its medicine
        pass

    def is_groomed(self):
        # TODO: return True if the pet has been groomed
        pass


class Owner:
    def __init__(self, first_name, last_name, pet_name, availability):
        self.first_name = first_name
        self.last_name = last_name
        self.pet_name = pet_name
        self.availability = availability

    def is_available(self):
        # TODO: return True if the owner has time available
        pass


class Task:
    def __init__(self, name, duration, priority, completed=False):
        self.name = name
        self.duration = duration
        self.priority = priority
        self.completed = completed

    def mark_done(self):
        # TODO: set self.completed to True
        pass


class Schedule:
    def __init__(self, name, date, owner):
        self.name = name
        self.date = date
        self.owner = owner
        self.tasks = []  # list of Task objects

    def add_task(self, task):
        # TODO: add a Task to self.tasks
        pass

    def total_time(self):
        # TODO: return the sum of durations of all tasks
        pass

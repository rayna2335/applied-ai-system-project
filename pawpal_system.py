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
    def __init__(self, first_name, last_name, pet_name, available_minutes):
        self.first_name = first_name
        self.last_name = last_name
        self.pet_name = pet_name
        self.available_minutes = available_minutes  # how many minutes the owner has today

    def is_available(self):
        # Owner has time if they have any minutes free
        return self.available_minutes > 0


class Task:
    # maps priority text to a number so tasks can be sorted (higher = more important)
    PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}

    def __init__(self, name, duration, priority, completed=False):
        self.name = name
        self.duration = duration
        self.priority = priority
        self.completed = completed

    def mark_done(self):
        self.completed = True

    def priority_rank(self):
        # convert the priority string into a number for sorting
        return self.PRIORITY_RANK.get(self.priority, 0)


class Schedule:
    def __init__(self, name, date, owner, pet):
        self.name = name
        self.date = date
        self.owner = owner
        self.pet = pet          # which pet this plan is for
        self.tasks = []         # list of Task objects
        self.reasons = []       # notes on why each task was/wasn't added (for explain())

    def add_task(self, task):
        self.tasks.append(task)

    def total_time(self):
        return sum(task.duration for task in self.tasks)

    def build_plan(self, available_tasks):
        """Pick tasks by priority until the owner runs out of time."""
        self.tasks = []
        self.reasons = []
        # highest priority first
        for task in sorted(available_tasks, key=lambda t: t.priority_rank(), reverse=True):
            if self.total_time() + task.duration <= self.owner.available_minutes:
                self.add_task(task)
                self.reasons.append(f"Added '{task.name}' ({task.priority} priority, {task.duration} min).")
            else:
                self.reasons.append(f"Skipped '{task.name}' — not enough time left.")
        return self.tasks

    def explain(self):
        """Return a human-readable reason for why this plan was chosen."""
        header = (f"Plan for {self.pet.name} on {self.date} — "
                  f"{self.total_time()} of {self.owner.available_minutes} min used.")
        return header + "\n" + "\n".join(self.reasons)

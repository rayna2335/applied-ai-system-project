### Logic layer (backend classes)
"""
PawPal — pet care planning system.

Class skeleton generated from diagrams/uml.mmd.
Attributes are set up in each __init__; method bodies are left as stubs
(marked with TODO) for you to implement.
"""
from datetime import date, timedelta

class Pet:
    def __init__(self, name, breed, weight, age, owner_name, on_medication):
        """Initialize a pet with its details and default (all-false) status flags."""
        self.name = name
        self.breed = breed
        self.weight = weight
        self.age = age
        self.owner_name = owner_name
        self.on_medication = on_medication

        # current status
        self.walking = False
        self.eating = False
        self.playing = False
        self.medicine_taken = False
        self.groomed = False

        # list of tasks for this pet
        self.tasks = []

    def is_walking(self):
        """Return True if the pet is currently walking."""
        return self.walking

    def is_eating(self):
        """Return True if the pet is currently eating."""
        return self.eating

    def is_playing(self):
        """Return True if the pet is currently playing."""
        return self.playing

    def took_medicine(self):
        """Return True if the pet has taken its medicine."""
        return self.medicine_taken

    def is_groomed(self):
        """Return True if the pet has been groomed."""
        return self.groomed

    def add_task(self, task):
        """Tag the task with this pet's name and add it to the pet's task list."""
        task.pet_name = self.name
        self.tasks.append(task)

    def filter_by_pet(self, pet_name):
        """Return tasks belonging to one pet."""
        return [
            task
            for task in self.tasks
            if task.pet_name == pet_name
        ]

class Owner:
    def __init__(self, first_name, last_name, available_minutes):
        """Initialize an owner with their name, available minutes, and empty pet list."""
        self.first_name = first_name
        self.last_name = last_name
        self.available_minutes = available_minutes
        self.pets = []

    def is_available(self):
        """Return True if the owner has any free minutes available."""
        # Owner has time if they have any minutes free
        return self.available_minutes > 0

    def add_pet(self, pet):
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return a combined list of tasks across all of the owner's pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

class Task:
    # maps priority text to a number so tasks can be sorted (higher = more important)
    PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}

    def __init__(
            self,
            name,
            time,
            duration,
            priority,
            frequency=None,
            completed=False
        ):
        self.name = name
        self.time = time
        self.duration = duration
        self.priority = priority
        self.frequency = frequency
        self.completed = completed

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def create_next_occurrence(self):
        """Create the next occurrence of a recurring task.

        Returns a fresh Task that copies this task's name, time, duration,
        priority, and frequency (so it will keep recurring). Recurring tasks
        always start out incomplete. Returns None if this task is one-off
        (frequency is not "daily" or "weekly").
        """
        if self.frequency in ("daily", "weekly"):
            return Task(
                self.name,
                self.time,
                self.duration,
                self.priority,
                self.frequency
            )
        return None
    
    def priority_rank(self):
        """Return the numeric rank of this task's priority for sorting."""
        # convert the priority string into a number for sorting
        return self.PRIORITY_RANK.get(self.priority, 0)


class Schedule:
    def __init__(self, owner):
        """Initialize a schedule for an owner's whole day with empty task and reason lists."""
        self.owner = owner      # this plan covers all of the owner's pets
        self.tasks = []         # list of Task objects
        self.reasons = []       # notes on why each task was/wasn't added (for explain())

    def sort_by_time(self):
        """Return tasks sorted by HH:MM time."""
        return sorted(
            self.tasks,
            key=lambda task: task.time
        )
    def filter_by_completion(self, completed):
        """Return completed or incomplete tasks."""
        return [
            task
            for task in self.tasks
            if task.completed == completed
        ]
    
    def add_task(self, task):
        """Add a task to this schedule."""
        self.tasks.append(task)

    def total_time(self):
        """Return the total duration in minutes of all scheduled tasks."""
        return sum(task.duration for task in self.tasks)

    def build_plan(self, available_tasks):
        """Greedily fill the schedule with the highest-priority tasks that fit.

        Sorts available_tasks by priority (high to low), then walks the list
        adding each task whose duration still fits within the owner's
        available_minutes. A running total is kept so the time check stays
        O(1) per task, making the whole build O(n log n) (dominated by the
        sort). Every task is logged to self.reasons — added or skipped — so
        explain() can report why each decision was made.

        Args:
            available_tasks: the candidate Task objects to schedule from.

        Note:
            Resets self.tasks and self.reasons on each call, so build_plan
            can be re-run safely.
        """
        self.tasks = []
        self.reasons = []
        used = 0

        for task in sorted(
            available_tasks,
            key=lambda t: t.priority_rank(),
            reverse=True
        ):
            if used + task.duration <= self.owner.available_minutes:
                self.add_task(task)
                used += task.duration
                self.reasons.append(
                    f"Added '{task.name}' for {task.pet_name} "
                    f"({task.priority} priority, {task.duration} min)."
                )
            else:
                self.reasons.append(
                    f"Skipped '{task.name}' for {task.pet_name} — not enough time left."
                )

    def detect_conflicts(self):
        """Find tasks that are scheduled at the same time.

        Groups the scheduled tasks into buckets keyed by their start time in a
        single O(n) pass, then reports any time slot holding more than one
        task.

        Returns:
            A list of human-readable warning strings, one per clashing time
            slot. Empty if no two tasks share a start time.
        """
        by_time = {}
        for task in self.tasks:
            by_time.setdefault(task.time, []).append(task.name)

        return [
            f"Conflict: {' and '.join(names)} both occur at {time}"
            for time, names in by_time.items()
            if len(names) > 1
        ]
    def explain(self):
        """Return a formatted text summary of the owner's scheduled tasks."""
        header = f"Daily plan for {self.owner.first_name} {self.owner.last_name}:"

        lines = []
        for task in self.tasks:
            lines.append(
                f"  {task.time} — {task.name} for {task.pet_name} "
                f"({task.duration} min) "
                f"[priority: {task.priority}]"
            )

        return header + "\n" + "\n".join(lines)

    def display_schedule(self):
        """Print each scheduled task with its duration and priority."""
        for task in self.tasks:
            print(f"{task.name} ({task.duration} min) - {task.priority}")


# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]

#edge cases
"""
1. 
"""
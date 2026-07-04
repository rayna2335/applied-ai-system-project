# testing file

from pawpal_system import Owner, Pet, Schedule, Task

owner = Owner(
    first_name="Rayna",
    last_name="Maruyama",
    available_minutes=120
)

pet1 = Pet(
    name="Cookie",
    breed="Holland lop",
    weight=10,
    age=2,
    owner_name="Rayna Maruyama",
    on_medication=False
)

pet2 = Pet(
    name="pansy",
    breed="Schnauzer",
    weight=20,
    age=4,
    owner_name="Rayna Maruyama",
    on_medication=True
)


owner.add_pet(pet1)
owner.add_pet(pet2)


print("Today's Schedule")
print("----------------------------")
task1 = Task(
    "Playtime",
    "08:00",
    20,
    "medium"
)

task2 = Task(
    "Feed Breakfast",
    "08:00",
    10,
    "high"
)

task3 = Task(
    "Morning Walk",
    "09:00",
    30,
    "high"
)
pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)

schedule = Schedule(owner=owner)

schedule.build_plan(owner.get_all_tasks())

print(schedule.explain())

# Test sorting
print("\nTasks sorted by time:")
for task in schedule.sort_by_time():
    print(task.time, task.name)

# Test filtering
print("\nIncomplete tasks:")
unfinished = schedule.filter_by_completion(False)

for task in unfinished:
    print(task.name)



task1.mark_complete()

next_task = task1.create_next_occurrence()

if next_task:
    print(
        f"Created recurring task: "
        f"{next_task.name} at {next_task.time}"
    )



print("\nConflict Detection:")
conflicts = schedule.detect_conflicts()

if conflicts:
    for conflict in conflicts:
        print(conflict)
else:
    print("No conflicts found.")
    
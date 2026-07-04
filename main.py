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
task1 = Task("Morning Walk", "08:00", 30, "high")
task2 = Task("Feed Breakfast", "09:00", 10, "high")
task3 = Task("Playtime", "10:00", 20, "medium")

pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)

schedule = Schedule(
    owner=owner,
    pet=pet1
)

schedule.build_plan(owner.get_all_tasks())

print(schedule.explain())
from pawpal_system import Pet, Task


def test_task_completion():
    # Create a task
    task = Task(
        name="Morning Walk",
        time="08:00",
        duration=30,
        priority="high"
    )

    # Verify task starts incomplete
    assert task.completed is False

    # Mark task complete
    task.mark_complete()

    # Verify completion status changed
    assert task.completed is True


def test_task_addition():
    # Create a pet
    pet = Pet(
        name="Cookie",
        breed="Holland lop",
        weight=10,
        age=2,
        owner_name="Rayna Maruyama",
        on_medication=False
    )

    # Count tasks before
    initial_count = len(pet.tasks)

    # Add a task
    task = Task(
        name="Feed Breakfast",
        time="09:00",
        duration=10,
        priority="high"
    )

    pet.add_task(task)

    # Verify task count increased
    assert len(pet.tasks) == initial_count + 1
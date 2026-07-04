from pawpal_system import Owner, Pet, Schedule, Task


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


def test_tasks_returned_in_chronological_order():
    # Build a schedule for an owner
    owner = Owner(
        first_name="Rayna",
        last_name="Maruyama",
        available_minutes=120
    )
    schedule = Schedule(owner)

    # Add tasks out of chronological order
    schedule.add_task(Task(name="Evening Walk", time="18:00", duration=30, priority="high"))
    schedule.add_task(Task(name="Morning Walk", time="08:00", duration=30, priority="high"))
    schedule.add_task(Task(name="Lunch", time="12:00", duration=15, priority="medium"))

    # Sort by time
    ordered = schedule.sort_by_time()

    # Verify tasks come back earliest-to-latest
    times = [task.time for task in ordered]
    assert times == ["08:00", "12:00", "18:00"]
    assert times == sorted(times)


def test_completing_daily_task_creates_next_days_task():
    # Create a recurring daily task
    task = Task(
        name="Feed Breakfast",
        time="09:00",
        duration=10,
        priority="high",
        frequency="daily"
    )

    # Mark today's task complete
    task.mark_complete()
    assert task.completed is True

    # Completing a daily task should spawn the next occurrence
    next_task = task.create_next_occurrence()

    # A new task exists and is distinct from the original
    assert next_task is not None
    assert next_task is not task

    # It carries over the recurring details
    assert next_task.name == task.name
    assert next_task.time == task.time
    assert next_task.duration == task.duration
    assert next_task.priority == task.priority
    assert next_task.frequency == "daily"

    # The following day's task starts fresh (incomplete)
    assert next_task.completed is False


def test_one_off_task_has_no_next_occurrence():
    # A task with no recurring frequency should not spawn a follow-up
    task = Task(name="Vet Visit", time="14:00", duration=45, priority="high")
    task.mark_complete()

    assert task.create_next_occurrence() is None


def test_scheduler_flags_duplicate_times():
    owner = Owner(
        first_name="Rayna",
        last_name="Maruyama",
        available_minutes=120
    )
    schedule = Schedule(owner)

    # Two tasks scheduled at the same time
    schedule.add_task(Task(name="Morning Walk", time="08:00", duration=30, priority="high"))
    schedule.add_task(Task(name="Feed Breakfast", time="08:00", duration=10, priority="high"))
    # And one at a distinct time that should not be flagged
    schedule.add_task(Task(name="Lunch", time="12:00", duration=15, priority="medium"))

    conflicts = schedule.detect_conflicts()

    # Exactly one clashing time slot is reported
    assert len(conflicts) == 1
    conflict = conflicts[0]
    assert "08:00" in conflict
    assert "Morning Walk" in conflict
    assert "Feed Breakfast" in conflict
    # The non-conflicting time is never mentioned
    assert "12:00" not in conflict
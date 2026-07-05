import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.title("🐾 PawPal+")
st.caption("A pet care planning assistant. Add your pets, list their care tasks, "
           "and PawPal+ builds a daily plan that fits your available time.")


# ---------------------------------------------------------------------------
# setup of the Owner in session state
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        first_name="Rayna",
        last_name="Maruyama",
        available_minutes=120,
    )

owner = st.session_state.owner


# ---------------------------------------------------------------------------
# Sidebar: owner settings where it shows the number of pets/tasks entered.
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("👤 Owner settings")

    owner.first_name = st.text_input("First name", value=owner.first_name)
    owner.last_name = st.text_input("Last name", value=owner.last_name)

    st.divider()
    st.metric("Available minutes", owner.available_minutes)
    st.metric("Pets", len(owner.pets))
    st.metric("Tasks", len(owner.get_all_tasks()))


# ---------------------------------------------------------------------------
# Step 1: Ask owner the available time they have
# ---------------------------------------------------------------------------
st.header("⏱️ Available time")
st.caption("How much total time do you have for pet care today? "
           "PawPal+ only schedules tasks that fit within this budget.")

col_hours, col_minutes = st.columns(2)
with col_hours:
    hours = st.number_input("Hours", min_value=0, max_value=24, value=owner.available_minutes // 60)
with col_minutes:
    minutes = st.number_input("Minutes", min_value=0, max_value=59, value=owner.available_minutes % 60, step=5)

owner.available_minutes = int(hours) * 60 + int(minutes)
st.info(f"Total available time today: **{owner.available_minutes} minutes** "
        f"({hours}h {minutes}m).")


st.divider()


# ---------------------------------------------------------------------------
# Step 2: Add pets
# ---------------------------------------------------------------------------
st.header("Add a pet")

with st.form("add_pet_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", placeholder="e.g. Biscuit")
        breed = st.text_input("Breed", placeholder="e.g. Golden Retriever")
    with col2:
        weight = st.number_input("Weight (lbs)", min_value=1, max_value=300, value=10)
        age = st.number_input("Age (years)", min_value=0, max_value=40, value=2)

    on_medication = st.checkbox("On medication")

    submitted_pet = st.form_submit_button("Add pet")

    if submitted_pet:
        if not pet_name.strip():
            st.error("Please enter a pet name.")
        else:
            owner.add_pet(
                Pet(
                    name=pet_name.strip(),
                    breed=breed.strip(),
                    weight=int(weight),
                    age=int(age),
                    owner_name=f"{owner.first_name} {owner.last_name}",
                    on_medication=on_medication,
                )
            )
            st.success(f"Added {pet_name} to your pets!")

# Show the current pets
if owner.pets:
    st.markdown("**Your pets:**")
    for pet in owner.pets:
        badge = " 💊" if pet.on_medication else ""
        st.write(f"• {pet.name} ({pet.breed}){badge}")
else:
    st.info("No pets yet — add one above to get started.")


st.divider()


# ---------------------------------------------------------------------------
# Step 3: Add tasks to a pet
# ---------------------------------------------------------------------------
st.header("Add care tasks")

if not owner.pets:
    st.warning("Add a pet first before creating tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet_name = st.selectbox(
            "Which pet is this task for?",
            [pet.name for pet in owner.pets],
        )

        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task title", placeholder="e.g. Morning walk")
            task_time = st.time_input("Time")
        with col2:
            duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20
            )
            priority = st.selectbox("Priority", ["high", "medium", "low"])

        submitted_task = st.form_submit_button("Add task")

        if submitted_task:
            if not task_title.strip():
                st.error("Please enter a task title.")
            else:
                selected_pet = next(
                    pet for pet in owner.pets if pet.name == selected_pet_name
                )
                selected_pet.add_task(
                    Task(
                        name=task_title.strip(),
                        time=task_time.strftime("%H:%M"),
                        duration=int(duration),
                        priority=priority,
                    )
                )
                st.success(f"Added '{task_title}' to {selected_pet_name}.")

    # Show all tasks across pets
    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.markdown("**All tasks:**")
        st.table(
            [
                {
                    "Pet": task.pet_name,
                    "Time": task.time,
                    "Task": task.name,
                    "Duration": task.duration,
                    "Priority": task.priority,
                }
                for task in all_tasks
            ]
        )

        # --- Live running total of time used vs. available ---
        used = sum(task.duration for task in all_tasks)
        available = owner.available_minutes
        remaining = available - used

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Time needed", f"{used} min")
        col_b.metric("Available", f"{available} min")
        col_c.metric("Remaining", f"{remaining} min")

        # progress bar (capped at 100% so it doesn't error when over budget)
        if available > 0:
            st.progress(min(used / available, 1.0))

        if remaining < 0:
            st.warning(
                f"⚠️ Your tasks need {used} min but you only have {available} min — "
                f"over by {abs(remaining)} min. The schedule will drop lower-priority tasks to fit."
            )
        else:
            st.caption(f"You have {remaining} min of free time left in today's budget.")


st.divider()


# ---------------------------------------------------------------------------
# Step 4: generate tasks into schedule.
# ---------------------------------------------------------------------------
st.header("Build the daily plan")
st.caption("Generates a plan using the highest-priority tasks that fit your available time.")

if st.button("Generate schedule", type="primary"):
    if not owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        schedule = Schedule(owner=owner)
        schedule.build_plan(owner.get_all_tasks())

        # Conflict warnings
        conflicts = schedule.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(f"⚠️ {warning}")
        else:
            st.success("No scheduling conflicts detected.")

        # Sorted plan
        sorted_tasks = schedule.sort_by_time()
        if sorted_tasks:
            st.success(
                f"Planned {len(sorted_tasks)} task(s) using "
                f"{schedule.total_time()} of {owner.available_minutes} available minutes."
            )
            st.markdown("#### 📅 Daily Plan (sorted by time)")
            st.table(
                [
                    {
                        "Time": task.time,
                        "Task": task.name,
                        "Pet": task.pet_name,
                        "Duration (min)": task.duration,
                        "Priority": task.priority,
                    }
                    for task in sorted_tasks
                ]
            )
        else:
            st.warning("No tasks could fit within the available time.")

        # Reasoning
        with st.expander("Why these tasks?"):
            for reason in schedule.reasons:
                st.write(f"• {reason}")

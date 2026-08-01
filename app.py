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
            st.rerun()
            
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
    selected_pet_name = st.selectbox(
        "Which pet is this task for?",
        [pet.name for pet in owner.pets],
    )
    task_title = st.text_input("Task title", placeholder="e.g. Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, step=5)
    priority = st.selectbox("Priority", ["high", "medium", "low"])

    def time_to_minutes(t):
        h, m = map(int, t.split(":"))
        return h * 60 + m

    busy_ranges = []
    for t in owner.get_all_tasks():
        start = time_to_minutes(t.time)
        end = start + t.duration
        busy_ranges.append((start, end))

    # Candidate start times every 15 minutes across the day
    available_slots = []
    for start in range(0, 24 * 60, 15):
        end = start + int(duration)
        if end > 24 * 60:
            continue  # would run past midnight
        overlaps = any(start < b_end and end > b_start for (b_start, b_end) in busy_ranges)
        if not overlaps:
            h, m = divmod(start, 60)
            available_slots.append(f"{h:02d}:{m:02d}")

    if not available_slots:
        st.warning(f"No open slots fit a {duration}-minute task today — try a shorter duration.")
    else:
        task_time_str = st.selectbox("Time", available_slots)

        if st.button("Add task"):
            if not task_title.strip():
                st.error("Please enter a task title.")
            else:
                selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
                selected_pet.add_task(
                    Task(
                        name=task_title.strip(),
                        time=task_time_str,
                        duration=int(duration),
                        priority=priority,
                    )
                )
                st.success(f"Added '{task_title}' to {selected_pet_name}.")
                st.rerun()

    # Show all tasks across pets, with delete buttons
    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.markdown("**All tasks:**")

        header_cols = st.columns([2, 2, 3, 2, 2, 1])
        for col, label in zip(header_cols, ["Pet", "Time", "Task", "Duration", "Priority", ""]):
            col.markdown(f"**{label}**")

        for i, task in enumerate(all_tasks):
            row_cols = st.columns([2, 2, 3, 2, 2, 1])
            row_cols[0].write(task.pet_name)
            row_cols[1].write(task.time)
            row_cols[2].write(task.name)
            row_cols[3].write(f"{task.duration} min")
            row_cols[4].write(task.priority)

            if row_cols[5].button("🗑️", key=f"delete_task_{i}_{task.name}_{task.time}"):
                owning_pet = next(p for p in owner.pets if p.name == task.pet_name)
                owning_pet.remove_task(task)
                st.rerun()

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
        st.session_state.schedule = schedule

        # Conflict warnings
        conflicts = schedule.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(f"⚠️ {warning}")
        else:
            st.success("No scheduling conflicts detected.")
            
        # 24-hour timetable view
        st.markdown("#### 🕐 24-Hour Timetable")
        timetable = schedule.get_24hr_timetable()

        rows = []
        for hour_label, tasks_in_hour in timetable.items():
            if tasks_in_hour:
                for task in tasks_in_hour:
                    rows.append({
                        "Hour": hour_label,
                        "Task": task.name,
                        "Pet": task.pet_name,
                        "Duration (min)": str(task.duration),
                        "Priority": task.priority,
                    })
            else:
                rows.append({
                    "Hour": hour_label,
                    "Task": "—",
                    "Pet": "",
                    "Duration (min)": "",
                    "Priority": "",
                })

        st.table(rows)

        # Postponed tasks list
        if schedule.postponed:
            st.markdown("#### ⏸️ Postponed (didn't fit today)")
            st.table(
                [
                    {
                        "Task": t.name,
                        "Pet": t.pet_name,
                        "Duration (min)": t.duration,
                        "Priority": t.priority,
                    }
                    for t in schedule.postponed
                ]
            )
        else:
            st.caption("Nothing postponed — everything fit!")

        # Reasoning
        with st.expander("Why these tasks?"):
            for reason in schedule.reasons:
                st.write(f"• {reason}")



# ---------------------------------------------------------------------------
# Step 5: Ask the AI about your schedule (RAG + guardrail)
# ---------------------------------------------------------------------------
st.divider()
st.header("🤖 Ask PawPal+ about your schedule")
st.caption("Ask a question about today's plan — answered using your actual schedule data.")

question = st.text_input("Your question", placeholder="e.g. Why was grooming postponed?")

if st.button("Ask"):
    if "schedule" not in st.session_state:
        st.warning("Generate a schedule first.")
    else:
        from ai_assistant import ask_schedule_question
        result = ask_schedule_question(st.session_state.schedule, owner, question)

        if result["warning"]:
            st.error(f"⚠️ {result['warning']}")
        if result["answer"]:
            st.write(result["answer"])
            if result["grounded"]:
                st.caption("✅ Guardrail check: answer appears grounded in real schedule data.")
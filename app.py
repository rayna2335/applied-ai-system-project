import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


# Create Owner only once
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        first_name="Rayna",
        last_name="Maruyama",
        available_minutes=120
    )

if st.session_state.owner.pets:
    pet_names = [pet.name for pet in st.session_state.owner.pets]

    selected_pet_name = st.selectbox(
        "Choose a pet",
        pet_names
    )

    selected_pet = next(
        pet for pet in st.session_state.owner.pets
        if pet.name == selected_pet_name
    )
else:
    st.warning("Add a pet first.")
    selected_pet = None

task_time = st.text_input("Task Time", value="08:00")

pet_name = st.text_input("Pet Name")
breed = st.text_input("Breed")

if st.button("Add Pet"):
    pet = Pet(
        name=pet_name,
        breed=breed,
        weight=10,
        age=2,
        owner_name="Rayna Maruyama",
        on_medication=False
    )

    st.session_state.owner.add_pet(pet)
    st.success(f"{pet_name} added!")



st.header("My Pets")

for pet in st.session_state.owner.pets:
    st.write(f"• {pet.name} ({pet.breed})")


st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task") and selected_pet:

    task = Task(
        name=task_title,
        time=task_time,
        duration=int(duration),
        priority=priority
    )

    selected_pet.add_task(task)

    st.success(
        f"Added '{task_title}' to {selected_pet.name}"
    )

if st.session_state.owner.get_all_tasks():

    rows = []

    for task in st.session_state.owner.get_all_tasks():
        rows.append({
            "Pet": task.pet_name,
            "Time": task.time,
            "Task": task.name,
            "Duration": task.duration,
            "Priority": task.priority
        })

    st.table(rows)
    
st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):

    if selected_pet:
        schedule = Schedule(
            owner=st.session_state.owner,
            pet=selected_pet
        )

        schedule.build_plan(
            st.session_state.owner.get_all_tasks()
        )

        st.text(schedule.explain())

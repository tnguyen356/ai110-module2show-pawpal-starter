import streamlit as st
from pawpal_system import Task, Pet, Owner, Plan

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

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

st.markdown("### Pets")
st.caption("Add one or more pets for this owner.")

if "pets" not in st.session_state:
    st.session_state.pets = []

pcol1, pcol2, pcol3 = st.columns(3)
with pcol1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with pcol2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
with pcol3:
    new_pet_age = st.number_input("Age", min_value=0, max_value=40, value=1)

if st.button("Add pet"):
    st.session_state.pets.append(
        {"name": new_pet_name, "species": new_pet_species, "age": int(new_pet_age)}
    )

if st.session_state.pets:
    st.write("Current pets:")
    st.table(st.session_state.pets)
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

pet_names = [p["name"] for p in st.session_state.pets]

if not pet_names:
    st.info("Add a pet before adding tasks.")
else:
    col0, col1, col2, col3, col4 = st.columns(5)
    with col0:
        task_pet = st.selectbox("Pet", pet_names)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        start_time = st.text_input("Start time", value="08:00 AM")

    freq_col, days_col = st.columns(2)
    with freq_col:
        frequency = st.selectbox("Repeats", ["daily", "weekly", "once"])

    recurrence_days: list[str] = []
    if frequency == "weekly":
        with days_col:
            recurrence_days = st.multiselect(
                "On which day(s)",
                ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                default=["Mon"],
            )

    if st.button("Add task"):
        st.session_state.tasks.append(
            {
                "pet_name": task_pet,
                "title": task_title,
                "duration_minutes": int(duration),
                "priority": priority,
                "start_time": start_time,
                "frequency": frequency,
                "recurrence_days": recurrence_days,
                "is_completed": False,
            }
        )

if st.session_state.tasks:
    filter_pets = st.multiselect(
        "Filter by pet", pet_names, default=pet_names, key="task_pet_filter"
    )
    filtered_tasks = [
        (i, t) for i, t in enumerate(st.session_state.tasks) if t["pet_name"] in filter_pets
    ]

    st.write("Current tasks:")
    if filtered_tasks:
        header = st.columns([3, 2, 2, 2, 2, 2])
        for col, label in zip(header, ["Task", "Pet", "Duration", "Priority", "Start", "Done"]):
            col.markdown(f"**{label}**")

        for i, t in filtered_tasks:
            row = st.columns([3, 2, 2, 2, 2, 2])
            row[0].write(t["title"])
            row[1].write(t["pet_name"])
            row[2].write(f"{t['duration_minutes']} min")
            row[3].write(t["priority"])
            row[4].write(t["start_time"])
            st.session_state.tasks[i]["is_completed"] = row[5].checkbox(
                "Completed", value=t.get("is_completed", False), key=f"task_done_{i}",
                label_visibility="collapsed",
            )
    else:
        st.info("No tasks match the selected pet(s).")
else:
    filter_pets = pet_names
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
time_available = st.number_input(
    "Time available today (minutes)", min_value=1, max_value=1440, value=60
)

if st.button("Generate schedule"):
    selected_tasks = [t for t in st.session_state.tasks if t["pet_name"] in filter_pets]

    if not st.session_state.pets:
        st.warning("Add at least one pet first.")
    elif not selected_tasks:
        st.warning("Add at least one task for the selected pet(s) first.")
    else:
        owner = Owner(name=owner_name, preferences={})
        pets_by_name = {}
        for p in st.session_state.pets:
            if p["name"] not in filter_pets:
                continue
            pet = Pet(name=p["name"], species=p["species"], age=p["age"])
            owner.add_pet(pet)
            pets_by_name[p["name"]] = pet

        for t in selected_tasks:
            task = Task(
                name=t["title"],
                description=t["title"],
                category="General",
                duration_minutes=t["duration_minutes"],
                priority=t["priority"],
                start_time=t["start_time"],
                frequency=t["frequency"],
                recurrence_days=t["recurrence_days"],
            )
            if t.get("is_completed"):
                task.mark_complete()
            pets_by_name[t["pet_name"]].add_task(task)

        plan = Plan(owner=owner)
        plan.build_plan(time_available_minutes=int(time_available))
        st.text(plan.explain())

# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov

# Run the tests:
python3 -m pytest

'''
The test covered adding a test to a pet increases count by 1, sorts tasks by time, tests for duplicate times.

Terminal output: 

============================================== test session starts ===============================================
platform darwin -- Python 3.13.2, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/raynamaruyama/codepath week4 project/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 6 items                                                                                                

tests/test_pawpal.py ......                                                                                [100%]

=============================================== 6 passed in 0.03s ================================================

confidence level: 5

'''
```

Sample test output:

```
Today's Schedule
----------------------------
Daily plan for Cookie (Holland lop):
  08:00 — Morning Walk (30 min) [priority: high]
  09:00 — Feed Breakfast (10 min) [priority: high]
  10:00 — Playtime (20 min) [priority: medium]
  ```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |
| Sorting | Schedule.sort_by_time() | Sorts tasks by HH:MM time
| Filtering | Schedule.filter_by_pet() and Schedule.filter_by_completion() | Filters tasks by pet and tasks that are completed.
| Conflict detection | Schedule.detect_conflicts() | Detects tasks scheduled at the same time.
| Recurring task | Task.create_next_occurance() | Automatically creates daily or weekly tasks.

## 📸 Demo Walkthrough

1. **`streamlit run app.py` to run the app**
2. Enter your first and last name as a owner of your pets.
3. Enter the available time you have today.
4. Add your pets (see left dashboard to see the count of your pets added) with age, name, breed and weight. Check if the pet is on medication.
5. Add pets tasks under **Add care tasks** with duration, name, time and priority level.
6. Generate a daily plan according to those pets and tasks added to the list.

Example workflow: add a pet → schedule a task → view today's plan

1. Under **Available time**, enter `2` hours `0` minutes. PawPal+ confirms that the total number of time you have for the day (120 minutes)
2. Under **Add a pet**, enter name `Cookie`, breed `Holland Lop`, weight `4` lbs, age `2`, and check **On medication**. Click **Add pet**. Then the app will add your pet and the sidebar pet count goes up by 1.
3. Under **Add care tasks**, select `Cookie`, then add:
   - Feed Breakfast, 08:00, 10 min, priority high
   - Morning Walk, 09:00, 30 min, priority high
   - Playtime, 10:00, 20 min, priority medium

   The running total shows 60 min needed / 120 available / 60 remaining

4. Click **Generate schedule**. PawPal+ checks for conflicts, keeps the highest-priority tasks that fit your 120-minute budget, and displays the daily plan sorted by time.


| Key Sceduler behaviors | Method(s) | What it does |
|------------------------|-----------|--------------|
| Building plan | build_plan() | sorts tasks by priority and adds each task. only if its duration still fits the owners available_minutes. |
| Sorting by time | sort_by_time() | returns scheduled tasks ordered by HH:MM start time. |
|Conflict detection | detect_conflicts() | If there are any missed prompt it will warn the user. |


### Sample CLI output (`python3 main.py`)

```text
Today's Schedule
----------------------------
Daily plan for Rayna Maruyama:
  08:00 — Feed Breakfast for Cookie (10 min) [priority: high]
  09:00 — Morning Walk for pansy (30 min) [priority: high]
  08:00 — Playtime for Cookie (20 min) [priority: medium]

Tasks sorted by time:
08:00 Feed Breakfast
08:00 Playtime
09:00 Morning Walk

Incomplete tasks:
Feed Breakfast
Morning Walk
Playtime

Conflict Detection:
Conflict: Feed Breakfast and Playtime both occur at 08:00
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->



#  3 core actions

The User should be able to:

1. add pet information (name, weight, age, owner, behavior)
2. Track pets actions (feed time, walk schedule)
3. Track owners schedule/plan
4. add Pets health information (meds, appointments)
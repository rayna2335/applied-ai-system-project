# Pet Plan Scheduler (Module 2 Project)

**PawPal+**  is a Streamlit app that helps a pet owner plan care tasks for their pet. The user just needs to add their availability, their pets, and tasks. This generates a simple schedule based on the owner's availability.

## Title and Summary

**Pet Plan Scheduler** allows pet owners to schedule/plan their tasks in organized time blocks within the 24hour timeline. It creates a 24-hour table to easily see the owner's schedule. Any tasks that wouldn't fit into the plan would be marked as a postponed list for low-priority tasks. This helps the pet owners to stay organized and utilize users' busy times to accomplish the tasks that need to be accomplished within the available time frame.

The pet owner can add pets, tasks for each of their pets, owners' availability, and priority for each task.


## Architecture Overview

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly in a 24 hour timetable format
- Also display other tasks that are postponed due to time constraints.
- Include tests for the most important scheduling behaviors

## Getting started

### Setup Instructions

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install anthropic python-dotenv
streamlit run app.py 
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Interactions
1. Enter the owner's name in the sidebar (First Name \ Last Name)
2. Enter the total amount of time you have during the day.
3. Add your pets to the system. It will auto-populate the number of pets in the sidebar.
4. Add care tasks for each of the pets you’ve entered. (Enter the name of the pet that will execute the plan, task title, duration, priority, and the time it will be executed).
5. Click on ‘Generate Schedule’ to schedule out a plan in 24 hour time table.
6. Anything that didn't fit into the schedule will go into the ‘Postponed’ task list.
7. At the very bottom, you can ask AI some specific questions about the schedule.

## Example 1
Input:
Available time: 60 minutes

Tasks:
Feed Cookie (10 min, High)
Walk Cookie (30 min, High)
Brush Cookie (20 min, Medium)

Output: 
8:00 Feed Cookie
8:10 Walk Cookie
8:40 Brush Cookie

No postponed tasks.

## Example 2
Input:
Available time: 30 minutes

Output:
Feed Cookie
Walk postponed

Reason:
Not enough available time.

## Example 3 with AI
Input:
Why wasn't brushing scheduled?

Ouput:
Brushing was postponed because there was not enough available time after scheduling higher-priority tasks.

## Exmaple 4 with AI 
Input:
Why should Cookie the bunny go to a vet?

Output:
Based on the provided schedule data, I do not have information regarding why 'Cookie' needs to go to the vet. The log only shows that a 20-minute, high-priority task named 'Cookie' for visit a vet was added to Rayna Maruyama's schedule today at 12:00 PM.



## Design Decisions
I built it this way because I want to test out how the AI model will make decisions based on level of priority and give reasoning for how it's scheduled the way it did. I limited the AI assistant to answering questions only from the generated schedule (using RAG). This prevents the AI from inventing information, but it also means it cannot answer questions that are not contained in the schedule.

## Testing Summary
I was able to implement the AI feature in the application and the ability to answer questions from available data with responses based on the priority level and timing. One challenge that I encountered was using the Anthropic API. The implementation was correct, but the API returned an error stating that the account didn't have sufficient API credits. But we used the Gemini API to connect to the AI model. From this experience, I learned the importance of grounding AI responses in real app data to reduce hallucinations and improve reliability in those responses.


## Reflection
This project taught me that building an AI application involves more than connecting to a language model. I learned how to combine scheduling logic, retrieval, and guardrails to create reliable AI responses. Testing also showed the importance of validating outputs and handling errors gracefully.

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


## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
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




## Reliability and evaluations (Human evaluations)
Summary: I performed 4 tests that cover scheduling, AI responses, guardrails and error handeling. All 4 tests passed.

| Test Inputs | Evaluation Criteria(s) | Results |
|------------------------|-----------|--------------|
| Schedule fits available time | No overflow | Pass |
| Prioritization order | Complete higher priority tasks before medium or lower level | Pass |
|AI only answers from scheduled daily plan | There are no hallucinations| Pass |
| Empty question | Returns message | Pass |

### Sample CLI output (`python3 main.py`)

## Portfolio Reflection

This project demonstrates my ability use Retrieval-Augmented Generation (RAG), prompt engineering, and guardrails. It also highlights the importance of testing, validation, and reliable AI system design. Through this project, I gained experience building an AI-assisted application that balances functionality, usability, and responsible AI practices.
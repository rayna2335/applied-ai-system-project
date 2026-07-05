# PawPal+ Project Reflection

## 1. System Design

This app is primarly used to track your pet's tasks that can plan out walks, play time, dinner, grooming, and medication times.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    #### brainstorm objects

    - The main object: pet, owner, task, schedule

    - A pet can have attributes such as name, weight, age, owner's name, and whether the pet is taking medication. With method of is_walking(), is_eating(), is_playing(),took_medicine(), isPlaying, isGroomed().

    - The Owner class can have attributes such as first and last name, pet name, and owner availability. With methods of isAvailable() to see when the owner is available to make a schedule.
    
    -  Task class can have attributes of the name, duration, priority level, and whether the task is completed or not, with methods of markDone().

    -  A schedule class can have attributes with a task name, date, and owner, with methods of add_task() and total_time() it takes to do each of those tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    #### change log
    - Added schedule time to be able to see if tasks acturally fits in the day/schedule.

    - The old design had no link to the pet a plan was for. Since this is a pet-care app, the Schedule now references the Pet it belongs to.

    - Added priority_rank() and a PRIORITY_RANK map to see the priority level, and mapped out the scheduler to see which tasks are more important than the other. 

    - Added build_plan() to be able to produce a daily plan and explain why tasks were added or skipped and why.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

    - The scheduler class goes over time and priority. All of the tasks duration is caluclated, and anything that pushes the budget over is skipped. The priorities are mapped with numeric values, and the tasks are sorted by priority before filling in the time budget.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

    - One tradeoff that my scheduler makes is that my Scheduler uses a simple detection algorithm that checks only if two tasks start at the same time. It doesn't necessarily check the schedule if it overlaps with other tasks. I chose this approach because it makes scheduling logic application simple for a small pet care app.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

    - I used AI tools like Claude to debugg errors and making sure that the code works as it should. From my experience, asking AI with a detailed/specific prompts made the response more consice and helpful rather than explaining a concept without details and what you expect of the response.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

    - One part when I didn't accept an AI suggestion was when I was working on the UI part. Claude would try to make it look complicated and add more lines of code. And there were some parts where it didn't align with the rest of my code, and I verified that by checking the methods inside the class and making sure that they do exist.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Some of the behaviors that I have tested are making sure that the tasks are scheduled in chronological order and making sure that the tasks are added successfully to the list of tasks. I also made sure that the conflict detection was properly set up and flagged when there are tasks that overlap with each other. These tests are important because this is what makes the app useful for the pet owners.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

    - I am confident that my scheduler works correctly. It adds the owner's name, pets, tasks, and schedules tasks in order. If I had more time, I would create an actual time range and make sure that the times don't overlap with each other. The app does the bare minimum of using the start time and duration of the time, but it doesn't check if it's going to overlap within that timeframe.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - From the entire project, I am most satisfied that the code works as it should. The owner is able to add tasks and create a schedule based on them. It also counts the number of pets and tasks the owner currently has, which makes it easier for the user to keep track of how many things to do throughout the day.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    - If I could improve the design of this app, I would improve the UI of the app. I think that would go to, like, web design, but it would be cool if we could also design the look/feel of the app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    - One important thing that I learned from this project is that AI is a tool and it doesn't replace us humans making the code work 100% because a lot of the time there are mistakes and some breaks into the code.
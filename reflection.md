# PawPal+ Project Reflection

## 1. System Design

This app is primarly used to track your pet's tasks that can plan out walks, play time, dinner, grooming, and medication times.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    #### brainstorm objects

    - The main object: pet, owner, task, schedule

    - Pet can have an attribiute of pets name, weight, age, owner name, and whether or not the pet is taking medication. With method of is_walking(), is_eating(), is_playing(),took_medicine(), isPlaying, isGroomed().

    - Ower class can have attributes of first and last name, pet name, and owner availability. With methods of isAvailable() to see when the owner is available to make schedule.

    - Task class can have attributes of the name, duration,priority level, and if the task is completed or not with methods of markDone().

    - Schedule class can have attributes with a task name, date, and owner with methods of add_task() and total_time() it takes to do each of those tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    #### change log
    - Added schedule time to be able to see if tasks acturally fits in the day/schedule.
    - The old design had no link to the pet a plan was for. Since this is a pet-care app, the Schedule now references the Pet it belongs to.

    - added priority_rank() and a PRIORITY_RANK map to see the priority level, and mapped out the scheduler to see which tasks are more important then the other. 

    - added build_plan() to be able to produce a daily plan and explain why tasks were added or skipped and why.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff that my schdeuler makes are that my Scheduler uses simple detection algorithm that checks only if two tasks that starts at the same time. It doesnt necessarily check the schedule if it overlapped with other tasks. I chose this approach because it makes scheduling logic application simple for a small petcare app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

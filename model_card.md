# # Pet Plan Scheduler Model Card (Reflection)

## 1) What is this system?

**Name:** Pet Plan Scheduler (Pawpal+) 
**Purpose:**  Pet Plan Scheduler helps pet owners organize daily pet schedules based on their available time. The system prioritizes important tasks and generates an achievable schedule. The pet owner is also able to use an AI assistant that answers any questions regarding how it was scheduled the way it was.

**Intended users:** 
The intended users for this app are pet owners who want help with planning daily pet care activities such as feeding, walks, playtime, and grooming while also managing limited time in busy owners' schedules.

---

## 2) How does it work?

Plan: The user enters their available time and pet care tasks and priority levels with durations of those tasks.

Analyze: A scheduling algorithm that evaluates tasks, prioritizes them, and determines which tasks fit within the available time frame.

Act: The scheduler creates a daily schedule, and AI can reason why the tasks were created in that order. The generated schedule is converted into a text context and sent to the language model using Retrieval-Augmented Generation (RAG). The AI answers questions only using the generated schedule.

Test: The application is tested by creating different tasks for different pets with different priorities and checking if the questions that were asked are accurate in response.

Reflect: The results are reviewed and made sure that the tasks are scheduled correctly and do not overlap with other tasks.

---

## 3) Inputs and outputs

**Inputs:**

* Enter the total available time.
* Pet information (name, breed, weight, age, medication status)
* Enter tasks (for which pet, task title, duration, priority, time)
* Pet owner asks a question about the schedule to AI.

**Outputs:**
- Schedule of tasks within scheduled time.
- List of postponed tasks.
- AI generated answer to pet owners question.

---

## 4) Reliability and safety rules
* AI is only instructed to answer using the generated schedule.
* This reduces hallucination and prevents AI from inventing tasks, pets, or time that was never created.

---

## 5) Observed failure modes

* While testing the AI assistant, the application returned an Anthropic API billing error because the API didn't have sufficient credits. The scheduling worked perfectly, but the AI assistant could not generate any responses.
* When I asked a question to the AI, it only generated half of a sentence. That is because the Mac output token uses up the whole tokens, which cuts off mid-sentence.

---

## 6) Improvement idea
* One improvement that I would make is to regenerate a timetable schedule by asking the AI to add tasks into the schedule. This would improve functionality and keep the system easy to use for pet owners.


## 7) Limitation and Bias
* The AI implemented into the application only answers questions using the generated schedule. It wont be able to provide any advice outside of schedules thats not mentioned in the schedules.

## 8) Potential Misuse
* The AI is only able to answer questions about the generated schedule and to respond only questions about the gejnerated schedule and to respons that it lacks information when a question falls outside of the inputs.

## 9) Reliability
* Implementing guardrails helped AI to limit its responses to the available task schedule and prevent from the AI to make assumptions.
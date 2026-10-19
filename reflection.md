# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Class OWNER: preference + pets 
Class PET: pet info + required responsibility
Class TASKS: include tasks, time
class PLAN: Build plan  

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
I keep the 4 classes the same, just add some validation to pet and task so that I can validate the pet does belong to the right owner, and that the named task is required for the pet.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
My scheduler considers mainly time and priority, preferences is partially handled by allowing the Owner to set tasks' priority. 
Time matters the most since the owner is trying to work around their own schedule to take care of their pets, so every free time slot matters.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
Enumerator is better to handle recurrance (daily, once, weekly), but it is not worth adding an import for just 3 values
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I have used Claude to help me generate a mermaid.js, implement my methods, verify bottlenecks, and writing pytest. The kind of prompts that I find most helpful is asking Claude to do something, while still giving constraints or specification, like "Can you flesh out the core implementaion of Task where it represents a single activity (description, name, frequency, completion status)"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
I did tell Claude to come up with the classes needed for the Pawpal app, and then compare its suggestion what I have. While most of its suggestion lines up with what I have, Claude also gives me some extra class that I find overcomplicated the project, like ScheduledTask while already having Scheduler/Plan. I verify by comparing our design against each other and asking Claude if certain class is truly needed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested for marking for a status of a task, task count increasing when add, recurrance tasks handling, sorting tasks by priority/time, and conflict handling.
These tests are important because they are the main feature of the app, to ensure that the app works as intended

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I'm about 90% confidence, the other 10% is because of edge cases. 
I would test 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

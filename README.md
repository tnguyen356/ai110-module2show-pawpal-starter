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

(.venv) PS C:\Users\scarl\OneDrive\Documents\CODEPATH\ai110-module2show-pawpal-starter> python main.py
Plan for Alice's pets (100 of 120 minutes used):
  08:00 AM — Walk for Buddy (30 min) [priority: high]
  10:00 AM — Vet Visit for Buddy (60 min) [priority: high]
  07:00 AM — Feed for Mittens (10 min) [priority: medium]
(.venv) PS C:\Users\scarl\OneDrive\Documents\CODEPATH\ai110-module2show-pawpal-starter> 

## 📐 Smarter Scheduling

1)  Task sorting:
- Implement in: `Plan.build_plan()`, `_parse_start_time()` 
- Candidates are sorted by priority first (`high` → `medium` → `low`), then by `start_time` as a tie-breaker within the same priority, so same-priority tasks come out in chronological order. 

2)  Filtering 
- Implement in: `Plan.build_plan()`, `Task.is_due()` 
- Before sorting, tasks are filtered down to only those due on the plan's date (`task.is_due(self.for_date)`). Tasks are also skipped if they no longer fit the remaining `time_available_minutes` budget. 

3)  Conflict handling 
- Implement in: `_time_range()`, `_overlaps()`, `Plan.build_plan()` 
- Each task's time window (`start_time` to `start_time + duration_minutes`) is checked against every already-scheduled task's window. 
- An overlapping task is skipped rather than double-booked and recorded in `Plan.skipped_conflicts`, since the owner can't do two things at once. 

4) Recurring tasks 
- Implement in: `Task.is_due()`, `Task.mark_complete()` / `mark_incomplete()` 
- `frequency` drives recurrence: `"once"` tasks are due until completed and never again; `"weekly"` tasks are due only on their `recurrence_days` (e.g. `["Mon", "Thu"]`), or every day if none are set; `"daily"` (and any other frequency) tasks are due every day except the exact date they were last completed, tracked via `last_completed_on`. 

## 🧪 Testing PawPal+ (python -m pytest)

`tests/test_pawpal.py` covers the core scheduling behaviors:

- **Task completion** — marking a task complete/incomplete updates its status.
- **Recurrence** (`Task.is_due()`) — `"once"` tasks are due until completed then never again; `"weekly"` tasks are due only on their `recurrence_days` (or every day if none are set); `"daily"` tasks recur every day except the exact date they were last completed.
- **Sorting** — scheduled tasks come out ordered by priority first, then by `start_time` as a tie-breaker within the same priority.
- **Conflict detection** — an overlapping lower-priority task is skipped (and recorded in `Plan.skipped_conflicts`) rather than double-booked against an already-scheduled task, while non-overlapping tasks of the same priority both get scheduled.
- **CONFIDENCE LEVEL** - 5/5


Sample test output:
(.venv) PS C:\Users\scarl\OneDrive\Documents\CODEPATH\ai110-module2show-pawpal-starter> python -m pytest
============================================================ test session starts ============================================================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\scarl\OneDrive\Documents\CODEPATH\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 14 items                                                                                                                           

tests\test_pawpal.py ..............                                                                                                    [100%]

============================================================ 14 passed in 0.36s =============================================================
(.venv) PS C:\Users\scarl\OneDrive\Documents\CODEPATH\ai110-module2show-pawpal-starter> 



## 📸 Demo Walkthrough

1. Run `streamlit run app.py` and enter the **Owner name** at the top of the page.
2. Under **Pets**, enter a pet's name, species, and age, then click **Add pet**. Repeat for each pet — they'll appear in the "Current pets" table.
3. Under **Tasks**, pick a pet, a task title, duration, priority, and start time. Choose how it **Repeats**: `daily`, `weekly` (pick the day(s) it recurs on), or `once`. Click **Add task** to add it to the list.
4. In the "Current tasks" list, use **Filter by pet** to show only the tasks for one or more pets, and check **Completed** on any task that's already done — completed tasks are left out of the next schedule (permanently for `once` tasks, just for today for `daily`/`weekly`).
5. Set **Time available today (minutes)** under "Build Schedule" to the owner's time budget for the day.
6. Click **Generate schedule**. PawPal+ builds the day's plan: tasks are chosen by priority first, then by start time, and any task that no longer fits the time budget or overlaps an already-scheduled task is left out.
7. Read the printed plan: each scheduled task shows its time, pet, duration, and priority, followed by a "Skipped due to time conflicts" section listing any tasks that were bumped because their time window overlapped something higher up the list.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

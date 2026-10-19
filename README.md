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

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Plan.build_plan()`, `_parse_start_time()` | Candidates are sorted by priority first (`high` → `medium` → `low`), then by `start_time` as a tie-breaker within the same priority, so same-priority tasks come out in chronological order. |
| Filtering | `Plan.build_plan()`, `Task.is_due()` | Before sorting, tasks are filtered down to only those due on the plan's date (`task.is_due(self.for_date)`). Tasks are also skipped if they no longer fit the remaining `time_available_minutes` budget. |
| Conflict handling | `_time_range()`, `_overlaps()`, `Plan.build_plan()` | Each task's time window (`start_time` to `start_time + duration_minutes`) is checked against every already-scheduled task's window. An overlapping task is skipped rather than double-booked and recorded in `Plan.skipped_conflicts`, since the owner can't do two things at once. |
| Recurring tasks | `Task.is_due()`, `Task.mark_complete()` / `mark_incomplete()` | `frequency` drives recurrence: `"once"` tasks are due until completed and never again; `"weekly"` tasks are due only on their `recurrence_days` (e.g. `["Mon", "Thu"]`), or every day if none are set; `"daily"` (and any other frequency) tasks are due every day except the exact date they were last completed, tracked via `last_completed_on`. |

See `Plan.explain()` for how scheduled tasks and skipped conflicts are reported, and `tests/test_pawpal.py` for coverage of the recurrence rules above.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

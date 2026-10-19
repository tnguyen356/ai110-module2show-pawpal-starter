from datetime import date, datetime, timedelta
from dataclasses import dataclass, field

@dataclass
class Task:
    name: str
    description: str
    category: str
    duration_minutes: int
    priority: str
    start_time: str
    frequency: str
    pet_name: str = ""
    is_completed: bool = False
    recurrence_days: list[str] = field(default_factory=list)
    last_completed_on: date | None = None

    def mark_complete(self, on_date: date | None = None) -> None:
        """Mark this task as completed for the given date (defaults to today)."""
        self.is_completed = True
        self.last_completed_on = on_date or date.today()

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.is_completed = False
        self.last_completed_on = None

    def is_due(self, on_date: date | None = None) -> bool:
        """Return whether this task should be scheduled on the given date.

        - "once" tasks are due until they're completed, then never again.
        - "weekly" tasks are only due on their recurrence_days (e.g. ["Mon", "Thu"]);
          with no recurrence_days set, they're treated as due every day.
        - "daily" (and any other frequency) tasks recur every day except the day
          they were last completed on.
        """
        on_date = on_date or date.today()

        if self.frequency == "once":
            return not self.is_completed

        if self.frequency == "weekly" and self.recurrence_days:
            if on_date.strftime("%a") not in self.recurrence_days:
                return False

        return self.last_completed_on != on_date


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet, tagging it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's list of tasks."""
        return self.tasks


@dataclass
class Owner:
    name: str
    preferences: dict
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _parse_start_time(start_time: str) -> datetime:
    """Parse a start time like '08:00 AM' for sorting; unparseable times sort last."""
    try:
        return datetime.strptime(start_time.strip(), "%I:%M %p")
    except ValueError:
        return datetime.max


def _time_range(task: Task) -> tuple[datetime, datetime] | None:
    """Return the (start, end) window a task occupies, or None if its start_time can't be parsed."""
    try:
        start = datetime.strptime(task.start_time.strip(), "%I:%M %p")
    except ValueError:
        return None
    return start, start + timedelta(minutes=task.duration_minutes)


def _overlaps(a: tuple[datetime, datetime], b: tuple[datetime, datetime]) -> bool:
    """Return True if time windows a and b share any overlapping minutes."""
    return a[0] < b[1] and b[0] < a[1]


@dataclass
class Plan:
    owner: Owner
    scheduled_tasks: list[Task] = field(default_factory=list)
    time_available_minutes: int = 0
    skipped_conflicts: list[tuple[Task, Task]] = field(default_factory=list)
    for_date: date = field(default_factory=date.today)

    def build_plan(self, time_available_minutes: int, for_date: date | None = None) -> None:
        """Schedule tasks across all pets by priority until the time budget runs out.

        Tasks whose time window overlaps an already-scheduled task are skipped as
        conflicts rather than double-booked, since the owner can't do two things at once.
        """
        self.time_available_minutes = time_available_minutes
        self.for_date = for_date or date.today()
        self.scheduled_tasks = []
        self.skipped_conflicts = []

        # Filtering: only consider tasks that recur on this date (see Task.is_due).
        candidates = [task for task in self.owner.get_all_tasks() if task.is_due(self.for_date)]

        # Sort: highest priority first; within the same priority, earliest start_time first.
        candidates.sort(
            key=lambda task: (
                _PRIORITY_ORDER.get(task.priority, len(_PRIORITY_ORDER)),
                _parse_start_time(task.start_time),
            )
        )

        time_used = 0
        scheduled_ranges: list[tuple[Task, tuple[datetime, datetime]]] = []
        for task in candidates:
            if time_used + task.duration_minutes > time_available_minutes:
                continue

            # Task conflict: skip this task if its time window overlaps one already scheduled.
            task_range = _time_range(task)
            if task_range is not None:
                conflicting_task = next(
                    (other for other, other_range in scheduled_ranges if _overlaps(task_range, other_range)),
                    None,
                )
                if conflicting_task is not None:
                    self.skipped_conflicts.append((task, conflicting_task))
                    continue
                scheduled_ranges.append((task, task_range))

            self.scheduled_tasks.append(task)
            time_used += task.duration_minutes

    def explain(self) -> str:
        """Return a human-readable summary of the scheduled plan."""
        if not self.scheduled_tasks:
            return "No tasks scheduled."

        lines = [
            f"Plan for {self.owner.name}'s pets "
            f"({self.total_time_used()} of {self.time_available_minutes} minutes used):"
        ]
        for task in self.scheduled_tasks:
            lines.append(
                f"  {task.start_time} — {task.name} for {task.pet_name} "
                f"({task.duration_minutes} min) [priority: {task.priority}]"
            )

        if self.skipped_conflicts:
            lines.append("")
            lines.append("Skipped due to time conflicts:")
            for task, conflicting_task in self.skipped_conflicts:
                lines.append(
                    f"  {task.name} for {task.pet_name} ({task.start_time}) conflicts with "
                    f"{conflicting_task.name} for {conflicting_task.pet_name} ({conflicting_task.start_time})"
                )

        return "\n".join(lines)

    def total_time_used(self) -> int:
        """Return the total minutes used by the scheduled tasks."""
        return sum(task.duration_minutes for task in self.scheduled_tasks)

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

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.is_completed = False


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


@dataclass
class Plan:
    owner: Owner
    scheduled_tasks: list[Task] = field(default_factory=list)
    time_available_minutes: int = 0

    def build_plan(self, time_available_minutes: int) -> None:
        """Schedule tasks across all pets by priority until the time budget runs out."""
        self.time_available_minutes = time_available_minutes
        self.scheduled_tasks = []

        candidates = [task for task in self.owner.get_all_tasks() if not task.is_completed]
        candidates.sort(key=lambda task: _PRIORITY_ORDER.get(task.priority, len(_PRIORITY_ORDER)))

        time_used = 0
        for task in candidates:
            if time_used + task.duration_minutes > time_available_minutes:
                continue
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
        return "\n".join(lines)

    def total_time_used(self) -> int:
        """Return the total minutes used by the scheduled tasks."""
        return sum(task.duration_minutes for task in self.scheduled_tasks)

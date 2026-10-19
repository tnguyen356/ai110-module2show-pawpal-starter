from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    category: str
    duration_minutes: int
    priority: str
    start_time: str


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Owner:
    name: str
    preferences: dict
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass


@dataclass
class Plan:
    owner: Owner
    pet: Pet
    scheduled_tasks: list[Task] = field(default_factory=list)
    time_available_minutes: int = 0

    def build_plan(self, pet: Pet, time_available_minutes: int) -> None:
        pass

    def explain(self) -> str:
        pass

    def total_time_used(self) -> int:
        pass

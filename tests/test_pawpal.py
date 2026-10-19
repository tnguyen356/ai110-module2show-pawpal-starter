from pawpal_system import Task, Pet


def make_task(**overrides):
    defaults = dict(
        name="Walk",
        description="Take the dog for a walk",
        category="Exercise",
        duration_minutes=30,
        priority="high",
        start_time="08:00 AM",
        frequency="daily",
    )
    defaults.update(overrides)
    return Task(**defaults)


def test_mark_complete_changes_task_status():
    task = make_task()
    assert task.is_completed is False

    task.mark_complete()

    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", age=5)
    assert len(pet.get_tasks()) == 0

    pet.add_task(make_task())

    assert len(pet.get_tasks()) == 1

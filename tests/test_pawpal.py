from datetime import date, timedelta

from pawpal_system import Task, Pet

MONDAY = date(2026, 10, 19)
TUESDAY = MONDAY + timedelta(days=1)
NEXT_MONDAY = MONDAY + timedelta(days=7)


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


def test_daily_task_is_due_every_day_until_completed():
    task = make_task(frequency="daily")
    assert task.is_due(MONDAY) is True
    assert task.is_due(TUESDAY) is True


def test_daily_task_is_not_due_on_the_day_it_was_completed():
    task = make_task(frequency="daily")

    task.mark_complete(on_date=MONDAY)

    assert task.is_due(MONDAY) is False


def test_daily_task_is_due_again_the_next_day_after_completion():
    task = make_task(frequency="daily")

    task.mark_complete(on_date=MONDAY)

    assert task.is_due(TUESDAY) is True


def test_once_task_is_due_until_completed_then_never_again():
    task = make_task(frequency="once")
    assert task.is_due(MONDAY) is True

    task.mark_complete(on_date=MONDAY)

    assert task.is_due(MONDAY) is False
    assert task.is_due(TUESDAY) is False
    assert task.is_due(NEXT_MONDAY) is False


def test_weekly_task_is_due_only_on_its_recurrence_days():
    task = make_task(frequency="weekly", recurrence_days=["Mon"])

    assert task.is_due(MONDAY) is True
    assert task.is_due(TUESDAY) is False
    assert task.is_due(NEXT_MONDAY) is True


def test_weekly_task_without_recurrence_days_is_due_every_day():
    task = make_task(frequency="weekly", recurrence_days=[])

    assert task.is_due(MONDAY) is True
    assert task.is_due(TUESDAY) is True


def test_weekly_task_is_not_due_on_its_day_once_completed_for_that_date():
    task = make_task(frequency="weekly", recurrence_days=["Mon"])

    task.mark_complete(on_date=MONDAY)

    assert task.is_due(MONDAY) is False
    assert task.is_due(NEXT_MONDAY) is True


def test_mark_incomplete_resets_last_completed_on():
    task = make_task(frequency="daily")
    task.mark_complete(on_date=MONDAY)
    assert task.is_due(MONDAY) is False

    task.mark_incomplete()

    assert task.is_completed is False
    assert task.is_due(MONDAY) is True

from pawpal_system import Task, Pet, Owner, Plan

owner = Owner(name="Alice", preferences={"reminder": True}, pets=[])

Pet1 = Pet(name="Buddy", species="Dog", age=5)
Pet2 = Pet(name="Mittens", species="Cat", age=3)

owner.add_pet(Pet1)
owner.add_pet(Pet2)

Pet1.add_task(Task(name="Walk", 
                   description="Take Buddy for a walk", 
                   category="Exercise", duration_minutes=30, 
                   priority="high", 
                   start_time="08:00 AM", 
                   frequency="daily"))

Pet2.add_task(Task(name="Feed", 
                   description="Feed Mittens", 
                   category="Nutrition", 
                   duration_minutes=10, 
                   priority="medium", 
                   start_time="07:00 AM", 
                   frequency="daily"))

Pet1.add_task(Task(name="Vet Visit",
                   description="Annual check-up for Buddy",
                   category="Health",
                   duration_minutes=60,
                   priority="high",
                   start_time="10:00 AM",
                   frequency="yearly"))

Pet2.add_task(Task(name="Grooming",
                   description="Groom Mittens",
                   category="Hygiene",
                   duration_minutes=20,
                   priority="medium",
                   start_time="08:00 AM",
                   frequency="daily"))

plan = Plan(owner=owner)
plan.build_plan(time_available_minutes=120)
print(plan.explain())
from datetime import datetime
from management.models import Formation, Student, StateValues
from django.db.models import Count


def save_formation(formation: Formation) -> Formation:
    formation.save()
    return formation


def formation_converter(
    code: str,
    name: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> Formation:
    formation = Formation()
    formation.name = name
    formation.code = code
    formation.start_date = start_date
    formation.end_date = end_date
    return formation


def formation_exists(code: str) -> bool:
    return Formation.objects.filter(code=code).exists()


def get_formation_stats(formation: Formation):
    all_states = {choice[0]: choice[1] for choice in StateValues.choices}

    state_counts = (
        Student.objects.filter(formation=formation)
        .values("state")
        .annotate(count=Count("state"))
    )

    total_students = sum(state["count"] for state in state_counts)

    state_stats = [
        {
            "state": all_states[state["state"]],
            "count": state["count"],
            "percentage": (
                (state["count"] / total_students * 100) if total_students > 0 else 0
            ),
        }
        for state in state_counts
    ]

    for state_value, state_label in all_states.items():
        if not any(stat["state"] == state_label for stat in state_stats):
            state_stats.append(
                {
                    "state": state_label,
                    "count": 0,
                    "percentage": 0,
                }
            )

    return state_stats, total_students

from .formation_service import save_formation, formation_converter
from .student_service import save_students, student_converter
from management.utils.validators import validate_state
from django.db import transaction
from management.viewmodels import FormationStudentsViewModel
from datetime import datetime
from management.models import Formation
from django.core.exceptions import ValidationError


def save_formation_and_students(
    formation: FormationStudentsViewModel,
    start_date: datetime.date,
    end_date: datetime.date,
):
    if Formation.objects.filter(code=formation.formation_code).exists():
        raise ValidationError(
            f"El código de formación '{formation.formation_code}' ya existe en la base de datos."
        )

    if (start_date and end_date) and end_date < start_date:
        raise ValidationError(
            f"La fecha de finalización no puede ser anterior a la fecha de inicio."
        )

    formation_data = formation_converter(
        formation.formation_code, formation.formation_name, start_date, end_date
    )

    with transaction.atomic():
        new_formation = save_formation(formation_data)

        valid_students = [
            student_converter(student, new_formation)
            for student in formation.students
            if validate_state(student.state)
        ]

        save_students(valid_students)

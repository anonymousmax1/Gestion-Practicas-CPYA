from django.core.exceptions import ValidationError
import os
from datetime import datetime
import re
from django.utils.translation import gettext_lazy as _


def validate_excel_file(value):
    valid_extensions = [".xls", ".xlsx"]
    valid_mime_types = [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions or value.content_type not in valid_mime_types:
        raise ValidationError("El archivo debe ser un Excel válido (.xls o .xlsx).")


class PracticesApplicationValidator:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def validate_contract_modality(self) -> bool:
        valid_types = [
            "Contrato de Aprendizaje",
            "Pasantia",
            "Vinculo Laboral",
            "Proyecto Productivo",
        ]
        if self.data.get("contract_modality") not in valid_types:
            self.errors.append(
                f"El tipo de contrato {self.data.get('contract_modality')} no es válido."
            )

    def validate_required_fields(self):
        required_fields = [
            "formation_code",
            "formation_level",
            "formation_name",
            "student_name",
            "student_document_type",
            "student_document_number",
            "student_address",
            "enterprise_name",
            "practices_start_date",
            "practices_end_date",
            "start_lective",
            "end_lective",
        ]

        field_labels = {
            "formation_code": _("Código de formación"),
            "formation_level": _("Nivel de formación"),
            "formation_name": _("Nombre de formación"),
            "student_name": _("Nombre del estudiante"),
            "student_document_type": _("Tipo de documento"),
            "student_document_number": _("Número de documento"),
            "student_address": _("Dirección del estudiante"),
            "enterprise_name": _("Nombre de la empresa"),
            "practices_start_date": _("Fecha de inicio de prácticas"),
            "practices_end_date": _("Fecha de fin de prácticas"),
            "start_lective": _("Inicio del ciclo lectivo"),
            "end_lective": _("Fin del ciclo lectivo"),
        }

        for field in required_fields:
            if not self.data.get(field):
                field_label = field_labels.get(field, field)
                self.errors.append(f"El campo {field_label} es obligatorio.")

    def validate_document_type(self):
        valid_types = ["CC", "TI", "PEP"]
        if self.data.get("student_document_type") not in valid_types:
            self.errors.append("El tipo de documento debe ser CC, TI o PEP.")

    def validate_dates(self):
        try:
            start = self.data.get("practices_start_date")
            end = self.data.get("practices_end_date")

            if not start or not end:
                self.errors.append("Las fechas de inicio y fin son obligatorias.")
                return

            # Convertir strings a datetime
            if isinstance(start, str) and isinstance(end, str):
                try:
                    start_date = datetime.strptime(start.split()[0], "%Y-%m-%d")
                    end_date = datetime.strptime(end.split()[0], "%Y-%m-%d")
                except ValueError:
                    self.errors.append("Las fechas deben estar en formato YYYY-MM-DD.")
                    return
            else:
                start_date = start
                end_date = end

            if end_date < start_date:
                self.errors.append(
                    "La fecha de fin de prácticas no puede ser anterior a la fecha de inicio."
                )

        except Exception as e:
            self.errors.append(f"Error al validar las fechas: {str(e)}")

    def validate(self):
        self.validate_required_fields()
        self.validate_document_type()
        self.validate_contract_modality()
        self.validate_dates()
        return self.errors


def validate_state(state: str) -> bool:
    valid_states = ["EN FORMACION", "CONDICIONADO"]
    return state in valid_states


def validate_name_contains_letter(value):
    if not re.search(r"[a-zA-Z]", value):
        raise ValidationError("El nombre debe contener al menos una letra.")


def validate_code_length(value):
    if not re.match(r"^\d{7}$", value):
        raise ValidationError(
            "El código debe contener exactamente 7 dígitos numéricos."
        )


def validate_document(value):
    if not re.match(r"^\d{6,15}$", value):
        raise ValidationError("El número de documento no es válido.")


def validate_formation_exists(value):
    from management.services.formation_service import formation_exists

    if formation_exists(value):
        raise ValidationError(_("Ya existe una formación con este número de ficha."))

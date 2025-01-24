from typing import Dict
from management.models import Student, ContractInfo, CustomUser
from management.values import StateValues
from management.utils.validators import PracticesApplicationValidator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from datetime import datetime
from management.converters import str_contrat_type_to_value, str_doc_type_to_value
from django.db import transaction


class ContractService:
    def create_contract_handler(self, data, instructor):
        self.validate_data(data)

        with transaction.atomic():
            student = self.get_student_from_contract(data)
            self.update_student_data(student, data, instructor)
            contract = self.create_or_update_contract(data, student)
            self.update_student_state(student)
            student.save()

    def validate_data(self, data):
        validator = PracticesApplicationValidator(data)
        errors = validator.validate()
        if errors:
            raise ValidationError(errors)

    def create_or_update_contract(self, data, student: Student):
        try:
            contract, created = ContractInfo.objects.update_or_create(
                student=student,
                defaults=self.extract_contract_data(data),
            )
            return contract
        except Exception as e:
            raise ValidationError(f"Error al crear o actualizar el contrato: {str(e)}")

    def extract_contract_data(self, data):
        try:
            return {
                "contract_type": str_contrat_type_to_value(data["contract_modality"]),
                "enterprise_name": data["enterprise_name"],
                "enterprise_address": data["enterprise_address"],
                "enterprise_neighborhood": data["enterprise_neighborhood"],
                "enterprise_region": data["enterprise_region"],
                "enterprise_city": data["enterprise_city"],
                "enterprise_cellphone": data["enterprise_cellphone"],
                "enterprise_phone": data["enterprise_phone"],
                "enterprise_email": data["enterprise_email"],
                "boss_name": data["boss_name"],
                "practices_start_date": self.parse_date(data["practices_start_date"]),
                "practices_end_date": self.parse_date(data["practices_end_date"]),
                "enterprise_nit": data["enterprise_nit"],
                "student_eps": data["student_eps"],
                "student_arl": data["student_arl"],
            }
        except KeyError as e:
            raise ValidationError(f"Falta el campo requerido: {str(e)}")

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str.split()[0], "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Las fechas deben estar en formato YYYY-MM-DD.")

    def update_student_data(self, student: Student, data, instructor: CustomUser = None):
        student.document_type = str_doc_type_to_value(data["student_document_type"])
        student.email_sena = data["email_sena"]
        student.cellphone = data["student_cellphone"]
        student.city = data["student_city"]
        student.address = data["student_address"]
        student.neighborhood = data["student_neighborhood"]
        student.instructor = instructor

    def update_student_state(self, student: Student):
        if student.state in [StateValues.EVALUATED.value, StateValues.CANCELED.value]:
            raise ValidationError(
                "No se puede crear contrato para aprendices con estado Evaluado o Cancelado."
            )

        student.state = StateValues.IN_TRACKING.value if student.instructor else StateValues.NO_TRACKING.value

    def get_student_from_contract(self, data: Dict) -> Student:
        try:
            return Student.objects.get(document=data["student_document_number"])
        except ObjectDoesNotExist:
            raise ValidationError(
                f"No se encontró un aprendices con el número de documento {data['student_document_number']}."
            )
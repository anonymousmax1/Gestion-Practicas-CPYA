from management.utils.validators import PracticesApplicationValidator


class StudentBasicViewModel:
    def __init__(
        self, document_type, document_number, name, last_name, cellphone, email, state
    ):
        self.document_type = document_type
        self.document_number = document_number
        self.name = name
        self.last_name = last_name
        self.cellphone = cellphone
        self.email = email
        self.state = state


class FormationStudentsViewModel:
    def __init__(self, formation_code, formation_name, students):
        self.formation_code = formation_code
        self.formation_name = formation_name
        self.students = students


class PracticesApplicationViewModel:
    def __init__(self, data) -> None:
        validator = PracticesApplicationValidator(data)
        errors = validator.validate()
        
        if errors:
            raise ValueError(errors)

        self.formation_code = data["formation_code"]
        self.formation_level = data["formation_level"]
        self.formation_name = data["formation_name"]
        self.student_name = data["student_name"]
        self.student_document_type = data["student_document_type"]
        self.student_document_number = data["student_document_number"]
        self.student_address = data["student_address"]
        self.student_neighborhood = data["student_neighborhood"]
        self.student_city = data["student_city"]
        self.student_cellphone = data["student_cellphone"]
        self.email_sena = data["email_sena"]
        self.contract_modality = data["contract_modality"]
        self.enterprise_name = data["enterprise_name"]
        self.enterprise_address = data["enterprise_address"]
        self.enterprise_neighborhood = data["enterprise_neighborhood"]
        self.enterprise_region = data["enterprise_region"]
        self.enterprise_city = data["enterprise_city"]
        self.enterprise_cellphone = data["enterprise_cellphone"]
        self.enterprise_phone = data["enterprise_phone"]
        self.enterprise_email = data["enterprise_email"]
        self.boss_name = data["boss_name"]
        self.practices_start_date = data["practices_start_date"]
        self.practices_end_date = data["practices_end_date"]
        self.enterprise_nit = data["enterprise_nit"]
        self.student_eps = data["student_eps"]
        self.student_arl = data["student_arl"]
        self.start_lective = data["start_lective"]
        self.end_lective = data["end_lective"]

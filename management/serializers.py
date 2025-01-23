from .viewmodels import (
    StudentBasicViewModel,
    FormationStudentsViewModel,
    PracticesApplicationViewModel,
)
from typing import Dict


def formation_to_dict(formation: FormationStudentsViewModel) -> Dict:
    return {
        "formation_code": formation.formation_code,
        "formation_name": formation.formation_name,
        "students": [student_to_dict(s) for s in formation.students],
    }


def student_to_dict(student: StudentBasicViewModel) -> Dict:
    return {
        "document_type": str(student.document_type),
        "document_number": student.document_number,
        "name": student.name,
        "last_name": student.last_name,
        "cellphone": student.cellphone,
        "email": student.email,
        "state": student.state,
    }


def dict_to_formation(data_dict: Dict) -> FormationStudentsViewModel:
    students_data = [
        StudentBasicViewModel(
            document_type=student["document_type"],
            document_number=student["document_number"],
            name=student["name"],
            last_name=student["last_name"],
            cellphone=student["cellphone"],
            email=student["email"],
            state=student["state"],
        )
        for student in data_dict.get("students", [])
    ]
    return FormationStudentsViewModel(
        formation_code=data_dict["formation_code"],
        formation_name=data_dict["formation_name"],
        students=students_data,
    )


def practices_application_to_dict(student_data: PracticesApplicationViewModel) -> Dict:
    return {
        "formation_code": student_data.formation_code,
        "formation_level": student_data.formation_level,
        "formation_name": student_data.formation_name,
        "student_name": student_data.student_name,
        "student_document_type": student_data.student_document_type,
        "student_document_number": student_data.student_document_number,
        "student_address": student_data.student_address,
        "student_neighborhood": student_data.student_neighborhood,
        "student_city": student_data.student_city,
        "student_cellphone": student_data.student_cellphone,
        "email_sena": student_data.email_sena,
        "contract_modality": student_data.contract_modality,
        "enterprise_name": student_data.enterprise_name,
        "enterprise_address": student_data.enterprise_address,
        "enterprise_neighborhood": student_data.enterprise_neighborhood,
        "enterprise_region": student_data.enterprise_region,
        "enterprise_city": student_data.enterprise_city,
        "enterprise_cellphone": student_data.enterprise_cellphone,
        "enterprise_phone": student_data.enterprise_phone,
        "enterprise_email": student_data.enterprise_email,
        "boss_name": student_data.boss_name,
        "practices_start_date": student_data.practices_start_date,
        "practices_end_date": student_data.practices_end_date,
        "enterprise_nit": student_data.enterprise_nit,
        "student_eps": student_data.student_eps,
        "student_arl": student_data.student_arl,
        "start_lective": student_data.start_lective,
        "end_lective": student_data.end_lective,
    }


def dict_to_practices_application(data_dict: Dict) -> PracticesApplicationViewModel:
    view_model = PracticesApplicationViewModel()

    view_model.formation_code = data_dict["formation_code"]
    view_model.formation_level = data_dict["formation_level"]
    view_model.formation_name = data_dict["formation_name"]
    view_model.student_name = data_dict["student_name"]
    view_model.student_document_type = data_dict["student_document_type"]
    view_model.student_document_number = data_dict["student_document_number"]
    view_model.student_address = data_dict["student_address"]
    view_model.student_neighborhood = data_dict["student_neighborhood"]
    view_model.student_city = data_dict["student_city"]
    view_model.student_cellphone = data_dict["student_cellphone"]
    view_model.email_sena = data_dict["email_sena"]
    view_model.contract_modality = data_dict["contract_modality"]
    view_model.enterprise_name = data_dict["enterprise_name"]
    view_model.enterprise_address = data_dict["enterprise_address"]
    view_model.enterprise_neighborhood = data_dict["enterprise_neighborhood"]
    view_model.enterprise_region = data_dict["enterprise_region"]
    view_model.enterprise_city = data_dict["enterprise_city"]
    view_model.enterprise_cellphone = data_dict["enterprise_cellphone"]
    view_model.enterprise_phone = data_dict["enterprise_phone"]
    view_model.enterprise_email = data_dict["enterprise_email"]
    view_model.boss_name = data_dict["boss_name"]
    view_model.practices_start_date = data_dict["practices_start_date"]
    view_model.practices_end_date = data_dict["practices_end_date"]
    view_model.enterprise_nit = data_dict["enterprise_nit"]
    view_model.student_eps = data_dict["student_eps"]
    view_model.student_arl = data_dict["student_arl"]
    view_model.start_lective = data_dict["start_lective"]
    view_model.end_lective = data_dict["end_lective"]

    return view_model

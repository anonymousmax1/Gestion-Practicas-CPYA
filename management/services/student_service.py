from management.models import Student, Formation, CustomUser
from management.values import DocumentTypesValues
from typing import List
from management.viewmodels import StudentBasicViewModel


def save_students(students: List[Student]):
    for student in students:
        student.save()


def student_converter(student: StudentBasicViewModel, formation: Formation) -> Student:
    new_student = Student()
    new_student.name = student.name
    new_student.last_name = student.last_name
    new_student.email = student.email
    new_student.cellphone = student.cellphone
    new_student.formation = formation
    new_student.document = student.document_number
    new_student.document_type = get_document_type(student.document_type)
    return new_student


def get_document_type(doc_type: str) -> DocumentTypesValues:
    values = {
        "CC": DocumentTypesValues.CC.value,
        "TI": DocumentTypesValues.TI.value,
        "PEP": DocumentTypesValues.PEP.value,
    }
    return values.get(doc_type)


def get_instructor_by_student_document(document: str) -> CustomUser | None:
        return CustomUser.objects.filter(students__document=document).first()

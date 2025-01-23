from modeltranslation.translator import translator, TranslationOptions
from .models import CustomUser, Formation, Student, ContractInfo, Advancement


# Traducción para el modelo CustomUser
class CustomUserTranslationOptions(TranslationOptions):
    fields = ("email", "first_name", "last_name", "cellphone", "password")


# Traducción para el modelo Formation
class FormationTranslationOptions(TranslationOptions):
    fields = ("name", "code", "start_date", "end_date")


# Traducción para el modelo Student
class StudentTranslationOptions(TranslationOptions):
    fields = (
        "document_type",
        "document",
        "name",
        "last_name",
        "email",
        "email_sena",
        "cellphone",
        "city",
        "address",
        "neighborhood",
        "formation",
        "state",
        "instructor",
    )


# Traducción para el modelo ContractInfo
class ContractInfoTranslationOptions(TranslationOptions):
    fields = (
        "contract_type",
        "student",
        "enterprise_name",
        "enterprise_address",
        "enterprise_neighborhood",
        "enterprise_region",
        "enterprise_city",
        "enterprise_cellphone",
        "enterprise_phone",
        "enterprise_email",
        "boss_name",
        "practices_start_date",
        "practices_end_date",
        "enterprise_nit",
        "student_eps",
        "student_arl",
    )


# Traducción para el modelo Advancement
class AdvancementTranslationOptions(TranslationOptions):
    fields = ("student", "binnacle", "has_partial", "has_final", "has_concertation")


# Registrar las opciones de traducción
translator.register(CustomUser, CustomUserTranslationOptions)
translator.register(Formation, FormationTranslationOptions)
translator.register(Student, StudentTranslationOptions)
translator.register(ContractInfo, ContractInfoTranslationOptions)
translator.register(Advancement, AdvancementTranslationOptions)

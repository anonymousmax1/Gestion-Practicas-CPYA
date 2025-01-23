from django.db import models
from django.utils.translation import gettext_lazy as _


class StateValues(models.TextChoices):
    NO_CONTRACT = "1", _("No Contract")
    IN_TRACKING = "2", _("In Tracking")
    NO_TRACKING = "3", _("No Tracking")
    EVALUATED = "4", _("Evaluated")
    CANCELED = "5", _("Cancelled")


class RoleValues(models.TextChoices):
    MANAGER = "1", _("Administrator")
    INSTRUCTOR = "2", _("Instructor")


class DocumentTypesValues(models.TextChoices):
    CC = "1", _("Citizenship Card")
    TI = "2", _("Identity Card")
    PEP = "3", _("Special Permit to Stay")


class ContractTypeValues(models.TextChoices):
    LEARNING_CONTRACT = "1", _("Apprenticeship Contract")
    INTERNSHIP = "2", _("Internship")
    EMPLOYMENT = "3", _("Employment Relationship")
    PRODUCTIVE_PROJECT = "4", _("Productive Project")

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from .values import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from management.utils.validators import (
    validate_document,
    validate_name_contains_letter,
    validate_code_length,
)


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    cellphone = models.CharField(max_length=17, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.email}"


class Formation(models.Model):
    code = models.CharField(
        unique=True, max_length=8, validators=[validate_code_length]
    )
    name = models.CharField(max_length=100, validators=[validate_name_contains_letter])
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(
                {
                    "end_date": "La fecha de finalización no puede ser anterior a la fecha de inicio."
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Student(models.Model):
    document_type = models.CharField(
        max_length=2, choices=DocumentTypesValues, default=DocumentTypesValues.CC.value
    )
    document = models.CharField(
        unique=True,
        max_length=15,
        validators=[validate_document],
    )
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    email_sena = models.EmailField(blank=True, null=True, max_length=100)
    cellphone = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    address = models.CharField(blank=True, null=True, max_length=100)
    neighborhood = models.CharField(blank=True, null=True, max_length=100)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2, choices=StateValues, default=StateValues.NO_CONTRACT.value
    )
    instructor = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="students",
    )

    @property
    def state_display(self):
        return dict(StateValues.choices).get(self.state, _("No State"))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not hasattr(self, "advancement"):
            Advancement.objects.create(student=self)

    def __str__(self) -> str:
        return f"{self.name.title()} {self.last_name.title()}"


class ContractInfo(models.Model):
    contract_type = models.CharField(
        max_length=2,
        choices=ContractTypeValues,
        default=ContractTypeValues.LEARNING_CONTRACT.value,
    )
    student = models.OneToOneField(Student, models.CASCADE, related_name="contract")
    enterprise_name = models.CharField(max_length=100)
    enterprise_address = models.CharField(max_length=100)
    enterprise_neighborhood = models.CharField(max_length=100)
    enterprise_region = models.CharField(max_length=100)
    enterprise_city = models.CharField(max_length=100)
    enterprise_cellphone = models.CharField(max_length=100)
    enterprise_phone = models.CharField(max_length=100)
    enterprise_email = models.EmailField()
    boss_name = models.CharField(max_length=100)
    practices_start_date = models.DateField()
    practices_end_date = models.DateField()
    enterprise_nit = models.CharField(max_length=100)
    student_eps = models.CharField(max_length=100)
    student_arl = models.CharField(max_length=100)


class Advancement(models.Model):
    student = models.OneToOneField(Student, models.CASCADE, related_name="advancement")
    binnacle = models.PositiveIntegerField(default=0)
    has_partial = models.BooleanField(default=False)
    has_final = models.BooleanField(default=False)
    has_concertation = models.BooleanField(default=False)

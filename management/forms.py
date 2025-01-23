from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelChoiceField, DateField, FileField
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from .models import CustomUser, Student, ContractInfo, Formation, Advancement
from management.utils.validators import (
    validate_code_length,
    validate_excel_file,
    validate_name_contains_letter,
)
from management.utils.translators import translate_form_fields
from django.contrib.auth.models import Group
from management.values import StateValues
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label=_("Groups"),
        help_text=_("Select the groups to which the user belongs."),
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "cellphone",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email is already in use."))
        return email


class CustomUserUpdateForm(UserChangeForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label=_("Groups"),
        help_text=_("Select the groups to which the user belongs."),
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "cellphone", "groups"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)
        self.fields.pop("password", None)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("Este correo electrónico ya está en uso."))
        return email


class LoadExcelFileForm(forms.Form):
    file = FileField(
        label=_("Select the file with the formation data"),
        validators=[validate_excel_file],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)


class SubmitFormationForm(forms.Form):
    start_date = DateField(
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={"type": "date"},
        ),
        label=_("Start date"),
    )
    end_date = DateField(
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={"type": "date"},
        ),
        label=_("End date"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                self.add_error(
                    "end_date", _("The end date cannot be earlier than the start date.")
                )

        return cleaned_data


class ContractInfoForm(forms.ModelForm):
    class Meta:
        model = ContractInfo
        fields = [
            "contract_type",
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
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)


class StudentContractSubmitForm(forms.Form):
    instructor = ModelChoiceField(
        queryset=CustomUser.objects.filter(groups__name="Instructor", is_active=True),
        empty_label=_("Ninguno"),
        required=False,
        label=_("Instructor"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"))
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "password-input", "id": "password-field"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)


class FilterStudentsListForm(forms.Form):
    formation = forms.ModelChoiceField(
        queryset=Formation.objects.all(),
        empty_label="",
        required=False,
        label=_("Formation"),
    )

    state = forms.ChoiceField(
        choices=[("", "")] + StateValues.choices,
        required=False,
        label=_("State"),
    )

    search = forms.CharField(
        required=False,
        label=_("Name or Document"),
        widget=forms.TextInput(attrs={"placeholder": _("Enter name or document")}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)


class FilterFormationsListForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=_("Search"),
        widget=forms.TextInput(attrs={"placeholder": _("Enter code or name")}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "document_type",
            "document",
            "name",
            "last_name",
            "email",
            "cellphone",
            "formation",
        ]
        widgets = {
            "state": forms.Select(),
            "formation": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "document_type",
            "name",
            "last_name",
            "email",
            "email_sena",
            "cellphone",
            "city",
            "address",
            "neighborhood",
            "instructor",
        ]
        widgets = {
            "formation": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)
        self.fields["instructor"].queryset = CustomUser.objects.filter(
            groups__name="Instructor", is_active=True
        )
        if self.instance.state in [
            StateValues.NO_CONTRACT.value,
            StateValues.CANCELED.value,
            StateValues.EVALUATED.value,
        ]:
            self.fields["instructor"].disabled = True

    def clean_instructor(self):
        instructor = self.cleaned_data.get("instructor")
        state = self.instance.state

        if state in [
            StateValues.NO_CONTRACT.value,
            StateValues.CANCELED.value,
            StateValues.EVALUATED.value,
        ]:
            if instructor:
                raise ValidationError(
                    _(
                        "No se puede asignar un instructor de seguimiento cuando el estado es 'Sin Contrato', 'Cancelado' o 'Evaluado'."
                    )
                )
        return instructor

    def clean(self):
        cleaned_data = super().clean()
        instructor = cleaned_data.get("instructor")

        if not instructor:
            self.instance.state = StateValues.NO_TRACKING.value
        else:
            self.instance.state = StateValues.IN_TRACKING.value

        return cleaned_data


class AdvancementForm(forms.ModelForm):
    class Meta:
        model = Advancement
        fields = [
            "binnacle",
            "has_concertation",
            "has_partial",
            "has_final",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)


class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ["code", "name", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "end_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }

    code = forms.CharField(
        label=_("Code"),
        help_text=_("Enter the formation code"),
        validators=[validate_code_length],
        max_length=7,
        widget=forms.NumberInput(attrs={"placeholder": _("Enter 7 digits")}),
    )

    name = forms.CharField(
        label=_("Name"),
        help_text=_("Enter the formation name"),
        validators=[validate_name_contains_letter],
        widget=forms.TextInput(attrs={"placeholder": _("Enter formation's name")}),
    )

    def clean_code(self):
        code = self.cleaned_data.get("code")
        instance = getattr(self, "instance", None)

        if Formation.objects.filter(code=code).exclude(pk=instance.pk).exists():
            raise ValidationError(
                _("A formation with this code already exists.")
            )

        return code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        translate_form_fields(self)

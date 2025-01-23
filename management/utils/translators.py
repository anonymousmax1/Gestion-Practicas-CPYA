from django.utils.translation import gettext_lazy as _
from django.forms import ModelChoiceField


def translate_form_fields(form):
    for field in form.fields.values():
        if field.label:
            field.label = _(field.label)
        if field.help_text:
            field.help_text = _(field.help_text)
        if isinstance(field, ModelChoiceField):
            if field.empty_label:
                field.empty_label = _(field.empty_label)

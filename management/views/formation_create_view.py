from management.mixins import GroupRequiredMixin
from management.models import Formation
from management.forms import FormationForm
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError


class FormationCreateView(GroupRequiredMixin, CreateView):
    model = Formation
    form_class = FormationForm
    template_name = "formation_create.html"
    group_required = "Administrador"
    redirect_url = "formation_list"

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            if "code" in str(e):
                messages.error(
                    self.request,
                    "El código de formación debe ser único. Ya existe un código con ese valor.",
                )
            else:
                messages.error(self.request, "Hubo un error al crear la formación.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Hubo un error al crear la formación. Por favor, revisa los campos.",
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return self.request.path

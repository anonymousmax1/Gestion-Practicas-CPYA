from management.mixins import GroupRequiredMixin
from management.models import Formation
from management.forms import FormationForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib import messages


class FormationUpdateView(GroupRequiredMixin, UpdateView):
    model = Formation
    form_class = FormationForm
    template_name = "formation_update.html"
    group_required = "Administrador"
    redirect_url = "formation_detail"

    def get_success_url(self):
        return reverse_lazy("formation_detail", kwargs={"pk": self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        print(form["start_date"].value())
        print(form["end_date"].value())
        return form

    def form_valid(self, form):
        messages.success(
            self.request,
            f"La formación '{form.instance.name}' ha sido actualizada con éxito.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Hubo un error al actualizar la formación. Por favor, revisa los campos.",
        )
        return super().form_invalid(form)

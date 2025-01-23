from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse
from management.mixins import GroupRequiredMixin
from management.models import Student
from management.forms import StudentUpdateForm


class StudentUpdateView(GroupRequiredMixin, UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = "student_update.html"
    group_required = "Administrador"
    redirect_url = "student_detail"

    def get_success_url(self):
        return reverse("student_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Los datos se han actualizado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Hubo un error al actualizar los datos del aprendiz."
        )
        return super().form_invalid(form)

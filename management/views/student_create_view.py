from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from management.mixins import GroupRequiredMixin
from management.models import Student
from management.forms import StudentCreateForm


class StudentCreateView(GroupRequiredMixin, CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = "student_create.html"
    success_url = reverse_lazy("student_list")
    group_required = "Administrador"
    redirect_url = "student_list"
    send_args = False

    def form_valid(self, form):
        return super().form_valid(form)

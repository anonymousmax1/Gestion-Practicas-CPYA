from django.views.generic import DetailView
from management.models import Student
from django.contrib.auth.mixins import LoginRequiredMixin


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "student_details.html"
    context_object_name = "student"

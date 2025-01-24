from django.views.generic import ListView
from management.models import Student
from management.forms import FilterStudentsListForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students_show.html"
    context_object_name = "students"
    paginate_by = 30

    def get_queryset(self):
        queryset = Student.objects.all().order_by('formation__name', 'name')

        if self.request.user.groups.filter(name="Instructor").exists() and not self.request.user.groups.filter(name="Administrador").exists():
            queryset = queryset.filter(instructor=self.request.user)

        form = FilterStudentsListForm(self.request.GET)

        if form.is_valid():
            formation = form.cleaned_data.get("formation")
            state = form.cleaned_data.get("state")
            search = form.cleaned_data.get("search")

            if formation:
                queryset = queryset.filter(formation=formation)
            if state:
                queryset = queryset.filter(state=state)
            if search:
                queryset = queryset.filter(
                    models.Q(name__icontains=search) | models.Q(document__icontains=search)
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["form"] = FilterStudentsListForm(self.request.GET)
        context["student_count"] = queryset.count()
        context["formation_count"] = queryset.values("formation").distinct().count()
        return context

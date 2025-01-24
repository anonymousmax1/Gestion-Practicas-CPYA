from management.models import Formation
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from management.forms import FilterFormationsListForm
from django.db import models

class FormationListView(LoginRequiredMixin, ListView):
    model = Formation
    template_name = "formation_show.html"
    context_object_name = "formations"
    paginate_by = 30

    def get_queryset(self):
        queryset = Formation.objects.all().order_by("name")
        form = FilterFormationsListForm(self.request.GET)

        if self.request.user.groups.filter(name="Instructor").exists() and not self.request.user.groups.filter(name="Administrador").exists():
            queryset = queryset.filter(student__instructor=self.request.user)

        if form.is_valid():
            search = form.cleaned_data.get("search")

            if search:
                queryset = queryset.filter(
                    models.Q(code__icontains=search) | models.Q(name__icontains=search)
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["form"] = FilterFormationsListForm(self.request.GET)
        context["formations_count"] = queryset.count()
        return context

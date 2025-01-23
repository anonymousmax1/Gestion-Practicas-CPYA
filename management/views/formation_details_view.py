from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from management.models import Formation, Student
from django.views import View
from management.services.formation_service import get_formation_stats

class FormationDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        formation = get_object_or_404(Formation, pk=pk)
        students = Student.objects.filter(formation=formation)

        state_stats, total_students = get_formation_stats(formation)

        context = {
            "formation": formation,
            "students": students,
            "state_stats": sorted(state_stats, key=lambda x: x["state"]),
            "total_students": total_students,
        }

        return render(request, "formation_details.html", context)

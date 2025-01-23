from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from management.mixins import GroupRequiredMixin
from management.models import Formation
from django.http import Http404
from management.services.formation_service import get_formation_stats


class FormationDeleteView(GroupRequiredMixin, View):
    template_name = "formation_delete.html"
    group_required = "Administrador"
    redirect_url = "formation_detail"
    send_args = False

    def get(self, request, pk):
        try:
            formation = get_object_or_404(Formation, pk=pk)
            state_stats, total_students = get_formation_stats(pk)
        except Formation.DoesNotExist:
            raise Http404("La formación no existe.")

        return render(
            request,
            self.template_name,
            {
                "formation": formation,
                "state_stats": sorted(state_stats, key=lambda x: x["state"]),
                "total_students": total_students,
            },
        )

    def post(self, request, pk):
        formation = get_object_or_404(Formation, pk=pk)
        confirm = request.POST.get("confirm_delete")

        if confirm == "on":
            formation.delete()
            messages.success(
                request,
                f"La formación '{formation.code} - {formation.name}' ha sido eliminada.",
            )
            return redirect("formation_list")
        else:
            messages.error(request, "Debe confirmar la eliminación de la formación.")
            return redirect("formation_delete", pk=pk)

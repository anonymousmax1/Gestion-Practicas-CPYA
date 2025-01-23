# views.py
from django.shortcuts import redirect, render
from django.views import View
from management.mixins import GroupRequiredMixin
from management.models import Student, Advancement
from management.forms import AdvancementForm
from management.values import StateValues
from django.contrib import messages


class StudentAdvancementView(GroupRequiredMixin, View):
    group_required = ["Administrador", "Instructor"]
    redirect_url = "student_detail"
    template_name = "student_advancement.html"

    def get(self, request, pk):
        try:
            student = Student.objects.get(
                id=pk,
                state__in=[
                    StateValues.IN_TRACKING.value,
                    StateValues.NO_TRACKING.value,
                    StateValues.EVALUATED.value,
                ],
            )
        except Student.DoesNotExist:
            messages.error(
                request,
                "El estudiante no existe o no está en un estado válido para ver los avances.",
            )
            return redirect("student_detail", pk=pk)

        advancement, created = Advancement.objects.get_or_create(student=student)

        form = AdvancementForm(instance=advancement)
        return render(request, self.template_name, {"form": form, "student": student})

    def post(self, request, pk):
        action = request.POST.get("action")
        try:
            student = Student.objects.get(
                id=pk,
                state__in=[
                    StateValues.IN_TRACKING.value,
                    StateValues.NO_TRACKING.value,
                    StateValues.EVALUATED.value,
                ],
            )
        except Student.DoesNotExist:
            messages.error(
                request,
                "El estudiante no existe o no está en un estado válido para ver los avances.",
            )
            return redirect("student_detail", pk=pk)

        if action == "set_to_evaluated":
            student.state = StateValues.EVALUATED.value
            student.save()
            messages.success(request, "El estudiante ha sido marcado como evaluado.")
            return redirect("student_detail", pk=pk)

        advancement, created = Advancement.objects.get_or_create(student=student)
        form = AdvancementForm(request.POST, instance=advancement)

        if form.is_valid():
            form.save()
            messages.success(request, "Los avances del estudiante han sido actualizados.")
            return redirect("student_detail", pk=pk)
        else:
            messages.error(request, "Por favor corrige los errores a continuación.")
            return render(request, self.template_name, {"form": form, "student": student})

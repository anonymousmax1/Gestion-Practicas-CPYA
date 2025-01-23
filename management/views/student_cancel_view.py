from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from management.mixins import GroupRequiredMixin
from management.models import Student
from management.values import StateValues

class StudentCancelView(GroupRequiredMixin, View):
    template_name = "student_cancel.html"
    group_required = "Administrador"
    redirect_url = "student_detail"

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return render(request, self.template_name, {"student": student})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        confirm = request.POST.get("confirm_cancel")

        if confirm == "on":
            student.state = StateValues.CANCELED.value
            student.instructor = None
            student.save()
            messages.success(request, f"El estado del aprendiz '{student.name} {student.last_name}' ha sido cambiado a 'Cancelado'.")
            return redirect("student_detail", pk=pk)
        else:
            messages.error(request, "Debe confirmar la cancelación de la matrícula del aprendiz.")
            return redirect("student_cancel", pk=pk)
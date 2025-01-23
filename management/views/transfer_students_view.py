from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from management.mixins import GroupRequiredMixin
from management.models import Student, Formation, CustomUser
from django.contrib import messages
from management.values import StateValues

class TransferStudentsView(GroupRequiredMixin, View):
    template_name = "transfer_students.html"
    group_required = "Administrador"
    redirect_url = "student_list"
    send_args = False

    def get(self, request):
        context = {
            'formations': Formation.objects.all(),
            'all_instructors': CustomUser.objects.filter(groups__name="Instructor")
        }

        formation_filter = request.GET.get('formation')
        source_instructor_filter = request.GET.get('source_instructor')

        students_query = Student.objects.filter(state__in=[StateValues.IN_TRACKING.value, StateValues.NO_TRACKING.value])

        if source_instructor_filter:
            if source_instructor_filter == "none":
                students_query = students_query.filter(instructor__isnull=True)
                context['instructor'] = None
            else:
                students_query = students_query.filter(instructor_id=source_instructor_filter)
                context['instructor'] = get_object_or_404(CustomUser, pk=source_instructor_filter)
        context['instructors'] = context['all_instructors']

        if formation_filter:
            students_query = students_query.filter(formation_id=formation_filter)

        context['students'] = students_query

        return render(request, self.template_name, context)

    def post(self, request):
        selected_students = request.POST.getlist('selected_students')
        new_instructor_id = request.POST.get('new_instructor')

        if not selected_students:
            messages.error(request, "No has seleccionado ningún estudiante.")
            return redirect('transfer_students')

        if not new_instructor_id:
            messages.error(request, "No has seleccionado un instructor destino.")
            return redirect('transfer_students')

        new_instructor = get_object_or_404(CustomUser, pk=new_instructor_id)

        for student_id in selected_students:
            student = get_object_or_404(Student, pk=student_id)
            if student.state not in [StateValues.IN_TRACKING.value, StateValues.NO_TRACKING.value]:
                messages.error(request, f"El estudiante {student.name} {student.last_name} no está en un estado transferible.")
                continue
            student.instructor = new_instructor
            student.save()

        messages.success(request, "Los estudiantes han sido transferidos exitosamente.")
        return redirect('transfer_students')
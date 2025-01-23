from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from management.models import Student, Formation, CustomUser
from django.db import models
from management.values import StateValues

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        total_students = Student.objects.count()
        total_formations = Formation.objects.count()
        students_by_state = Student.objects.values('state').annotate(count=models.Count('state'))
        students_by_state_labels = [StateValues(item['state']).label for item in students_by_state]
        students_by_state_counts = [item['count'] for item in students_by_state]

        students_in_tracking = Student.objects.filter(state=StateValues.IN_TRACKING.value).count()
        students_no_tracking = Student.objects.filter(state=StateValues.NO_TRACKING.value).count()
        students_evaluated = Student.objects.filter(state=StateValues.EVALUATED.value).count()
        students_canceled = Student.objects.filter(state=StateValues.CANCELED.value).count()

        formations = Formation.objects.all()
        formation_labels = []
        in_tracking_counts = []
        no_tracking_counts = []
        evaluated_counts = []
        canceled_counts = []

        for formation in formations:
            formation_labels.append(formation.name)
            in_tracking_counts.append(Student.objects.filter(formation=formation, state=StateValues.IN_TRACKING.value).count())
            no_tracking_counts.append(Student.objects.filter(formation=formation, state=StateValues.NO_TRACKING.value).count())
            evaluated_counts.append(Student.objects.filter(formation=formation, state=StateValues.EVALUATED.value).count())
            canceled_counts.append(Student.objects.filter(formation=formation, state=StateValues.CANCELED.value).count())

        instructors = CustomUser.objects.filter(groups__name="Instructor")
        instructor_labels = [instructor.get_full_name() for instructor in instructors]
        instructor_student_counts = [Student.objects.filter(instructor=instructor).count() for instructor in instructors]

        context = {
            'total_students': total_students,
            'total_formations': total_formations,
            'students_by_state_labels': students_by_state_labels,
            'students_by_state_counts': students_by_state_counts,
            'students_in_tracking': students_in_tracking,
            'students_no_tracking': students_no_tracking,
            'students_evaluated': students_evaluated,
            'students_canceled': students_canceled,
            'formation_labels': formation_labels,
            'in_tracking_counts': in_tracking_counts,
            'no_tracking_counts': no_tracking_counts,
            'evaluated_counts': evaluated_counts,
            'canceled_counts': canceled_counts,
            'instructor_labels': instructor_labels,
            'instructor_student_counts': instructor_student_counts,
        }

        return render(request, 'dashboard.html', context)
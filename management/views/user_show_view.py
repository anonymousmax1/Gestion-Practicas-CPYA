from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin


class UserListView(LoginRequiredMixin, View):
    template_name = "user_show.html"

    def get(self, request):
        instructor_group = Group.objects.get(name="Instructor")
        admin_group = Group.objects.get(name="Administrador")

        instructors = instructor_group.user_set.all()
        administrators = admin_group.user_set.all()

        is_admin = request.user.groups.filter(name="Administrador").exists()

        context = {
            "instructors": instructors,
            "instructors_count": instructors.count(),
            "administrators": administrators,
            "administrators_count": administrators.count(),
            "is_admin": is_admin,
        }
        return render(request, self.template_name, context)

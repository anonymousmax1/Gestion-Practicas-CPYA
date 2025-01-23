from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from management.models import CustomUser, Student
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, View):
    template_name = "profile.html"

    def get(self, request, pk=None):
        if pk is None:
            user = request.user
        else:
            try:
                user = CustomUser.objects.get(pk=pk)
            except CustomUser.DoesNotExist:
                messages.error(request, "El usuario no existe.")
                return redirect("user_list")

        is_instructor = user.groups.filter(name="Instructor").exists()

        context = {"user": user, "is_instructor": is_instructor, "own_profile": pk == request.user.id}

        if is_instructor:
            students = Student.objects.filter(instructor=user)
            paginator = Paginator(students, 30)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            context.update(
                {
                    "students": page_obj,
                    "students_count": students.count(),
                }
            )

        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        action = request.POST.get("action")

        if user.students.exists():
            messages.error(
                request,
                "No se puede desactivar o eliminar un usuario que tiene aprendices a cargo.",
            )
            return redirect("profile", pk=pk)

        if action == "deactivate" and request.user.id != pk:
            user.is_active = False
            user.save()
            messages.success(
                request,
                f"El usuario '{user.first_name} {user.last_name}' ha sido desactivado.",
            )
        elif action == "activate":
            user.is_active = True
            user.save()
            messages.success(
                request,
                f"El usuario '{user.first_name} {user.last_name}' ha sido activado.",
            )
        elif action == "delete" and request.user.id != pk:
            user.delete()
            messages.success(
                request,
                f"El usuario '{user.first_name} {user.last_name}' ha sido eliminado.",
            )
            return redirect("user_list")

        return redirect("profile", pk=pk)

from management.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from management.mixins import GroupRequiredMixin


class ChangePasswordView(GroupRequiredMixin, View):
    group_required = ["Administrador", "Instructor"]
    redirect_url = "profile"
    template_name = "change_password.html"

    def get(self, request, pk=None):
        if pk:
            if (
                not request.user.groups.filter(name="Administrador").exists()
                and request.user.id != pk
            ):
                messages.error(
                    request,
                    "No tienes permiso para cambiar la contraseña de otro usuario.",
                )
                return redirect(self.redirect_url, pk=pk if pk else user.id)
            user = get_object_or_404(CustomUser, pk=pk)
            form = SetPasswordForm(user)
        else:
            user = request.user
            form = PasswordChangeForm(user)

        return render(request, self.template_name, {"form": form, "pk": pk})

    def post(self, request, pk=None):
        if pk:
            user = get_object_or_404(CustomUser, pk=pk)
            form = SetPasswordForm(user, request.POST)
        else:
            user = request.user
            form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "La contraseña ha sido cambiada exitosamente.")
            return redirect(self.redirect_url, pk=pk if pk else user.id)
        else:
            messages.error(request, "Por favor corrige los errores a continuación.")
            return render(request, self.template_name, {"form": form, "pk": pk})

from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from management.models import CustomUser
from management.forms import CustomUserUpdateForm
from django.shortcuts import get_object_or_404, redirect


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "user_update.html"

    def dispatch(self, request, *args, **kwargs):
        user_id = self.kwargs.get("pk")
        if user_id:
            if (
                not request.user.groups.filter(name="Administrador").exists()
                and request.user.id != user_id
            ):
                messages.error(
                    request,
                    "No tienes permiso para actualizar la información de este usuario.",
                )
                return redirect("profile", pk=user_id)
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.groups.filter(name="Administrador").exists():
            form.fields.pop("groups")
        return form

    def get_object(self, queryset=None):
        user_id = self.kwargs.get("pk")
        if user_id:
            return get_object_or_404(CustomUser, pk=user_id)
        return self.request.user

    def get_success_url(self):
        return reverse("profile", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(
            self.request, "Los datos del usuario se han actualizado correctamente."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Hubo un error al actualizar los datos del usuario."
        )
        return super().form_invalid(form)

from management.mixins import GroupRequiredMixin
from management.forms import CustomUserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group


class AddUserView(GroupRequiredMixin, CreateView):
    template_name = "user_add.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("user_create")
    group_required = "Administrador"
    redirect_url = "user_list"
    send_args = False

    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            user.is_staff = (
                form.cleaned_data["groups"].filter(name="Administrador").exists()
            )
            user.is_superuser = False
            user.username = form.cleaned_data["email"]
            user.save()

            user.groups.set(form.cleaned_data["groups"])
            messages.success(self.request, "El usuario se creó exitosamente.")
        except Group.DoesNotExist:
            messages.error(self.request, "Uno o más grupos seleccionados no existen.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Hubo un error al crear el usuario. Por favor, verifica los datos ingresados.",
        )
        return super().form_invalid(form)

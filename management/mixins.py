from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

class GroupRequiredMixin(LoginRequiredMixin):
    group_required = None
    redirect_url = "student_list"
    redirect_kwargs = None
    send_args = True

    def dispatch(self, request, *args, **kwargs):
        self.redirect_kwargs = kwargs  # Store kwargs for redirection
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if isinstance(self.group_required, (list, tuple)):
            grupos_usuario = request.user.groups.values_list("name", flat=True)
            if not any(group in grupos_usuario for group in self.group_required):
                return self.handle_no_permission()
        elif isinstance(self.group_required, str):
            if not request.user.groups.filter(name=self.group_required).exists():
                return self.handle_no_permission()
        else:
            raise ValueError(
                "El atributo 'group_required' debe ser un str, list o tuple."
            )

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        redirect_url = self.redirect_url
        if self.send_args and self.redirect_kwargs:
            redirect_url = reverse_lazy(self.redirect_url, kwargs=self.redirect_kwargs)
        query_params = self.request.GET.urlencode()
        if query_params:
            redirect_url = f"{redirect_url}?{query_params}"
        return redirect(redirect_url)

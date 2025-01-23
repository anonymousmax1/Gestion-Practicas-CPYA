from django.shortcuts import redirect, render
from django.views import View
from management.forms import EmailAuthenticationForm
from management.services.authentication_service import AuthenticationService


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", context={"form": EmailAuthenticationForm()})

    def post(self, request):
        form = EmailAuthenticationForm(request, data=request.POST)

        if not form.is_valid():
            return render(request, "login.html", context={"form": form})

        email = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        AuthenticationService.login(request, email, password)

        return redirect(request.GET.get("next", "student_list"))

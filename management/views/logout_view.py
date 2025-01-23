from django.shortcuts import redirect
from django.views import View
from management.services.authentication_service import AuthenticationService


class LogoutView(View):
    def get(self, request):
        AuthenticationService.logout_user(request)
        return redirect("login")
    
    def post(self, request):
        AuthenticationService.logout_user(request)
        return redirect("login")
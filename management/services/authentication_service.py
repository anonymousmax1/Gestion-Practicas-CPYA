from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from management.utils.exceptions import InvalidCredentialsError


class AuthenticationService:
    def login(request: HttpRequest, email: str, password: str):
        user = authenticate(request, email=email, password=password)

        if user is None:
            raise InvalidCredentialsError()

        login(request, user)

    def logout_user(request: HttpRequest):
        logout(request)

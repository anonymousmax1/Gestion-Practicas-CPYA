from django.contrib import admin
from django.urls import path
from management.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("", StudentListView.as_view(), name="none"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("load_formation/", LoadFormationFileView.as_view(), name="load_formation"),
    path(
        "submit_formation_data/",
        SubmitFormationDataView.as_view(),
        name="submit_formation_data",
    ),
    path("load_contract/", LoadContractFileView.as_view(), name="load_contract_file"),
    path(
        "submit_contract_data/",
        SubmitContractDataView.as_view(),
        name="submit_contract_data",
    ),
    path("students/", StudentListView.as_view(), name="student_list"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student_detail"),
    path("students/create/", StudentCreateView.as_view(), name="student_create"),
    path(
        "students/update/<int:pk>/", StudentUpdateView.as_view(), name="student_update"
    ),
    path(
        "students/<int:pk>/advancement/",
        StudentAdvancementView.as_view(),
        name="student_advancement",
    ),
    path(
        "students/cancel/<int:pk>/", StudentCancelView.as_view(), name="student_cancel"
    ),
    path("users/create/", AddUserView.as_view(), name="user_create"),
    path("users/update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("formations/", FormationListView.as_view(), name="formation_list"),
    path("formations/create/", FormationCreateView.as_view(), name="formation_create"),
    path(
        "formations/<int:pk>/update/",
        FormationUpdateView.as_view(),
        name="formation_update",
    ),
    path(
        "formations/<int:pk>/",
        FormationDetailView.as_view(),
        name="formation_detail",
    ),
    path(
        "formations/<int:pk>/delete/",
        FormationDeleteView.as_view(),
        name="formation_delete",
    ),
    path(
        "transfer_students/",
        TransferStudentsView.as_view(),
        name="transfer_students",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path(
        "change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="change_user_password",
    ),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
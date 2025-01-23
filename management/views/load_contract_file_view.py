from django.shortcuts import render, redirect
from django.views import View
from management.mixins import GroupRequiredMixin
from management.forms import LoadExcelFileForm
from management.services.excel_handler import excel_file_handler
from management.enums import ExcelTypes
from django.contrib import messages


class LoadContractFileView(GroupRequiredMixin, View):
    group_required = "Administrador"
    redirect_url = "student_list"
    send_args = False

    def get(self, request):
        self.clear_session_data(request, "excel_formation_data")
        return self.render_initial_view(request)

    def post(self, request):
        if "upload_file" in request.POST:
            return self.handle_file_upload(request)
        return self.render_initial_view(request)

    def handle_file_upload(self, request):
        form = LoadExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            try:
                contract_data = excel_file_handler(file, ExcelTypes.STUDENT_CONTRACT)
                request.session["excel_formation_data"] = contract_data
                return redirect("submit_contract_data")
            except Exception as e:
                messages.error(request, str(e))
                self.clear_session_data(request, "excel_formation_data")

        return self.render_initial_view(request, form)

    def render_initial_view(self, request, form=None):
        form = form or LoadExcelFileForm()
        return render(request, "load_contract_file.html", {"form": form})

    def clear_session_data(self, request, key_name):
        if key_name in request.session:
            del request.session[key_name]

from management.mixins import GroupRequiredMixin
from management.forms import StudentContractSubmitForm
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from management.services.contract_service import ContractService
from management.services import student_service


class SubmitContractDataView(GroupRequiredMixin, View):
    group_required = "Administrador"
    redirect_url = "student_list"
    send_args = False

    def get(self, request):
        data_dict = request.session.get("excel_formation_data", None)
        if not data_dict:
            messages.error(
                request, "No se puede acceder a esta página sin datos cargados."
            )
            return redirect("load_contract_file")

        submit_form = StudentContractSubmitForm(
            initial={
                "instructor": student_service.get_instructor_by_student_document(
                    str(data_dict["student_document_number"])
                )
            }
        )

        context = {
            "data": data_dict,
            "submit_form": submit_form,
        }
        return render(request, "submit_contract_data.html", context)

    def post(self, request):
        data_dict = request.session.get("excel_formation_data", {})
        submit_form = StudentContractSubmitForm(request.POST)

        if not submit_form.is_valid():
            messages.error(request, "Ocurrió un error.")
            return self.render_submit_view(request, data_dict, submit_form)

        if not data_dict:
            messages.error(request, "Ocurrió un error inesperado al leer los datos.")
            return redirect("load_contract_file")

        try:
            instructor = submit_form.cleaned_data.get("instructor")
            ContractService().create_contract_handler(data_dict, instructor)
            self.clear_session_data(request, "excel_formation_data")
            messages.success(request, "Contrato creado exitosamente.")
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
        except Exception as e:
            messages.error(request, f"Error al guardar los datos: {str(e)}")
        finally:
            return redirect("load_contract_file")

    def render_submit_form(self, request, submit_form):
        return render(
            request, "submit_contract_data.html", {"submit_form": submit_form}
        )

    def clear_session_data(self, request, key_name):
        if key_name in request.session:
            del request.session[key_name]

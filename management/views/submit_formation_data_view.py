from django.core.exceptions import ValidationError
from django.views import View
from management.mixins import GroupRequiredMixin
from management.services import formation_student_handler
from management.forms import SubmitFormationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from management.services import formation_student_handler
from management.serializers import dict_to_formation


class SubmitFormationDataView(GroupRequiredMixin, View):
    group_required = "Administrador"
    redirect_url = "formation_list"
    send_args = False

    def get(self, request):
        formation_data = request.session.get("excel_student_data", None)
        if not formation_data:
            messages.error(
                request, "No se puede acceder a esta página sin datos cargados."
            )
            return redirect("load_formation")

        submit_form = SubmitFormationForm()
        context = {
            "data": formation_data,
            "submit_form": submit_form,
        }
        return render(request, "submit_formation_data.html", context)

    def post(self, request):
        formation_data = request.session.get("excel_student_data", {})
        submit_form = SubmitFormationForm(request.POST)

        if not submit_form.is_valid():
            messages.error(request, "Ocurrió un error.")
            return self.render_submit_view(request, formation_data, submit_form)

        if not formation_data:
            messages.error(request, "Ocurrió un error inesperado al leer los datos.")
            return redirect("load_formation")

        try:
            start_date = submit_form.cleaned_data.get("start_date")
            end_date = submit_form.cleaned_data.get("end_date")

            formation_data_model = dict_to_formation(formation_data)
            formation_student_handler.save_formation_and_students(
                formation_data_model, start_date, end_date
            )

            self.clear_session_data(request, "excel_student_data")
            messages.success(request, "Formación guardada exitosamente.")
            return redirect("load_formation")

        except ValueError as e:
            messages.error(request, f"Error al guardar los datos: {str(e)}")
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
        except Exception as e:
            messages.error(request, f"Error al guardar los datos: {str(e)}")
        finally:
            return redirect("load_formation")

    def render_submit_view(self, request, formation_data, submit_form=None):
        submit_form = submit_form or SubmitFormationForm()
        context = {
            "data": formation_data,
            "submit_form": submit_form,
        }
        return render(request, "submit_formation_data.html", context)

    def clear_session_data(self, request, key_name):
        if key_name in request.session:
            del request.session[key_name]

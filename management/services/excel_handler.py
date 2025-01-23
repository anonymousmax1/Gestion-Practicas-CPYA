from management.enums import ExcelTypes
from .formation_excel_service import FormationExcelService
from .contract_excel_service import ContractExcelService
from .base_excel_service import BaseExcelService


def excel_file_handler(file, file_type):
    services = {
        ExcelTypes.FORMATION: FormationExcelService,
        ExcelTypes.STUDENT_CONTRACT: ContractExcelService,
    }

    service_class = services.get(file_type)
    if not service_class:
        raise ValueError("Tipo de archivo no soportado")

    service = service_class(file)
    return __process_excel_file(service)


def __process_excel_file(service: BaseExcelService):
    if not service.check_format():
        raise ValueError("El formato del archivo no es válido.")

    data = service.read_data()
    return data

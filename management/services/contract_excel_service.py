from .base_excel_service import BaseExcelService
from datetime import datetime
from typing import Dict


class ContractExcelService(BaseExcelService):
    def __init__(self, file) -> None:
        super().__init__(file)
        self.cell_conditions = {
            "A2": "ID Ficha de Formación",
            "B2": "NIVEL DE FORMACION",
            "C2": "NOMBRE DE LA FORMACION",
            "D2": "NOMBRE Y APELLIDO APRENDIZ",
            "E2": "Tipo de Documento",
            "G2": "DIRECCION",
            "H2": "BARRIO",
            "I2": "CIUDAD DE RESIDENCIA DEL APRENDIZ",
            "J2": "TELEFONO",
            "K2": "CORREO ELECTRONICO @soysena.edu.co",
            "M2": "EMPRESA",
            "O2": "BARRIO DE LA EMPRESA",
            "P2": "DEPARTAMENTO DE LA EMPRESA",
            "Q2": "CIUDAD DE LA EMPRESA",
            "S2": "TELEFONO FIJO DE LA EMPRESA",
            "T2": "CORREO ELECTRONICO DE LA EMPRESA",
            "U2": "JEFE INMEDIATO",
            "V2": "FECHA DE INICIO DE LA ETAPA PRODUCTIVA O PASANTÍAS. (DD/MM/AA)",
            "W2": "FECHA FIN DE LA ETAPA PRODUCTIVA",
            "X2": "NIT DE LA EMPRESA",
            "Z2": "NOMBRE DEL ARL",
            "AA2": "FECHA INICIAL DE LA ETAPA LECTIVA",
            "AB2": "FECHA FINAL DE LA ETAPA LECTIVA",
        }

    def check_format(self) -> bool:
        self.load_file()
        for cell, expected_value in self.cell_conditions.items():
            actual_value = self._get_cell_value(cell).strip().lower()
            if actual_value != expected_value.strip().lower():
                raise ValueError(
                    f"Error en el formato: Se esperaba '{expected_value}' en la celda {cell}."
                )
        return True

    def read_data(self) -> Dict:
        self.load_file()

        def convert_datetime(value):
            if isinstance(value, datetime):
                return value.strftime("%d/%m/%Y")
            return value

        return {
            "formation_code": self._get_cell_value("A3"),
            "formation_level": self._get_cell_value("B3"),
            "formation_name": self._get_cell_value("C3"),
            "student_name": self._get_cell_value("D3"),
            "student_document_type": self._get_cell_value("E3"),
            "student_document_number": self._get_cell_value("F3"),
            "student_address": self._get_cell_value("G3"),
            "student_neighborhood": self._get_cell_value("H3"),
            "student_city": self._get_cell_value("I3"),
            "student_cellphone": self._get_cell_value("J3"),
            "email_sena": self._get_cell_value("K3"),
            "contract_modality": self._get_cell_value("L3"),
            "enterprise_name": self._get_cell_value("M3"),
            "enterprise_address": self._get_cell_value("N3"),
            "enterprise_neighborhood": self._get_cell_value("O3"),
            "enterprise_region": self._get_cell_value("P3"),
            "enterprise_city": self._get_cell_value("Q3"),
            "enterprise_cellphone": self._get_cell_value("R3"),
            "enterprise_phone": self._get_cell_value("S3"),
            "enterprise_email": self._get_cell_value("T3"),
            "boss_name": self._get_cell_value("U3"),
            "practices_start_date": convert_datetime(self._get_cell_value("V3")),
            "practices_end_date": convert_datetime(self._get_cell_value("W3")),
            "enterprise_nit": self._get_cell_value("X3"),
            "student_eps": self._get_cell_value("Y3"),
            "student_arl": self._get_cell_value("Z3"),
            "start_lective": convert_datetime(self._get_cell_value("AA3")),
            "end_lective": convert_datetime(self._get_cell_value("AB3")),
        }

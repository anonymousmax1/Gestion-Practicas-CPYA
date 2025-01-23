from .base_excel_service import BaseExcelService
from typing import Dict


class FormationExcelService(BaseExcelService):
    def __init__(self, file) -> None:
        super().__init__(file)
        self.cell_conditions = {
            "A2": "Ficha de Caracterización:",
            "A3": "Estado:",
            "A4": "Fecha del Reporte:",
            "A5": "Tipo de Documento",
            "B5": "Número de Documento",
            "C5": "Nombre",
            "D5": "Apellidos",
            "E5": "Celular",
            "F5": "Correo Electrónico",
            "G5": "Estado",
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
        code_name = str(self._get_cell_value("C2")).replace(".", "").split("-")
        code, name = code_name[0].strip(), code_name[1].strip()

        students_data = [
            self._get_row_values(row_idx)
            for row_idx in range(6, self.max_rows + 1)
        ]

        return {
            "formation_code": code,
            "formation_name": name,
            "students": [
                {
                    "document_type": str(student[0]),
                    "document_number": str(student[1]),
                    "name": student[2],
                    "last_name": student[3],
                    "cellphone": str(student[4]),
                    "email": student[5],
                    "state": student[6],
                }
                for student in students_data
            ],
        }

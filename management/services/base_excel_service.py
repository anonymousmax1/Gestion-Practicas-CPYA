from abc import ABC, abstractmethod
import openpyxl
import xlrd



class BaseExcelService(ABC):
    def __init__(self, file) -> None:
        self.file = file
        self.workbook = None
        self.worksheet = None
        self.max_rows = 0

    def load_file(self):
        self.file.seek(0)
        if self.file.name.endswith(".xlsx"):
            self.workbook = openpyxl.load_workbook(self.file)
            self.worksheet = self.workbook.active
            self.max_rows = self.worksheet.max_row
        elif self.file.name.endswith(".xls"):
            self.workbook = xlrd.open_workbook(file_contents=self.file.read())
            self.worksheet = self.workbook.sheet_by_index(0)
            self.max_rows = self.worksheet.nrows
        else:
            raise ValueError("Formato de archivo no soportado (solo .xls o .xlsx).")

    @abstractmethod
    def check_format(self) -> bool:
        pass

    @abstractmethod
    def read_data(self):
        pass

    def _get_cell_value(self, cell):
        row, col = self._cellname_to_rowcol(cell)
        if isinstance(self.worksheet, openpyxl.worksheet.worksheet.Worksheet):
            return str(self.worksheet[cell].value or "")
        elif isinstance(self.worksheet, xlrd.sheet.Sheet):
            return str(self.worksheet.cell_value(row, col) or "")

    def _get_row_values(self, row_idx):
        if isinstance(self.worksheet, openpyxl.worksheet.worksheet.Worksheet):
            return [cell.value for cell in self.worksheet[row_idx]]
        elif isinstance(self.worksheet, xlrd.sheet.Sheet):
            return self.worksheet.row_values(row_idx - 1)

    def _cellname_to_rowcol(self, cell_name):
        column = 0
        row = 0
        for i, char in enumerate(cell_name):
            if char.isdigit():
                row = int(cell_name[i:]) - 1
                break
            column = column * 26 + (ord(char.upper()) - ord("A") + 1)
        return row, column - 1

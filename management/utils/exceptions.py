class InvalidCredentialsError(Exception):
    def __init__(self, message = "Las credenciales ingresadas son inválidas"):
        super().__init__(message)

class CustomExcelError(Exception):
    def __init__(self, message = "Error al procesar el archivo"):
        super().__init__(message)



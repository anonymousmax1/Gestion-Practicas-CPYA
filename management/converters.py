from .values import ContractTypeValues, DocumentTypesValues


def str_contrat_type_to_value(contract_type: str) -> ContractTypeValues:
    values = {
        "Contrato de Aprendizaje": ContractTypeValues.LEARNING_CONTRACT.value,
        "Pasantia": ContractTypeValues.INTERNSHIP.value,
        "Vinculo Laboral": ContractTypeValues.EMPLOYMENT.value,
        "Proyecto Productivo": ContractTypeValues.PRODUCTIVE_PROJECT.value,
    }

    return values[contract_type]


def str_doc_type_to_value(doc_type: str) -> DocumentTypesValues:
    values = {
        "CC": DocumentTypesValues.CC.value,
        "TI": DocumentTypesValues.TI.value,
        "PEP": DocumentTypesValues.PEP.value,
    }

    return values[doc_type]

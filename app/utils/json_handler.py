import json
from app.config import configs

def read_from(json_path_file) -> list[dict]:
    """
    Lê o arquivo JSON e retorna o conteúdo.
    Returns:
        list: Lista de dicionários carregados do arquivo.
    """
    with open(json_path_file, 'r', encoding=configs.ENCODING_TYPE) as file:
        temp_list = json.load(file)
    return temp_list

def save_to(json_path_file, file_to_save):
    """
    Salvar os dados no arquivo JSON.
    """
    with open(json_path_file, 'w', encoding=configs.ENCODING_TYPE) as file:
        json.dump(file_to_save, file, indent=configs.BASE_INDENT, ensure_ascii=configs.ENSURE_ASCII)
    return True
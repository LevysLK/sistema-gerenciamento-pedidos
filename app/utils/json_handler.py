import json
from app.config import configs, paths
from pathlib import Path

def check_temp_files() -> list[str] | bool:
    """
    Checa a existência de arquivos temporários não tratados.
    Returns:
        list: Lista com os nomes dos arquivos existentes.
        False: Não existem arquivos temporários no sistema.
    """
    temp_list = []
    for path in paths.JSON_PATHS:
        temp_file = path.with_suffix(path.suffix + '.temp')
        if temp_file.is_file():
            temp_list.append(f'  - Arquivo: {temp_file.name!r}')

    if temp_list:
        return temp_list
    return False

def read_from(json_path_file) -> list[dict]:
    """
    Lê o arquivo JSON e retorna o conteúdo.
    Returns:
        list: Lista de dicionários carregados do arquivo.
    """
    with open(json_path_file, 'r', encoding=configs.ENCODING_TYPE) as file:
        temp_list = json.load(file)
    return temp_list

def save_to(json_path_file: Path, file_to_save) -> None:
    """
    Salvar os dados no arquivo temporário,
    e depois substitui o arquivo JSON original.
    """
    temp_file = json_path_file.with_suffix(json_path_file.suffix + '.temp') 
    try:
        with temp_file.open('w', encoding=configs.ENCODING_TYPE) as file:
            json.dump(file_to_save, file, indent=configs.BASE_INDENT, ensure_ascii=configs.ENSURE_ASCII)
    except Exception:
        temp_file.unlink(missing_ok=True)
        raise
    temp_file.replace(json_path_file)

def delete_file(json_path_file) -> bool:
    """
    Deleta o arquivo JSON especificado.
    Returns:
        True: Exclusão efetuada sem erros.
        False: Erro na exclusão ou arquivo inexistente.
    """
    try:
        Path(json_path_file).unlink()
        return True
    except FileNotFoundError:
        return False

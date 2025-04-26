import os
from utils.log import setup_logging

log = setup_logging(log_file="logs/files.log")

def _open_file(file_path: str) -> str:
    """Abre um arquivo e retorna seu conteúdo."""
    full_path = os.path.join(os.getcwd(), file_path)
    log.info(f"Tentando abrir arquivo: {full_path}")

    try:
        with open(full_path, "r") as file:
            content = file.read()
            log.info(f"Arquivo lido com sucesso: {full_path}")
            return content

    except FileNotFoundError:
        log.error(f"Arquivo não encontrado: {full_path}", exc_info=True)
        raise

    except Exception as e:
        log.error(f"Erro inesperado ao abrir arquivo: {full_path} | Erro: {str(e)}", exc_info=True)
        raise

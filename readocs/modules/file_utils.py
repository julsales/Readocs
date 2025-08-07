import os

def read_file(path: str) -> str:
    """Lê o conteúdo de um arquivo do projeto e o retorna como string,
    tratando possíveis erros de codificação.
    
    Args:
        path: O caminho do arquivo a ser lido.
    
    Returns:
        O conteúdo do arquivo como string ou uma mensagem de erro.
    """
    if not os.path.exists(path):
        return f"Erro: O arquivo '{path}' não foi encontrado."

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1", errors="replace") as f:
            return f.read()
    except Exception as e:
        return f"Erro inesperado ao ler o arquivo '{path}': {e}"

    
def list_files(directory: str) -> str:
    """Lista todos os arquivos e diretórios em um caminho especificado.
    Args:
        directory: O caminho para o diretório a ser listado.
    """
    items = os.listdir(directory)
    file_list = "\n".join(items)
    return f"Arquivos e diretórios em '{directory}':\n{file_list}"
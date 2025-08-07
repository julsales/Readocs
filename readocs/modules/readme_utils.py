import os
import re

def update_readme(section_title: str, section_content: str, project_title: str = "Projeto Readocs") -> str:
    """Adiciona ou atualiza uma seção no README.md.

    Se a seção já existir, seu conteúdo será substituído. Caso contrário,
    uma nova seção será adicionada no final.
    
    Args:
        section_title: O título da seção a ser atualizada.
        section_content: O novo conteúdo em markdown para a seção.
        project_title: O título principal do projeto, usado para criar o arquivo se ele não existir.
    
    Returns:
        Uma mensagem de sucesso ou erro.
    """
    path = "README.md"
    
    # 1. Se o README.md não existir, crie-o com o título do projeto e a nova seção.
    if not os.path.exists(path):
        content = f"# {project_title}\n\n## {section_title}\n{section_content}\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"README.md criado com a seção '{section_title}'."

    # 2. Se o arquivo existir, leia o conteúdo completo.
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define o padrão para encontrar a seção
    # Ele busca por um título de seção e captura tudo que vem depois, até o próximo título ou o final do arquivo.
    pattern = r"(^## " + re.escape(section_title) + r")\n.*?(?=\n## |\Z)"
    
    new_section_content = f"## {section_title}\n{section_content}\n"

    # 3. Tenta encontrar e substituir a seção.
    if re.search(pattern, content, re.DOTALL | re.MULTILINE):
        updated_content = re.sub(
            pattern,
            new_section_content,
            content,
            flags=re.DOTALL | re.MULTILINE
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        return f"Seção '{section_title}' atualizada com sucesso."
    else:
        # 4. Se a seção não for encontrada, adicione-a no final do arquivo.
        content += f"\n{new_section_content}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Seção '{section_title}' adicionada com sucesso."
import os
import re

def update_readme(section_title: str, section_content: str, project_title: str = "Projeto Readocs") -> str:
    """Adiciona ou atualiza uma seção no README.md.

    Se a seção já existir, seu conteúdo será substituído. Caso contrário,
    uma nova seção será adicionada no final. Garante que o marcador
    {{BADGE_SECTION}} esteja no topo do arquivo.

    Args:
        section_title: O título da seção a ser atualizada.
        section_content: O novo conteúdo em markdown para a seção.
        project_title: O título principal do projeto, usado para criar o arquivo se ele não existir.
    
    Returns:
        Uma mensagem de sucesso ou erro.
    """
    path = "README.md"
    badge_header = f"{{{{BADGE_SECTION}}}}\n# {project_title}\n"

    # 1. Se o README.md não existir, crie-o com o marcador e a nova seção.
    if not os.path.exists(path):
        content = f"{badge_header}\n\n## {section_title}\n{section_content}\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"README.md criado com a seção '{section_title}'."

    # 2. Se o arquivo existir, leia o conteúdo completo.
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 3. Garante que o marcador esteja no topo
    if not content.startswith("{{BADGE_SECTION}}"):
        # Remove qualquer ocorrência perdida de BADGE_SECTION fora do topo
        content = content.replace("{{BADGE_SECTION}}", "")
        # Remove título duplicado
        content = re.sub(r"^# .*\n", "", content, count=1)
        content = badge_header + "\n" + content.lstrip()

    # 4. Atualiza ou adiciona a seção
    pattern = r"(^##\s+" + re.escape(section_title) + r")\n.*?(?=\n## |\Z)"
    new_section = f"## {section_title}\n{section_content}\n"

    if re.search(pattern, content, re.DOTALL | re.MULTILINE):
        content = re.sub(
            pattern,
            lambda m: new_section,
            content,
            flags=re.DOTALL | re.MULTILINE
        )
        result_msg = f"Seção '{section_title}' atualizada com sucesso."
    else:
        content += f"\n{new_section}"
        result_msg = f"Seção '{section_title}' adicionada com sucesso."

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return result_msg

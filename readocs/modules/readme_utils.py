import os

def update_readme(section_title: str, section_content: str) -> str:
    path = "README.md"

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Projeto Readocs\n\n")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if section_title in content:
        return "Seção já existe, não foi alterada."

    content += f"\n## {section_title}\n{section_content}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return "README.md atualizado com sucesso."
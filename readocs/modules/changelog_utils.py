from datetime import datetime
import os

def update_changelog(titulo: str = "Atualização automática", descricao: str = "") -> str:
    path = "CHANGELOG.md"
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Changelog\n\n")

    entrada = f"## [{data_atual}] - {titulo}\n{descricao}\n\n"

    with open(path, "a", encoding="utf-8") as f:
        f.write(entrada)

    return f"CHANGELOG.md atualizado com a entrada de {data_atual}."
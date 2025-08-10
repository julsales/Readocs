from datetime import datetime
import os
import re
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from agno.team import Team
from agno.models.anthropic import Claude
from .ui import print_banner

from .agents.doc_agent import doc_agent
from .agents.curation_agent import curation_agent

# Safe imports for tools
try:
    from .modules.readme_cleaner import ensure_clean_readme, fix_readme_duplicates
except Exception:
    def ensure_clean_readme(path: str = "README.md"):  # type: ignore
        pass
    def fix_readme_duplicates(path: str = "README.md"):  # type: ignore
        return False

# ========== CONFIG DE EXECUÇÃO (padrões; sobrescritura via CLI/env) ==========
PROJECT_FOLDER = os.getenv("READOCS_PROJECT_FOLDER", "readocs")
ROOT_DIR = os.getenv("READOCS_ROOT_DIR", "..")
MODEL_ID = os.getenv("READOCS_MODEL_ID", "claude-3-haiku-20240307")
DRY_RUN = os.getenv("READOCS_DRY_RUN", "0") == "1"
SKIP_CLEAN = os.getenv("READOCS_SKIP_CLEAN", "0") == "1"
SKIP_CHANGELOG = os.getenv("READOCS_SKIP_CHANGELOG", "0") == "1"
# ==========================================================================


def print_header():
    print_banner("Documentação personalizada com agentes")


def print_step(step: int, total: int, message: str):
    print(f"[{step}/{total}] {message}")


def setup_directories(project_folder: Optional[str] = None, root_dir: Optional[str] = None) -> str:
    pf = project_folder or PROJECT_FOLDER
    rd = root_dir or ROOT_DIR
    current = Path.cwd()

    if (current / pf).exists():
        project_path = f"./{pf}"
    elif current.name == pf:
        os.chdir(current.parent)
        project_path = f"./{pf}"
    else:
        os.chdir(Path(rd).resolve())
        project_path = f"./{pf}"

    print(f"📁 Analisando: {project_path}")
    return project_path


def get_next_version() -> str:
    if not os.path.exists("CHANGELOG.md"):
        return "0.1.0"

    try:
        with open("CHANGELOG.md", "r", encoding="utf-8") as f:
            content = f.read()
        versions = re.findall(r"## \\[(\\d+)\\.(\\d+)\\.(\\d+)\\]", content)
        if not versions:
            return "0.1.0"
        version_tuples = [tuple(map(int, v)) for v in versions]
        major, minor, patch = max(version_tuples)
        return f"{major}.{minor}.{patch + 1}"
    except Exception as e:
        print(f"Erro ao processar CHANGELOG.md: {e}")
        return "0.1.0"


# Minimal tool versions used by Team

def tool_read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler '{path}': {e}"


def tool_list_files(directory: str) -> str:
    try:
        files = []
        for root, _, filelist in os.walk(directory):
            for file in filelist:
                if file.endswith((".py", ".md", ".txt", ".yml", ".yaml", ".json")):
                    rel_path = os.path.relpath(os.path.join(root, file), directory)
                    files.append(rel_path)
        return "\n".join(sorted(files))
    except Exception as e:
        return f"Erro ao listar arquivos: {e}"


def set_runtime_options(
    project_folder: Optional[str] = None,
    root_dir: Optional[str] = None,
    model: Optional[str] = None,
    dry_run: Optional[bool] = None,
    skip_clean: Optional[bool] = None,
    skip_changelog: Optional[bool] = None,
):
    global PROJECT_FOLDER, ROOT_DIR, MODEL_ID, DRY_RUN, SKIP_CLEAN, SKIP_CHANGELOG
    if project_folder is not None:
        PROJECT_FOLDER = project_folder
        os.environ["READOCS_PROJECT_FOLDER"] = project_folder
    if root_dir is not None:
        ROOT_DIR = root_dir
        os.environ["READOCS_ROOT_DIR"] = root_dir
    if model is not None:
        MODEL_ID = model
        os.environ["READOCS_MODEL_ID"] = model
    if dry_run is not None:
        DRY_RUN = bool(dry_run)
        os.environ["READOCS_DRY_RUN"] = "1" if DRY_RUN else "0"
    if skip_clean is not None:
        SKIP_CLEAN = bool(skip_clean)
        os.environ["READOCS_SKIP_CLEAN"] = "1" if SKIP_CLEAN else "0"
    if skip_changelog is not None:
        SKIP_CHANGELOG = bool(skip_changelog)
        os.environ["READOCS_SKIP_CHANGELOG"] = "1" if SKIP_CHANGELOG else "0"


def run_generation() -> bool:
    print_header()

    print_step(1, 5, "Configurando projeto...")
    project_path = setup_directories()
    load_dotenv()

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("❌ ANTHROPIC_API_KEY não definida no .env")
        return False

    print_step(2, 5, "Analisando versão...")
    next_version = get_next_version()
    current_date = datetime.now().strftime("%Y-%m-%d")
    project_name = os.path.basename(project_path)

    print_step(3, 5, "Limpando duplicatas...")
    try:
        if not SKIP_CLEAN and os.path.exists("README.md"):
            ensure_clean_readme("README.md")
            fix_readme_duplicates("README.md")
    except Exception:
        pass

    print_step(4, 5, "Conectando com Claude...")

    team = Team(
        mode="coordinate",
        members=[curation_agent, doc_agent],
        model=Claude(
            id=MODEL_ID,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        ),
        tools=[tool_read_file, tool_list_files],
        success_criteria="Criar documentação específica baseada no código real do projeto.",
        instructions=[
            "Leia e analise o código ANTES de escrever documentação",
            "Use informações REAIS do projeto, não templates genéricos",
            "Documente o que o código realmente faz",
            "Seja específico sobre funcionalidades encontradas",
            "Use português brasileiro e formato markdown",
        ],
        markdown=True,
    )

    prompt = f"""
    Você é um agente que deve analisar completamente o projeto para gerar a documentação personalizada.
    A documentação deve ser toda em português e seguir as diretrizes do projeto.

    PROJETO: {project_name}
    VERSÃO: {next_version}
    DATA: {current_date}
    CÓDIGO EM: {project_path}

    Para o README.md, você deve:
        1. Use a ferramenta 'list_files' para ter uma visão geral da estrutura do projeto em '{project_path}'.
        2. Com base na lista de arquivos, use a ferramenta 'read_file' para analisar os arquivos relevantes, como 'main.py' e 'requirements.txt', para entender o propósito e as dependências do projeto.
        3. Atualize o README.md com uma seção de 'Introdução' e uma de 'Instalação' baseadas na análise real.
        4. Não cite a complexidade do projeto; pode fazer um pequeno pitch do que ele faz.
        5. Se identificar venv, adicione instruções de ativação no Windows e Linux.

        Diretrizes para o CHANGELOG.md:
            1. Adicione uma nova entrada para a versão {next_version}.
            2. Inclua a data de hoje ({current_date}).
            3. Descreva as mudanças de forma clara e concisa.
            4. Relate mudanças feitas no README.md.
            5. Se não houver mudanças significativas, use "Nenhuma mudança significativa".

    IMPORTANTE:
    - ZERO conteúdo genérico ou template
    - Documente apenas o que encontrar no código
    - Se encontrar agentes, explique o que cada um faz
    - Se encontrar APIs, liste os endpoints reais
    - Se encontrar funções, documente as principais
    - Baseie tudo na análise real dos arquivos

    Comece analisando os arquivos agora.
    """

    print_step(5, 5, "Gerando documentação...")

    def ensure_changelog_entry(version: str, date: str, note: str):
        if SKIP_CHANGELOG or DRY_RUN:
            print("\nℹ️ Modo sem alterações em CHANGELOG (pulado ou dry-run).")
            return
        changelog_path = "CHANGELOG.md"
        new_entry = f"## [{version}] - {date}\n{note}\n\n"
        try:
            if not os.path.exists(changelog_path):
                with open(changelog_path, "w", encoding="utf-8") as f:
                    f.write("# Changelog\n\n")
                    f.write(new_entry)
            else:
                with open(changelog_path, "r+", encoding="utf-8") as f:
                    content = f.read()
                    if f"## [{version}]" not in content:
                        f.seek(0, 0)
                        f.write(new_entry + content)
        except Exception as e:
            print(f"⚠️ Erro ao atualizar o CHANGELOG.md: {e}")

    def ensure_minimal_readme():
        if os.path.exists("README.md"):
            return
        if DRY_RUN:
            print("[dry-run] Criaria README.md mínimo.")
            return
        try:
            content = (
                "# Readocs\n\n"
                "Ferramenta para gerar e atualizar README.md e CHANGELOG.md baseados no seu código.\n\n"
                "## CLI\n\n"
                "- `python -m readocs generate`\n"
                "- `python -m readocs generate --dry-run`\n"
            )
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(content)
            print("📄 README.md (mínimo) criado.")
        except Exception as e:
            print(f"⚠️ Erro ao criar README.md mínimo: {e}")

    try:
        team.print_response(prompt)

        if SKIP_CHANGELOG or DRY_RUN:
            print("\nℹ️ Modo sem alterações em CHANGELOG (pulado ou dry-run).")
            print("✅ Fluxo concluído.")
            return True

        # Garante que o CHANGELOG seja incrementado
        ensure_changelog_entry(next_version, current_date, "- Documentação atualizada automaticamente.")

        print(f"\n✅ Documentação gerada!")
        print(f"📄 README.md personalizado")
        print(f"📋 CHANGELOG.md v{next_version}")
        return True

    except Exception as e:
        print(f"❌ Erro: {e}")
        # Fallback: ainda garantir CHANGELOG e README mínimo
        ensure_changelog_entry(next_version, current_date, "- Falha na geração automática (ver logs).")
        ensure_minimal_readme()
        return False


def main():
    return run_generation()


if __name__ == "__main__":
    main()

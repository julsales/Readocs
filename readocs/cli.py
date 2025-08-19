import os
from pathlib import Path
from typing import Optional

import typer
from rich import print
from .ui import print_banner
from dotenv import load_dotenv

from .main import run_generation, set_runtime_options

app = typer.Typer(help="Readocs CLI - gere README e CHANGELOG baseados no seu código.")


@app.callback()
def setup_env(ctx: typer.Context):
    """Load environment early so commands can rely on it."""
    # Descobre .env no cwd ou acima
    load_dotenv(override=False)
    # Banner será mostrado dentro de cada comando


@app.command("generate")
def generate(
    project_path: str = typer.Argument(
        ".",
        help="Caminho para o projeto a ser documentado (padrão: diretório atual).",
        show_default=True,
    ),
    output_dir: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Diretório onde salvar a documentação (padrão: mesmo diretório do projeto).",
    ),
    model: str = typer.Option(
        os.getenv("READOCS_MODEL_ID", "claude-3-haiku-20240307"),
        "--model",
        help="Modelo a ser usado pelo agente (ex.: claude-3-haiku-20240307)",
        show_default=True,
    ),
    dry_run: bool = typer.Option(
        os.getenv("READOCS_DRY_RUN", "0") == "1",
        "--dry-run",
        help="Executa a análise sem escrever README/CHANGELOG.",
    ),
    skip_clean: bool = typer.Option(
        os.getenv("READOCS_SKIP_CLEAN", "0") == "1",
        "--skip-clean",
        help="Não executa limpeza automática de duplicatas no README.",
    ),
    skip_changelog: bool = typer.Option(
        os.getenv("READOCS_SKIP_CHANGELOG", "0") == "1",
        "--skip-changelog",
        help="Não cria/atualiza a entrada do CHANGELOG.",
    ),
):
    """Gera documentação com base no código do projeto."""
    print_banner()
    set_runtime_options(
        project_folder=project_path,  # Usar project_path agora
        root_dir=output_dir,  # Usar output_dir como root_dir
        model=model,
        dry_run=dry_run,
        skip_clean=skip_clean,
        skip_changelog=skip_changelog,
    )

    ok = run_generation()
    raise typer.Exit(code=0 if ok else 1)


@app.command("version")
def version():
    print_banner("Versão")
    from importlib.metadata import version as _v, PackageNotFoundError

    try:
        v = _v("readocs")
    except PackageNotFoundError:
        v = "0.0.0"
    print(f"Readocs CLI v{v}")


@app.command("env")
def show_env():
    """Exibe informações de ambiente úteis para troubleshooting."""
    print_banner("Ambiente")
    api = os.getenv("ANTHROPIC_API_KEY")
    print("ANTHROPIC_API_KEY:", "definida" if api else "não definida")
    print("CWD:", Path.cwd())


if __name__ == "__main__":
    app()

import os
import subprocess
import sys
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
        help="Modelo Claude: números 1-6, nomes (haiku, sonnet, opus) ou IDs completos. Use 'python -m readocs models' para ver todos",
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
    
    # Resolver o modelo (número, nome parcial ou ID completo)
    resolved_model = resolve_model_id(model)
    
    set_runtime_options(
        project_folder=project_path,  # Usar project_path agora
        root_dir=output_dir,  # Usar output_dir como root_dir
        model=resolved_model,
        dry_run=dry_run,
        skip_clean=skip_clean,
        skip_changelog=skip_changelog,
    )

    ok = run_generation()
    raise typer.Exit(code=0 if ok else 1)


@app.command("version")
def version():
    """Versão do Readocs CLI."""
    print_banner("Versão")
    from importlib.metadata import version as _v, PackageNotFoundError

    try:
        v = _v("readocs")
    except PackageNotFoundError:
        v = "0.0.1"
    print(f"Readocs CLI v{v}")


@app.command("dev-setup")
def dev_setup():
    """Configuração completa para desenvolvedores (venv, dependências, etc)."""
    print_banner("Setup para Desenvolvedores")
    
    print("Este comando irá:")
    print("   - Verificar/criar ambiente virtual (.venv)")
    print("   - Instalar dependências de desenvolvimento")
    print("   - Configurar ambiente completo")
    
    choice = input("\nContinuar? (s/N): ").strip().lower()
    if choice not in ['s', 'sim', 'y', 'yes']:
        print("Setup cancelado")
        return
    
    print(f"Iniciando setup de desenvolvimento...")
    
    try:
        # 1. Verificar se está em venv e configurações do venv_path
        def is_in_venv():
            return (hasattr(sys, 'real_prefix') or 
                   (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
                   os.environ.get('VIRTUAL_ENV') is not None)
        
        venv_path = Path(".venv")
        python_exe_path = venv_path / ("Scripts/python.exe" if os.name == 'nt' else "bin/python")
        pip_exe_path = venv_path / ("Scripts/pip.exe" if os.name == 'nt' else "bin/pip")
        activate_script_path = venv_path / ("Scripts/activate.bat" if os.name == 'nt' else "bin/activate")
        
        print(f"Verificando ambiente virtual em: {venv_path.absolute()}")
        
        if not is_in_venv():
            print("Não está executando em um ambiente virtual")
            
            if not venv_path.exists():
                print(f"Criando ambiente virtual em {venv_path}...")
                result = subprocess.run([sys.executable, "-m", "venv", str(venv_path)], 
                                      check=True, capture_output=True, text=True)
                print(f"Ambiente virtual criado em: {venv_path.absolute()}")
                
                # Verificar se os executáveis foram criados corretamente
                if python_exe_path.exists() and pip_exe_path.exists():
                    print(f"Python venv: {python_exe_path}")
                    print(f"Pip venv: {pip_exe_path}")
                else:
                    print("Aviso: Alguns executáveis do venv podem não ter sido criados corretamente")
            else:
                print(f"Ambiente virtual já existe em: {venv_path.absolute()}")
                
                # Verificar integridade do venv existente
                if python_exe_path.exists():
                    print(f"Python encontrado: {python_exe_path}")
                else:
                    print("Aviso: Executável Python não encontrado no venv existente")
                
                if pip_exe_path.exists():
                    print(f"Pip encontrado: {pip_exe_path}")
                else:
                    print("Aviso: Pip não encontrado no venv existente")
            
            # Instruções para ativar venv
            if os.name == 'nt':  # Windows
                activate_script = venv_path / "Scripts" / "activate.bat"
                print(f"� Para ativar o ambiente virtual, execute:")
                print(f"   {activate_script}")
                print(f"   ou simplesmente: .venv\\Scripts\\activate")
            else:  # Unix/Linux/MacOS
                activate_script = venv_path / "bin" / "activate"
                print(f"Para ativar o ambiente virtual, execute:")
                print(f"   source {activate_script}")
            
            print("\nIMPORTANTE: Ative o ambiente virtual e execute este comando novamente")
            print("   para completar a instalação das dependências.")
            raise typer.Exit(0)
        
        print("Executando em ambiente virtual")
        
        # 2. Instalar dependências de desenvolvimento
        print("Instalando dependências...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                              check=True, capture_output=True, text=True)
        print("Dependências instaladas")
        
        # 3. Verificar informações do ambiente virtual atual
        current_venv = os.environ.get('VIRTUAL_ENV')
        if current_venv:
            current_venv_path = Path(current_venv)
            print(f"Ambiente virtual ativo: {current_venv_path}")
            
            # Verificar se é o mesmo venv que estamos configurando
            if current_venv_path.name == venv_path.name:
                print("Usando o ambiente virtual correto")
            else:
                print(f"Aviso: Ambiente ativo ({current_venv_path.name}) difere do esperado ({venv_path.name})")
        
        # 4. Verificar versão do Python no ambiente atual
        try:
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            print(f"Versão do Python: {python_version}")
        except:
            print("Não foi possível determinar a versão do Python")
        
        # 3. Criar .env se não existir
        env_file = Path(".env")
        if not env_file.exists():
            env_example = Path(".env.example")
            if env_example.exists():
                import shutil
                shutil.copy(env_example, env_file)
                print("Arquivo .env criado a partir do .env.example")
            else:
                print("Arquivo .env.example não encontrado")
        
        # 4. Executar configuração inicial
        print("Executando configuração inicial...")
        setup()
        
        print("\nSetup de desenvolvimento concluído com sucesso!")
        print("Agora você pode usar 'python -m readocs generate' para testar")
        
    except subprocess.CalledProcessError as e:
        print(f"Erro durante instalação: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        raise typer.Exit(1)
    except Exception as e:
        print(f"Erro no setup de desenvolvimento: {e}")
        raise typer.Exit(1)


@app.command("setup")
def setup():
    """Configurar Readocs pela primeira vez (API key, modelo, etc)."""
    print_banner("Configuração Inicial")
    
    env_file = Path(".env")
    
    # Verificar se já tem .env
    if env_file.exists():
        print("Arquivo .env já existe")
        choice = input("Deseja reconfigurar? (s/N): ").strip().lower()
        if choice not in ['s', 'sim', 'y', 'yes']:
            print("Configuração cancelada")
            return

    print("\nConfigure sua chave API do Anthropic:")
    print("   Obtenha em: https://console.anthropic.com/")
    api_key = input("Digite sua ANTHROPIC_API_KEY: ").strip()
    
    if not api_key:
        print(" API key é obrigatória")
        raise typer.Exit(1)
    
    print("\nEscolha o modelo Claude:")
    print("   1. claude-3-haiku-20240307 (Rápido e econômico) [PADRÃO]")
    print("   2. claude-3-5-haiku-20241022 (Haiku mais recente)")
    print("   3. claude-3-sonnet-20240229 (Sonnet clássico)")
    print("   4. claude-3-5-sonnet-20240620 (Sonnet 3.5 junho)")
    print("   5. claude-3-5-sonnet-20241022 (Sonnet 3.5 mais recente)")
    print("   6. claude-3-opus-20240229 (Mais potente e caro)")
    
    choice = input("Escolha (1-6 ou Enter para padrão): ")

    models = {
        "1": "claude-3-haiku-20240307",
        "2": "claude-3-5-haiku-20241022", 
        "3": "claude-3-sonnet-20240229",
        "4": "claude-3-5-sonnet-20240620",
        "5": "claude-3-5-sonnet-20241022",
        "6": "claude-3-opus-20240229"
    }
    
    model = models.get(choice, "claude-3-haiku-20240307")
    
    # Criar .env
    env_content = f"""# Readocs Configuration
ANTHROPIC_API_KEY={api_key}
READOCS_MODEL_ID={model}
READOCS_DRY_RUN=0
READOCS_SKIP_CLEAN=0
READOCS_SKIP_CHANGELOG=0
"""
    
    env_file.write_text(env_content, encoding='utf-8')
    print(f"\nConfiguração salva em {env_file}")
    print(f"Modelo selecionado: {model}")
    print("\nPronto! Use: python -m readocs generate")


@app.command("env")
def show_env():
    """Exibe informações de ambiente úteis para troubleshooting."""
    print_banner("Ambiente")
    
    # Informações da API
    api = os.getenv("ANTHROPIC_API_KEY")
    print("ANTHROPIC_API_KEY:", "definida" if api else "não definida")
    
    # Informações do modelo
    current_model = os.getenv("READOCS_MODEL_ID", "claude-3-haiku-20240307")
    print(f"READOCS_MODEL_ID: {current_model}")
    
    # Informações do diretório
    print("CWD:", Path.cwd())
    
    # Informações detalhadas do ambiente virtual
    print("\n=== INFORMAÇÕES DO AMBIENTE VIRTUAL ===")
    
    venv_path = Path(".venv")
    python_exe_path = venv_path / ("Scripts/python.exe" if os.name == 'nt' else "bin/python")
    pip_exe_path = venv_path / ("Scripts/pip.exe" if os.name == 'nt' else "bin/pip")
    activate_script_path = venv_path / ("Scripts/activate.bat" if os.name == 'nt' else "bin/activate")
    
    print(f"Caminho do venv local: {venv_path.absolute()}")
    print(f"Venv existe: {'Sim' if venv_path.exists() else 'Não'}")
    
    if venv_path.exists():
        print(f"Python venv: {'Encontrado' if python_exe_path.exists() else 'Não encontrado'} - {python_exe_path}")
        print(f"Pip venv: {'Encontrado' if pip_exe_path.exists() else 'Não encontrado'} - {pip_exe_path}")
        print(f"Script ativação: {'Encontrado' if activate_script_path.exists() else 'Não encontrado'} - {activate_script_path}")
    
    # Verificar ambiente virtual ativo
    current_venv = os.environ.get('VIRTUAL_ENV')
    if current_venv:
        print(f"Ambiente virtual ativo: {current_venv}")
        current_venv_path = Path(current_venv)
        match_status = "Sim" if current_venv_path.name == venv_path.name else "Não"
        print(f"Corresponde ao venv local: {match_status}")
    else:
        print("Ambiente virtual ativo: Nenhum")
    
    # Informações do Python atual
    print(f"\n=== PYTHON ATUAL ===")
    print(f"Executável: {sys.executable}")
    print(f"Versão: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"Em venv: {'Sim' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'Não'}")
    
    # Informações do sistema
    print(f"\n=== SISTEMA ===")
    print(f"OS: {os.name}")
    print(f"Platform: {sys.platform}")


@app.command("models")
def list_models():
    """Lista todos os modelos Claude disponíveis com suas características."""
    print_banner("Modelos Disponíveis")
    
    models = [
        {
            "name": "claude-3-haiku-20240307",
            "family": "Haiku",
            "version": "3.0",
            "speed": "⚡ Muito rápido",
            "cost": "💰 Econômico",
            "quality": "⭐⭐⭐ Boa",
            "best_for": "Tarefas simples, prototipagem rápida"
        },
        {
            "name": "claude-3-5-haiku-20241022", 
            "family": "Haiku",
            "version": "3.5",
            "speed": "⚡ Muito rápido",
            "cost": "💰 Econômico",
            "quality": "⭐⭐⭐⭐ Muito boa",
            "best_for": "Melhor versão do Haiku, boa para a maioria das tarefas"
        },
        {
            "name": "claude-3-sonnet-20240229",
            "family": "Sonnet", 
            "version": "3.0",
            "speed": "🔄 Moderado",
            "cost": "💰💰 Médio",
            "quality": "⭐⭐⭐⭐ Muito boa",
            "best_for": "Análise detalhada, documentação complexa"
        },
        {
            "name": "claude-3-5-sonnet-20240620",
            "family": "Sonnet",
            "version": "3.5 (Jun)",
            "speed": "🔄 Moderado",
            "cost": "💰💰 Médio",
            "quality": "⭐⭐⭐⭐⭐ Excelente",
            "best_for": "Projetos grandes, análise profunda"
        },
        {
            "name": "claude-3-5-sonnet-20241022",
            "family": "Sonnet",
            "version": "3.5 (Out)",
            "speed": "🔄 Moderado",
            "cost": "💰💰 Médio", 
            "quality": "⭐⭐⭐⭐⭐ Excelente",
            "best_for": "Versão mais recente, melhor qualidade geral"
        },
        {
            "name": "claude-3-opus-20240229",
            "family": "Opus",
            "version": "3.0",
            "speed": "🐌 Mais lento",
            "cost": "💰💰💰 Caro",
            "quality": "⭐⭐⭐⭐⭐ Excepcional",
            "best_for": "Projetos críticos, máxima qualidade"
        }
    ]
    
    print("📋 Modelos Claude disponíveis para usar no Readocs:\n")
    
    for i, model in enumerate(models, 1):
        print(f"{'='*60}")
        print(f"🤖 {i}. {model['family']} {model['version']}")
        print(f"📝 ID: {model['name']}")
        print(f"⚡ Velocidade: {model['speed']}")
        print(f"💰 Custo: {model['cost']}")
        print(f"🎯 Qualidade: {model['quality']}")
        print(f"✨ Melhor para: {model['best_for']}")
        print()
    
    print("💡 Dicas de uso:")
    print("   • Para desenvolvimento/teste: Haiku 3.5 (claude-3-5-haiku-20241022)")
    print("   • Para uso geral: Sonnet 3.5 Out (claude-3-5-sonnet-20241022)")
    print("   • Para projetos críticos: Opus 3.0 (claude-3-opus-20240229)")
    print()
    print("🔧 Como usar:")
    print("   python -m readocs generate --model claude-3-5-sonnet-20241022")
    print("   ou configure no setup: python -m readocs setup")


def resolve_model_id(model_input: str) -> str:
    """Converte número (1-6) ou ID parcial em ID completo do modelo."""
    models_map = {
        "1": "claude-3-haiku-20240307",
        "2": "claude-3-5-haiku-20241022", 
        "3": "claude-3-sonnet-20240229",
        "4": "claude-3-5-sonnet-20240620",
        "5": "claude-3-5-sonnet-20241022",
        "6": "claude-3-opus-20240229"
    }
    
    # Se for um número de 1-6, converter
    if model_input in models_map:
        return models_map[model_input]
    
    # Se for um ID completo, retornar como está
    if model_input.startswith("claude-"):
        return model_input
    
    # Se for nome parcial, tentar mapear
    partial_map = {
        "haiku": "claude-3-haiku-20240307",
        "haiku-3.5": "claude-3-5-haiku-20241022",
        "sonnet": "claude-3-sonnet-20240229", 
        "sonnet-3.5": "claude-3-5-sonnet-20241022",
        "opus": "claude-3-opus-20240229"
    }
    
    if model_input.lower() in partial_map:
        return partial_map[model_input.lower()]
    
    # Se não encontrou, retornar como estava
    return model_input


if __name__ == "__main__":
    app()

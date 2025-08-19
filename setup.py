#!/usr/bin/env python
"""
Script de setup simplificado para Readocs
"""

import os
import subprocess
import sys
from pathlib import Path

def print_step(step, message):
    print(f"\n{'='*50}")
    print(f"[{step}] {message}")
    print(f"{'='*50}")

def print_info(message):
    print(f"💡 {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def is_in_venv():
    """Verifica se está executando dentro de um ambiente virtual."""
    # Verifica diferentes formas de detectar venv
    checks = []
    
    # Check 1: virtualenv (mais antigo)
    has_real_prefix = hasattr(sys, 'real_prefix')
    checks.append(('real_prefix', has_real_prefix))
    
    # Check 2: venv padrão do Python 3.3+
    has_base_prefix = hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    checks.append(('base_prefix', has_base_prefix))
    
    # Check 3: variável de ambiente VIRTUAL_ENV
    has_venv_var = os.environ.get('VIRTUAL_ENV') is not None
    checks.append(('VIRTUAL_ENV', has_venv_var))
    
    # Check 4: verifica se o executável está em um subdiretório típico de venv
    python_path = sys.executable.lower()
    is_venv_path = any(pattern in python_path for pattern in [
        'venv', '.venv', 'env', '.env', 'virtualenv'
    ])
    checks.append(('exec_path', is_venv_path))
    
    # Debug info (comentado por padrão)
    # print(f"Debug - Checks: {checks}")
    # print(f"Debug - sys.prefix: {sys.prefix}")
    # print(f"Debug - sys.base_prefix: {getattr(sys, 'base_prefix', 'N/A')}")
    # print(f"Debug - VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV')}")
    
    # Retorna True se qualquer check for positivo
    return any(result for _, result in checks)

def find_existing_venv():
    """Procura por ambientes virtuais existentes no diretório atual."""
    common_venv_names = ['.venv', 'venv', 'env', '.env_python', 'virtualenv']
    found_venvs = []
    
    for venv_name in common_venv_names:
        venv_path = Path(venv_name)
        if venv_path.exists() and venv_path.is_dir():
            # Verifica se tem os arquivos típicos de uma venv
            if os.name == 'nt':  # Windows
                python_exe = venv_path / "Scripts" / "python.exe"
                activate_script = venv_path / "Scripts" / "activate.bat"
            else:  # Linux/Mac
                python_exe = venv_path / "bin" / "python"
                activate_script = venv_path / "bin" / "activate"
            
            if python_exe.exists():
                found_venvs.append({
                    'name': venv_name,
                    'path': venv_path,
                    'python': python_exe,
                    'activate': activate_script
                })
    
    return found_venvs

def check_and_setup_venv():
    """Verifica e opcionalmente cria um ambiente virtual."""
    if is_in_venv():
        print("✅ Executando dentro de um ambiente virtual")
        print(f"   Ambiente: {sys.prefix}")
        return True
    
    print("❌ Não está em um ambiente virtual!")
    print_info("Ambientes virtuais são recomendados para isolar dependências")
    
    # Verifica se já existe uma venv
    existing_venvs = find_existing_venv()
    
    if existing_venvs:
        print(f"\n🔍 Encontrado(s) {len(existing_venvs)} ambiente(s) virtual(is) existente(s):")
        for i, venv in enumerate(existing_venvs, 1):
            print(f"   {i}. {venv['name']} ({venv['path']})")
        
        print(f"\n💡 Para usar um ambiente existente:")
        for venv in existing_venvs:
            if os.name == 'nt':  # Windows
                activate_cmd = f"{venv['name']}\\Scripts\\activate"
            else:  # Linux/Mac
                activate_cmd = f"source {venv['name']}/bin/activate"
            print(f"   {activate_cmd}")
        
        print(f"\n🤔 Opções disponíveis:")
        print(f"   1. Usar ambiente existente (recomendado)")
        print(f"   2. Criar novo ambiente")
        print(f"   3. Continuar sem ambiente virtual")
        
        if is_ci_environment():
            print_info("CI detectado - continuando sem ambiente virtual (opção 3)")
            choice = "3"
        else:
            choice = input(f"   Escolha (1/2/3): ").strip()
        
        if choice == "1":
            # Ativa o ambiente virtual e executa o script novamente
            venv = existing_venvs[0]  # Usa o primeiro encontrado
            if os.name == 'nt':  # Windows
                python_cmd = str(venv['path'] / "Scripts" / "python.exe")
            else:  # Linux/Mac
                python_cmd = str(venv['path'] / "bin" / "python")
            
            print(f"\n🔄 Ativando ambiente virtual '{venv['name']}' e reiniciando setup...")
            
            try:
                # Executa o script novamente dentro da venv
                result = subprocess.run([
                    python_cmd, 
                    __file__  # Este próprio script
                ], check=True)
                
                # Se chegou aqui, o script foi executado com sucesso
                # Sair completamente para evitar execução dupla
                sys.exit(0)
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao executar dentro da venv: {e}")
                print("🔄 Tentando com instruções manuais...")
                print(f"\n💡 Execute manualmente:")
                if os.name == 'nt':  # Windows
                    activate_cmd = f"{venv['name']}\\Scripts\\Activate.ps1"
                else:  # Linux/Mac
                    activate_cmd = f"source {venv['name']}/bin/activate"
                print(f"   {activate_cmd}")
                print(f"   python setup.py")
                return False
        elif choice == "2":
            return create_new_venv()
        else:
            print_warning("Continuando sem ambiente virtual...")
            print_info("Recomendamos usar venv para evitar conflitos de dependências")
            return True
    else:
        if is_ci_environment():
            print_info("Ambiente CI detectado - continuando sem ambiente virtual")
            return True
        
        choice = input("\n🤔 Deseja criar um ambiente virtual? (s/N): ").strip().lower()
        if choice in ['s', 'sim', 'y', 'yes']:
            return create_new_venv()
        else:
            print_warning("Continuando sem ambiente virtual...")
            print_info("Recomendamos usar venv para evitar conflitos de dependências")
            return True

def create_new_venv():
    """Cria um novo ambiente virtual."""
    if is_ci_environment():
        venv_name = ".venv"
        print_info(f"CI detectado - usando nome padrão: {venv_name}")
    else:
        venv_name = input("📁 Nome do ambiente virtual (padrão: .venv): ").strip() or ".venv"
    
    # Verifica se já existe
    if Path(venv_name).exists():
        print(f"❌ Diretório '{venv_name}' já existe!")
        return True
    
    try:
        print(f"🏗️  Criando ambiente virtual '{venv_name}'...")
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print(f"✅ Ambiente virtual '{venv_name}' criado com sucesso!")
        
        # Ativa automaticamente o novo ambiente virtual
        if os.name == 'nt':  # Windows
            python_path = Path(venv_name) / "Scripts" / "python.exe"
        else:  # Linux/Mac
            python_path = Path(venv_name) / "bin" / "python"
        
        print(f"🔄 Ativando novo ambiente virtual e reiniciando setup...")
        
        try:
            # Executa o script novamente dentro da nova venv
            result = subprocess.run([
                str(python_path), 
                __file__  # Este próprio script
            ], check=True)
            
            # Se chegou aqui, o script foi executado com sucesso
            # Sair completamente para evitar execução dupla
            sys.exit(0)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar dentro da nova venv: {e}")
            print("🔄 Tentando com instruções manuais...")
            if os.name == 'nt':  # Windows
                activate_cmd = f"{venv_name}\\Scripts\\activate"
            else:  # Linux/Mac
                activate_cmd = f"source {venv_name}/bin/activate"
            
            print(f"\n🔧 Execute manualmente:")
            print(f"   {activate_cmd}")
            print(f"   python setup.py")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        print_warning("Continuando sem ambiente virtual...")
        return True

def check_python_version():
    """Verifica se a versão do Python é adequada."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")
    return True

def check_requirements():
    """Verifica se as dependências principais estão instaladas."""
    critical_packages = {
        'anthropic': 'anthropic',
        'typer': 'typer', 
        'rich': 'rich',
        'python-dotenv': 'dotenv',
        'agno': 'agno',
        'pydantic': 'pydantic'
    }
    
    missing = []
    for pip_name, import_name in critical_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pip_name)
    
    if missing:
        print(f"❌ Pacotes necessários não encontrados: {', '.join(missing)}")
        return False
    else:
        print("✅ Principais dependências já instaladas")
        return True

def install_requirements():
    """Instala as dependências."""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ Arquivo requirements.txt não encontrado!")
        return False
    
    print(f"📦 Instalando dependências de {requirements_file}...")
    print("   (isso pode levar alguns minutos)")
    
    try:
        # Primeiro, mostra quais pacotes serão instalados
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except UnicodeDecodeError:
            # Tenta com encoding diferente se UTF-8 falhar
            with open(requirements_file, 'r', encoding='latin-1') as f:
                packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"   📋 {len(packages)} pacotes a serem instalados")
        
        # Instala com output visível
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"],
            check=True,
            text=True,
            capture_output=False  # Mostra o progresso
        )
        
        print("✅ Dependências instaladas com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências:")
        print(f"   Código de saída: {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def create_env_file():
    """Cria arquivo .env se não existir."""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Arquivo .env já existe")
        return True
    
    print("\n🔑 Configuração da API Key:")
    if is_ci_environment():
        api_key = ""
        print_info("CI detectado - pular configuração de API key")
    else:
        api_key = input("Digite sua chave API do Anthropic (ou Enter para configurar depois): ").strip()
    
    # Seleção do modelo Claude
    print("\n🤖 Seleção do Modelo Claude:")
    print("Escolha o modelo que você quer usar:")
    
    claude_models = {
        "1": ("claude-3-haiku-20240307", "Claude 3 Haiku (Rápido e econômico) [RECOMENDADO]"),
        "2": ("claude-3-5-haiku-20241022", "Claude 3.5 Haiku (Mais recente)"),
        "3": ("claude-3-sonnet-20240229", "Claude 3 Sonnet (Equilibrado)"),
        "4": ("claude-3-5-sonnet-20240620", "Claude 3.5 Sonnet (Melhor performance)"),
        "5": ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet (Mais recente)"),
        "6": ("claude-3-opus-20240229", "Claude 3 Opus (Mais potente, mais caro)")
    }
    
    for key, (model_id, description) in claude_models.items():
        print(f"   {key}. {description}")
    
    print("\n💡 Dica: Haiku é mais barato e rápido para a maioria dos projetos")
    
    if is_ci_environment():
        selected_model = "claude-3-haiku-20240307"
        print_info("CI detectado - usando modelo padrão: Claude 3 Haiku")
    else:
        while True:
            choice = input("Escolha um modelo (1-6, ou Enter para padrão Haiku): ").strip()
            
            if not choice:  # Enter pressionado
                selected_model = "claude-3-haiku-20240307"
                print("✅ Usando modelo padrão: Claude 3 Haiku")
                break
            elif choice in claude_models:
                selected_model, description = claude_models[choice]
                print(f"✅ Selecionado: {description}")
                break
            else:
                print("❌ Escolha inválida. Digite um número de 1 a 6 ou Enter.")
    
    env_content = f"""# Configuração do Readocs
ANTHROPIC_API_KEY={api_key}

# Configurações opcionais
READOCS_MODEL_ID={selected_model}
READOCS_DRY_RUN=0
READOCS_SKIP_CLEAN=0
READOCS_SKIP_CHANGELOG=0
"""
    
    try:
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ Arquivo .env criado!")
        if not api_key:
            print("⚠️ Lembre-se de adicionar sua chave API ao arquivo .env")
        print(f"🤖 Modelo configurado: {selected_model}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def test_installation():
    """Testa a instalação."""
    try:
        # Testa o CLI
        result = subprocess.run([sys.executable, "-m", "readocs", "version"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ CLI funcionando!")
            print(f"   Saída: {result.stdout.strip().split()[-1]}")  # Mostra versão
            return True
        else:
            print(f"❌ CLI com erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def is_ci_environment():
    """Detecta se está rodando em ambiente de CI/CD."""
    ci_vars = [
        'CI', 'CONTINUOUS_INTEGRATION',
        'GITHUB_ACTIONS', 'GITHUB_WORKFLOW',
        'TRAVIS', 'CIRCLECI', 'JENKINS_URL',
        'GITLAB_CI', 'AZURE_PIPELINES',
        'BUILD_BUILDID', 'TF_BUILD'
    ]
    return any(os.environ.get(var) for var in ci_vars)

def main():
    """Setup principal."""
    print("🚀 READOCS - SETUP UNIVERSAL")
    print("   Configurando gerador de documentação com IA")
    
    # Verifica ambiente virtual
    print_step("1/6", "Verificando ambiente virtual")
    if not check_and_setup_venv():
        print("\n🔄 Execute este script novamente dentro do ambiente virtual!")
        return False
    
    # Verifica Python
    print_step("2/6", "Verificando versão do Python")
    if not check_python_version():
        return False
    
    # Instala dependências
    print_step("3/6", "Verificando e instalando dependências")
    if not check_requirements():
        print("📦 Instalando dependências necessárias...")
        if not install_requirements():
            return False
    else:
        print("💡 Para forçar reinstalação, use: pip install -r requirements.txt --upgrade")
    
    # Cria arquivo .env
    print_step("4/6", "Configurando variáveis de ambiente")
    if not create_env_file():
        return False
    
    # Testa instalação
    print_step("5/6", "Testando instalação")
    if not test_installation():
        return False
    
    # Finalização
    print_step("6/6", "Setup concluído!")
    venv_info = "✅ Executando em ambiente virtual" if is_in_venv() else "⚠️ Sem ambiente virtual"
    
    # Se está na venv, sugere como ativar manualmente
    activation_tip = ""
    if is_in_venv():
        existing_venvs = find_existing_venv()
        if existing_venvs:
            venv = existing_venvs[0]
            if os.name == 'nt':  # Windows
                activation_tip = f"\n🔧 Para usar o Readocs, ative o ambiente virtual:\n   {venv['name']}\\Scripts\\Activate.ps1"
            else:  # Linux/Mac
                activation_tip = f"\n🔧 Para usar o Readocs, ative o ambiente virtual:\n   source {venv['name']}/bin/activate"
    
    print(f"""
✅ Readocs instalado com sucesso!
{venv_info}{activation_tip}

📖 Como usar:
   python -m readocs generate                 # Documenta projeto atual
   python -m readocs generate /meu/projeto    # Documenta projeto específico
   python -m readocs generate --help          # Ver todas as opções

🔧 Configuração:
   - Configure sua ANTHROPIC_API_KEY no arquivo .env
   - O Readocs detectará automaticamente o tipo do seu projeto
   
📚 Documentação completa: README.md

💡 Dica: Use sempre um ambiente virtual para projetos Python!
""")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

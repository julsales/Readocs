from agents.doc_agent import doc_agent
from agents.curation_agent import curation_agent
from agno.team import Team
from agno.models.anthropic import Claude
from datetime import datetime
import re
import os
from pathlib import Path
import sys

from dotenv import load_dotenv

# ========== CONFIGURAÇÃO DO PROJETO ==========
# Ajuste estes caminhos conforme seu projeto:

PROJECT_FOLDER = "readocs"  # Nome da pasta com o código
ROOT_DIR = ".."             # Onde criar README/CHANGELOG (.. = pasta pai)

# Para outros projetos, mude apenas essas variáveis:
# PROJECT_FOLDER = "src"     # ou "app", "backend", etc.
# ROOT_DIR = "."             # ou "../..", etc.

# =============================================

def print_header():
    """Exibe cabeçalho bonito do programa"""
    print("=" * 60)
    print("🚀  READOCS - DOCUMENTAÇÃO AUTOMÁTICA COM IA  🚀")
    print("=" * 60)
    print("📝 Sistema inteligente de geração de documentação")
    print("🤖 Powered by Anthropic Claude AI")
    print("=" * 60)
    print()

def print_step(step, total, message, status="🔄"):
    """Exibe progresso de forma bonita"""
    progress = int((step / total) * 40)
    bar = "█" * progress + "░" * (40 - progress)
    percentage = int((step / total) * 100)
    print(f"{status} [{bar}] {percentage:3d}% | {message}")

def print_success(message):
    """Exibe mensagem de sucesso"""
    print(f"\n✅ {message}")

def print_error(message):
    """Exibe mensagem de erro"""
    print(f"\n❌ {message}")

def print_info(message):
    """Exibe informação"""
    print(f"ℹ️  {message}")

def setup_directories():
    """Configura diretórios de forma inteligente"""
    current = Path.cwd()
    
    print_step(1, 8, "Configurando diretórios do projeto...")
    
    # Se já estamos no diretório que tem o PROJECT_FOLDER, vai para o pai
    if (current / PROJECT_FOLDER).exists():
        target_root = current
        project_path = f"./{PROJECT_FOLDER}"
    
    # Se estamos dentro do PROJECT_FOLDER, sobe um nível  
    elif current.name == PROJECT_FOLDER:
        target_root = current.parent
        project_path = f"./{PROJECT_FOLDER}"
        os.chdir(target_root)
    
    # Caso geral: usa ROOT_DIR configurado
    else:
        target_root = Path(ROOT_DIR).resolve()
        project_path = f"./{PROJECT_FOLDER}"
        os.chdir(target_root)
    
    print(f"📁 Diretório raiz: {os.getcwd()}")
    print(f"🔍 Código analisado: {project_path}")
    print()
    
    return project_path

def get_next_version():
    """Determina a próxima versão baseada no CHANGELOG existente"""
    changelog_path = "CHANGELOG.md"
    
    print_step(2, 8, "Analisando versões existentes...")
    
    if not os.path.exists(changelog_path):
        print_info("CHANGELOG.md não encontrado, iniciando versão 0.0.1")
        return "0.0.1"
    
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Padrão para capturar versões no formato [0.0.1] - YYYY-MM-DD
        version_pattern = r'## \[(\d+)\.(\d+)\.(\d+)\] - \d{4}-\d{2}-\d{2}'
        versions = re.findall(version_pattern, content)
        
        if not versions:
            print_info("Nenhuma versão encontrada no CHANGELOG, iniciando versão 0.0.1")
            return "0.0.1"
        
        # Pega a versão mais alta encontrada
        max_version = (0, 0, 0)
        for version in versions:
            major, minor, patch = map(int, version)
            if (major, minor, patch) > max_version:
                max_version = (major, minor, patch)
        
        major, minor, patch = max_version
        
        # Incrementa patch por padrão
        new_version = f"{major}.{minor}.{patch + 1}"
        print_info(f"Última versão: {major}.{minor}.{patch} → Nova: {new_version}")
        
        return new_version
    
    except Exception as e:
        print_error(f"Erro ao ler CHANGELOG: {e}")
        return "0.0.1"

def check_readme_sections():
    """Verifica se README tem seções duplicadas"""
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        return False
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica títulos duplicados
        lines = content.split('\n')
        sections = []
        duplicates_found = False
        
        for line in lines:
            if line.startswith('## '):
                section = line.strip()
                if section in sections:
                    print(f"⚠️  Seção duplicada encontrada: {section}")
                    duplicates_found = True
                sections.append(section)
        
        return duplicates_found
    
    except Exception as e:
        print_error(f"Erro ao verificar README: {e}")
        return False

# Funções utilitárias que podem ser usadas como ferramentas
def read_file(path: str) -> str:
    """Lê o conteúdo de um arquivo"""
    if not os.path.exists(path):
        return f"⚠️ Arquivo '{path}' não encontrado."
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1", errors="replace") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler '{path}': {e}"

def list_files(directory: str) -> str:
    """Lista todos os arquivos em um diretório"""
    try:
        items = os.listdir(directory)
        return "\n".join(items)
    except Exception as e:
        return f"Erro ao listar arquivos: {e}"

def main():
    print_header()
    
    # Configura diretórios automaticamente
    project_path = setup_directories()
    
    print_step(3, 8, "Carregando configurações...")
    load_dotenv()
    
    # Verifica API key
    if "ANTHROPIC_API_KEY" not in os.environ:
        print_error("Variável ANTHROPIC_API_KEY não definida.")
        print("💡 Defina sua chave API do Claude no arquivo .env")
        print("   Exemplo: ANTHROPIC_API_KEY=sua_chave_aqui")
        return
    
    # Verifica seções duplicadas
    print_step(4, 8, "Verificando documentação existente...")
    has_duplicates = check_readme_sections()
    
    # Determina versão
    next_version = get_next_version()
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    print_step(5, 8, f"Preparando versão {next_version}...")
    
    # Detecta o nome do projeto automaticamente
    project_name = os.path.basename(os.getcwd())
    
    print_step(6, 8, "Iniciando análise com IA...")
    print("🤖 Conectando com Anthropic Claude...")
    
    team = Team(
        mode="coordinate",
        members=[curation_agent, doc_agent],
        model=Claude(
            id="claude-3-haiku-20240307",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        ),
        tools=[read_file, list_files],
        success_criteria="Atualizar automaticamente a documentação técnica com curadoria humana.",
        instructions=[
            "Documentação deve ser clara, concisa e em markdown",
            "Instruções de instalação devem ser precisas e bem explicadas",
            "NUNCA duplicar seções existentes - sempre verificar antes de adicionar",
            "Se encontrar seções duplicadas, unificar em uma única seção",
            "Evitar repetir informações já documentadas",
            "Mantenha o README.md focado na visão geral e o CHANGELOG.md nas mudanças",
            "Mantenha imagens se existirem",
            "Use formatação consistente e profissional",
        ],
        markdown=True
    )
    
    print_step(7, 8, "Executando análise inteligente...")
    
    prompt = f"""
    Você é um agente especialista que deve analisar este projeto e atualizar a documentação.
    
    INFORMAÇÕES DO PROJETO:
    - Nome: {project_name}
    - Versão: {next_version}
    - Data: {current_date}
    - Caminho: {project_path}
    
    VERIFICAÇÃO IMPORTANTE:
    {"⚠️ ATENÇÃO: Seções duplicadas detectadas no README! Unifique-as." if has_duplicates else "✅ README sem duplicações detectadas."}
    
    TAREFAS OBRIGATÓRIAS:
    
    1. ANÁLISE DO PROJETO:
       - Use 'list_files' para mapear a estrutura em '{project_path}'
       - Use 'read_file' para examinar arquivos importantes (main.py, requirements.txt, README.md)
       
    2. ATUALIZAÇÃO DO README.md:
       - Verificar se já existe e ler o conteúdo atual
       - NUNCA duplicar seções existentes
       - Se faltarem seções importantes, adicionar apenas o que falta
       - Manter formatação consistente
       - Focar em clareza e profissionalismo
       
    3. ATUALIZAÇÃO DO CHANGELOG.md:
       - Verificar se já existe uma entrada para versão {next_version}
       - Se não existir, adicionar nova entrada no formato: ## [{next_version}] - {current_date}
       - Se já existir, NÃO duplicar - apenas verificar se está completa
       - Descrever mudanças feitas na documentação
       - Seguir formato Semantic Versioning (MAJOR.MINOR.PATCH)
       - Usar categorias: Adicionado, Alterado, Removido, Corrigido
    
    DIRETRIZES DE QUALIDADE:
    - Seja conciso mas informativo
    - Use português brasileiro
    - Mantenha tom profissional
    - Evite redundâncias
    - Teste mentalmente se faz sentido para um novo usuário
    """
    
    try:
        team.print_response(prompt)
        print_step(8, 8, "Finalizando documentação...", "✅")
        
        print("\n" + "=" * 60)
        print_success("DOCUMENTAÇÃO GERADA COM SUCESSO!")
        print("=" * 60)
        print(f"📄 README.md atualizado")
        print(f"📋 CHANGELOG.md versão {next_version}")
        print(f"📅 Data: {current_date}")
        print("=" * 60)
        
    except Exception as e:
        print_error(f"Erro durante a geração: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
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

# Importa a função de limpeza de duplicatas
try:
    from modules.readme_cleaner import ensure_clean_readme, fix_readme_duplicates
except ImportError:
    def ensure_clean_readme(path="README.md"):
        pass
    def fix_readme_duplicates(path="README.md"):
        return False

# ========== CONFIGURAÇÃO DO PROJETO ==========
PROJECT_FOLDER = "readocs"
ROOT_DIR = ".."
# =============================================

def print_header():
    print("=" * 50)
    print("🚀  READOCS - DOCUMENTAÇÃO PERSONALIZADA  🚀")
    print("=" * 50)
    print()

def print_step(step, total, message):
    print(f"[{step}/{total}] {message}")

def setup_directories():
    current = Path.cwd()
    
    if (current / PROJECT_FOLDER).exists():
        project_path = f"./{PROJECT_FOLDER}"
    elif current.name == PROJECT_FOLDER:
        os.chdir(current.parent)
        project_path = f"./{PROJECT_FOLDER}"
    else:
        os.chdir(Path(ROOT_DIR).resolve())
        project_path = f"./{PROJECT_FOLDER}"
    
    print(f"📁 Analisando: {project_path}")
    return project_path

def get_next_version():
    if not os.path.exists("CHANGELOG.md"):
        return "0.1.0"
    
    try:
        with open("CHANGELOG.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        versions = re.findall(r'## \[(\d+)\.(\d+)\.(\d+)\]', content)
        
        if not versions:
            return "0.1.0"
        
        version_tuples = [tuple(map(int, v)) for v in versions]
        latest_version = max(version_tuples)
        major, minor, patch = latest_version
        return f"{major}.{minor}.{patch + 1}"
    except Exception as e:
        print(f"Erro ao processar CHANGELOG.md: {e}")
        return "0.1.0"

def read_file(path: str) -> str:
    if not os.path.exists(path):
        return f"Arquivo '{path}' não encontrado."
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return f"Erro ao ler '{path}'"

def list_files(directory: str) -> str:
    try:
        files = []
        for root, dirs, filelist in os.walk(directory):
            for file in filelist:
                if file.endswith(('.py', '.md', '.txt', '.yml', '.yaml', '.json')):
                    rel_path = os.path.relpath(os.path.join(root, file), directory)
                    files.append(rel_path)
        return "\n".join(sorted(files))
    except:
        return "Erro ao listar arquivos"

def main():
    print_header()
    
    print_step(1, 5, "Configurando projeto...")
    project_path = setup_directories()
    load_dotenv()
    
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("❌ ANTHROPIC_API_KEY não definida no .env")
        return
    
    print_step(2, 5, "Analisando versão...")
    next_version = get_next_version()
    current_date = datetime.now().strftime("%Y-%m-%d")
    project_name = os.path.basename(project_path)  # Corrigido para usar o path real
    
    print_step(3, 5, "Limpando duplicatas...")
    try:
        if os.path.exists("README.md"):  # Evita erro se README não existe
            ensure_clean_readme("README.md")
            fix_readme_duplicates("README.md")
    except:
        pass
    
    print_step(4, 5, "Conectando com Claude...")
    
    team = Team(
        mode="coordinate",
        members=[curation_agent, doc_agent],
        model=Claude(
            id="claude-3-haiku-20240307",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        ),
        tools=[read_file, list_files],
        success_criteria="Criar documentação específica baseada no código real do projeto.",
        instructions=[
            "Leia e analise o código ANTES de escrever documentação",
            "Use informações REAIS do projeto, não templates genéricos",
            "Documente o que o código realmente faz",
            "Seja específico sobre funcionalidades encontradas",
            "Use português brasileiro e formato markdown"
        ],
        markdown=True
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
        3. Atualize o README.md com uma seção de 'Introdução' (baseada na sua análise) e uma seção de 'Instalação' (com as dependências e instruções para instalar o projeto que você encontrou).
        4. Não é para citar a complexidade do projeto (Não é para citar se é simples ou complexo,etc), mas pode fazer um pequeno pitch sobre o que ele faz na Introdução.
        5. Se identificar uma VENV ou ambiente virtual, adicione instruções para ativá-lo em sistemas operacionais Windows e Linux.

        Diretrizes para o CHANGELOG.md:
            1. Adicione uma nova entrada para a versão {next_version}.
            2. O novo registro deve incluir a data de hoje ({current_date}).
            3. Descreva as mudanças de forma clara e concisa, seguindo o padrão de formatação do CHANGELOG.md existente.
            4. Relate aqui as mudanças que você fez no README.md, como a adição de seções ou melhorias na clareza.
            5. Se não houver mudanças significativas, adicione uma entrada genérica como "Nenhuma mudança significativa".

    IMPORTANTE:
    - ZERO conteúdo genérico ou template
    - Documente apenas o que você encontrar no código
    - Se encontrar agentes, explique o que cada um faz
    - Se encontrar APIs, liste os endpoints reais  
    - Se encontrar funções, documente as principais
    - Baseie tudo na análise real dos arquivos

    Comece analisando os arquivos agora.
    """
    
    print_step(5, 5, "Gerando documentação...")
    
    try:
        team.print_response(prompt)

        # Garante que o CHANGELOG seja incrementado
        changelog_path = "CHANGELOG.md"
        new_entry = f"## [{next_version}] - {current_date}\n- Documentação atualizada automaticamente.\n\n"

        try:
            if not os.path.exists(changelog_path):
                with open(changelog_path, "w", encoding="utf-8") as f:
                    f.write("# Changelog\n\n")
                    f.write(new_entry)
            else:
                with open(changelog_path, "r+", encoding="utf-8") as f:
                    content = f.read()
                    if f"## [{next_version}]" not in content:
                        f.seek(0, 0)
                        f.write(new_entry + content)
        except Exception as e:
            print(f"⚠️ Erro ao atualizar o CHANGELOG.md: {e}")
        
        print(f"\n✅ Documentação gerada!")
        print(f"📄 README.md personalizado")
        print(f"📋 CHANGELOG.md v{next_version}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()

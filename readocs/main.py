from agents.doc_agent import doc_agent
from agents.curation_agent import curation_agent
from agno.team import Team
from agno.models.anthropic import Claude
from datetime import datetime
import re
import os
from pathlib import Path
from dotenv import load_dotenv

# ========== CONFIGURAÇÃO ==========
PROJECT_FOLDER = "readocs"
ROOT_DIR = ".."
# ==================================

def setup_directories():
    current = Path.cwd()
    
    if (current / PROJECT_FOLDER).exists():
        target_root = current
        project_path = f"./{PROJECT_FOLDER}"
    elif current.name == PROJECT_FOLDER:
        target_root = current.parent
        project_path = f"./{PROJECT_FOLDER}"
        os.chdir(target_root)
    else:
        target_root = Path(ROOT_DIR).resolve()
        project_path = f"./{PROJECT_FOLDER}"
        os.chdir(target_root)
    
    print(f"📁 Diretório raiz (arquivos): {os.getcwd()}")
    print(f"🔍 Código para análise: {project_path}")
    
    return project_path

def get_next_version():
    changelog_path = "CHANGELOG.md"
    
    if not os.path.exists(changelog_path):
        return "0.1.0"
    
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        version_pattern = r'## \[(\d+)\.(\d+)\.(\d+)\]'
        versions = re.findall(version_pattern, content)
        
        if not versions:
            return "0.1.0"
        
        major, minor, patch = map(int, versions[0])
        return f"{major}.{minor}.{patch + 1}"
    
    except Exception as e:
        print(f"Erro ao ler CHANGELOG: {e}")
        return "0.1.0"

# ⚠️ Aqui estão suas funções utilitárias
def read_file(path: str) -> str:
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
    try:
        items = os.listdir(directory)
        return "\n".join(items)
    except Exception as e:
        return f"Erro ao listar arquivos: {e}"

def main():
    project_path = setup_directories()
    load_dotenv()

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("⚠️  Defina a variável ANTHROPIC_API_KEY no .env.")
        return

    next_version = get_next_version()
    current_date = datetime.now().strftime("%Y-%m-%d")
    project_name = os.path.basename(os.getcwd())

    # ✅ Executando manualmente (sem usar ferramentas)
    files_list = list_files(project_path)
    main_py = read_file(os.path.join(project_path, "main.py"))
    reqs_txt = read_file(os.path.join(project_path, "requirements.txt"))

    team = Team(
        mode="coordinate",
        members=[curation_agent, doc_agent],
        model=Claude(
            id="claude-3-haiku-20240307",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        ),
        success_criteria="Atualizar automaticamente a documentação técnica com curadoria humana.",
        instructions=[
            "Documentação deve ser clara, concisa e em markdown.",
            "Instruções de instalação devem ser precisas.",
            "Evitar sobrescrever conteúdo útil.",
            "Seções não devem ser duplicadas, caso estejam, o conteúdo deve ser unificado e só uma seção deve permanecer.",
            "Evitar repetir informações já documentadas.",
            "README.md: visão geral; CHANGELOG.md: mudanças.",
            "Mantenha imagens se existirem."
        ],
        markdown=True,
        # 🔥 Não adicionamos `tools=[]`, nem registramos funções
    )

    team.print_response(f"""
    Você é um agente que deve analisar completamente o projeto para gerar a documentação.
    A documentação deve ser toda em português e seguir as diretrizes do projeto.
    Para o README.md, você deve:
    1. Comece com o título sendo o nome do projeto que é '{project_name}'. Apenas a primeira letra do nome do projeto deve ser maiúscula.
    2. Use a ferramenta 'list_files' para ter uma visão geral da estrutura do projeto em '{project_path}'.
    3. Com base na lista de arquivos, use a ferramenta 'read_file' para analisar os arquivos relevantes, como 'main.py' e 'requirements.txt', para entender o propósito e as dependências do projeto.
    4. Atualize o README.md com uma seção de 'Introdução' (baseada na sua análise) e uma seção de 'Instalação' (com as dependências e instruções para instalar o projeto que você encontrou).
    5. Se identificar uma VENV ou ambiente virtual, adicione instruções para ativá-lo em sistemas operacionais Windows e Linux.
    6. Crie uma seção de Funcionalidades que descreva o que o projeto faz, baseado na análise dos arquivos.
    Diretrizes para o CHANGELOG.md:
    1. Adicione uma nova entrada para a versão {next_version}.
    2. O novo registro deve incluir a data de hoje ({current_date}).
    3. A entrada deve ser: "- (Adicionado) Inicialização do sistema de documentação com agentes."
    """)

    print(f"\n✅ Documentação gerada.")
    print(f"📄 Arquivos README.md e CHANGELOG.md atualizados no diretório atual.")

if __name__ == "__main__":
    main()
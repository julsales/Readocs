from agents.doc_agent import doc_agent
from agents.curation_agent import curation_agent
from agno.team import Team
from agno.models.anthropic import Claude
from datetime import datetime
import re
import os
from pathlib import Path

from dotenv import load_dotenv

# ========== CONFIGURAÇÃO DO PROJETO ==========
# Ajuste estes caminhos conforme seu projeto:

PROJECT_FOLDER = "readocs"  # Nome da pasta com o código
ROOT_DIR = ".."             # Onde criar README/CHANGELOG (.. = pasta pai)

# Para outros projetos, mude apenas essas variáveis:
# PROJECT_FOLDER = "src"     # ou "app", "backend", etc.  
# ROOT_DIR = "."             # ou "../..", etc.

# =============================================

def setup_directories():
    """Configura diretórios de forma inteligente"""
    current = Path.cwd()
    
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
    
    print(f"📁 Diretório raiz (arquivos): {os.getcwd()}")
    print(f"🔍 Código para análise: {project_path}")
    
    return project_path

def get_next_version():
    """Determina a próxima versão baseada no CHANGELOG existente"""
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

def main():
    # Configura diretórios automaticamente
    project_path = setup_directories()
    
    load_dotenv()
    
    # Verifica API key
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("⚠️  Variável ANTHROPIC_API_KEY não definida.")
        print("Defina sua chave API do Claude para usar os agentes.")
        return
    
    # Determina versão
    next_version = get_next_version()
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"🏷️  Próxima versão: {next_version}")
    
    # Detecta o nome do projeto automaticamente
    project_name = os.path.basename(os.getcwd())
    
    team = Team(
        mode="coordinate",
        members=[curation_agent, doc_agent],
        model=Claude(
            id="claude-3-haiku-20240307",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        ),
        success_criteria="Atualizar automaticamente a documentação técnica com curadoria humana.",
        instructions=[
            "Documentação deve ser clara, concisa e em markdown",
            "Instruções de instalação devem ser precisas e bem explicadas",
            "Evitar sobrescrever conteúdo útil",
            "Evitar repetir informações já documentadas",
            "Se existirem títulos duplicados, junte os conteúdos e apague um título"
            "Mantenha o README.md focado na visão geral e o CHANGELOG.md nas mudanças",
            "Mantenha imagens se existirem",
        ],
        markdown=True
    )
    
    team.print_response(f"""
    Você é um agente que deve analisar completamente o projeto para gerar a documentação.
    A documentação deve ser toda em português e seguir as diretrizes do projeto.
    Primeiro, coloque o nome do projeto, que é '{project_name}', com a primeira letra sendo a única maiúscula.
    Para fazer o README.md, você deve:
    1. Use a ferramenta 'list_files' para ter uma visão geral da estrutura do projeto em '{project_path}'.
    2. Com base na lista de arquivos, use a ferramenta 'read_file' para analisar os arquivos relevantes, como 'main.py' e 'requirements.txt', para entender o propósito e as dependências do projeto.
    3. Atualize o README.md com uma seção de 'Introdução' (baseada na sua análise) e uma seção de 'Instalação' (com as dependências e instruções para instalar o projeto que você encontrou).
    4. Não é para citar a complexidade do projeto (Não é para citar se é simples ou complexo,etc), mas pode fazer um pequeno pitch sobre o que ele faz na Introdução.
    5. Se identificar uma VENV ou ambiente virtual, adicione instruções para ativá-lo em sistemas operacionais Windows e Linux.
    6. Se houver imagens, mantenha-as no README.md, mas não é necessário criar uma seção de imagens, apenas mantenha as imagens que já existirem.

    Diretrizes para o CHANGELOG.md:
    1. Adicione uma nova entrada para a versão {next_version}.
    2. O novo registro deve incluir a data de hoje ({current_date}).
    3. Descreva as mudanças de forma clara e concisa, seguindo o padrão de formatação do CHANGELOG.md existente.
    4. Relate aqui as mudanças que você fez no README.md, como a adição de seções ou melhorias na clareza.
    5. Se não houver mudanças significativas, adicione uma entrada genérica como "Nenhuma mudança significativa".
    """)

main()
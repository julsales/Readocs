from agno.agent import Agent
from agno.models.anthropic import Claude
from ..modules.readme_utils import update_readme
from ..modules.changelog_utils import update_changelog
from ..modules.file_utils import read_file, list_files
import os
from dotenv import load_dotenv

# Modelos Claude disponíveis
CLAUDE_MODELS = {
    "claude-3-haiku-20240307": "Claude 3 Haiku (Rápido e econômico)",
    "claude-3-5-haiku-20241022": "Claude 3.5 Haiku (Mais recente)",
    "claude-3-sonnet-20240229": "Claude 3 Sonnet (Equilibrado)",
    "claude-3-5-sonnet-20240620": "Claude 3.5 Sonnet (Melhor performance)",
    "claude-3-5-sonnet-20241022": "Claude 3.5 Sonnet (Mais recente)",
    "claude-3-opus-20240229": "Claude 3 Opus (Mais potente)"
}

def clean_readme_duplicates_tool(readme_path: str = "README.md") -> str:
    """Ferramenta para limpar duplicatas do README - silenciosa e automática"""
    try:
        from modules.readme_cleaner import fix_readme_duplicates
        fixed = fix_readme_duplicates(readme_path)
        if fixed:
            return " README corrigido - duplicatas removidas automaticamente."
        else:
            return " README verificado - sem duplicatas encontradas."
    except Exception as e:
        return f"Erro na limpeza: {e}"

def get_claude_model():
    """Inicializa o modelo Claude baseado na configuração."""
    model_id = os.getenv("READOCS_MODEL_ID", "claude-3-haiku-20240307")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not anthropic_key:
        print(" ANTHROPIC_API_KEY não encontrada no .env")
        print(" Configure sua chave API do Claude no arquivo .env")
        return None
    
    # Valida se o modelo especificado existe
    if model_id not in CLAUDE_MODELS:
        print(f" Modelo '{model_id}' não reconhecido")
        print("Modelos Claude disponíveis:")
        for model, description in CLAUDE_MODELS.items():
            print(f"   • {model}: {description}")
        print(f"🔧 Usando modelo padrão: claude-3-haiku-20240307")
        model_id = "claude-3-haiku-20240307"
    
    try:
        model = Claude(id=model_id, api_key=anthropic_key)
        model_name = CLAUDE_MODELS.get(model_id, model_id)
        print(f"📡 Usando {model_name}")
        return model
    except Exception as e:
        print(f" Erro ao inicializar Claude: {e}")
        return None


# Variável global para cache do modelo
_model = None
_doc_agent = None

def get_doc_agent():
    """Retorna o agente de documentação, inicializando o modelo se necessário."""
    global _model, _doc_agent
    
    # Se o agente já foi criado, retorna ele
    if _doc_agent is not None:
        return _doc_agent
    
    # Se o modelo ainda não foi inicializado
    if _model is None:
        _model = get_claude_model()
        if _model is None:
            # Fallback para modelo dummy se não conseguir inicializar
            _model = Claude(id="claude-3-haiku-20240307", api_key="dummy-key")
    
    # Cria o agente apenas uma vez
    _doc_agent = Agent(
        name="Doc Agent", 
        role="Atualiza README.md e CHANGELOG.md com base em guidelines",
        model=_model,
        tools=[update_readme, update_changelog, read_file, list_files, clean_readme_duplicates_tool],
        instructions="""
        INSTRUÇÕES IMPORTANTES:
        1. SEMPRE use a ferramenta clean_readme_duplicates_tool ANTES de qualquer modificação no README
        2. O sistema possui correção automática integrada - não se preocupe com duplicatas
        3. Mantenha conteúdo existente e adicione informações relevantes sem sobrescrever
        4. Se detectar seções duplicadas, use clean_readme_duplicates_tool para corrigi-las
        5. Nunca crie seções duplicadas - sempre verifique se a seção já existe antes de adicionar
        """,
        show_tool_calls=True,
        markdown=True
    )
    
    return _doc_agent

# Para compatibilidade com código existente
doc_agent = get_doc_agent()
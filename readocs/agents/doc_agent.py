from agno.agent import Agent
from agno.models.anthropic import Claude
from ..modules.readme_utils import update_readme
from ..modules.changelog_utils import update_changelog
from ..modules.file_utils import read_file, list_files
import os

def clean_readme_duplicates_tool(readme_path: str = "README.md") -> str:
    """Ferramenta para limpar duplicatas do README - silenciosa e automática"""
    try:
        from modules.readme_cleaner import fix_readme_duplicates
        fixed = fix_readme_duplicates(readme_path)
        if fixed:
            return "✅ README corrigido - duplicatas removidas automaticamente."
        else:
            return "✅ README verificado - sem duplicatas encontradas."
    except Exception as e:
        return f"⚠️ Erro na limpeza: {e}"

model_id = os.getenv("READOCS_MODEL_ID", "claude-3-haiku-20240307")

doc_agent = Agent(
    name="Doc Agent", 
    role="Atualiza README.md e CHANGELOG.md com base em guidelines",
    model=Claude(
    id=model_id,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    ),
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
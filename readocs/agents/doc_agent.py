from agno.agent import Agent
from agno.models.anthropic import Claude  
import os

curation_agent = Agent(
    name="Curation Agent",
    role="Valida se as atualizações seguem as guidelines da equipe",
    model=Claude(
        id="claude-3-haiku-20240307",  
        api_key=os.getenv("ANTHROPIC_API_KEY")
    ),
    instructions="Não modifique o conteúdo. Apenas valide se as atualizações seguem as diretrizes da equipe e aprove a saída.",  # Instrução de validação
    show_tool_calls=False,
    markdown=True
)
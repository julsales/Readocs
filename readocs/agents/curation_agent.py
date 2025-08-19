from agno.agent import Agent
from agno.models.anthropic import Claude  
import os

_curation_agent_instance = None

def curation_agent():
    """Retorna instância do curation_agent, criando apenas quando necessário."""
    global _curation_agent_instance
    if _curation_agent_instance is None:
        _curation_agent_instance = Agent(
            name="Curation Agent",
            role="Valida se as atualizações seguem as guidelines da equipe",
            model=Claude(
                id=os.getenv("READOCS_MODEL_ID", "claude-3-haiku-20240307"),  
                api_key=os.getenv("ANTHROPIC_API_KEY")
            ),
            instructions="Não modifique o conteúdo. Apenas valide se as atualizações seguem as diretrizes da equipe e aprove a saída.",
            show_tool_calls=False,
            markdown=True
        )
    return _curation_agent_instance
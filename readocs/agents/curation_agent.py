from agno.agent import Agent
from agno.models.google import Gemini

curation_agent = Agent(
    name="Curation Agent",
    role="Valida se as atualizações seguem as guidelines da equipe",
    model=Gemini(id="gemini-2.5-flash-lite"),
    instructions="Não modifique o conteúdo. Apenas valide se as atualizações seguem as diretrizes da equipe e aprove a saída.", # Instrução de validação
    show_tool_calls=False,
    markdown=True
)

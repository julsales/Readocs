from agno.agent import Agent
from agno.models.openai import OpenAIChat

curation_agent = Agent(
    name="Curation Agent",
    role="Valida se as atualizações seguem as guidelines da equipe",
    model=OpenAIChat(id="gpt-4o"),
    instructions="Garanta que tudo siga a curadoria humana. Faça revisão antes do push.",
    show_tool_calls=False,
    markdown=True
)

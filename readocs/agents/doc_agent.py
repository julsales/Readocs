from agno.agent import Agent
from agno.models.openai import OpenAIChat
from modules.readme_utils import update_readme
from modules.changelog_utils import update_changelog

doc_agent = Agent(
    name="Doc Agent",
    role="Atualiza README.md e CHANGELOG.md com base em guidelines",
    model=OpenAIChat(id="gpt-4o"),
    tools=[update_readme, update_changelog],
    instructions="Mantenha conteúdo existente e adicione informações relevantes sem sobrescrever.",
    show_tool_calls=True,
    markdown=True
)
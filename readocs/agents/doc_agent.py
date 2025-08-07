from agno.agent import Agent
from agno.models.anthropic import Claude  # Mudança aqui!
from modules.readme_utils import update_readme
from modules.changelog_utils import update_changelog
from modules.file_utils import read_file, list_files
import os

doc_agent = Agent(
    name="Doc Agent",
    role="Atualiza README.md e CHANGELOG.md com base em guidelines",
    model=Claude(
        id="claude-3-haiku-20240307",  # Modelo mais barato
        api_key=os.getenv("ANTHROPIC_API_KEY")
    ),
    tools=[update_readme, update_changelog, read_file, list_files],
    instructions="Mantenha conteúdo existente e adicione informações relevantes sem sobrescrever.",
    show_tool_calls=True,
    markdown=True
)
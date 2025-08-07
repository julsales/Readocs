from agno.agent import Agent
from agno.models.google import Gemini
from modules.readme_utils import update_readme
from modules.changelog_utils import update_changelog
from modules.file_utils import read_file, list_files

doc_agent = Agent(
    name="Doc Agent",
    role="Atualiza README.md e CHANGELOG.md com base em guidelines",
    model=Gemini(id="gemini-2.5-flash-lite"),
    tools=[update_readme, update_changelog, read_file,list_files],
    instructions="Mantenha conteúdo existente e adicione informações relevantes sem sobrescrever.",
    show_tool_calls=True,
    markdown=True
)
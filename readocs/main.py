from agents.doc_agent import doc_agent
from agents.curation_agent import curation_agent
from agno.team import Team
from agno.models.google import Gemini

from dotenv import load_dotenv
import os

load_dotenv()

# Certifique-se de que a variável de ambiente GOOGLE_API_KEY está definida.
# Se você estiver usando o modelo Gemini, o AGNO buscará a chave aqui.
if "GOOGLE_API_KEY" not in os.environ:
    print("Atenção: A variável de ambiente 'GOOGLE_API_KEY' não está definida.")
    print("Por favor, defina-a com sua chave de API do Gemini para que o código funcione.")

team = Team(
    mode="coordinate",
    members=[curation_agent, doc_agent],
    model=Gemini(id="gemini-1.5-flash-latest"),  # Usando o modelo Gemini.
    success_criteria="Atualizar automaticamente a documentação técnica com curadoria humana.",
    instructions=["Documentação deve ser clara, concisa e em markdown", "Evitar sobrescrever conteúdo útil"],
    markdown=True
)

team.print_response("Atualize a documentação do projeto Readocs com base nos padrões definidos.")
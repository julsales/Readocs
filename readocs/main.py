from agents.doc_agent import doc_agent
from agents.curation_agent import curation_agent
from agno.team import Team
from agno.models.google import Gemini
from dotenv import load_dotenv
import os

print(f"O diretório de trabalho atual é: {os.getcwd()}")

load_dotenv()

# Certifique-se de que a variável de ambiente GOOGLE_API_KEY está definida.
# Se você estiver usando o modelo Gemini, o AGNO buscará a chave aqui.
if "GOOGLE_API_KEY" not in os.environ:
    print("Atenção: A variável de ambiente 'GOOGLE_API_KEY' não está definida.")
    print("Por favor, defina-a com sua chave de API do Gemini para que o código funcione.")

team = Team(
    mode="coordinate",
    members=[curation_agent, doc_agent],
    model=Gemini(id="gemini-2.5-flash-lite"),  # Usando o modelo Gemini.
    success_criteria="Atualizar automaticamente a documentação técnica com curadoria humana.",
    instructions=["Documentação deve ser clara, concisa e em markdown", "Evitar sobrescrever conteúdo útil"],
    markdown=True
)

team.print_response("""
    Você é um agente que deve analisar completamente o projeto para gerar a documentação.
    Para o README.md, você deve:
    1. Use a ferramenta 'list_files' para ter uma visão geral da estrutura do projeto.
    2. Com base na lista de arquivos, use a ferramenta 'read_file' para analisar os arquivos relevantes, como 'main.py' e 'requirements.txt', para entender o propósito e as dependências do projeto.
    3. Atualize o README.md com uma seção de 'Introdução' (baseada na sua análise) e uma seção de 'Instalação' (com as dependências que você encontrou).

    Diretrizes para o CHANGELOG.md:
    1. Adicione uma nova entrada para a versão 0.1.0.
    2. O novo registro deve incluir a data de hoje.
    3. A entrada deve ser: "- (Adicionado) Inicialização do sistema de documentação com agentes."
""")
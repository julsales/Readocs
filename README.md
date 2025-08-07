# Readocs

## Introdução
readocs é um sistema de documentação automatizada usando agentes de inteligência artificial. O projeto utiliza a biblioteca Anthropic para acessar o modelo de linguagem Claude e gerar documentação técnica de forma inteligente e curada.

O sistema é composto por dois agentes principais:
- **Doc Agent**: Responsável por analisar o projeto e gerar a documentação técnica, como README.md e CHANGELOG.md.
- **Curation Agent**: Responsável por revisar e aprimorar a documentação gerada pelo Doc Agent, garantindo que siga as diretrizes do projeto.

## Instalação
Para instalar e executar o projeto readocs, siga as instruções abaixo:

1. Certifique-se de ter o Python 3.x instalado em seu sistema.
2. Crie um ambiente virtual (recomendado):
   - **Windows**: `python -m venv venv` e depois `venv\Scripts\activate`
   - **Linux/macOS**: `python3 -m venv venv` e depois `source venv/bin/activate`
3. Instale as dependências do projeto:
   - Não foi possível encontrar um arquivo `requirements.txt`, então você precisará instalar as dependências manualmente. Elas incluem:
     - [Anthropic](https://www.anthropic.com/)
     - [python-dotenv](https://github.com/theskumar/python-dotenv)
4. Defina a variável de ambiente `ANTHROPIC_API_KEY` com sua chave de API do Anthropic.
5. Execute o script `main.py` para gerar a documentação automatizada.

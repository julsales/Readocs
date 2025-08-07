# Readocs

## Introdução
## Introdução
O projeto `readocs` é um sistema de documentação técnica automatizada utilizando agentes de inteligência artificial. Ele inclui dois agentes principais:

- `doc_agent`: Responsável por gerar e atualizar a documentação técnica do projeto.
- `curation_agent`: Responsável por revisar e curar a documentação gerada pelo `doc_agent`.

O projeto é configurado com algumas variáveis como `PROJECT_FOLDER` e `ROOT_DIR` que podem ser ajustadas para outros projetos.

## Instalação
## Instalação

Dependências:
- Python 3.x
- Bibliotecas Python listadas em `requirements.txt`

Para instalar o projeto, siga os seguintes passos:

1. Certifique-se de ter o Python 3.x instalado em seu sistema.
2. Crie um ambiente virtual (recomendado):
   - **Windows**: `python -m venv venv` e `venv\Scripts\activate`
   - **Linux/macOS**: `python3 -m venv venv` e `source venv/bin/activate`
3. Instale as dependências do projeto:
   ```
   pip install -r requirements.txt
   ```
4. Defina a variável de ambiente `ANTHROPIC_API_KEY` com sua chave de API do Claude.
5. Execute o script `main.py` para gerar a documentação.

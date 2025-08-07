# Readocs

## Introdução
O projeto Readocs é uma aplicação Python que utiliza uma equipe de agentes inteligentes para gerar automaticamente a documentação de projetos, incluindo um README.md e um CHANGELOG.md. O objetivo é manter a documentação atualizada e alinhada com as melhores práticas.

Os principais componentes do projeto são:

- Módulos de agentes inteligentes (doc_agent, curation_agent) que utilizam a API da Anthropic (modelo Claude) para gerar respostas em markdown.
- Um sistema de gerenciamento de equipe (agno.Team) para coordenar a atuação dos agentes.
- Lógica em `main.py` para configurar o ambiente, determinar a próxima versão e executar os agentes.

## Instalação
## Instalação

Para instalar e executar o projeto Readocs, siga as instruções abaixo:

1. Certifique-se de ter o Python 3.x instalado em seu sistema.
2. Crie e ative um ambiente virtual (VENV) para isolar as dependências do projeto:
   - **Windows:**
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Instale as dependências do projeto:
   ```
   pip install -r requirements.txt
   ```
4. Defina a variável de ambiente `ANTHROPIC_API_KEY` com sua chave de API da Anthropic.
5. Execute o script `main.py` para gerar a documentação:
   ```
   python main.py
   ```

O README.md e o CHANGELOG.md serão atualizados no diretório raiz do projeto.

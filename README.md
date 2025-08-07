# Readocs

## Introdução
O projeto "readocs" é uma ferramenta automatizada de geração de documentação técnica. Ele utiliza uma equipe de agentes inteligentes (definidos no arquivo `main.py`) para analisar o código-fonte do projeto e gerar um README.md e um CHANGELOG.md atualizados.

Os agentes seguem algumas diretrizes específicas para manter a documentação clara, concisa e bem estruturada. Eles evitam sobrescrever conteúdo útil e mantêm o foco da documentação em uma visão geral do projeto e nas principais mudanças.

## Instalação
## Instalação

Para instalar e executar o projeto "readocs", siga as instruções abaixo:

1. Certifique-se de ter o Python 3.x instalado em seu sistema.
2. Crie e ative um ambiente virtual (VENV):

   **Windows:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux/macOS:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências do projeto:
   ```
   pip install -r requirements.txt
   ```

4. Defina a variável de ambiente `ANTHROPIC_API_KEY` com sua chave de API do Claude.
5. Execute o script principal:
   ```
   python main.py
   ```

Pronto! O projeto "readocs" está instalado e pronto para uso.

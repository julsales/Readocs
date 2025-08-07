# Readocs

## Introdução
O projeto `readocs` é uma ferramenta que utiliza agentes de inteligência artificial (AI) para automatizar a atualização da documentação técnica de um projeto. Ele inclui um agente de curadoria e um agente de documentação que trabalham em conjunto para manter a documentação clara, concisa e atualizada, seguindo diretrizes pré-definidas. O projeto é construído usando a API do Claude, um modelo de linguagem da Anthropic.

## Instalação
Para instalar e utilizar o projeto `readocs`, siga estas etapas:

1. Certifique-se de ter o Python 3.x instalado em seu sistema.
2. Crie um ambiente virtual (venv) para isolar as dependências do projeto:
   - **Windows**: `python -m venv venv` e `venv\Scripts\activate`
   - **Linux/macOS**: `python3 -m venv venv` e `source venv/bin/activate`
3. Instale as dependências do projeto:
   ```
   pip install -r requirements.txt
   ```
4. Defina a variável de ambiente `ANTHROPIC_API_KEY` com sua chave de API do modelo Claude.
5. Execute o script `main.py` para gerar e atualizar automaticamente a documentação do projeto.

## Recursos
- Geração automatizada de documentação a partir de comentários no código
- Integração com ferramentas de CI/CD para atualização contínua da documentação
- Interface web responsiva para visualização da documentação
- Suporte a múltiplos formatos de saída (HTML, PDF, Markdown)

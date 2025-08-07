# Readocs

## Introdução
Este é um projeto de agentes que tem como objetivo atualizar automaticamente a documentação técnica com curadoria humana. O código principal está localizado no diretório `./readocs` e inclui os seguintes arquivos:

- `main.py`: O arquivo principal que configura os agentes e gera a documentação.
- `agents/`: Diretório com os agentes responsáveis pela geração e atualização da documentação.

## Instalação
Para instalar e executar este projeto, siga as etapas abaixo:

1. Certifique-se de ter o Python 3.x instalado em seu sistema.
2. Clone este repositório para o seu computador.
3. Navegue até o diretório do projeto (`./readocs`) no terminal.
4. Crie e ative um ambiente virtual (virtualenv, venv, etc).
   - No Windows, execute `python -m venv venv` e depois `venv\Scripts\activate`.
   - No Linux/macOS, execute `python3 -m venv venv` e depois `source venv/bin/activate`.
5. Instale as dependências do projeto:
   - Não foi possível encontrar um arquivo `requirements.txt`, então você precisará instalar manualmente as dependências necessárias.
6. Configure a variável de ambiente `ANTHROPIC_API_KEY` com sua chave da API do Anthropic.
7. Execute o arquivo `main.py` para gerar a documentação automaticamente.

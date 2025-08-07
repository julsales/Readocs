# Readocs

## Introdução
O Readocs é um projeto que utiliza agentes de IA para automatizar a geração e atualização da documentação de projetos. Ele é composto por módulos reutilizáveis e agentes especializados em diferentes tarefas, como curadoria e geração de documentação.

O objetivo do Readocs é facilitar o processo de manutenção da documentação técnica, tornando-o mais eficiente e preciso. Ele analisa a estrutura do projeto, suas dependências e características, e então atualiza automaticamente o README.md e o CHANGELOG.md com as informações relevantes.

## Instalação
## Instalação

O Readocs requer as seguintes dependências:

- Python 3.7 ou superior
- Bibliotecas especificadas no arquivo `requirements.txt`

Para instalar as dependências, siga as instruções abaixo:

1. Crie um ambiente virtual (recomendado):

   - **Windows**:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure a chave da API do Anthropic:
   - Defina a variável de ambiente `ANTHROPIC_API_KEY` com a sua chave de API.

4. Execute o projeto:
   ```
   python main.py
   ```

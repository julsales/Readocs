# Readocs

## Introdução
Readocs é um projeto que visa automatizar a geração e manutenção da documentação técnica de um projeto. Ele utiliza uma equipe de agentes inteligentes para analisar o código-fonte, identificar funcionalidades e dependências, e atualizar automaticamente o conteúdo do README.md e CHANGELOG.md.

O objetivo principal do Readocs é facilitar o processo de documentação, garantindo que a documentação esteja sempre atualizada e alinhada com o código-fonte do projeto.

## Instalação
## Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pipenv (opcional, para criar e gerenciar um ambiente virtual)

### Instruções
1. Clone o repositório:
```
git clone https://github.com/seu-usuario/readocs.git
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   - Windows:
     ```
     cd readocs
     python -m venv venv
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```
     cd readocs
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto e adicione a seguinte variável de ambiente:
```
ANTHROPIC_API_KEY=sua_chave_api_aqui
```

5. Execute o projeto:
```
python main.py
```

## Funcionalidades
## Funcionalidades

O Readocs é capaz de:

- Analisar automaticamente o código-fonte do projeto e identificar suas funcionalidades.
- Gerar e atualizar automaticamente o conteúdo do arquivo README.md, incluindo seções como Introdução, Instalação e Funcionalidades.
- Gerar e atualizar automaticamente o arquivo CHANGELOG.md, registrando as alterações no projeto.
- Utilizar uma equipe de agentes inteligentes para garantir que a documentação esteja clara, concisa e alinhada com as diretrizes do projeto.

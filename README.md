{{BADGE_SECTION}}
# readocs

## Introdução
O projeto 'readocs' é uma solução automatizada para atualizar a documentação técnica de um projeto, incluindo o README.md e o CHANGELOG.md. Ele utiliza uma equipe de agentes (curation_agent e doc_agent) da biblioteca Agno, que são responsáveis por analisar o código-fonte e as dependências do projeto, e gerar a documentação de forma clara e concisa.

O objetivo é manter a documentação sempre atualizada e alinhada com as melhores práticas, evitando a sobrescrita de conteúdo útil e repetição de informações.

## Instalação
Antes de instalar o projeto, certifique-se de ter as seguintes dependências instaladas:

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

Para instalar o projeto, siga os seguintes passos:

1. Clone o repositório do projeto:
```
git clone https://github.com/seu-usuario/readocs.git
```

2. Navegue até o diretório do projeto:
```
cd readocs
```

3. Crie e ative um ambiente virtual (VENV) usando o Python:

**Windows**:
```
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**:
```
python3 -m venv venv
source venv/bin/activate
```

4. Instale as dependências do projeto:
```
pip install -r requirements.txt
```

5. Execute o script principal:
```
python main.py
```

Pronto! Agora você pode utilizar o projeto 'readocs' em seu ambiente de desenvolvimento.

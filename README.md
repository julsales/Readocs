# Readocs

## Introdução
O projeto 'readocs' é um sistema de documentação automatizado que utiliza uma equipe de agentes de Inteligência Artificial para gerar e manter a documentação técnica de um projeto. Ele faz uso da biblioteca 'agno' para orquestrar os agentes, que incluem um agente de documentação e um agente de curadoria.

O ponto de entrada do projeto é o arquivo 'main.py', que é responsável por configurar os diretórios, determinar a próxima versão do projeto e inicializar a equipe de agentes. Os agentes são configurados com instruções específicas para gerar a documentação, seguindo diretrizes como clareza, concisão e uso de Markdown.

## Instalação
## Instalação

O projeto 'readocs' não possui um arquivo centralizado de dependências (como `requirements.txt`). No entanto, é provável que ele utilize algumas bibliotecas Python, como a `agno` mencionada no código.

Para instalar o projeto, siga estas etapas:

1. Clone o repositório do projeto:
```
git clone https://github.com/seu-usuario/readocs.git
```

2. Crie e ative um ambiente virtual (recomendado):

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

3. Instale as dependências necessárias:
```
pip install -r requirements.txt
```

4. Execute o script principal:
```
python main.py
```

Observe que, como não foi encontrado um arquivo `requirements.txt`, você pode precisar instalar manualmente as bibliotecas utilizadas pelo projeto, como a `agno`.

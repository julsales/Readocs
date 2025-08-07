# Readocs

## Introdução
Este projeto é um sistema de documentação automatizada que utiliza agentes de Inteligência Artificial para gerar e manter a documentação técnica do projeto.

O código principal está localizado na pasta 'readocs' e inclui os seguintes módulos:
- `agents`: contém os agentes responsáveis pela geração e curadoria da documentação
- `main.py`: script principal que coordena a atuação dos agentes

O projeto utiliza a API do Claude, um modelo de linguagem da Anthropic, para executar as tarefas de documentação. Antes de executar o projeto, é necessário configurar a variável de ambiente `ANTHROPIC_API_KEY` com sua chave de API do Claude.

## Instalação
## Instalação

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/readocs.git
```

2. Crie e ative um ambiente virtual (recomendado):
```
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Defina a variável de ambiente `ANTHROPIC_API_KEY` com sua chave de API do Claude.

5. Execute o script principal:
```
python main.py
```

E pronto, o sistema de documentação automatizada está configurado e pronto para uso!

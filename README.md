# Readocs

## Introdução
O projeto **Readocs** é uma ferramenta que utiliza agentes de inteligência artificial para automatizar a geração e atualização da documentação técnica de um projeto de software. Ele é capaz de analisar o código-fonte, as dependências e a estrutura do projeto para gerar um README.md e um CHANGELOG.md atualizados.

O sistema é composto por dois agentes principais:
- **Agente de Documentação**: Responsável por analisar o código-fonte e gerar a documentação inicial.
- **Agente de Curadoria**: Revisa a documentação gerada e a aprimora, seguindo as diretrizes do projeto.

Essa abordagem permite manter a documentação atualizada de forma automática e consistente, facilitando a compreensão e a manutenção do projeto por parte dos desenvolvedores e usuários.

## Instalação
Para utilizar o Readocs, é necessário ter o Python 3.x instalado em seu sistema.

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

3. Instale as dependências do projeto:

```
pip install -r requirements.txt
```

4. Defina a variável de ambiente `ANTHROPIC_API_KEY` com sua chave de API do Anthropic:

```
# Windows
set ANTHROPIC_API_KEY=sua-chave-api

# Linux/macOS
export ANTHROPIC_API_KEY=sua-chave-api
```

5. Execute o script principal:

```
python main.py
```

O Readocs irá gerar automaticamente o README.md e o CHANGELOG.md com base na análise do seu projeto.

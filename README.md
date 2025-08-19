# Readocs 

<div align="center">

<img width="250" height="250" alt="Readocs Logo" src="https://github.com/user-attachments/assets/9545feb4-e2e2-4ff4-af61-514f814cd564" />

**🚀 Gerador inteligente de documentação usando IA para qualquer projeto**

</div>

## 📋 Introdução

O **Readocs** é uma ferramenta universal que utiliza inteligência artificial para analisar automaticamente qualquer projeto de código e gerar documentação personalizada e precisa. Ele funciona com projetos Python, Node.js, React, Java, .NET, Go, Rust e muitos outros.

### ✨ Principais Características

- **🤖 Análise Inteligente**: Detecta automaticamente o tipo de projeto e suas dependências
- **📝 Documentação Personalizada**: Gera README.md e CHANGELOG.md baseados no código real
- **🌍 Universal**: Funciona com qualquer linguagem de programação
- **🔧 Flexível**: CLI simples com opções configuráveis
- **🎯 Preciso**: Zero conteúdo genérico - apenas informações reais do projeto

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Chave API do Anthropic (Claude)

### Instalação Automática (Recomendada) 🎯

```bash
# Clone o repositório
git clone https://github.com/julsales/Readocs.git
cd readocs

# Execute o setup automático
python setup.py
```

**O script de setup irá:**
- Verificar se você tem uma venv existente
- Instalar todas as dependências  
- Configurar o arquivo `.env` com a chave da API 

### Instalação Manual

```bash
# Clone o repositório
git clone https://github.com/julsales/Readocs.git
cd readocs

# Crie e ative um ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Configuração da API
Crie um arquivo `.env` seguindo o padrão do arquivo .env.example :
```env
ANTHROPIC_API_KEY=sua_chave_api_aqui

```

## 💻 Como Usar

### Uso Básico

```bash
# Documentar o projeto atual
python -m readocs generate

# Documentar um projeto específico
python -m readocs generate /caminho/para/projeto

# Documentar com saída em diretório específico
python -m readocs generate /projeto --output /docs

# Modo de teste (sem modificar arquivos)
python -m readocs generate --dry-run
```

### Exemplos Práticos

```bash
# Documentar um projeto Python
python -m readocs generate ./meu-projeto-python

# Documentar um projeto Node.js
python -m readocs generate ./meu-app-react

# Documentar múltiplos projetos
for project in projeto1 projeto2 projeto3; do
    python -m readocs generate ./$project
done
```

### Opções Disponíveis

- `--output, -o`: Diretório de saída para a documentação
- `--model`: Modelo Claude a usar (padrão: claude-3-haiku-20240307)
- `--dry-run`: Executa análise sem modificar arquivos
- `--skip-clean`: Pula limpeza de duplicatas no README
- `--skip-changelog`: Não atualiza o CHANGELOG.md

## 🛠️ Tipos de Projeto Suportados

O Readocs detecta automaticamente e adapta a documentação para:

- **Python**: Detecta setup.py, pyproject.toml, requirements.txt
- **Node.js**: Analisa package.json, dependências npm
- **React/Next.js**: Identifica frameworks JavaScript
- **Java**: Processa arquivos .java e pom.xml
- **C#/.NET**: Analisa arquivos .cs e .csproj
- **Go**: Detecta go.mod e arquivos .go
- **Rust**: Processa Cargo.toml
- **Docker**: Identifica Dockerfile e docker-compose.yml

## 📁 Estrutura do Projeto

```
readocs/
├── readocs/
│   ├── __init__.py          # Módulo principal
│   ├── cli.py              # Interface de linha de comando
│   ├── main.py             # Lógica principal
│   ├── ui.py               # Interface de usuário
│   ├── agents/             # Agentes de IA
│   │   ├── doc_agent.py    # Agente de documentação
│   │   └── curation_agent.py # Agente de curadoria
│   └── modules/            # Módulos auxiliares
│       ├── readme_utils.py
│       ├── changelog_utils.py
│       ├── file_utils.py
│       └── readme_cleaner.py
├── examples/               # Exemplos de uso
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```env
# Configurações da API
ANTHROPIC_API_KEY=sua_chave_api_aqui

# Configurações padrão
READOCS_MODEL_ID=claude-3-haiku-20240307
READOCS_DRY_RUN=0
READOCS_SKIP_CLEAN=0
READOCS_SKIP_CHANGELOG=0
```

## 🤝 Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 🆘 Suporte

- **Issues**: Reporte bugs e solicite features no [GitHub Issues]
- **Discussões**: Participe das discussões no [GitHub Discussions]

---

<div align="center">
Desenvolvido com ❤️ usando IA para tornar a documentação de código mais inteligente
</div>

<div align="center">
    
# Readocs 
    
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
Crie um arquivo `.env` seguindo o padrão do arquivo `.env.example` :
```env
ANTHROPIC_API_KEY=sua_chave_api_aqui

READOCS_MODEL_ID= id_do_modelo

# Executar em modo de teste sem modificar arquivos (0=não, 1=sim)
READOCS_DRY_RUN=0

# Pular limpeza automática de duplicatas (0=não, 1=sim)
READOCS_SKIP_CLEAN=0

# Pular criação/atualização do CHANGELOG.md (0=não, 1=sim)
READOCS_SKIP_CHANGELOG=0

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

## Introdução
O Readocs é uma ferramenta poderosa que facilita a criação e manutenção de documentação de projetos. Com recursos avançados de edição, colaboração e publicação, o Readocs se destaca como a escolha ideal para manter sua documentação atualizada e acessível.

## Instalação
1. Baixe o pacote do Readocs a partir do [link de download](https://example.com/readocs-download).
2. Descompacte o arquivo em um diretório de sua escolha.
3. Execute o script de instalação para configurar o Readocs em seu sistema.
4. Siga as instruções na tela para concluir a instalação.

## Uso
1. Abra o Readocs após a instalação.
2. Crie um novo projeto ou abra um projeto existente.
3. Utilize as ferramentas de edição para criar e atualizar a documentação do seu projeto.
4. Personalize as configurações e layouts de acordo com suas necessidades.
5. Publique sua documentação para torná-la acessível a sua equipe e usuários.

## Tipos de Projeto Suportados
O Readocs é compatível com uma ampla variedade de tipos de projeto, incluindo:
- Aplicativos web
- Bibliotecas e APIs
- Sistemas embarcados
- Aplicativos móveis
- Projetos de ciência de dados
- E muito mais!

## Estrutura do Projeto
O Readocs organiza a documentação do projeto em uma estrutura hierárquica, com as seguintes seções padrão:
- Visão Geral
- Guia de Início Rápido
- Referência da API
- Tutoriais
- Guia do Desenvolvedor
- Perguntas Frequentes

## Configuração Avançada
O Readocs permite que você personalize ainda mais a documentação do seu projeto:
- Definir estilos e layouts personalizados
- Integrar com sistemas de controle de versão
- Configurar fluxos de trabalho de publicação
- Habilitar recursos de busca e navegação avançados
- Integrar com ferramentas de colaboração e revisão

## Como Contribuir
Sua contribuição é muito bem-vinda! Siga estas etapas para começar:
1. Faça um fork do repositório do Readocs
2. Crie uma nova branch para suas alterações
3. Implemente suas melhorias e corrija quaisquer problemas
4. Envie um pull request detalhando suas contribuições
5. Aguarde a revisão e incorporação de sua contribuição

## Licença
O Readocs é distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Suporte
Se você precisar de ajuda ou tiver dúvidas sobre o Readocs, entre em contato conosco:
- Envie um e-mail para suporte@readocs.com
- Acesse nosso [FAQ](https://readocs.com/faq) para obter respostas a perguntas comuns
- Abra uma nova [issue no GitHub](https://github.com/readocs/readocs/issues/new) para relatar problemas ou solicitar recursos

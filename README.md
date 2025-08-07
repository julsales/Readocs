# 📚 Readocs

**Sistema inteligente de documentação automática com IA**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-Anthropic%20Claude-purple.svg)](https://anthropic.com)

---

## 🚀 Sobre o Projeto

O **Readocs** é uma ferramenta revolucionária que utiliza inteligência artificial para gerar e manter documentação técnica de projetos Python de forma completamente automatizada. Ele analisa seu código, identifica padrões e estruturas, e cria documentação profissional usando IA da Anthropic Claude.

### ✨ Principais Funcionalidades

- 🤖 **Análise Inteligente**: IA examina automaticamente a estrutura do projeto
- 📝 **Geração Automática**: Cria README.md e CHANGELOG.md profissionais
- 🔄 **Atualização Contínua**: Mantém documentação sempre sincronizada
- 🎯 **Detecção de Padrões**: Identifica dependências, funcionalidades e arquitetura
- 🛡️ **Controle de Versão**: Sistema automático de versionamento semântico
- 🔍 **Validação**: Evita duplicações e inconsistências na documentação

### 💡 Como Funciona

1. **Análise**: O sistema varre o projeto identificando arquivos importantes
2. **Processamento**: IA da Anthropic Claude analisa código e dependências  
3. **Geração**: Cria documentação técnica clara e profissional
4. **Validação**: Verifica consistência e evita duplicações
5. **Versionamento**: Atualiza changelog com controle semântico

---

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Chave API da Anthropic Claude
- Git (para clonagem)

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/julsales/Readocs.git
   cd Readocs
   ```

2. **Crie ambiente virtual**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS  
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instale dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   ```bash
   # Crie arquivo .env na raiz
   echo "ANTHROPIC_API_KEY=sua_chave_aqui" > .env
   ```

5. **Teste a instalação**
   ```bash
   python readocs/main.py
   ```

---

## 🎯 Como Usar

### Execução Básica

```bash
# Ative o ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Execute o sistema
python readocs/main.py
```

### Configuração Personalizada

Edite as variáveis no arquivo `readocs/main.py`:

```python
PROJECT_FOLDER = "seu_projeto"  # Pasta com código fonte
ROOT_DIR = ".."                 # Onde criar documentação
```

### Exemplo de Saída

```
🚀  READOCS - DOCUMENTAÇÃO AUTOMÁTICA COM IA  🚀
============================================================
📝 Sistema inteligente de geração de documentação
🤖 Powered by Anthropic Claude AI
============================================================

🔄 [████████████████████████████████████████] 100% | Documentação gerada!

✅ DOCUMENTAÇÃO GERADA COM SUCESSO!
============================================================
📄 README.md atualizado
📋 CHANGELOG.md versão 0.0.3
📅 Data: 2025-08-07
============================================================
```

---

## 🛠️ Tecnologias

| Componente | Tecnologia | Versão |
|------------|------------|--------|
| **Linguagem** | Python | 3.8+ |
| **IA** | Anthropic Claude | 3-Haiku |
| **Framework** | Agno | Latest |
| **Versionamento** | Semantic Versioning | 2.0.0 |
| **Documentação** | Markdown | - |

---

## 📁 Estrutura do Projeto

```
Readocs/
├── 📄 README.md              # Este arquivo
├── 📋 CHANGELOG.md           # Histórico de versões
├── ⚙️ requirements.txt       # Dependências Python
├── 🔑 .env                   # Configurações (API keys)
├── 📁 readocs/               # Sistema principal
│   ├── main.py               # Ponto de entrada
│   ├── agents/               # Agentes de IA
│   │   ├── doc_agent.py      # Geração de documentação
│   │   └── curation_agent.py # Curadoria de conteúdo
│   └── modules/              # Módulos utilitários
│       ├── file_utils.py     # Manipulação de arquivos
│       ├── readme_utils.py   # Utilitários README
│       └── changelog_utils.py # Utilitários CHANGELOG
└── 📁 venv/                  # Ambiente virtual
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add: AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Diretrizes

- Siga as convenções de código Python (PEP 8)
- Adicione testes para novas funcionalidades
- Atualize documentação quando necessário
- Use commits semânticos (feat:, fix:, docs:, etc.)

---

## 🐛 Reportar Problemas

Encontrou um bug? [Abra uma issue](https://github.com/julsales/Readocs/issues) com:

- Descrição clara do problema
- Passos para reproduzir
- Ambiente (SO, Python, etc.)
- Logs/screenshots se aplicável

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

</div>

# 🚀 Como Usar o Workflow Universal do Readocs

Este workflow permite que **qualquer projeto** use o Readocs para gerar documentação automaticamente.

## 📋 Pré-requisitos

### 1. 🔑 Configurar Secrets do GitHub

Vá em **Settings > Secrets and Variables > Actions** do seu repositório e adicione:

```
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
```

**Opcional** (para fallback):
```
GEMINI_API_KEY=sua_chave_google_aqui
GOOGLE_API_KEY=sua_chave_google_aqui
READOCS_MODEL_ID=claude-3-haiku-20240307
```

### 2. 📁 Estrutura Necessária

Copie o arquivo do workflow para seu projeto:

```
seu-projeto/
├── .github/
│   └── workflows/
│       └── universal_docs.yml  ← Copie este arquivo
├── README.md                   ← Será atualizado automaticamente
├── CHANGELOG.md               ← Será criado/atualizado automaticamente
└── (seus arquivos de código)
```

## 🎯 Como Funciona

### Execução Automática
O workflow roda automaticamente quando você:
- 🔄 Faz push para `main` ou `master`
- 🎮 Executa manualmente via "Actions" no GitHub

### Processo
1. 🔍 **Detecta** automaticamente o tipo do seu projeto
2. 🤖 **Analisa** o código com IA (Claude/Gemini)
3. 📝 **Gera** README.md e CHANGELOG.md personalizados
4. 🔄 **Cria/atualiza** PR automaticamente
5. ✅ **Aguarda** sua revisão para merge

## 🛠️ Personalização

### Badges Dinâmicos
Se quiser badges no README, adicione em qualquer lugar:
```markdown
{{BADGE_SECTION}}
```

O workflow substituirá automaticamente por badges do seu projeto.

### Projetos Suportados
- 🐍 **Python** (requirements.txt, setup.py, *.py)
- 🌐 **Node.js** (package.json, *.js, *.ts)
- ⚛️ **React/Vue/Next.js** (detecta pelas dependências)
- ☕ **Java** (pom.xml, *.java)
- 🏃 **Go** (go.mod, *.go)
- 🦀 **Rust** (Cargo.toml, *.rs)
- 📦 **Qualquer outro projeto** (análise genérica)

## 🔧 Configuração Avançada

### Modificar Model IA
```yaml
env:
  READOCS_MODEL_ID: claude-3-sonnet-20240229  # Modelo mais potente
```

### Alterar Branches
```yaml
on:
  push:
    branches: [main, master, develop]  # Adicione suas branches
```

### Executar Dry-run
Para testar sem modificar arquivos:
```yaml
python -m readocs generate . --dry-run
```

## 📊 Monitoramento

### Ver Execuções
1. Vá em **Actions** no seu repositório
2. Selecione **"📚 Documentação Universal com Readocs"**
3. Veja os logs de execução

### Pull Requests
- PRs são criados automaticamente com título: **"📚 Documentação automática com Readocs Universal"**
- PRs existentes são atualizados se houver novas mudanças
- Labels: `documentation`, `readocs`, `automated`

## ⚡ Troubleshooting

### Erro de API Key
```
❌ Error: Authentication failed
```
**Solução**: Verificar se `ANTHROPIC_API_KEY` está configurado nos Secrets.

### Readocs não encontrado
```
❌ Error: No module named 'readocs'
```
**Solução**: O workflow instala automaticamente. Se persistir, verificar conectividade.

### Sem mudanças detectadas
```
📝 Nenhuma mudança detectada
```
**Normal**: Significa que a documentação já está atualizada.

## 💡 Dicas

- ✅ **Revise sempre** os PRs antes de fazer merge
- 🔄 **Configure branch protection** para exigir revisão
- 📝 **Customize** o modelo de IA conforme necessário
- 🚀 **Use dry-run** para testar antes de aplicar

---

🤖 **Workflow criado para o Readocs Universal** - Funciona em qualquer projeto!

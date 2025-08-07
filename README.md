# readocs

## Introdução
O projeto "readocs" é uma ferramenta que automatiza a geração de documentação personalizada para projetos de software. Ela utiliza uma equipe de agentes inteligentes, como o doc_agent e o curation_agent, para analisar o código-fonte do projeto e gerar um README.md e um CHANGELOG.md adaptados às características do projeto.

A ferramenta é capaz de:

- Ler e analisar os arquivos do projeto, incluindo o `main.py` e o `requirements.txt`, para entender seu propósito e dependências.
- Gerar uma seção de "Introdução" no README.md com uma breve descrição do projeto.
- Criar uma seção de "Instalação" no README.md com as instruções de instalação e ativação do ambiente virtual (se aplicável).
- Atualizar o CHANGELOG.md com uma nova entrada para a versão mais recente.

## Instalação

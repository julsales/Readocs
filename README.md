<div align="center">

<img src="https://img.shields.io/github/repo-size/julsales/Readocs?style=for-the-badge">
<img src="https://img.shields.io/github/languages/count/julsales/Readocs?style=for-the-badge">
<img src="https://img.shields.io/github/forks/julsales/Readocs?style=for-the-badge">
<img src="https://img.shields.io/github/issues/julsales/Readocs?style=for-the-badge">
<img src="https://img.shields.io/github/issues-pr/julsales/Readocs?style=for-the-badge">
<br><br>
<img src="https://via.placeholder.com/480x320.png?text=Imagem+do+Projeto" height="320">
</div>
# readocs

## Introdução
Este é um projeto Python que utiliza a biblioteca Agno para coordenar uma equipe de agentes (doc_agent e curation_agent) que trabalham em conjunto para gerar a documentação do projeto de forma automatizada. O projeto é estruturado de forma padrão, com um diretório principal `readocs` contendo os arquivos-chave como `main.py` e `requirements.txt`.

## Instalação
1. Certifique-se de ter o Python 3 instalado em seu sistema.
2. Crie e ative um ambiente virtual (VENV):
   - Windows: `python -m venv venv` e `venv\Scripts\activate`
   - Linux/macOS: `python3 -m venv venv` e `source venv/bin/activate`
3. Instale as dependências do projeto:
   ```
   pip install -r requirements.txt
   ```
4. Configure a variável de ambiente `ANTHROPIC_API_KEY` com sua chave de API do Claude.
5. Execute o arquivo `main.py` para gerar a documentação.

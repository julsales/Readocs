# Readocs
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/840aea5f-1132-4b43-90ec-9ef40eb30388" />
## Introdução
Este projeto tem como objetivo gerar automaticamente a documentação técnica de um sistema, usando uma abordagem baseada em agentes. Ele utiliza a API do modelo de linguagem Claude, da Anthropic, para processar instruções e gerar o conteúdo do README e CHANGELOG.

- `modules`: provavelmente contém módulos/pacotes usados pelo projeto
- `agents`: provavelmente contém os agentes usados para gerar a documentação
- `main.py`: script principal que configura o ambiente e executa os agentes

## Instalação
## Instalação

### Pré-requisitos
- Python 3.x
- Pacotes listados em `requirements.txt`

### Instruções
1. Clone o repositório:
```
git clone https://github.com/seu-usuario/seu-projeto.git
```

2. Crie e ative um ambiente virtual (recomendado):

   - **Windows**:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux/macOS**:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Configure a chave da API do Anthropic:
```
export ANTHROPIC_API_KEY=sua-chave-api
```

5. Execute o script principal:
```
python main.py
```

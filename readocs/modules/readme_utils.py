import os
import re
from .readme_cleaner import ensure_clean_readme

def update_readme(section_title: str, section_content: str, project_title: str = "Projeto Readocs") -> str:
    """Adiciona ou atualiza uma seção no README.md.

    Se a seção já existir, seu conteúdo será substituído. Caso contrário,
    uma nova seção será adicionada no final.
    
    Args:
        section_title: O título da seção a ser atualizada.
        section_content: O novo conteúdo em markdown para a seção.
        project_title: O título principal do projeto, usado para criar o arquivo se ele não existir.
    
    Returns:
        Uma mensagem de sucesso ou erro.
    """
    path = "README.md"
    
    # CORREÇÃO AUTOMÁTICA: Limpa duplicatas antes de qualquer modificação
    if os.path.exists(path):
        ensure_clean_readme(path)
    
    # 1. Se o README.md não existir, crie-o com o título do projeto e a nova seção.
    if not os.path.exists(path):
        content = f"# {project_title}\n\n## {section_title}\n{section_content}\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"README.md criado com a seção '{section_title}'."

    # 2. Se o arquivo existir, leia o conteúdo completo.
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define o padrão para encontrar a seção
    # Ele busca por um título de seção e captura tudo que vem depois, até o próximo título ou o final do arquivo.
    # A flag re.escape() garante que caracteres especiais no título não causem problemas.
    pattern = r"(^##\s+" + re.escape(section_title) + r")\n.*?(?=\n## |\Z)"

    # Prepara a nova seção para a substituição
    # A string de substituição precisa de tratamento para evitar 'bad escape'
    new_section_content_with_title = f"## {section_title}\n{section_content}\n"

    # 3. Tenta encontrar e substituir a seção.
    if re.search(pattern, content, re.DOTALL | re.MULTILINE):
        # O re.sub pode falhar se `new_section_content_with_title` tiver escapes inválidos.
        # A solução mais segura é usar uma função de callback ou escapar os caracteres.
        
        # Correção: use uma função de callback (lambda) que retorna a string de substituição.
        # O argumento 'm' é o match object. Usar um callback impede o `re.sub` de interpretar
        # a string de substituição como uma regex.
        updated_content = re.sub(
            pattern,
            lambda m: new_section_content_with_title,
            content,
            flags=re.DOTALL | re.MULTILINE
        )
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        # CORREÇÃO PÓS-PROCESSAMENTO: Limpa duplicatas que possam ter sido criadas
        ensure_clean_readme(path)
            
        return f"Seção '{section_title}' atualizada com sucesso."
    else:
        # 4. Se a seção não for encontrada, adicione-a no final do arquivo.
        content += f"\n{new_section_content_with_title}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        # CORREÇÃO PÓS-PROCESSAMENTO: Limpa duplicatas que possam ter sido criadas
        ensure_clean_readme(path)
            
        return f"Seção '{section_title}' adicionada com sucesso."
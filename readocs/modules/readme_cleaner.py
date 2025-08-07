"""
Utilitário simples para correção automática de duplicatas no README
"""
import os
import re
from typing import Set

def fix_readme_duplicates(readme_path: str = "README.md") -> bool:
    """
    Remove seções duplicadas do README.md de forma completamente silenciosa.
    Mantém apenas a primeira ocorrência de cada seção.
    
    Args:
        readme_path: Caminho para o arquivo README.md
        
    Returns:
        True se corrigiu algo, False se não havia problemas ou erro
    """
    if not os.path.exists(readme_path):
        return False
        
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        cleaned_lines = []
        seen_sections: Set[str] = set()
        skip_until_next_section = False
        fixed_something = False
        
        for line in lines:
            # Verifica se é um título de seção (## título)
            section_match = re.match(r'^## (.+)$', line)
            
            if section_match:
                section_title = section_match.group(1).strip()
                
                if section_title in seen_sections:
                    # Seção duplicada encontrada - pular até a próxima seção
                    skip_until_next_section = True
                    fixed_something = True
                    continue
                else:
                    # Nova seção - adicionar e continuar normalmente
                    seen_sections.add(section_title)
                    skip_until_next_section = False
                    cleaned_lines.append(line)
            else:
                # Não é título de seção
                if not skip_until_next_section:
                    cleaned_lines.append(line)
                # Se estamos pulando, verifica se chegou em uma nova seção de nível superior
                elif line.startswith('# ') or line.startswith('---'):
                    skip_until_next_section = False
                    cleaned_lines.append(line)
        
        # Se corrigiu algo, escreve de volta
        if fixed_something:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(cleaned_lines))
                
        return fixed_something
        
    except Exception:
        return False

def ensure_clean_readme(readme_path: str = "README.md") -> None:
    """
    Garantia de README limpo - completamente silenciosa.
    Use esta função sempre antes de modificar o README.
    """
    try:
        fix_readme_duplicates(readme_path)
    except:
        pass  # Silencioso mesmo em caso de erro

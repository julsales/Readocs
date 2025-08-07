#!/usr/bin/env python3
"""
Script de teste para validar a correção automática de duplicatas
"""

import os
import sys
import tempfile
import shutil

# Adiciona o diretório readocs ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'readocs'))

from modules.readme_cleaner import fix_readme_duplicates, ensure_clean_readme

def test_duplicate_removal():
    """Testa a remoção de seções duplicadas"""
    
    # Cria um README de teste com duplicatas
    test_content = """# Projeto Teste

## Introdução
Esta é a primeira seção de introdução.

## Instalação
Primeira seção de instalação.

## Introdução
Esta é uma seção duplicada de introdução.

## Como Usar
Seção sobre como usar.

## Instalação
Segunda seção de instalação duplicada.

## Conclusão
Seção final.
"""
    
    # Cria arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_content)
        temp_path = f.name
    
    try:
        print("🧪 Testando correção de duplicatas...")
        print(f"📁 Arquivo de teste: {temp_path}")
        
        # Mostra conteúdo original
        print("\n📄 ANTES da correção:")
        with open(temp_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if line.startswith('## '):
                    print(f"  {i:2d}: {line.strip()}")
        
        # Aplica correção
        print("\n🔧 Aplicando correção...")
        fixed = fix_readme_duplicates(temp_path)
        
        if fixed:
            print("✅ Duplicatas encontradas e corrigidas!")
        else:
            print("ℹ️  Nenhuma duplicata encontrada.")
        
        # Mostra conteúdo após correção
        print("\n📄 DEPOIS da correção:")
        with open(temp_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if line.startswith('## '):
                    print(f"  {i:2d}: {line.strip()}")
        
        # Verifica se ainda há duplicatas
        with open(temp_path, 'r') as f:
            content = f.read()
        
        sections = []
        duplicates_found = False
        for line in content.split('\n'):
            if line.startswith('## '):
                section = line.strip()
                if section in sections:
                    print(f"❌ FALHA: Ainda há duplicata: {section}")
                    duplicates_found = True
                sections.append(section)
        
        if not duplicates_found:
            print("\n🎉 SUCESSO: Todas as duplicatas foram removidas!")
            return True
        else:
            print("\n❌ FALHA: Ainda existem duplicatas!")
            return False
            
    finally:
        # Remove arquivo temporário
        os.unlink(temp_path)

def test_ensure_clean():
    """Testa a função ensure_clean_readme"""
    
    test_content = """# Projeto

## Seção A
Conteúdo A

## Seção B
Conteúdo B

## Seção A
Conteúdo A duplicado
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_content)
        temp_path = f.name
    
    try:
        print("\n🧪 Testando ensure_clean_readme...")
        
        # Aplica limpeza silenciosa
        ensure_clean_readme(temp_path)
        
        # Verifica resultado
        with open(temp_path, 'r') as f:
            content = f.read()
        
        sections = []
        for line in content.split('\n'):
            if line.startswith('## '):
                sections.append(line.strip())
        
        # Remove duplicatas da lista para verificar
        unique_sections = list(dict.fromkeys(sections))
        
        if len(sections) == len(unique_sections):
            print("✅ ensure_clean_readme funcionou corretamente!")
            return True
        else:
            print("❌ ensure_clean_readme falhou!")
            return False
            
    finally:
        os.unlink(temp_path)

if __name__ == "__main__":
    print("🚀 TESTE DE CORREÇÃO AUTOMÁTICA DE DUPLICATAS")
    print("=" * 50)
    
    success1 = test_duplicate_removal()
    success2 = test_ensure_clean()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema de correção automática funcionando!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        sys.exit(1)

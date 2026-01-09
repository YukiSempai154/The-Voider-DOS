#!/usr/bin/env python3
"""
Исправление структуры проекта
"""

import os
import sys

def fix_imports():
    """Исправить все импорты в проекте"""
    
    print("Создаю __init__.py файлы...")
    
    # Создаем __init__.py файлы
    init_files = [
        "voider_dos/__init__.py",
        "voider_dos/core/__init__.py",
        "voider_dos/ui/__init__.py",
    ]
    
    for file in init_files:
        if not os.path.exists(file):
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, 'w', encoding='utf-8') as f:
                f.write('"""Package module"""\n')
            print(f"✅ Создан: {file}")
        else:
            print(f"✓ Уже существует: {file}")
    
    print("\nИсправляю main.py...")
    
    # Исправляем main.py
    main_py = "main.py"
    if os.path.exists(main_py):
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Добавляем sys.path.insert после shebang
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if i == 0 and line.startswith('#!/'):
                # После shebang добавляем пути
                new_lines.append('')
                new_lines.append('import sys')
                new_lines.append('import os')
                new_lines.append('')
                new_lines.append('# Добавляем текущую папку в путь Python')
                new_lines.append('current_dir = os.path.dirname(os.path.abspath(__file__))')
                new_lines.append('if current_dir not in sys.path:')
                new_lines.append('    sys.path.insert(0, current_dir)')
                new_lines.append('')
        
        with open(main_py, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("✅ main.py исправлен")
    
    print("\nТестирую импорты...")
    
    # Тест импортов
    try:
        # Добавляем текущую папку в путь
        sys.path.insert(0, os.getcwd())
        
        import voider_dos
        print("✅ voider_dos импортируется")
        
        from voider_dos.core import game_state
        print("✅ game_state импортируется")
        
        from voider_dos.ui import main_menu
        print("✅ main_menu импортируется")
        
        print("\n✅ Все импорты работают!")
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("\nПроверьте наличие файлов:")
        print("  voider_dos/__init__.py")
        print("  voider_dos/core/__init__.py")
        print("  voider_dos/ui/__init__.py")

if __name__ == "__main__":
    fix_imports()
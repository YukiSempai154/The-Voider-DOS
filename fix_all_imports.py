#!/usr/bin/env python3
"""
Исправление всех импортов в проекте
"""

import os
import re

def fix_imports_in_file(filepath):
    """Исправить импорты в одном файле"""
    if not os.path.exists(filepath):
        print(f"⚠ Файл не найден: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем относительные импорты на абсолютные
    changes = False
    
    # Паттерн для поиска относительных импортов
    patterns = [
        (r'from \.(\w+) import', r'from voider_dos.ui.\1 import'),  # для ui/
        (r'from \.\.(\w+) import', r'from voider_dos.\1 import'),   # для core/из других мест
        (r'from \.\.commands', r'from voider_dos.commands'),        # для commands
        (r'from \.\.utils', r'from voider_dos.utils'),              # для utils
    ]
    
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes = True
    
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Исправлен: {filepath}")
        return True
    else:
        print(f"✓ Без изменений: {filepath}")
        return False

print("Исправление импортов в проекте...")
print("=" * 60)

# Файлы для исправления
files_to_fix = [
    r"f:\clone\voider_dos\ui\main_menu.py",
    r"f:\clone\voider_dos\ui\console_ui.py", 
    r"f:\clone\voider_dos\ui\color_scheme.py",
    r"f:\clone\voider_dos\core\session_manager.py",
    r"f:\clone\voider_dos\core\vfs_generator.py",
    r"f:\clone\voider_dos\core\cipher_system.py",
    r"f:\clone\voider_dos\core\game_state.py",
]

fixed_count = 0
for filepath in files_to_fix:
    if fix_imports_in_file(filepath):
        fixed_count += 1

print("\n" + "=" * 60)
print(f"Исправлено файлов: {fixed_count}/{len(files_to_fix)}")

# Также создаем упрощенный main_menu.py если нужно
print("\nСоздаю упрощенный main_menu.py без сложных импортов...")

simple_main_menu = r"f:\clone\voider_dos\ui\simple_main_menu.py"
simple_content = '''"""
Упрощенный MainMenu для тестирования
"""

import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)

class MainMenu:
    def __init__(self, game_state):
        self.game_state = game_state
    
    def display(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Счет в правом верхнем углу
            score = self.game_state.total_score if hasattr(self.game_state, 'total_score') else 0
            score_text = f"Score: {score}"
            print(f"{Fore.GREEN}{score_text:>70}{Style.RESET_ALL}")
            
            # ASCII заголовок (упрощенный)
            print(f"\n{Fore.LIGHTCYAN_EX}{'THE-VOIDER-DOS':^80}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTCYAN_EX}{'='*80}{Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}1. Начать игру{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}2. Помощь{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}3. Справка{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}4. Выйти{Style.RESET_ALL}")
            
            # Информация о версии внизу справа
            print(f"\n\n\n{Fore.LIGHTBLACK_EX}{'v0.1.0 Alpha by Prunt (Yuki_Sempai)':>80}{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}Выберите пункт [1-4]: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                return "new_game"
            elif choice == "2":
                self.show_help()
            elif choice == "3":
                self.show_about()
            elif choice == "4":
                self.exit_game()
                return "exit"
            else:
                input(f"{Fore.RED}Неверный выбор. Нажмите Enter...{Style.RESET_ALL}")
    
    def show_help(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{'ПОМОЩЬ':^80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Основные команды:{Style.RESET_ALL}")
        print("  dir - показать содержимое директории")
        print("  cd <папка> - перейти в папку")
        print("  cd .. - вернуться назад")
        print("  decode <шифр> <текст> - расшифровать директорию")
        print("  help - эта справка")
        print("  exit - выход в меню")
        input(f"\n{Fore.YELLOW}Нажмите Enter для возврата...{Style.RESET_ALL}")
    
    def show_about(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{'ОБ ИГРЕ':^80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}THE-VOIDER-DOS{Style.RESET_ALL}")
        print("Консольная игра с процедурной генерацией файловой системы")
        print("Исследуйте виртуальную файловую систему,")
        print("расшифровывайте директории, находите пасхалки!")
        print(f"\n{Fore.YELLOW}Версия: 0.1.0 Alpha{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Автор: Prunt (Yuki_Sempai){Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Нажмите Enter для возврата...{Style.RESET_ALL}")
    
    def exit_game(self):
        print(f"\n{Fore.GREEN}Сохранение прогресса...{Style.RESET_ALL}")
        if hasattr(self.game_state, 'save'):
            self.game_state.save()
        print(f"{Fore.GREEN}Спасибо за игру!{Style.RESET_ALL}")
        import time
        time.sleep(2)
        sys.exit(0)
'''

with open(simple_main_menu, 'w', encoding='utf-8') as f:
    f.write(simple_content)
print(f"✅ Создан упрощенный файл: {simple_main_menu}")

print("\n✅ Готово! Теперь запустите:")
print("python simple_main.py")
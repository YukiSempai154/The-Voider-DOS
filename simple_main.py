#!/usr/bin/env python3
"""
Упрощенный запуск игры
"""

import sys
import os
from colorama import init, Fore, Style

init(autoreset=True)

def main():
    print(f"{Fore.CYAN}Загрузка THE-VOIDER-DOS...{Style.RESET_ALL}")
    
    try:
        # Добавляем путь к проекту
        project_root = r"f:\clone"
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # Загружаем модули напрямую (без пакетов)
        import importlib.util
        
        # Загружаем game_state.py
        game_state_path = r"f:\clone\voider_dos\core\game_state.py"
        spec = importlib.util.spec_from_file_location("game_state", game_state_path)
        game_state_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(game_state_module)
        GameState = game_state_module.GameState
        
        # Загружаем main_menu.py
        main_menu_path = r"f:\clone\voider_dos\ui\main_menu.py"
        spec = importlib.util.spec_from_file_location("main_menu", main_menu_path)
        main_menu_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_menu_module)
        MainMenu = main_menu_module.MainMenu
        
        print(f"{Fore.GREEN}Модули загружены!{Style.RESET_ALL}")
        
        # Создаем состояние игры
        game_state = GameState()
        game_state.load()
        
        # Показываем меню
        menu = MainMenu(game_state)
        choice = menu.display()
        
        if choice == "new_game":
            print(f"{Fore.YELLOW}Запуск новой игры...{Style.RESET_ALL}")
            # Здесь будет сессия игры
            
    except Exception as e:
        print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()
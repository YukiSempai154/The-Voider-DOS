#!/usr/bin/env python3
"""
THE-VOIDER-DOS - Консольная игра с процедурной генерацией файловой системы
Автор: Prunt (Yuki_Sempai)
"""

import sys
import os
from colorama import init, Fore, Style

# Инициализация colorama для цветного вывода в Windows/Linux/Mac
init(autoreset=True)

def main():
    """Главная функция запуска игры"""
    try:
        print(f"{Fore.CYAN}Загрузка THE-VOIDER-DOS...{Style.RESET_ALL}")
        
        # Динамический импорт для избежания циклических зависимостей
        # Эти модули нужно будет создать следующими
        from voider_dos.core.game_state import GameState
        from voider_dos.ui.main_menu import MainMenu
        from voider_dos.core.session_manager import GameSession
        
        # Инициализация состояния игры
        print(f"{Fore.YELLOW}Инициализация игрового состояния...{Style.RESET_ALL}")
        game_state = GameState()
        game_state.load()
        
        # Главный игровой цикл
        print(f"{Fore.GREEN}Игра загружена!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Добро пожаловать в THE-VOIDER-DOS!{Style.RESET_ALL}")
        
        while True:
            # Показ главного меню и получение выбора пользователя
            menu = MainMenu(game_state)
            choice = menu.display()
            
            if choice == "new_game":
                # Запуск новой игровой сессии
                print(f"{Fore.YELLOW}Генерация новой файловой системы...{Style.RESET_ALL}")
                session = GameSession(game_state, new_game=True)
                session.run()
                
            elif choice == "continue":
                # Продолжение сохраненной игры
                if game_state.has_save():
                    print(f"{Fore.YELLOW}Загрузка последнего сохранения...{Style.RESET_ALL}")
                    session = GameSession(game_state, new_game=False)
                    session.run()
                else:
                    print(f"{Fore.RED}Сохранений не найдено.{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
                    
            elif choice == "help":
                # Показ помощи (будет обработан в меню)
                continue
                
            elif choice == "about":
                # Показ информации об игре (будет обработан в меню)
                continue
                
            elif choice == "stats":
                # Показ статистики (будет обработан в меню)
                continue
                
            elif choice == "settings":
                # Показ настроек (будет обработан в меню)
                continue
                
            elif choice == "exit":
                # Выход из игры
                menu.exit_game()
                
    except KeyboardInterrupt:
        # Обработка Ctrl+C
        print(f"\n\n{Fore.YELLOW}Игра прервана пользователем.{Style.RESET_ALL}")
        sys.exit(0)
        
    except ImportError as e:
        # Если отсутствуют необходимые модули
        print(f"\n{Fore.RED}Ошибка импорта: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Убедитесь, что все модули созданы:{Style.RESET_ALL}")
        print("  1. voider_dos/core/game_state.py")
        print("  2. voider_dos/ui/main_menu.py")
        print("  3. voider_dos/core/session_manager.py")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
        
    except Exception as e:
        # Обработка всех остальных ошибок
        print(f"\n{Fore.RED}Критическая ошибка: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")
        sys.exit(1)

if __name__ == "__main__":
    # Создание необходимых директорий, если они отсутствуют
    os.makedirs("voider_dos/saves", exist_ok=True)
    os.makedirs("voider_dos/data/ascii_art", exist_ok=True)
    os.makedirs("voider_dos/data/name_lists", exist_ok=True)
    os.makedirs("voider_dos/data/help_texts", exist_ok=True)
    
    # Запуск игры
    main()
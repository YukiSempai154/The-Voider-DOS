#!/usr/bin/env python3
"""
Правильный запуск игры THE-VOIDER-DOS
"""

import sys
import os
from colorama import init, Fore, Style

# Инициализация цветов
init(autoreset=True)

def main():
    print(f"{Fore.CYAN}Загрузка THE-VOIDER-DOS...{Style.RESET_ALL}")
    
    # Добавляем путь к проекту
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    try:
        # Импортируем через полные пути
        print(f"{Fore.YELLOW}Импорт модулей...{Style.RESET_ALL}")
        
        # 1. GameState
        sys.path.insert(0, os.path.join(project_root, 'voider_dos'))
        sys.path.insert(0, os.path.join(project_root, 'voider_dos/core'))
        
        from voider_dos.core.game_state import GameState
        print(f"{Fore.GREEN}✅ GameState загружен{Style.RESET_ALL}")
        
        # 2. MainMenu (используем простую версию)
        menu_path = os.path.join(project_root, 'voider_dos/ui/simple_main_menu.py')
        if os.path.exists(menu_path):
            # Добавляем путь к ui
            sys.path.insert(0, os.path.join(project_root, 'voider_dos/ui'))
            from voider_dos.ui.simple_main_menu import MainMenu
            print(f"{Fore.GREEN}✅ MainMenu загружен{Style.RESET_ALL}")
        else:
            # Создаем простой меню
            print(f"{Fore.YELLOW}⚠ Создаю простое меню...{Style.RESET_ALL}")
            class MainMenu:
                def __init__(self, game_state):
                    self.game_state = game_state
                def display(self):
                    print(f"\n{Fore.LIGHTCYAN_EX}{'THE-VOIDER-DOS':^60}{Style.RESET_ALL}")
                    print(f"{Fore.LIGHTCYAN_EX}{'='*60}{Style.RESET_ALL}")
                    print(f"\n{Fore.YELLOW}1. Начать игру{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}2. Помощь{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}3. Справка{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}4. Выйти{Style.RESET_ALL}")
                    
                    # Версия в правом нижнем углу
                    print(f"\n\n{Fore.LIGHTBLACK_EX}{'v0.1.0 Alpha by Prunt':>60}{Style.RESET_ALL}")
                    
                    choice = input(f"\n{Fore.CYAN}Выберите [1-4]: {Style.RESET_ALL}")
                    return "new_game" if choice == "1" else "exit"
        
        # Создаем состояние игры
        game_state = GameState()
        game_state.load()
        
        print(f"{Fore.GREEN}✅ Игра загружена!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Текущий счет: {game_state.total_score}{Style.RESET_ALL}")
        
        # Показываем меню
        menu = MainMenu(game_state)
        choice = menu.display()
        
        if choice == "new_game":
            print(f"\n{Fore.GREEN}🎮 НОВАЯ ИГРА НАЧАТА!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Исследуйте виртуальную файловую систему...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Введите команды (help - справка, exit - выход){Style.RESET_ALL}")
            
            # Простая игровая сессия
            score = game_state.total_score
            while True:
                try:
                    # Приглашение с путем и счетом
                    prompt = f"{Fore.GREEN}[{score}]{Style.RESET_ALL} {Fore.CYAN}VOID:\\>{Style.RESET_ALL} "
                    cmd = input(prompt).strip().lower()
                    
                    if cmd == "exit":
                        print(f"{Fore.YELLOW}Выход в меню...{Style.RESET_ALL}")
                        break
                    elif cmd == "help":
                        print(f"\n{Fore.YELLOW}ДОСТУПНЫЕ КОМАНДЫ:{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}  dir - показать содержимое директории{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}  cd <папка> - перейти в папку{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}  decode <шифр> <текст> - расшифровать директорию{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}  help - эта справка{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}  exit - выход в меню{Style.RESET_ALL}")
                    elif cmd == "dir":
                        print(f"\n{Fore.CYAN}Содержимое VOID:\\:{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}  <DIR>   System32{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}  <DIR>   Users{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}  <DIR>   [ЗАШИФРОВАНО] 48656C6C6F{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}         README.txt{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}         CONFIG.dat{Style.RESET_ALL}")
                    elif cmd.startswith("decode"):
                        parts = cmd.split()
                        if len(parts) == 3:
                            cipher, text = parts[1], parts[2]
                            if cipher == "48656C6C6F" and text.lower() == "hello":
                                print(f"{Fore.GREEN}  ✓ Директория расшифрована: HELLO{Style.RESET_ALL}")
                                print(f"{Fore.GREEN}  +50 очков!{Style.RESET_ALL}")
                                score += 50
                                game_state.record_decryption(50)
                            else:
                                print(f"{Fore.RED}  ✗ Неверная расшифровка{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}  Использование: decode <шифр> <текст>{Style.RESET_ALL}")
                    elif cmd == "score":
                        print(f"{Fore.GREEN}  Текущий счет: {score}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}  Неизвестная команда: '{cmd}'{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}  Введите 'help' для списка команд{Style.RESET_ALL}")
                    
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Выход в меню...{Style.RESET_ALL}")
                    break
            
            # Сохраняем прогресс
            game_state.save()
            print(f"{Fore.GREEN}Прогресс сохранен! Итоговый счет: {score}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}До новых встреч в пустоте DOS-а!{Style.RESET_ALL}")
        
    except ImportError as e:
        print(f"{Fore.RED}❌ Ошибка импорта: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Проверьте:{Style.RESET_ALL}")
        print(f"  1. Файл существует: voider_dos/core/game_state.py")
        print(f"  2. Есть __init__.py в папках")
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    input(f"\n{Fore.YELLOW}Нажмите Enter для выхода...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
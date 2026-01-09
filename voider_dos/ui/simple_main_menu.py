"""
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
            print(f"
{Fore.LIGHTCYAN_EX}{'THE-VOIDER-DOS':^80}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTCYAN_EX}{'='*80}{Style.RESET_ALL}")
            
            print(f"
{Fore.YELLOW}1. Начать игру{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}2. Помощь{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}3. Справка{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}4. Выйти{Style.RESET_ALL}")
            
            # Информация о версии внизу справа
            print(f"


{Fore.LIGHTBLACK_EX}{'v0.1.0 Alpha by Prunt (Yuki_Sempai)':>80}{Style.RESET_ALL}")
            
            choice = input(f"
{Fore.CYAN}Выберите пункт [1-4]: {Style.RESET_ALL}").strip()
            
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
        print(f"
{Fore.YELLOW}Основные команды:{Style.RESET_ALL}")
        print("  dir - показать содержимое директории")
        print("  cd <папка> - перейти в папку")
        print("  cd .. - вернуться назад")
        print("  decode <шифр> <текст> - расшифровать директорию")
        print("  help - эта справка")
        print("  exit - выход в меню")
        input(f"
{Fore.YELLOW}Нажмите Enter для возврата...{Style.RESET_ALL}")
    
    def show_about(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{'ОБ ИГРЕ':^80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"
{Fore.GREEN}THE-VOIDER-DOS{Style.RESET_ALL}")
        print("Консольная игра с процедурной генерацией файловой системы")
        print("Исследуйте виртуальную файловую систему,")
        print("расшифровывайте директории, находите пасхалки!")
        print(f"
{Fore.YELLOW}Версия: 0.1.0 Alpha{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Автор: Prunt (Yuki_Sempai){Style.RESET_ALL}")
        input(f"
{Fore.YELLOW}Нажмите Enter для возврата...{Style.RESET_ALL}")
    
    def exit_game(self):
        print(f"
{Fore.GREEN}Сохранение прогресса...{Style.RESET_ALL}")
        if hasattr(self.game_state, 'save'):
            self.game_state.save()
        print(f"{Fore.GREEN}Спасибо за игру!{Style.RESET_ALL}")
        import time
        time.sleep(2)
        sys.exit(0)

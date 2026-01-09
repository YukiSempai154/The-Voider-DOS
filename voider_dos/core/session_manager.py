"""
Класс GameSession: управление игровой сессией, основной игровой цикл
"""

import sys
import os

# ДОБАВЬТЕ ЭТО В САМОМ НАЧАЛЕ файла:
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Теперь остальные импорты
import time
import random
from datetime import datetime
from typing import Optional, Dict, Any, List
from colorama import init, Fore, Style

from config import UI, COLORS, VERSION_STRING
from voider_dos.core.vfs_generator import VirtualFileSystem
from voider_dos.core.game_state import GameState

# Пути к

# Добавляем путь для импорта config.py из корня проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from config import UI, COLORS, VERSION_STRING
from voider_dos.core.vfs_generator import VirtualFileSystem
from voider_dos.core.game_state import GameState

# Импортируем обработчик команд (пока заглушка)
HAS_COMMAND_HANDLER = False

# Пока используем заглушку, так как handler.py еще не создан
class CommandHandler:
    def __init__(self, vfs, game_state):
        self.vfs = vfs
        self.game_state = game_state
    
    def execute(self, command):
        if command == "dir":
            items = self.vfs.list_directory()
            return ["Содержимое директории:"] + items if items else ["Директория пуста"]
        elif command == "help":
            return ["Доступные команды:", "dir - показать содержимое", "help - справка", "exit - выход"]
        else:
            return f"Команда '{command}' не распознана. Введите 'help' для списка команд."

print(f"{Fore.YELLOW}[INFO] Используется временный обработчик команд{Style.RESET_ALL}")


class GameSession:
    """Класс для управления игровой сессией и основным игровым циклом"""
    
    def __init__(self, game_state: GameState, new_game: bool = True, seed: Optional[int] = None):
        """
        Инициализация игровой сессии
        
        Args:
            game_state: Состояние игры
            new_game: Начинать ли новую игру
            seed: Seed для генерации VFS (если None - случайный)
        """
        # Инициализация цветов
        init(autoreset=True)
        
        self.game_state = game_state
        self.new_game = new_game
        self.seed = seed
        
        # Инициализация VFS
        print(f"{Fore.CYAN}Инициализация виртуальной файловой системы...{Style.RESET_ALL}")
        self.vfs = VirtualFileSystem(seed=self.seed)
        
        # Инициализация обработчика команд
        self.command_handler = CommandHandler(self.vfs, self.game_state)
        
        # Статистика сессии
        self.session_start_time = time.time()
        self.commands_executed = 0
        self.last_command_time = None
        self.command_history = []
        
        # Состояние сессии
        self.is_running = True
        self.show_hidden = False
        self.debug_mode = False
        
        # Начинаем новую сессию в состоянии игры
        if new_game:
            self.game_state.start_new_session(seed=self.vfs.seed)
            print(f"{Fore.GREEN}Новая игровая сессия начата!{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Игровая сессия загружена.{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}Seed системы: {self.vfs.seed}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Введите 'help' для списка команд, 'exit' для выхода в меню.{Style.RESET_ALL}")
    
    # ... остальной код без изменений ...
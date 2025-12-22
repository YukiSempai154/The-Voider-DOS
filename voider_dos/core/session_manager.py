"""
Класс GameSession: управление игровой сессией, основной игровой цикл
"""

import time
import random
import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from colorama import init, Fore, Style

# Добавляем путь для импорта config.py из корня проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from config import UI, COLORS, VERSION_STRING
from .vfs_generator import VirtualFileSystem
from .game_state import GameState

# Импортируем обработчик команд (создадим его следующим)
try:
    from ..commands.handler import CommandHandler
    HAS_COMMAND_HANDLER = True
except ImportError:
    HAS_COMMAND_HANDLER = False
    print(f"{Fore.YELLOW}[WARNING] CommandHandler не найден. Используется заглушка.{Style.RESET_ALL}")


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
        if HAS_COMMAND_HANDLER:
            self.command_handler = CommandHandler(self.vfs, self.game_state)
        else:
            # Заглушка для тестирования
            self.command_handler = self._create_stub_handler()
        
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
    
    def _create_stub_handler(self):
        """Создать заглушку для обработчика команд"""
        class StubCommandHandler:
            def __init__(self, vfs, game_state):
                self.vfs = vfs
                self.game_state = game_state
            
            def execute(self, command):
                return f"CommandHandler не загружен. Команда: {command}"
        
        return StubCommandHandler(self.vfs, self.game_state)
    
    def run(self) -> None:
        """Основной игровой цикл"""
        self._clear_screen()
        self._print_welcome_message()
        
        try:
            while self.is_running:
                # Отображаем приглашение и получаем ввод
                user_input = self._get_user_input()
                
                # Обрабатываем специальные команды
                if self._handle_special_commands(user_input):
                    continue
                
                # Выполняем команду через обработчик
                result = self.command_handler.execute(user_input)
                
                # Обрабатываем результат
                self._handle_command_result(user_input, result)
                
                # Обновляем статистику
                self.commands_executed += 1
                self.last_command_time = time.time()
                self.command_history.append(user_input)
                
                # Ограничиваем размер истории
                if len(self.command_history) > UI['max_history_size']:
                    self.command_history.pop(0)
                
        except KeyboardInterrupt:
            self._handle_keyboard_interrupt()
        except Exception as e:
            self._handle_error(e)
        finally:
            self._cleanup()
    
    def _clear_screen(self) -> None:
        """Очистить экран"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _print_welcome_message(self) -> None:
        """Вывести приветственное сообщение"""
        print(f"{Fore.LIGHTCYAN_EX}{'='*UI['console_width']}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}{'ТЕМНАЯ ПУСТОТА DOS-А ОЖИДАЕТ...':^{UI['console_width']}}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}{'='*UI['console_width']}{Style.RESET_ALL}")
        print()
    
    def _get_user_input(self) -> str:
        """Получить ввод от пользователя"""
        try:
            # Подготовка приглашения
            prompt = self._build_prompt()
            
            # Получение ввода с поддержкой истории и автодополнения
            if sys.platform != 'win32' and HAS_COMMAND_HANDLER:
                # Для Linux/Mac используем readline для улучшения ввода
                import readline
                readline.set_completer(self._tab_completer)
                readline.parse_and_bind('tab: complete')
            
            # Отображение приглашения и получение ввода
            user_input = input(prompt).strip()
            
            return user_input
            
        except EOFError:
            # Ctrl+D на Unix или Ctrl+Z на Windows
            return "exit"
        except KeyboardInterrupt:
            raise
    
    def _build_prompt(self) -> str:
        """Построить строку приглашения"""
        # Получаем текущий путь
        current_path = self.vfs.get_current_path_str()
        
        # Получаем текущий счет
        current_score = self.game_state.score
        
        # Формируем строку приглашения
        prompt_parts = []
        
        # Добавляем счет (если не ноль)
        if current_score > 0:
            prompt_parts.append(f"{Fore.GREEN}[{current_score}]{Style.RESET_ALL}")
        
        # Добавляем путь
        prompt_parts.append(f"{Fore.CYAN}{current_path}{Style.RESET_ALL}")
        
        # Добавляем символ приглашения
        prompt_parts.append(f"{Fore.YELLOW}{UI['prompt_symbol']}{Style.RESET_ALL}")
        
        # Добавляем пробел для разделения
        prompt = ' '.join(prompt_parts) + ' '
        
        return prompt
    
    def _tab_completer(self, text: str, state: int) -> Optional[str]:
        """Функция автодополнения по Tab"""
        # Получаем список возможных дополнений
        completions = []
        
        # Проверяем, начинается ли текст с команд
        possible_commands = ['dir', 'cd', 'decode', 'help', 'score', 'clear', 'cls', 'exit']
        for cmd in possible_commands:
            if cmd.startswith(text.lower()):
                completions.append(cmd)
        
        # Ищем файлы и директории в текущей директории
        for item in self.vfs.current_dir.children:
            if isinstance(item, DirNode):
                if item.name.lower().startswith(text.lower()):
                    completions.append(item.name)
            else:
                full_name = item.get_full_name()
                if full_name.lower().startswith(text.lower()):
                    completions.append(full_name)
        
        # Возвращаем соответствующее дополнение
        if state < len(completions):
            return completions[state]
        
        return None
    
    def _handle_special_commands(self, user_input: str) -> bool:
        """
        Обработка специальных команд, которые не проходят через CommandHandler
        
        Returns:
            True если команда обработана, False если нужно передать в CommandHandler
        """
        input_lower = user_input.lower()
        
        if input_lower == 'exit' or input_lower == 'quit':
            self.is_running = False
            print(f"{Fore.YELLOW}Выход в главное меню...{Style.RESET_ALL}")
            return True
        
        elif input_lower == 'clear' or input_lower == 'cls':
            self._clear_screen()
            self._print_welcome_message()
            return True
        
        elif input_lower == 'debug':
            self.debug_mode = not self.debug_mode
            status = "включен" if self.debug_mode else "выключен"
            print(f"{Fore.MAGENTA}Режим отладки {status}.{Style.RESET_ALL}")
            return True
        
        elif input_lower == 'history':
            self._show_command_history()
            return True
        
        elif input_lower == 'stats':
            self._show_session_stats()
            return True
        
        elif input_lower == 'version':
            print(f"{Fore.CYAN}{VERSION_STRING}{Style.RESET_ALL}")
            return True
        
        elif input_lower.startswith('seed'):
            parts = input_lower.split()
            if len(parts) > 1 and parts[1] == 'set':
                try:
                    new_seed = int(parts[2])
                    self.vfs = VirtualFileSystem(seed=new_seed)
                    print(f"{Fore.GREEN}Seed изменен на {new_seed}. ФС перегенерирована.{Style.RESET_ALL}")
                except (IndexError, ValueError):
                    print(f"{Fore.RED}Использование: seed set <число>{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}Текущий seed: {self.vfs.seed}{Style.RESET_ALL}")
            return True
        
        return False
    
    def _handle_command_result(self, user_input: str, result: Any) -> None:
        """Обработка результата выполнения команды"""
        if result is None:
            return
        
        # Если результат - строка, просто выводим ее
        if isinstance(result, str):
            print(result)
        
        # Если результат - список (например, от команды dir)
        elif isinstance(result, list):
            for line in result:
                print(line)
        
        # Если результат - словарь (специальная обработка)
        elif isinstance(result, dict):
            self._handle_dict_result(result)
        
        # Добавляем пустую строку для разделения
        print()
        
        # Отладочная информация
        if self.debug_mode:
            print(f"{Fore.LIGHTBLACK_EX}[DEBUG] Команда: '{user_input}'{Style.RESET_ALL}")
    
    def _handle_dict_result(self, result: Dict[str, Any]) -> None:
        """Обработка результата в виде словаря"""
        if 'type' in result:
            if result['type'] == 'file_content':
                self._display_file_content(result)
            elif result['type'] == 'decryption_success':
                self._handle_decryption_success(result)
            elif result['type'] == 'error':
                self._display_error(result)
    
    def _display_file_content(self, result: Dict[str, Any]) -> None:
        """Отобразить содержимое файла"""
        filename = result.get('filename', 'Неизвестный файл')
        content = result.get('content', '')
        is_easter_egg = result.get('is_easter_egg', False)
        
        # Заголовок файла
        if is_easter_egg:
            print(f"{Fore.MAGENTA}╔{'═'*78}╗")
            print(f"║{'🎉 ПАСХАЛКА НАЙДЕНА! 🎉':^78}║")
            print(f"╚{'═'*78}╝{Style.RESET_ALL}")
            print()
        
        print(f"{Fore.CYAN}Файл: {filename}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{content}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*80}{Style.RESET_ALL}")
        
        # Информация о начисленных очках
        if 'points' in result:
            points = result['points']
            reason = result.get('reason', '')
            print(f"{Fore.GREEN}+{points} очков {reason}{Style.RESET_ALL}")
    
    def _handle_decryption_success(self, result: Dict[str, Any]) -> None:
        """Обработка успешной расшифровки"""
        dir_name = result.get('dir_name', 'Неизвестная директория')
        points = result.get('points', 0)
        
        # Анимация успеха
        print(f"{Fore.GREEN}╔{'═'*78}╗")
        print(f"║{'🎯 ДИРЕКТОРИЯ РАСШИФРОВАНА! 🎯':^78}║")
        print(f"╚{'═'*78}╝{Style.RESET_ALL}")
        print()
        print(f"{Fore.CYAN}Доступ открыт к директории: {Fore.YELLOW}{dir_name}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}+{points} очков за расшифровку!{Style.RESET_ALL}")
        
        # Обновляем статистику в game_state
        self.game_state.record_decryption(points)
    
    def _display_error(self, result: Dict[str, Any]) -> None:
        """Отобразить ошибку"""
        message = result.get('message', 'Неизвестная ошибка')
        error_type = result.get('error_type', 'error')
        
        if error_type == 'warning':
            color = Fore.YELLOW
            prefix = '⚠'
        else:
            color = Fore.RED
            prefix = '✗'
        
        print(f"{color}{prefix} {message}{Style.RESET_ALL}")
    
    def _show_command_history(self) -> None:
        """Показать историю команд"""
        print(f"{Fore.CYAN}История команд ({len(self.command_history)}):{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{'-'*40}{Style.RESET_ALL}")
        
        for i, cmd in enumerate(self.command_history[-10:], 1):  # Последние 10 команд
            print(f"{Fore.LIGHTBLACK_EX}{i:3}. {cmd}{Style.RESET_ALL}")
        
        if len(self.command_history) > 10:
            print(f"{Fore.LIGHTBLACK_EX}... и еще {len(self.command_history) - 10} команд{Style.RESET_ALL}")
    
    def _show_session_stats(self) -> None:
        """Показать статистику текущей сессии"""
        current_time = time.time()
        session_duration = current_time - self.session_start_time
        minutes = int(session_duration // 60)
        seconds = int(session_duration % 60)
        
        # Статистика VFS
        vfs_stats = self.vfs.get_stats()
        
        print(f"{Fore.CYAN}Статистика текущей сессии:{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{'-'*40}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Seed системы: {Fore.YELLOW}{vfs_stats['seed']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Длительность: {Fore.YELLOW}{minutes:02d}:{seconds:02d}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Выполнено команд: {Fore.YELLOW}{self.commands_executed}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Текущий путь: {Fore.YELLOW}{vfs_stats['current_path']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Элементов в директории: {Fore.YELLOW}{vfs_stats['items_in_current_dir']}{Style.RESET_ALL}")
        print()
        print(f"{Fore.WHITE}Статистика VFS:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Всего директорий: {Fore.YELLOW}{vfs_stats['total_dirs']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Всего файлов: {Fore.YELLOW}{vfs_stats['total_files']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Зашифрованных директорий: {Fore.YELLOW}{vfs_stats['encrypted_dirs']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Пасхалок: {Fore.MAGENTA}{vfs_stats['easter_eggs']}{Style.RESET_ALL}")
    
    def _handle_keyboard_interrupt(self) -> None:
        """Обработка прерывания клавиатуры (Ctrl+C)"""
        print(f"\n\n{Fore.YELLOW}⚠  Прерывание (Ctrl+C). Выход в главное меню...{Style.RESET_ALL}")
        self.is_running = False
    
    def _handle_error(self, error: Exception) -> None:
        """Обработка ошибок в игровой сессии"""
        print(f"\n{Fore.RED}╔{'═'*78}╗")
        print(f"║{'ОШИБКА В ИГРОВОЙ СЕССИИ':^78}║")
        print(f"╚{'═'*78}╝{Style.RESET_ALL}")
        print(f"{Fore.RED}Ошибка: {error}{Style.RESET_ALL}")
        
        if self.debug_mode:
            import traceback
            traceback.print_exc()
        
        print(f"\n{Fore.YELLOW}Игровая сессия будет продолжена через 3 секунды...{Style.RESET_ALL}")
        time.sleep(3)
    
    def _cleanup(self) -> None:
        """Очистка ресурсов при завершении сессии"""
        print(f"{Fore.CYAN}Завершение игровой сессии...{Style.RESET_ALL}")
        
        # Завершаем сессию в game_state
        self.game_state.end_session()
        
        # Сохраняем прогресс
        print(f"{Fore.YELLOW}Сохранение прогресса...{Style.RESET_ALL}")
        self.game_state.save()
        
        # Выводим итоги сессии
        self._print_session_summary()
        
        print(f"{Fore.GREEN}Сессия завершена. Возврат в главное меню.{Style.RESET_ALL}")
        time.sleep(2)
    
    def _print_session_summary(self) -> None:
        """Вывести итоги игровой сессии"""
        session_duration = time.time() - self.session_start_time
        minutes = int(session_duration // 60)
        seconds = int(session_duration % 60)
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'ИТОГИ СЕССИИ':^60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"{Fore.WHITE}Длительность: {Fore.YELLOW}{minutes:02d}:{seconds:02d}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Выполнено команд: {Fore.YELLOW}{self.commands_executed}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Очков заработано: {Fore.GREEN}{self.game_state.session_score}{Style.RESET_ALL}")
        
        # Статистика VFS
        vfs_stats = self.vfs.get_stats()
        print(f"\n{Fore.WHITE}Исследовано:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Директорий: {Fore.YELLOW}{vfs_stats['total_dirs']}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Файлов: {Fore.YELLOW}{vfs_stats['total_files']}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Расшифровано: {Fore.YELLOW}{vfs_stats['total_dirs'] - vfs_stats['encrypted_dirs']}/{vfs_stats['total_dirs']}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Пасхалок найдено: {Fore.MAGENTA}{vfs_stats['easter_eggs']}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")


# Импорты для типов
try:
    from .vfs_generator import DirNode
except ImportError:
    # Заглушка для тестирования
    class DirNode:
        pass


# Тестирование класса (если файл запущен напрямую)
if __name__ == "__main__":
    print("Тестирование GameSession...")
    
    # Создаем состояние игры
    game_state = GameState()
    
    # Создаем игровую сессию
    print(f"{Fore.CYAN}Создание тестовой сессии...{Style.RESET_ALL}")
    session = GameSession(game_state, new_game=True, seed=42)
    
    # Запускаем сессию (но только для теста, без реального ввода)
    print(f"\n{Fore.YELLOW}Имитация работы сессии...{Style.RESET_ALL}")
    
    # Показываем текущий путь
    print(f"Текущий путь: {session.vfs.get_current_path_str()}")
    
    # Показываем содержимое корневой директории
    print(f"\nСодержимое корневой директории:")
    for item in session.vfs.list_directory():
        print(f"  {item}")
    
    # Тестируем обработку команды
    test_commands = ["dir", "help", "version", "stats"]
    
    for cmd in test_commands:
        print(f"\n{Fore.CYAN}Тест команды: '{cmd}'{Style.RESET_ALL}")
        result = session.command_handler.execute(cmd)
        if result:
            print(result)
    
    # Завершаем сессию
    print(f"\n{Fore.GREEN}Тест завершен успешно!{Style.RESET_ALL}")
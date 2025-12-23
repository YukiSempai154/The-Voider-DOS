"""
Класс MainMenu: главное меню игры с 4 кнопками и отображением счета
"""

import sys
import os
import time
from typing import Optional, Tuple, Dict, Any

# Импортируем конфигурацию
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from config import GAME_NAME, VERSION, BUILD_TYPE, AUTHOR, VERSION_STRING, UI

# Импортируем модули интерфейса
from .console_ui import ConsoleUI, console
from voider_dos.ui.color_scheme import ColorSchemeManager, color_manager


class MainMenu:
    """Класс для управления главным меню игры"""
    
    def __init__(self, game_state):
        """
        Инициализация главного меню
        
        Args:
            game_state: Объект состояния игры
        """
        self.game_state = game_state
        self.console = ConsoleUI(console_width=UI['console_width'])
        self.color_mgr = color_manager
        
        # Определяем пункты меню согласно требованиям
        self.menu_items = [
            ("1", "Начать игру", "Новая случайная файловая система"),
            ("2", "Помощь", "Список команд и руководство"),
            ("3", "Справка", "Об игре и управлении"),
            ("4", "Выйти", "Завершить игру"),
        ]
        
        # Загружаем ASCII-арт для заголовка
        self.title_art = self._load_title_art()
        
    def _load_title_art(self) -> str:
        """Загрузить ASCII-арт для заголовка"""
        try:
            # Пытаемся загрузить из файла
            art_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ascii_art', 'title.txt')
            if os.path.exists(art_path):
                with open(art_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except:
            pass
        
        # Если файла нет, используем заглушку
        return f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ████████╗██╗  ██╗███████╗    ██╗   ██╗ ██████╗ ██╗███████╗██████╗     ██████╗  ██████╗ ███████╗
║   ╚══██╔══╝██║  ██║██╔════╝    ██║   ██║██╔═══██╗██║██╔════╝██╔══██╗    ██╔════╝ ██╔═══██╗██╔════╝
║      ██║   ███████║█████╗      ██║   ██║██║   ██║██║█████╗  ██║  ██║    ██║  ███╗██║   ██║███████╗
║      ██║   ██╔══██║██╔══╝      ╚██╗ ██╔╝██║   ██║██║██╔══╝  ██║  ██║    ██║   ██║██║   ██║╚════██║
║      ██║   ██║  ██║███████╗     ╚████╔╝ ╚██████╔╝██║███████╗██████╔╝    ╚██████╔╝╚██████╔╝███████║
║      ╚═╝   ╚═╝  ╚═╝╚══════╝      ╚═══╝   ╚═════╝ ╚═╝╚══════╝╚═════╝      ╚═════╝  ╚═════╝ ╚══════╝
║                                                          ║
║                      Console Edition                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    
    def display(self) -> str:
        """
        Отобразить главное меню и получить выбор пользователя
        
        Returns:
            Код выбранного действия
        """
        while True:
            self._clear_and_display()
            choice = self._get_user_choice()
            
            if choice in ["1", "2", "3", "4"]:
                return self._process_choice(choice)
            else:
                self._show_error("Неверный выбор. Пожалуйста, введите цифру от 1 до 4.")
                time.sleep(1)
    
    def _clear_and_display(self) -> None:
        """Очистить экран и отобразить меню"""
        self.console.clear_screen()
        self._display_score()
        self._display_title()
        self._display_menu_items()
        self._display_version_info()
    
    def _display_score(self) -> None:
        """Отобразить счет в верхнем правом углу"""
        score = self.game_state.total_score
        score_text = f"Score: {score}"
        
        # Позиционируем счет в верхнем правом углу
        # Используем ANSI коды для позиционирования
        padding = UI['console_width'] - len(score_text) - 4
        print(f"\033[0;{padding}H{self.color_mgr.get_current_color('score')}{score_text}\033[0;0H")
        print()  # Переход на новую строку после позиционирования
    
    def _display_title(self) -> None:
        """Отобразить заголовок игры с ASCII-артом"""
        # Если есть ASCII-арт, отображаем его
        if self.title_art:
            art_lines = self.title_art.strip().split('\n')
            for line in art_lines:
                padding = (UI['console_width'] - len(line)) // 2
                print(f"{' ' * padding}{self.color_mgr.get_current_color('title')}{line}")
        else:
            # Иначе отображаем простое название
            print()
            self.console.print_header(GAME_NAME, 'title')
        print()
    
    def _display_menu_items(self) -> None:
        """Отобразить пункты меню"""
        # Отображаем рамку меню
        border_top = f"╔{'═' * (UI['console_width'] - 2)}╗"
        border_bottom = f"╚{'═' * (UI['console_width'] - 2)}╝"
        
        print(f"{self.color_mgr.get_current_color('menu_item')}{border_top}")
        
        # Отображаем каждый пункт меню
        for key, title, description in self.menu_items:
            # Формируем левую часть (номер и название)
            left_part = f" {self.color_mgr.get_current_color('menu_item')}{key}. {title}"
            
            # Формируем правую часть (описание)
            right_part = f"{self.color_mgr.get_current_color('version_info')}{description}"
            
            # Вычисляем отступ для центрирования
            left_len = len(key) + len(title) + 3  # 3 = ". " и пробел
            right_len = len(description)
            middle_padding = UI['console_width'] - left_len - right_len - 4  # -4 для границ и пробелов
            
            if middle_padding < 1:
                middle_padding = 1
            
            print(f"║{left_part}{' ' * middle_padding}{right_part} ║")
        
        print(f"{self.color_mgr.get_current_color('menu_item')}{border_bottom}")
        print()
    
    def _display_version_info(self) -> None:
        """Отобразить информацию о версии в нижнем правом углу"""
        # Позиционируем в нижней части экрана
        lines = VERSION_STRING.split('\n')
        for i, line in enumerate(lines):
            padding = UI['console_width'] - len(line) - 2
            line_pos = UI['console_width'] - len(lines) + i  # Примерное позиционирование
            print(f"\033[{line_pos};{padding}H{self.color_mgr.get_current_color('version_info')}{line}")
        
        # Возвращаем курсор в начало
        print(f"\033[{len(self.menu_items) + 15};0H")
    
    def _get_user_choice(self) -> str:
        """Получить выбор пользователя"""
        self.console.print_separator('path')
        choice = input(f"{self.color_mgr.get_current_color('prompt')}Выберите пункт [1-4]: ").strip()
        return choice
    
    def _show_error(self, message: str) -> None:
        """Показать сообщение об ошибке"""
        self.console.print_error(message)
        print()  # Пустая строка для разделения
    
    def _process_choice(self, choice: str) -> str:
        """
        Обработать выбор пользователя
        
        Returns:
            Код действия для основного цикла игры
        """
        if choice == "1":
            return "new_game"
        elif choice == "2":
            self._show_help()
            return "help"
        elif choice == "3":
            self._show_about()
            return "about"
        elif choice == "4":
            self._exit_game()
            return "exit"
        
        return "invalid"
    
    def _show_help(self) -> None:
        """Показать экран помощи"""
        self.console.clear_screen()
        self._display_score()
        
        # Загружаем текст помощи
        help_text = self._load_help_text()
        
        # Отображаем помощь
        self.console.print_header("ПОМОЩЬ ПО КОМАНДАМ", 'help_title')
        print()
        
        # Разбиваем текст на страницы если он длинный
        lines = help_text.split('\n')
        page_size = 20
        total_pages = (len(lines) + page_size - 1) // page_size
        
        for page in range(total_pages):
            start = page * page_size
            end = min(start + page_size, len(lines))
            
            for i in range(start, end):
                line = lines[i]
                # Проверяем, является ли строка командой (начинается с '  ')
                if line.startswith('  '):
                    # Разделяем команду и описание
                    if ' - ' in line:
                        cmd, desc = line.split(' - ', 1)
                        print(f"{self.color_mgr.get_current_color('help_command')}{cmd.strip()}")
                        print(f"     {desc.strip()}")
                    else:
                        print(f"{self.color_mgr.get_current_color('help_command')}{line}")
                elif ':' in line and not line.startswith(' '):
                    # Заголовок раздела
                    print(f"\n{self.color_mgr.get_current_color('help_title')}{line}")
                else:
                    # Обычный текст
                    print(f"{self.color_mgr.get_current_color('path')}{line}")
            
            # Если есть следующая страница, ждем нажатия
            if page < total_pages - 1:
                print(f"\n{self.color_mgr.get_current_color('warning')}--- Нажмите Enter для продолжения ---")
                input()
        
        print(f"\n{self.color_mgr.get_current_color('warning')}Нажмите Enter для возврата в меню...")
        input()
    
    def _load_help_text(self) -> str:
        """Загрузить текст помощи"""
        try:
            help_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'help_texts', 'help_ru.txt')
            if os.path.exists(help_path):
                with open(help_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except:
            pass
        
        # Текст помощи по умолчанию
        return """
ОСНОВНЫЕ КОМАНДЫ:
  dir - Показать содержимое текущей директории
  cd <папка> - Перейти в указанную папку
  cd .. - Вернуться на уровень выше
  pwd - Показать текущий путь

РАБОТА С ФАЙЛАМИ:
  <имя_файла> - Открыть файл (пример: README.txt)
  type <файл> - Показать содержимое файла
  find <текст> - Поиск файлов по содержимому

ШИФРОВАНИЕ:
  decode <шифр> <текст> - Расшифровать директорию
  ciphers - Показать доступные шифры
  encrypt <текст> <тип> - Зашифровать текст (для тренировки)

СИСТЕМНЫЕ КОМАНДЫ:
  score - Показать текущий счет
  stats - Подробная статистика
  history - История команд
  clear/cls - Очистить экран
  help - Эта справка
  exit - Выйти в главное меню

ПРИМЕРЫ ШИФРОВ:
  HEX: 48656C6C6F → Hello
  ASCII: 72 101 108 108 111 → Hello
  Binary: 01001000 01100101 → He
  Base64: SGVsbG8= → Hello
  ROT13: Uryyb → Hello
  Caesar(3): Khoor → Hello
"""
    
    def _show_about(self) -> None:
        """Показать информацию об игре"""
        self.console.clear_screen()
        self._display_score()
        
        # Загружаем текст о игре
        about_text = self._load_about_text()
        
        # Отображаем информацию
        self.console.print_header("ОБ ИГРЕ THE-VOIDER-DOS", 'help_title')
        print()
        
        lines = about_text.split('\n')
        for line in lines:
            if line.startswith('  •'):
                print(f"{self.color_mgr.get_current_color('success')}{line}")
            elif ':' in line and not line.startswith(' '):
                print(f"\n{self.color_mgr.get_current_color('help_title')}{line}")
            else:
                print(f"{self.color_mgr.get_current_color('path')}{line}")
        
        print(f"\n{self.color_mgr.get_current_color('warning')}Нажмите Enter для возврата в меню...")
        input()
    
    def _load_about_text(self) -> str:
        """Загрузить текст об игре"""
        try:
            about_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'help_texts', 'about.txt')
            if os.path.exists(about_path):
                with open(about_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except:
            pass
        
        # Текст по умолчанию
        return """
ИДЕЯ:
  THE-VOIDER-DOS - это консольная игра в стиле ретро, вдохновленная
  мини-игрой ProgressDOS из Progressbar95. Исследуйте процедурно
  генерируемую файловую систему, расшифровывайте директории и
  находите скрытые пасхалки.

ОСОБЕННОСТИ:
  • Процедурная генерация - каждый запуск создает уникальную ФС
  • 6 типов шифрования - HEX, ASCII, Binary, Base64, ROT13, Caesar
  • Система счета и достижений - собирайте очки и разблокируйте достижения
  • Скрытые пасхалки - найдите все секретные файлы
  • Сохранение прогресса - ваш счет сохраняется между сессиями

УПРАВЛЕНИЕ:
  • Используйте клавиатуру для ввода команд
  • Стрелки Вверх/Вниз - навигация по истории команд
  • Tab - автодополнение команд и имен файлов
  • Ctrl+C - экстренный выход в меню

ЦЕЛЬ ИГРЫ:
  Набрать как можно больше очков, исследуя файловую систему,
  расшифровывая директории и находя пасхалки.

"В пустоте DOS-а найдется больше, чем кажется на первый взгляд..."
"""
    
    def _exit_game(self) -> None:
        """Выйти из игры"""
        self.console.clear_screen()
        
        print(f"\n{self.color_mgr.get_current_color('title')}{'=' * 60}")
        print(f"{self.color_mgr.get_current_color('title')}{'ВЫХОД ИЗ ИГРЫ':^60}")
        print(f"{self.color_mgr.get_current_color('title')}{'=' * 60}")
        print()
        
        print(f"{self.color_mgr.get_current_color('warning')}Сохранение прогресса...")
        self.game_state.save()
        
        print(f"{self.color_mgr.get_current_color('success')}Прогресс сохранен!")
        print(f"{self.color_mgr.get_current_color('title')}Спасибо за игру в {GAME_NAME}!")
        print(f"{self.color_mgr.get_current_color('version_info')}До новых встреч в пустоте DOS-а...")
        
        time.sleep(2)
        
        # Выход из программы
        import sys
        sys.exit(0)


# Функция для быстрого создания и отображения меню
def show_main_menu(game_state) -> str:
    """
    Быстрая функция для отображения главного меню
    
    Args:
        game_state: Объект состояния игры
        
    Returns:
        Код выбранного действия
    """
    menu = MainMenu(game_state)
    return menu.display()


# Тестирование класса
if __name__ == "__main__":
    print("Тестирование MainMenu...")
    
    # Создаем заглушку для game_state
    class MockGameState:
        def __init__(self):
            self.total_score = 1234
            self.score = 1234
        
        def save(self):
            print("Сохранение состояния...")
    
    # Тестируем меню
    game_state = MockGameState()
    menu = MainMenu(game_state)
    
    print("Тестирование отображения меню...")
    menu._clear_and_display()
    
    # Тестируем отображение помощи
    print("\n\nТестирование экрана помощи...")
    menu._show_help()
    
    # Тестируем отображение информации об игре
    print("\n\nТестирование экрана 'Об игре'...")
    menu._show_about()
    
    print("\nТестирование завершено!")
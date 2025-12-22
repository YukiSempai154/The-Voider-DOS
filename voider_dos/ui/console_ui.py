"""
Модуль для консольного интерфейса: отрисовка псевдо-терминала, поля ввода и других элементов.
"""

import os
import sys
from colorama import Fore, Style, init

# Инициализация colorama
init(autoreset=True)

# Импортируем конфигурацию
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from config import UI, COLORS

# Создаем словарь цветов из строковых констант
COLOR_MAP = {
    'title': Fore.LIGHTCYAN_EX,
    'menu_item': Fore.YELLOW,
    'version_info': Fore.LIGHTBLACK_EX,
    'score': Fore.GREEN,
    'path': Fore.CYAN,
    'directory': Fore.BLUE,
    'file': Fore.WHITE,
    'encrypted': Fore.RED,
    'easter_egg': Fore.MAGENTA,
    'special': Fore.LIGHTYELLOW_EX,
    'error': Fore.RED,
    'success': Fore.GREEN,
    'warning': Fore.YELLOW,
    'prompt': Fore.WHITE,
    'help_title': Fore.LIGHTCYAN_EX,
    'help_command': Fore.YELLOW,
}


class ConsoleUI:
    """Класс для управления консольным интерфейсом игры"""
    
    def __init__(self, console_width: int = None):
        """
        Инициализация консольного интерфейса
        
        Args:
            console_width: Ширина консоли (если None, берется из конфига)
        """
        self.console_width = console_width or UI['console_width']
        self.current_position = 0
        self.output_buffer = []
        
        # Инициализация colorama для Windows
        init(autoreset=True)
    
    def clear_screen(self):
        """Очистить экран консоли"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.current_position = 0
    
    def get_color(self, color_name: str):
        """
        Получить цвет по имени из конфигурации
        
        Args:
            color_name: Имя цвета из конфига COLORS
            
        Returns:
            Объект цвета colorama
        """
        color_str = COLOR_MAP.get(color_name, Fore.WHITE)
        return color_str
    
    def print_color(self, text: str, color_name: str = None, end: str = '\n'):
        """
        Вывести текст указанным цветом
        
        Args:
            text: Текст для вывода
            color_name: Имя цвета из конфига COLORS
            end: Символ в конце строки
        """
        if color_name:
            color = self.get_color(color_name)
            print(f"{color}{text}{Style.RESET_ALL}", end=end)
        else:
            print(text, end=end)
        
        # Добавляем в буфер для возможного логирования
        self.output_buffer.append(text)
        if len(self.output_buffer) > 100:  # Ограничиваем размер буфера
            self.output_buffer.pop(0)
        
        self.current_position += 1
    
    def print_centered(self, text: str, color_name: str = None, width: int = None):
        """
        Вывести центрированный текст
        
        Args:
            text: Текст для вывода
            color_name: Имя цвета из конфига COLORS
            width: Ширина для центрирования
        """
        width = width or self.console_width
        
        # Разбиваем текст на строки
        lines = text.split('\n')
        for line in lines:
            centered_line = line.center(width)
            self.print_color(centered_line, color_name)
    
    def print_header(self, title: str, color_name: str = None, width: int = None):
        """
        Вывести заголовок с границами
        
        Args:
            title: Заголовок
            color_name: Имя цвета из конфига COLORS
            width: Ширина для заголовка
        """
        width = width or self.console_width
        
        border = '═' * (width - 2)  # -2 для символов границ
        self.print_color(f"╔{border}╗", color_name)
        self.print_centered(title, color_name, width)
        self.print_color(f"╚{border}╝", color_name)
    
    def print_separator(self, color_name: str = None, width: int = None):
        """
        Вывести разделитель
        
        Args:
            color_name: Имя цвета из конфига COLORS
            width: Ширина разделителя
        """
        width = width or self.console_width
        
        separator = '─' * width
        self.print_color(separator, color_name)
    
    def print_prompt(self, path: str, score: int = 0, prompt_symbol: str = None) -> str:
        """
        Вывести приглашение для ввода команды
        
        Args:
            path: Текущий путь в файловой системе
            score: Текущий счет
            prompt_symbol: Символ приглашения
            
        Returns:
            Строка приглашения (без ввода пользователя)
        """
        prompt_symbol = prompt_symbol or UI['prompt_symbol']
        
        # Формируем строку приглашения
        prompt_parts = []
        
        # Добавляем счет (если не ноль)
        if score > 0:
            prompt_parts.append(f"{Fore.GREEN}[{score}]{Style.RESET_ALL}")
        
        # Добавляем путь
        prompt_parts.append(f"{Fore.CYAN}{path}{Style.RESET_ALL}")
        
        # Добавляем символ приглашения
        prompt_parts.append(f"{Fore.YELLOW}{prompt_symbol}{Style.RESET_ALL}")
        
        prompt = ' '.join(prompt_parts) + ' '
        
        # Выводим приглашение без перевода строки
        print(prompt, end='')
        
        # Возвращаем строку приглашения (без цвета, если нужно для логирования)
        return prompt
    
    def print_error(self, text: str):
        """Вывести сообщение об ошибке"""
        self.print_color(f"✗ {text}", 'error')
    
    def print_success(self, text: str):
        """Вывести сообщение об успехе"""
        self.print_color(f"✓ {text}", 'success')
    
    def print_warning(self, text: str):
        """Вывести предупреждение"""
        self.print_color(f"⚠ {text}", 'warning')
    
    def print_info(self, text: str):
        """Вывести информационное сообщение"""
        self.print_color(text, 'path')  # Используем цвет пути для информации
    
    def print_debug(self, text: str):
        """Вывести отладочное сообщение"""
        self.print_color(f"[DEBUG] {text}", 'version_info')
    
    def print_table(self, data: list, headers: list, col_widths: list = None, color_name: str = None):
        """
        Вывести таблицу
        
        Args:
            data: Список списков (строки и столбцы)
            headers: Список заголовков
            col_widths: Список ширин столбцов. Если None, вычисляется автоматически.
            color_name: Имя цвета для таблицы
        """
        if not data or not headers:
            return
        
        # Определяем ширины столбцов
        if col_widths is None:
            col_widths = []
            for i, header in enumerate(headers):
                max_len = len(str(header))
                for row in data:
                    if i < len(row):
                        max_len = max(max_len, len(str(row[i])))
                col_widths.append(max_len + 2)  # Добавляем отступ
        
        # Вывод заголовков
        header_row = ''
        for i, header in enumerate(headers):
            header_row += str(header).ljust(col_widths[i])
        self.print_color(header_row, color_name)
        
        # Вывод разделителя
        separator = ''
        for width in col_widths:
            separator += '─' * width
        self.print_color(separator, color_name)
        
        # Вывод данных
        for row in data:
            row_str = ''
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    row_str += str(cell).ljust(col_widths[i])
            self.print_color(row_str, color_name)
    
    def print_file_content(self, filename: str, content: str, is_easter_egg: bool = False):
        """
        Вывести содержимое файла в стилизованном виде
        
        Args:
            filename: Имя файла
            content: Содержимое файла
            is_easter_egg: Флаг, является ли файл пасхалкой
        """
        if is_easter_egg:
            self.print_header("🎉 ПАСХАЛКА НАЙДЕНА! 🎉", 'easter_egg')
            print()  # Пустая строка
        
        self.print_color(f"Файл: {filename}", 'file')
        self.print_separator('file')
        self.print_color(content, 'file')
        self.print_separator('file')
    
    def print_decryption_success(self, dir_name: str, points: int):
        """
        Вывести сообщение об успешной расшифровке
        
        Args:
            dir_name: Имя директории
            points: Количество начисленных очков
        """
        self.print_header("🎯 ДИРЕКТОРИЯ РАСШИФРОВАНА! 🎯", 'success')
        print()  # Пустая строка
        self.print_color(f"Доступ открыт к директории: {dir_name}", 'path')
        self.print_color(f"+{points} очков за расшифровку!", 'success')
    
    def print_directory_listing(self, items: list, path: str, show_hidden: bool = False):
        """
        Вывести список содержимого директории
        
        Args:
            items: Список элементов (строк или объектов)
            path: Текущий путь
            show_hidden: Показывать ли скрытые файлы
        """
        self.print_color(f"Содержимое {path}:", 'path')
        self.print_separator('path')
        
        if not items:
            self.print_color("Директория пуста", 'warning')
            return
        
        for item in items:
            # Если item - строка
            if isinstance(item, str):
                self.print_color(f"  {item}", 'directory' if '<DIR>' in item else 'file')
            # Если item - объект DirNode или FileNode (из vfs_generator)
            elif hasattr(item, 'name'):
                if hasattr(item, 'encrypted') and item.encrypted:
                    self.print_color(f"  [ЗАШИФРОВАНО] {item.cipher_text}", 'encrypted')
                elif hasattr(item, 'is_easter_egg') and item.is_easter_egg:
                    self.print_color(f"  [E] {item.name}{getattr(item, 'extension', '')}", 'easter_egg')
                elif hasattr(item, 'is_special') and item.is_special:
                    self.print_color(f"  [S] {item.name}{getattr(item, 'extension', '')}", 'special')
                elif hasattr(item, 'extension'):  # Файл
                    self.print_color(f"       {item.name}{item.extension}", 'file')
                else:  # Директория
                    self.print_color(f"  <DIR>   {item.name}", 'directory')
        
        # Подсчет статистики
        dir_count = sum(1 for item in items if isinstance(item, str) and '<DIR>' in item or 
                       (hasattr(item, 'extension') == False and hasattr(item, 'name')))
        file_count = len(items) - dir_count
        
        self.print_separator('path')
        self.print_color(f"Директорий: {dir_count}, Файлов: {file_count}", 'path')
    
    def print_help_table(self, commands: list):
        """
        Вывести таблицу команд
        
        Args:
            commands: Список команд в формате [(команда, описание), ...]
        """
        headers = ["Команда", "Описание"]
        data = commands
        self.print_table(data, headers, col_widths=[20, 50], color_name='help_command')
    
    def print_progress_bar(self, current: int, total: int, width: int = 50, label: str = ""):
        """
        Вывести прогресс-бар
        
        Args:
            current: Текущее значение
            total: Максимальное значение
            width: Ширина прогресс-бара в символах
            label: Метка прогресс-бара
        """
        progress = current / total if total > 0 else 0
        bar_width = int(width * progress)
        bar = '█' * bar_width + '░' * (width - bar_width)
        percent = int(progress * 100)
        
        if label:
            self.print_color(f"{label}: [{bar}] {percent}% ({current}/{total})", 'success')
        else:
            self.print_color(f"[{bar}] {percent}% ({current}/{total})", 'success')
    
    def print_loading_screen(self, message: str = "Загрузка..."):
        """
        Вывести экран загрузки
        
        Args:
            message: Сообщение загрузки
        """
        self.clear_screen()
        self.print_centered("THE-VOIDER-DOS", 'title')
        print()
        self.print_centered(message, 'menu_item')
        print()
        
        # Анимация загрузки
        import time
        for i in range(3):
            self.print_centered("." * (i + 1), 'path')
            time.sleep(0.5)
            # Перемещаем курсор на строку выше
            print("\033[F\033[K", end='')
        
        self.clear_screen()
    
    def get_input(self, prompt: str = "", color_name: str = None) -> str:
        """
        Получить ввод от пользователя с цветным приглашением
        
        Args:
            prompt: Текст приглашения
            color_name: Имя цвета для приглашения
            
        Returns:
            Введенная строка
        """
        if prompt:
            if color_name:
                color = self.get_color(color_name)
                print(f"{color}{prompt}{Style.RESET_ALL}", end='')
            else:
                print(prompt, end='')
        
        try:
            user_input = input()
            return user_input.strip()
        except EOFError:
            return "exit"
        except KeyboardInterrupt:
            raise
    
    def wait_for_continue(self, message: str = "Нажмите Enter для продолжения..."):
        """
        Ожидание нажатия Enter
        
        Args:
            message: Сообщение для ожидания
        """
        self.print_color(message, 'warning')
        input()
    
    def print_version_info(self, version_string: str):
        """
        Вывести информацию о версии
        
        Args:
            version_string: Строка с информацией о версии
        """
        # Позиционируем в правом нижнем углу
        lines = version_string.split('\n')
        for line in lines:
            # Вычисляем позицию для правого края
            padding = self.console_width - len(line) - 2
            print(f"{' ' * padding}{Fore.LIGHTBLACK_EX}{line}{Style.RESET_ALL}")
    
    def print_score_display(self, score: int, position: str = "top_right"):
        """
        Вывести отображение счета в указанной позиции
        
        Args:
            score: Текущий счет
            position: Позиция ('top_right', 'top_left', 'bottom_right', 'bottom_left')
        """
        score_text = f"Score: {score}"
        
        if position == "top_right":
            # Перемещаем курсор и выводим счет
            print(f"\033[0;{self.console_width - len(score_text)}H{Fore.GREEN}{score_text}{Style.RESET_ALL}")
        elif position == "top_left":
            print(f"\033[0;0H{Fore.GREEN}{score_text}{Style.RESET_ALL}")
        # Для других позиций нужно сохранять текущую позицию курсора, что сложнее


# Создаем глобальный экземпляр для удобства
console = ConsoleUI()


# Функции для быстрого доступа (удобно для импорта)
def clear_screen():
    """Очистить экран"""
    console.clear_screen()

def print_color(text, color_name=None):
    """Вывести цветной текст"""
    console.print_color(text, color_name)

def print_centered(text, color_name=None):
    """Вывести центрированный текст"""
    console.print_centered(text, color_name)

def print_error(text):
    """Вывести ошибку"""
    console.print_error(text)

def print_success(text):
    """Вывести успех"""
    console.print_success(text)

def print_warning(text):
    """Вывести предупреждение"""
    console.print_warning(text)


# Тестирование класса
if __name__ == "__main__":
    print("Тестирование ConsoleUI...")
    
    ui = ConsoleUI(console_width=80)
    
    # Тестируем различные методы
    ui.print_loading_screen("Тестирование интерфейса...")
    
    ui.print_header("ТЕСТИРОВАНИЕ CONSOLE UI", 'title')
    print()
    
    ui.print_color("Обычный текст", 'file')
    ui.print_color("Текст ошибки", 'error')
    ui.print_color("Текст успеха", 'success')
    ui.print_color("Предупреждение", 'warning')
    print()
    
    ui.print_centered("Центрированный текст", 'path')
    print()
    
    ui.print_separator('path')
    
    # Тестируем таблицу
    commands = [
        ["dir", "Показать содержимое директории"],
        ["cd <папка>", "Перейти в папку"],
        ["decode <шифр> <текст>", "Расшифровать директорию"],
        ["help", "Показать справку"],
    ]
    ui.print_help_table(commands)
    print()
    
    # Тестируем прогресс-бар
    ui.print_progress_bar(25, 100, label="Прогресс тестирования")
    print()
    
    # Тестируем вывод содержимого файла
    ui.print_file_content("test.txt", "Это тестовое содержимое файла.\nВторая строка.")
    print()
    
    # Тестируем вывод успеха расшифровки
    ui.print_decryption_success("SECRET_DIR", 50)
    print()
    
    # Тестируем приглашение
    prompt = ui.print_prompt("VOID:\\System32", 150)
    print(" [симуляция ввода команды]")
    print()
    
    # Тестируем ввод
    # user_input = ui.get_input("Введите что-нибудь: ", 'prompt')
    # print(f"Вы ввели: {user_input}")
    
    ui.print_success("Тестирование завершено!")
"""
Цветовые схемы для THE-VOIDER-DOS с использованием Colorama
"""

from colorama import Fore, Back, Style, init
import sys

# Инициализация colorama
init(autoreset=True)

# Импортируем конфигурацию
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from config import COLORS


class ColorScheme:
    """Базовый класс для цветовых схем"""
    
    def __init__(self, name: str, description: str):
        """
        Инициализация цветовой схемы
        
        Args:
            name: Название схемы
            description: Описание схемы
        """
        self.name = name
        self.description = description
        self._colors = {}
    
    def get_color(self, element: str) -> str:
        """
        Получить цвет для элемента
        
        Args:
            element: Имя элемента из конфига COLORS
            
        Returns:
            Цвет в формате colorama (Fore.COLOR)
        """
        # Если цвет определен в схеме, возвращаем его
        if element in self._colors:
            return self._colors[element]
        
        # Иначе возвращаем цвет по умолчанию из конфига
        color_name = COLORS.get(element, 'WHITE')
        return getattr(Fore, color_name, Fore.WHITE)
    
    def set_color(self, element: str, color: str):
        """
        Установить цвет для элемента
        
        Args:
            element: Имя элемента
            color: Имя цвета (например, 'GREEN', 'RED', 'CYAN')
        """
        try:
            color_obj = getattr(Fore, color, Fore.WHITE)
            self._colors[element] = color_obj
        except AttributeError:
            print(f"Цвет '{color}' не найден, используется WHITE")
            self._colors[element] = Fore.WHITE
    
    def apply_theme(self):
        """Применить цветовую схему (абстрактный метод)"""
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def print_preview(self):
        """Показать предпросмотр цветовой схемы"""
        print(f"\n{self.get_color('title')}Цветовая схема: {self.name}")
        print(f"{self.get_color('menu_item')}{self.description}")
        print(f"{self.get_color('version_info')}{'─' * 60}")
        
        # Показываем примеры цветов
        elements = [
            ('Заголовок', 'title'),
            ('Меню', 'menu_item'),
            ('Путь', 'path'),
            ('Директория', 'directory'),
            ('Файл', 'file'),
            ('Зашифровано', 'encrypted'),
            ('Пасхалка', 'easter_egg'),
            ('Успех', 'success'),
            ('Ошибка', 'error'),
            ('Предупреждение', 'warning')
        ]
        
        for display_name, element_name in elements:
            color = self.get_color(element_name)
            print(f"{color}{display_name:20} → Пример текста")
        
        print()


class ClassicGreenScheme(ColorScheme):
    """Классическая зеленая схема (стандарт для DOS)"""
    
    def __init__(self):
        super().__init__(
            name="Классическая зеленая",
            description="Стандартная цветовая схема в стиле старых DOS терминалов"
        )
        
        # Определяем цвета для схемы
        self._colors = {
            'title': Fore.LIGHTGREEN_EX,
            'menu_item': Fore.GREEN,
            'version_info': Fore.LIGHTBLACK_EX,
            'score': Fore.LIGHTGREEN_EX,
            'path': Fore.GREEN,
            'directory': Fore.LIGHTCYAN_EX,
            'file': Fore.LIGHTGREEN_EX,
            'encrypted': Fore.LIGHTRED_EX,
            'easter_egg': Fore.LIGHTMAGENTA_EX,
            'special': Fore.LIGHTYELLOW_EX,
            'error': Fore.LIGHTRED_EX,
            'success': Fore.LIGHTGREEN_EX,
            'warning': Fore.LIGHTYELLOW_EX,
            'prompt': Fore.GREEN,
            'help_title': Fore.LIGHTCYAN_EX,
            'help_command': Fore.LIGHTGREEN_EX,
        }
    
    def apply_theme(self):
        """Применить классическую зеленую схему"""
        # Ничего не делаем, так как цвета уже установлены
        pass


class AmberScheme(ColorScheme):
    """Янтарная цветовая схема"""
    
    def __init__(self):
        super().__init__(
            name="Янтарная",
            description="Теплая янтарная цветовая схема в стиле мониторов 80-х"
        )
        
        # Определяем цвета для янтарной схемы
        self._colors = {
            'title': Fore.LIGHTYELLOW_EX,
            'menu_item': Fore.YELLOW,
            'version_info': Fore.LIGHTBLACK_EX,
            'score': Fore.LIGHTRED_EX,
            'path': Fore.LIGHTYELLOW_EX,
            'directory': Fore.YELLOW,
            'file': Fore.LIGHTYELLOW_EX,
            'encrypted': Fore.LIGHTRED_EX,
            'easter_egg': Fore.LIGHTMAGENTA_EX,
            'special': Fore.LIGHTCYAN_EX,
            'error': Fore.LIGHTRED_EX,
            'success': Fore.LIGHTGREEN_EX,
            'warning': Fore.YELLOW,
            'prompt': Fore.YELLOW,
            'help_title': Fore.LIGHTYELLOW_EX,
            'help_command': Fore.YELLOW,
        }
    
    def apply_theme(self):
        """Применить янтарную схему"""
        pass


class MonochromeScheme(ColorScheme):
    """Монохромная цветовая схема"""
    
    def __init__(self):
        super().__init__(
            name="Монохромная",
            description="Черно-белая схема для минимализма и ночных сессий"
        )
        
        # Определяем цвета для монохромной схемы
        self._colors = {
            'title': Fore.WHITE,
            'menu_item': Fore.WHITE,
            'version_info': Fore.LIGHTBLACK_EX,
            'score': Fore.WHITE,
            'path': Fore.WHITE,
            'directory': Fore.WHITE,
            'file': Fore.WHITE,
            'encrypted': Fore.LIGHTBLACK_EX,
            'easter_egg': Fore.WHITE,
            'special': Fore.WHITE,
            'error': Fore.WHITE,
            'success': Fore.WHITE,
            'warning': Fore.WHITE,
            'prompt': Fore.WHITE,
            'help_title': Fore.WHITE,
            'help_command': Fore.WHITE,
        }
    
    def apply_theme(self):
        """Применить монохромную схему"""
        # Для монохромной схемы отключаем стили
        print(Style.NORMAL)


class MatrixScheme(ColorScheme):
    """Схема 'Матрица' (зеленый на черном)"""
    
    def __init__(self):
        super().__init__(
            name="Матрица",
            description="Стиль 'Матрицы': зеленый текст на черном фоне с эффектами"
        )
        
        # Определяем цвета для схемы Матрица
        self._colors = {
            'title': Fore.GREEN,
            'menu_item': Fore.GREEN,
            'version_info': Fore.LIGHTBLACK_EX,
            'score': Fore.LIGHTGREEN_EX,
            'path': Fore.GREEN,
            'directory': Fore.LIGHTGREEN_EX,
            'file': Fore.GREEN,
            'encrypted': Fore.LIGHTRED_EX,
            'easter_egg': Fore.LIGHTCYAN_EX,
            'special': Fore.LIGHTYELLOW_EX,
            'error': Fore.LIGHTRED_EX,
            'success': Fore.LIGHTGREEN_EX,
            'warning': Fore.LIGHTYELLOW_EX,
            'prompt': Fore.GREEN,
            'help_title': Fore.LIGHTGREEN_EX,
            'help_command': Fore.GREEN,
        }
    
    def apply_theme(self):
        """Применить схему Матрица"""
        # Устанавливаем черный фон
        print(Back.BLACK, end='')


class RetroBlueScheme(ColorScheme):
    """Ретро синяя схема"""
    
    def __init__(self):
        super().__init__(
            name="Ретро синяя",
            description="Синяя цветовая схема в стиле старых компьютеров"
        )
        
        # Определяем цвета для ретро синей схемы
        self._colors = {
            'title': Fore.LIGHTBLUE_EX,
            'menu_item': Fore.BLUE,
            'version_info': Fore.LIGHTBLACK_EX,
            'score': Fore.LIGHTCYAN_EX,
            'path': Fore.BLUE,
            'directory': Fore.LIGHTCYAN_EX,
            'file': Fore.LIGHTBLUE_EX,
            'encrypted': Fore.LIGHTRED_EX,
            'easter_egg': Fore.LIGHTMAGENTA_EX,
            'special': Fore.LIGHTYELLOW_EX,
            'error': Fore.LIGHTRED_EX,
            'success': Fore.LIGHTGREEN_EX,
            'warning': Fore.LIGHTYELLOW_EX,
            'prompt': Fore.BLUE,
            'help_title': Fore.LIGHTBLUE_EX,
            'help_command': Fore.BLUE,
        }
    
    def apply_theme(self):
        """Применить ретро синюю схему"""
        pass


class HighContrastScheme(ColorScheme):
    """Схема с высоким контрастом"""
    
    def __init__(self):
        super().__init__(
            name="Высокий контраст",
            description="Яркие цвета с высоким контрастом для лучшей читаемости"
        )
        
        # Определяем цвета для схемы с высоким контрастом
        self._colors = {
            'title': Fore.LIGHTCYAN_EX + Style.BRIGHT,
            'menu_item': Fore.YELLOW + Style.BRIGHT,
            'version_info': Fore.WHITE,
            'score': Fore.LIGHTGREEN_EX + Style.BRIGHT,
            'path': Fore.CYAN + Style.BRIGHT,
            'directory': Fore.BLUE + Style.BRIGHT,
            'file': Fore.WHITE + Style.BRIGHT,
            'encrypted': Fore.LIGHTRED_EX + Style.BRIGHT,
            'easter_egg': Fore.LIGHTMAGENTA_EX + Style.BRIGHT,
            'special': Fore.LIGHTYELLOW_EX + Style.BRIGHT,
            'error': Fore.LIGHTRED_EX + Style.BRIGHT,
            'success': Fore.LIGHTGREEN_EX + Style.BRIGHT,
            'warning': Fore.YELLOW + Style.BRIGHT,
            'prompt': Fore.WHITE + Style.BRIGHT,
            'help_title': Fore.LIGHTCYAN_EX + Style.BRIGHT,
            'help_command': Fore.YELLOW + Style.BRIGHT,
        }
    
    def apply_theme(self):
        """Применить схему с высоким контрастом"""
        # Добавляем яркость ко всему тексту
        print(Style.BRIGHT, end='')


class ColorSchemeManager:
    """Менеджер для управления цветовыми схемами"""
    
    def __init__(self):
        """Инициализация менеджера цветовых схем"""
        self._schemes = {}
        self._current_scheme = None
        
        # Регистрируем стандартные схемы
        self.register_scheme('classic', ClassicGreenScheme())
        self.register_scheme('amber', AmberScheme())
        self.register_scheme('monochrome', MonochromeScheme())
        self.register_scheme('matrix', MatrixScheme())
        self.register_scheme('retro_blue', RetroBlueScheme())
        self.register_scheme('high_contrast', HighContrastScheme())
        
        # Устанавливаем схему по умолчанию
        self.set_scheme('classic')
    
    def register_scheme(self, scheme_id: str, scheme: ColorScheme):
        """
        Зарегистрировать новую цветовую схему
        
        Args:
            scheme_id: Идентификатор схемы
            scheme: Объект цветовой схемы
        """
        self._schemes[scheme_id] = scheme
    
    def get_scheme(self, scheme_id: str) -> ColorScheme:
        """
        Получить цветовую схему по идентификатору
        
        Args:
            scheme_id: Идентификатор схемы
            
        Returns:
            Объект цветовой схемы
            
        Raises:
            KeyError: Если схема не найдена
        """
        if scheme_id not in self._schemes:
            raise KeyError(f"Цветовая схема '{scheme_id}' не найдена")
        
        return self._schemes[scheme_id]
    
    def set_scheme(self, scheme_id: str) -> bool:
        """
        Установить текущую цветовую схему
        
        Args:
            scheme_id: Идентификатор схемы
            
        Returns:
            True если схема установлена успешно, иначе False
        """
        try:
            scheme = self.get_scheme(scheme_id)
            scheme.apply_theme()
            self._current_scheme = scheme
            return True
        except KeyError:
            print(f"Схема '{scheme_id}' не найдена, используется классическая")
            return self.set_scheme('classic')
    
    def get_current_scheme(self) -> ColorScheme:
        """
        Получить текущую цветовую схему
        
        Returns:
            Текущая цветовая схема
        """
        return self._current_scheme
    
    def get_current_color(self, element: str) -> str:
        """
        Получить цвет элемента в текущей схеме
        
        Args:
            element: Имя элемента
            
        Returns:
            Цвет в формате colorama
        """
        if self._current_scheme is None:
            # Возвращаем цвет по умолчанию из конфига
            color_name = COLORS.get(element, 'WHITE')
            return getattr(Fore, color_name, Fore.WHITE)
        
        return self._current_scheme.get_color(element)
    
    def list_schemes(self) -> list:
        """
        Получить список всех доступных цветовых схем
        
        Returns:
            Список кортежей (id, name, description)
        """
        schemes_list = []
        for scheme_id, scheme in self._schemes.items():
            schemes_list.append((scheme_id, scheme.name, scheme.description))
        
        return schemes_list
    
    def print_schemes_preview(self):
        """Показать предпросмотр всех цветовых схем"""
        print(f"{Fore.LIGHTCYAN_EX}╔{'═' * 78}╗")
        print(f"║{'ДОСТУПНЫЕ ЦВЕТОВЫЕ СХЕМЫ':^78}║")
        print(f"╚{'═' * 78}╝{Style.RESET_ALL}")
        print()
        
        schemes = self.list_schemes()
        for i, (scheme_id, name, description) in enumerate(schemes, 1):
            # Временно применяем схему для показа предпросмотра
            scheme = self.get_scheme(scheme_id)
            print(f"{scheme.get_color('title')}{i}. {name}")
            print(f"{scheme.get_color('menu_item')}   {description}")
            
            # Показываем небольшой пример
            example = f"   Пример: путь | директория | файл | ошибка"
            print(f"{scheme.get_color('path')}п{scheme.get_color('directory')}а{scheme.get_color('file')}т{scheme.get_color('error')}ь")
            print()
    
    def save_scheme_preference(self, scheme_id: str, filename: str = "color_scheme.cfg"):
        """
        Сохранить предпочтение цветовой схемы в файл
        
        Args:
            scheme_id: Идентификатор схемы
            filename: Имя файла для сохранения
        """
        try:
            with open(filename, 'w') as f:
                f.write(scheme_id)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении схемы: {e}")
            return False
    
    def load_scheme_preference(self, filename: str = "color_scheme.cfg") -> str:
        """
        Загрузить предпочтение цветовой схемы из файла
        
        Args:
            filename: Имя файла для загрузки
            
        Returns:
            Идентификатор схемы или None если не удалось загрузить
        """
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    scheme_id = f.read().strip()
                    return scheme_id
        except Exception as e:
            print(f"Ошибка при загрузке схемы: {e}")
        
        return None


# Создаем глобальный экземпляр менеджера цветовых схем
color_manager = ColorSchemeManager()


# Функции для удобного доступа к цветам
def get_color(element: str) -> str:
    """
    Получить цвет для элемента в текущей схеме
    
    Args:
        element: Имя элемента
        
    Returns:
        Цвет в формате colorama
    """
    return color_manager.get_current_color(element)


def set_scheme(scheme_id: str) -> bool:
    """
    Установить цветовую схему
    
    Args:
        scheme_id: Идентификатор схемы
        
    Returns:
        True если схема установлена успешно
    """
    return color_manager.set_scheme(scheme_id)


def print_color(element: str, text: str, end: str = '\n'):
    """
    Вывести текст цветом элемента из текущей схемы
    
    Args:
        element: Имя элемента для цвета
        text: Текст для вывода
        end: Символ в конце строки
    """
    color = get_color(element)
    print(f"{color}{text}{Style.RESET_ALL}", end=end)


def print_with_scheme(scheme_id: str, element: str, text: str, end: str = '\n'):
    """
    Вывести текст с использованием конкретной схемы
    
    Args:
        scheme_id: Идентификатор схемы
        element: Имя элемента для цвета
        text: Текст для вывода
        end: Символ в конце строки
    """
    scheme = color_manager.get_scheme(scheme_id)
    color = scheme.get_color(element)
    print(f"{color}{text}{Style.RESET_ALL}", end=end)


# Тестирование модуля
if __name__ == "__main__":
    print("Тестирование модуля цветовых схем...")
    
    # Показываем все доступные схемы
    color_manager.print_schemes_preview()
    
    # Тестируем переключение схем
    test_schemes = ['classic', 'amber', 'matrix', 'monochrome']
    
    for scheme_id in test_schemes:
        print(f"\n{Fore.LIGHTCYAN_EX}Тестируем схему: {scheme_id}{Style.RESET_ALL}")
        color_manager.set_scheme(scheme_id)
        
        # Показываем примеры цветов
        scheme = color_manager.get_scheme(scheme_id)
        scheme.print_preview()
    
    # Возвращаемся к классической схеме
    color_manager.set_scheme('classic')
    print(f"{Fore.GREEN}Возврат к классической схеме{Style.RESET_ALL}")
"""
КОНФИГУРАЦИЯ THE-VOIDER-DOS
Автор: Prunt (Yuki_Sempai)
"""

# ==================== ИНФОРМАЦИЯ О ВЕРСИИ ====================
GAME_NAME = "THE-VOIDER-DOS"
VERSION = "0.0.0.1"
BUILD_TYPE = "Alpha"  # Alpha/Beta/Demo/Release/Experimental/Crack
RELEASE_DATE = "2025"
AUTHOR = "Prunt (Yuki_Sempai)"

# Формат строки версии (отображается в меню)
VERSION_STRING = f"{GAME_NAME} v{VERSION} {BUILD_TYPE} by {AUTHOR}"

# ==================== НАСТРОЙКИ ГЕНЕРАЦИИ ====================
GENERATION = {
    'min_depth': 3,           # Минимальная глубина файловой системы
    'max_depth': 12,           # Максимальная глубина
    'min_dirs_per_level': 2,  # Минимальное количество директорий на уровень
    'max_dirs_per_level': 6,  # Максимальное количество директорий на уровень
    'min_files_per_dir': 1,   # Минимальное количество файлов в директории
    'max_files_per_dir': 5,   # Максимальное количество файлов в директории
    'encryption_chance': 0.4, # Вероятность шифрования директории (40%)
    'easter_egg_chance': 0.05,# Вероятность пасхалки в файле (5%)
    'special_dir_chance': 0.1 # Вероятность особой директории (10%)
}

# ==================== СИСТЕМА ОЧКОВ ====================
SCORING = {
    'directory_decrypted': 50,      # Очки за расшифровку директории
    'file_opened': 10,              # Очки за открытие файла
    'easter_egg_found': 100,        # Очки за пасхалку
    'special_dir_found': 75,        # Очки за особую директорию
    'first_decryption_bonus': 50,   # Бонус за первую расшифровку
    'completion_bonus': 500,        # Бонус за полное исследование
}

# ==================== СИСТЕМА ШИФРОВАНИЯ ====================
CIPHERS = {
    'enabled': ['hex', 'ascii', 'binary', 'base64', 'rot13', 'caesar'],
    'weights': {
        'hex': 30,      # 30% вероятность
        'ascii': 25,    # 25% вероятность
        'binary': 20,   # 20% вероятность
        'base64': 15,   # 15% вероятность
        'rot13': 5,     # 5% вероятность
        'caesar': 5,    # 5% вероятность
    },
    'caesar_shift_range': (1, 25)  # Диапазон сдвига для шифра Цезаря
}

# ==================== НАСТРОЙКИ ИНТЕРФЕЙСА ====================
UI = {
    'console_width': 80,            # Ширина консоли в символах
    'prompt_symbol': '>',           # Символ приглашения
    'path_separator': '\\',         # Разделитель пути (Windows-стиль)
    'root_name': 'VOID:',           # Название корневой директории
    'max_history_size': 50,         # Максимальный размер истории команд
    'show_hidden_by_default': False,# Показывать скрытые файлы по умолчанию
}

# ==================== ЦВЕТОВАЯ СХЕМА ====================
# Использует коды Colorama: Fore.*, Back.*, Style.*
COLORS = {
    'title': 'LIGHTCYAN_EX',
    'menu_item': 'YELLOW',
    'version_info': 'LIGHTBLACK_EX',
    'score': 'GREEN',
    'path': 'CYAN',
    'directory': 'BLUE',
    'file': 'WHITE',
    'encrypted': 'RED',
    'easter_egg': 'MAGENTA',
    'special': 'LIGHTYELLOW_EX',
    'error': 'RED',
    'success': 'GREEN',
    'warning': 'YELLOW',
    'prompt': 'WHITE',
    'help_title': 'LIGHTCYAN_EX',
    'help_command': 'YELLOW',
}

# ==================== ФАЙЛЫ СОХРАНЕНИЯ ====================
SAVES = {
    'save_dir': 'saves',
    'save_file': 'voider_save.json',
    'backup_count': 3,              # Количество резервных копий
    'auto_save_interval': 300,      # Автосохранение каждые 5 минут (в сек)
}

# ==================== ПУТИ К ФАЙЛАМ ДАННЫХ ====================
DATA_PATHS = {
    'ascii_art': {
        'title': 'data/ascii_art/title.txt',
        'easter_eggs_dir': 'data/ascii_art/easter_eggs/'
    },
    'name_lists': {
        'directories': 'data/name_lists/directory_names.txt',
        'files': 'data/name_lists/file_names.txt',
        'extensions': 'data/name_lists/extensions.txt'
    },
    'help_texts': {
        'help_ru': 'data/help_texts/help_ru.txt',
        'about': 'data/help_texts/about.txt'
    }
}

# ==================== НАСТРОЙКИ ПО УМОЛЧАНИЮ ====================
# Значения, используемые если файлы данных не найдены
DEFAULT_DATA = {
    'directory_names': ['System', 'User', 'Program', 'Data', 'Config', 'Temp', 
                       'Backup', 'Archive', 'Secret', 'Public', 'Logs', 'Cache'],
    'file_names': ['README', 'CONFIG', 'SETUP', 'INSTALL', 'HELP', 'INFO',
                  'DATA', 'TEMP', 'LOG', 'ERROR', 'DEBUG', 'BACKUP', 'NOTE'],
    'file_extensions': ['.txt', '.dat', '.cfg', '.sys', '.bin', '.log', '.tmp'],
    'title_art': """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                      ║
║   ████████╗██╗  ██╗███████╗    ██╗   ██╗ ██████╗ ██╗███████╗██████╗      ██████╗  ██████╗ ███████╗   ║
║   ╚══██╔══╝██║  ██║██╔════╝    ██║   ██║██╔═══██╗██║██╔════╝██╔══██╗    ██╔════╝ ██╔═══██╗██╔════╝   ║
║      ██║   ███████║█████╗      ██║   ██║██║   ██║██║█████╗  ██║  ██║    ██║  ███╗██║   ██║███████╗   ║
║      ██║   ██╔══██║██╔══╝      ╚██╗ ██╔╝██║   ██║██║██╔══╝  ██║  ██║    ██║   ██║██║   ██║╚════██║   ║
║      ██║   ██║  ██║███████╗     ╚████╔╝ ╚██████╔╝██║███████╗██████╔╝    ╚██████╔╝╚██████╔╝███████║   ║
║      ╚═╝   ╚═╝  ╚═╝╚══════╝      ╚═══╝   ╚═════╝ ╚═╝╚══════╝╚═════╝      ╚═════╝  ╚═════╝ ╚══════╝   ║
║                                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
""",
    'help_text': """
Основные команды:
  dir          - Показать содержимое текущей директории
  cd <папка>   - Перейти в указанную папку
  cd ..        - Вернуться на уровень выше
  pwd          - Показать текущий путь
  
Работа с файлами:
  <имя_файла>  - Открыть файл (пример: README.txt)
  type <файл>  - Показать содержимое файла
  find <текст> - Поиск файлов по содержимому
  
Шифрование:
  decode <шифр> <текст> - Расшифровать директорию
  ciphers      - Показать доступные шифры
  encrypt <текст> <тип> - Зашифровать текст (для тренировки)
  
Системные команды:
  score        - Показать текущий счет
  stats        - Подробная статистика
  history      - История команд
  clear/cls    - Очистить экран
  help         - Эта справка
  exit         - Выйти в главное меню
""",
    'about_text': """
THE-VOIDER-DOS - это консольная игра в стиле ретро, вдохновленная
мини-игрой ProgressDOS из Progressbar95. Исследуйте процедурно
генерируемую файловую систему, расшифровывайте директории и
находите скрытые пасхалки.

Особенности:
  • Процедурная генерация - каждый запуск создает уникальную ФС
  • 6 типов шифрования - HEX, ASCII, Binary, Base64, ROT13, Caesar
  • Система счета и достижений - собирайте очки и разблокируйте достижения
  • Скрытые пасхалки - найдите все секретные файлы
  • Сохранение прогресса - ваш счет сохраняется между сессиями
"""
}

# ==================== СПЕЦИАЛЬНЫЕ КОМАНДЫ ====================
SPECIAL_COMMANDS = {
    'debug_mode': False,            # Режим отладки
    'cheat_codes': {                # Чит-коды (только в dev-сборках)
        'UNLOCKALL': 'Расшифровать все директории',
        'MAXSCORE': 'Установить максимальный счет',
        'SHOWALL': 'Показать все скрытые файлы',
    }
}

# ==================== ТИПЫ ФАЙЛОВ И СОДЕРЖИМОЕ ====================
FILE_TYPES = {
    '.txt': {
        'templates': [
            "Файл: {filename}\nСоздан: {date}\n\n{content}",
            "Конфигурационный файл для системы.\nВерсия: {version}\n{content}",
            "Это файл с произвольными данными.\nКод: {code}\n{content}"
        ],
        'content_variants': [
            "Система работает в штатном режиме.",
            "Все параметры в пределах нормы.",
            "Резервное копирование завершено успешно.",
            "Обновление не требуется.",
            "Проверка целостности файлов... OK."
        ]
    },
    '.dat': {
        'templates': [
            "DATA_FILE:{id}\nTIMESTAMP:{time}\n{content}",
            "BINARY_DATA:{binary}\n{content}"
        ],
        'content_variants': [
            "01010100 01101000 01100101 00100000 01010110 01101111 01101001 01100100",
            "7A 68 65 20 56 6F 69 64 20 61 77 61 69 74 73",
            "U29tZSBzZWNyZXQgZGF0YSBpcyBzdG9yZWQgaGVyZQ=="
        ]
    },
    '.cfg': {
        'templates': [
            "enable_{feature}={value}\n{content}",
            "setting_{name}={value}\n{content}"
        ],
        'content_variants': [
            "graphics=high\nsound=enabled\ndifficulty=normal",
            "autosave=true\nlanguage=ru\ntheme=dark"
        ]
    },
    '.log': {
        'templates': [
            "[{timestamp}] {level}: {message}\n{content}",
            "Log entry #{id}\n{content}"
        ],
        'content_variants': [
            "Система загружена успешно",
            "Обнаружена новая периферия",
            "Очистка временных файлов"
        ]
    }
}
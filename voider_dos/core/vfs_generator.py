"""
Класс VirtualFileSystem: процедурная генерация файловой системы
"""

import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
import sys

# Добавляем путь для импорта config.py из корня проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from config import GENERATION, CIPHERS, FILE_TYPES, DEFAULT_DATA
from .cipher_system import CipherSystem

# Для случая, если cipher_system.py еще не создан
try:
    from .cipher_system import CipherSystem
except ImportError:
    # Заглушка для тестирования
    class CipherSystem:
        @staticmethod
        def encrypt(text, cipher_type):
            if cipher_type == 'hex':
                return text.encode().hex()
            return text
        
        @staticmethod
        def get_random_cipher():
            return 'hex'


@dataclass
class FileNode:
    """Узел файла в виртуальной файловой системе"""
    name: str
    extension: str
    content: str
    size: int
    created_date: str
    modified_date: str
    is_easter_egg: bool = False
    is_special: bool = False
    is_binary: bool = False
    is_hidden: bool = False
    score_value: int = 10
    
    def get_full_name(self) -> str:
        """Получить полное имя файла с расширением"""
        return f"{self.name}{self.extension}"
    
    def display_info(self, show_hidden: bool = False) -> str:
        """Получить строку для отображения в команде dir"""
        if self.is_hidden and not show_hidden:
            return ""
        
        size_str = f"{self.size:>6} bytes"
        date_str = self.modified_date[:10]
        
        prefix = "[E] " if self.is_easter_egg else "[S] " if self.is_special else "     "
        
        return f"{prefix}{self.get_full_name():<25} {size_str}  {date_str}"


@dataclass
class DirNode:
    """Узел директории в виртуальной файловой системе"""
    name: str
    path: str
    created_date: str
    modified_date: str
    children: List[Any] = field(default_factory=list)
    parent: Optional['DirNode'] = None
    encrypted: bool = False
    cipher_type: Optional[str] = None
    cipher_text: Optional[str] = None
    original_name: Optional[str] = None
    is_special: bool = False
    is_hidden: bool = False
    score_value: int = 50
    decoded: bool = False
    
    def get_child_count(self) -> Tuple[int, int]:
        """Получить количество файлов и директорий в текущей директории"""
        dirs = files = 0
        for child in self.children:
            if isinstance(child, DirNode):
                dirs += 1
            else:
                files += 1
        return dirs, files
    
    def find_child(self, name: str, search_type: str = "any") -> Optional[Any]:
        """Найти дочерний элемент по имени"""
        name_lower = name.lower()
        
        for child in self.children:
            if search_type == "dir" and not isinstance(child, DirNode):
                continue
            if search_type == "file" and isinstance(child, DirNode):
                continue
            
            if isinstance(child, DirNode):
                # Для директорий проверяем имя или зашифрованное имя
                if child.name.lower() == name_lower:
                    return child
                if child.encrypted and child.cipher_text and child.cipher_text.lower() == name_lower:
                    return child
            else:
                # Для файлов проверяем полное имя
                if child.get_full_name().lower() == name_lower:
                    return child
        
        return None


class VirtualFileSystem:
    """Класс для процедурной генерации виртуальной файловой системы"""
    
    def __init__(self, seed: Optional[int] = None):
        """Инициализация генератора файловой системы"""
        # Устанавливаем seed для воспроизводимости
        self.seed = seed if seed is not None else random.randint(1, 999999)
        random.seed(self.seed)
        
        # Корневая директория
        self.root = DirNode(
            name="VOID",
            path="VOID:\\",
            created_date=self._generate_timestamp(),
            modified_date=self._generate_timestamp()
        )
        
        # Текущая директория и путь
        self.current_dir = self.root
        self.current_path = ["VOID:\\"]
        
        # Статистика генерации
        self.generation_stats = {
            'total_dirs': 0,
            'total_files': 0,
            'encrypted_dirs': 0,
            'easter_eggs': 0,
            'special_items': 0
        }
        
        # Генерация структуры
        self._generate_structure()
        
        print(f"[DEBUG] VFS сгенерирована. Seed: {self.seed}")
        print(f"[DEBUG] Директорий: {self.generation_stats['total_dirs']}, "
              f"Файлов: {self.generation_stats['total_files']}")
    
    def _generate_structure(self) -> None:
        """Генерация полной структуры файловой системы"""
        # Сначала генерируем системные директории
        self._generate_system_dirs()
        
        # Затем рекурсивно генерируем остальную структуру
        depth = 0
        max_depth = random.randint(
            GENERATION['min_depth'], 
            GENERATION['max_depth']
        )
        
        for dir_node in self.root.children[:]:  # Копируем список
            if isinstance(dir_node, DirNode):
                self._generate_recursive(dir_node, depth + 1, max_depth)
    
    def _generate_system_dirs(self) -> None:
        """Генерация системных директорий"""
        system_dirs = [
            ("System32", True, False),
            ("Program Files", False, False),
            ("Users", False, False),
            ("Windows", True, False),
            ("Temp", True, True),  # Скрытая директория
        ]
        
        for name, is_special, is_hidden in system_dirs:
            new_dir = DirNode(
                name=name,
                path=f"VOID:\\{name}",
                created_date=self._generate_timestamp(),
                modified_date=self._generate_timestamp(),
                parent=self.root,
                is_special=is_special,
                is_hidden=is_hidden
            )
            
            # Добавляем файлы в системные директории
            self._add_files_to_dir(new_dir, is_system=True)
            
            self.root.children.append(new_dir)
            self.generation_stats['total_dirs'] += 1
    
    def _generate_recursive(self, parent_dir: DirNode, depth: int, max_depth: int) -> None:
        """Рекурсивная генерация структуры"""
        if depth >= max_depth:
            return
        
        # Определяем количество директорий для этого уровня
        num_dirs = random.randint(
            GENERATION['min_dirs_per_level'],
            GENERATION['max_dirs_per_level']
        )
        
        for i in range(num_dirs):
            # Решаем, создавать ли директорию (случайный шанс)
            if random.random() < 0.7:  # 70% шанс создания
                new_dir = self._create_random_dir(parent_dir, depth)
                
                # Добавляем файлы в директорию
                self._add_files_to_dir(new_dir)
                
                # Рекурсивный вызов для вложенных директорий
                if depth < max_depth - 1 and random.random() < 0.6:
                    self._generate_recursive(new_dir, depth + 1, max_depth)
                
                parent_dir.children.append(new_dir)
                self.generation_stats['total_dirs'] += 1
    
    def _create_random_dir(self, parent: DirNode, depth: int) -> DirNode:
        """Создать случайную директорию"""
        # Выбираем имя директории
        if random.random() < 0.3:
            # Используем имена из DEFAULT_DATA или генерируем
            name = random.choice(DEFAULT_DATA['directory_names'])
            if random.random() < 0.4:
                name += str(random.randint(1, 99))
        else:
            # Генерируем "техническое" имя
            prefixes = ["DIR", "FOLDER", "CAT", "MOD", "SEC", "DATA"]
            suffixes = ["", "_" + str(random.randint(1, 999)), 
                       "_V" + str(random.randint(1, 9)),
                       "_" + random.choice(["ALPHA", "BETA", "RC", "FINAL"])]
            name = random.choice(prefixes) + random.choice(suffixes)
        
        # Создаем путь
        path = f"{parent.path}{name}\\"
        
        # Создаем узел директории
        dir_node = DirNode(
            name=name,
            path=path,
            created_date=self._generate_timestamp(),
            modified_date=self._generate_timestamp(),
            parent=parent,
            is_special=random.random() < GENERATION['special_dir_chance']
        )
        
        # Шифруем директорию с определенной вероятностью
        if random.random() < GENERATION['encryption_chance']:
            self._encrypt_directory(dir_node)
            self.generation_stats['encrypted_dirs'] += 1
        
        return dir_node
    
    def _encrypt_directory(self, dir_node: DirNode) -> None:
        """Зашифровать директорию"""
        # Сохраняем оригинальное имя
        dir_node.original_name = dir_node.name
        
        # Выбираем случайный тип шифра
        cipher_type = CipherSystem.get_random_cipher()
        dir_node.cipher_type = cipher_type
        
        # Шифруем имя
        dir_node.cipher_text = CipherSystem.encrypt(dir_node.name, cipher_type)
        
        # Меняем отображаемое имя на зашифрованное
        dir_node.name = dir_node.cipher_text
        dir_node.encrypted = True
        
        # Обновляем путь
        if dir_node.parent:
            dir_node.path = f"{dir_node.parent.path}{dir_node.name}\\"
    
    def _add_files_to_dir(self, dir_node: DirNode, is_system: bool = False) -> None:
        """Добавить файлы в директорию"""
        num_files = random.randint(
            GENERATION['min_files_per_dir'],
            GENERATION['max_files_per_dir']
        )
        
        for i in range(num_files):
            # Создаем случайный файл
            file_node = self._create_random_file(dir_node, is_system)
            dir_node.children.append(file_node)
            self.generation_stats['total_files'] += 1
    
    def _create_random_file(self, parent_dir: DirNode, is_system: bool = False) -> FileNode:
        """Создать случайный файл"""
        # Выбираем имя файла
        if is_system:
            system_names = ["BOOT", "CONFIG", "SETUP", "INSTALL", "LOGON", "SYSTEM"]
            name = random.choice(system_names)
        else:
            name = random.choice(DEFAULT_DATA['file_names'])
            if random.random() < 0.3:
                name += str(random.randint(1, 9))
        
        # Выбираем расширение
        extension = random.choice(DEFAULT_DATA['file_extensions'])
        
        # Генерируем содержимое
        content = self._generate_file_content(name, extension)
        
        # Определяем размер (примерно по 1 байту на символ + накладные расходы)
        size = len(content.encode('utf-8')) + random.randint(0, 1024)
        
        # Определяем, является ли файл пасхалкой
        is_easter_egg = random.random() < GENERATION['easter_egg_chance']
        if is_easter_egg:
            self.generation_stats['easter_eggs'] += 1
        
        # Определяем, является ли файл специальным
        is_special = random.random() < 0.1  # 10% шанс
        
        # Определяем, является ли файл скрытым
        is_hidden = random.random() < 0.15  # 15% шанс
        
        # Определяем значение очков
        score_value = 100 if is_easter_egg else 75 if is_special else 10
        
        return FileNode(
            name=name,
            extension=extension,
            content=content,
            size=size,
            created_date=self._generate_timestamp(),
            modified_date=self._generate_timestamp(),
            is_easter_egg=is_easter_egg,
            is_special=is_special,
            is_hidden=is_hidden,
            is_binary=extension in ['.bin', '.dat'],
            score_value=score_value
        )
    
    def _generate_file_content(self, filename: str, extension: str) -> str:
        """Сгенерировать содержимое файла"""
        # Получаем настройки для типа файла
        file_type_config = FILE_TYPES.get(extension, FILE_TYPES['.txt'])
        
        # Выбираем случайный шаблон
        template = random.choice(file_type_config['templates'])
        
        # Заменяем плейсхолдеры
        content = template.format(
            filename=filename + extension,
            date=self._generate_timestamp(),
            version=f"{random.randint(1, 9)}.{random.randint(0, 9)}",
            code=random.randint(1000, 9999),
            time=int(time.time()),
            binary=''.join(random.choice('01') for _ in range(16)),
            id=random.randint(10000, 99999),
            feature=random.choice(['feature_a', 'feature_b', 'feature_c']),
            value=random.choice(['true', 'false', 'enabled', 'disabled']),
            name=random.choice(['quality', 'resolution', 'volume']),
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            level=random.choice(['INFO', 'WARNING', 'ERROR']),
            message=random.choice(['System started', 'Check completed', 'Operation successful'])
        )
        
        # Добавляем дополнительное содержимое
        if random.random() < 0.5:
            extra_content = random.choice(file_type_config['content_variants'])
            content += "\n" + extra_content
        
        return content
    
    def _generate_timestamp(self) -> str:
        """Сгенерировать случайную временную метку"""
        # Генерируем случайную дату за последние несколько лет
        import datetime
        now = datetime.datetime.now()
        random_days = random.randint(1, 365 * 3)  # До 3 лет назад
        random_date = now - datetime.timedelta(days=random_days)
        
        return random_date.strftime("%Y-%m-%d %H:%M:%S")
    
    # ==================== МЕТОДЫ ДЛЯ КОМАНД ====================
    
    def get_current_path_str(self) -> str:
        """Получить текущий путь в виде строки"""
        return "".join(self.current_path)
    
    def list_directory(self, show_hidden: bool = False) -> List[str]:
        """Получить список содержимого текущей директории"""
        result = []
        
        # Добавляем родительскую директорию (если не в корне)
        if self.current_dir != self.root:
            result.append("<DIR>   ..")
        
        # Сортируем: сначала директории, потом файлы
        dirs = []
        files = []
        
        for child in self.current_dir.children:
            if isinstance(child, DirNode):
                if child.is_hidden and not show_hidden:
                    continue
                
                prefix = "[E] " if child.encrypted else "[S] " if child.is_special else "<DIR> "
                dirs.append(f"{prefix}   {child.name}")
            else:
                file_info = child.display_info(show_hidden)
                if file_info:
                    files.append(file_info)
        
        # Сортируем и добавляем к результату
        result.extend(sorted(dirs))
        result.extend(sorted(files))
        
        return result
    
    def change_directory(self, target: str) -> Tuple[bool, str]:
        """Изменить текущую директорию"""
        if target == "..":
            # Переход на уровень выше
            if self.current_dir == self.root:
                return False, "Вы в корневой директории"
            
            self.current_dir = self.current_dir.parent
            self.current_path.pop()
            return True, f"Переход в {self.get_current_path_str()}"
        
        if target == "." or target == "":
            # Остаться в текущей директории
            return True, "Текущая директория"
        
        # Поиск директории
        dir_node = self.current_dir.find_child(target, search_type="dir")
        
        if dir_node is None:
            return False, f"Директория '{target}' не найдена"
        
        # Проверка на зашифрованность
        if dir_node.encrypted and not dir_node.decoded:
            return False, f"Директория зашифрована! Используйте decode {dir_node.cipher_text} <расшифрованное_имя>"
        
        # Переход в директорию
        self.current_dir = dir_node
        self.current_path.append(dir_node.name + "\\")
        
        return True, f"Переход в {self.get_current_path_str()}"
    
    def open_file(self, filename: str) -> Tuple[Optional[FileNode], str]:
        """Открыть файл по имени"""
        # Ищем файл
        file_node = self.current_dir.find_child(filename, search_type="file")
        
        if file_node is None:
            # Попробуем найти без расширения
            for child in self.current_dir.children:
                if not isinstance(child, DirNode) and child.name.lower() == filename.lower():
                    file_node = child
                    break
        
        if file_node is None:
            return None, f"Файл '{filename}' не найден"
        
        return file_node, "Файл найден"
    
    def decode_directory(self, cipher_text: str, attempt: str) -> Tuple[bool, Optional[DirNode], str]:
        """Попытаться расшифровать директорию"""
        # Ищем зашифрованную директорию в текущей директории
        for child in self.current_dir.children:
            if isinstance(child, DirNode) and child.encrypted and not child.decoded:
                if child.cipher_text.lower() == cipher_text.lower():
                    # Проверяем расшифровку
                    if self._check_decryption(attempt, child):
                        # Расшифровка успешна
                        child.decoded = True
                        child.encrypted = False
                        child.name = child.original_name or attempt
                        
                        # Обновляем путь
                        if child.parent:
                            child.path = f"{child.parent.path}{child.name}\\"
                        
                        # Обновляем статистику
                        self.generation_stats['encrypted_dirs'] -= 1
                        
                        return True, child, f"Директория расшифрована: {child.name}"
                    else:
                        return False, None, "Неверная расшифровка. Попробуйте еще раз."
        
        return False, None, f"Зашифрованная директория '{cipher_text}' не найдена"
    
    def _check_decryption(self, attempt: str, dir_node: DirNode) -> bool:
        """Проверить правильность расшифровки"""
        if dir_node.original_name:
            return attempt.lower() == dir_node.original_name.lower()
        
        # Если оригинальное имя не сохранено, пытаемся расшифровать
        try:
            decrypted = CipherSystem.decrypt(dir_node.cipher_text, dir_node.cipher_type)
            return attempt.lower() == decrypted.lower()
        except:
            return False
    
    def find_item(self, search_term: str, search_type: str = "any") -> List[Dict[str, Any]]:
        """Поиск файлов и директорий по имени"""
        results = []
        search_term_lower = search_term.lower()
        
        def search_recursive(node: DirNode, path: str):
            for child in node.children:
                current_path = f"{path}{child.name}{'\\' if isinstance(child, DirNode) else ''}"
                
                # Проверяем соответствие типу поиска
                if search_type == "dir" and not isinstance(child, DirNode):
                    continue
                if search_type == "file" and isinstance(child, DirNode):
                    continue
                
                # Проверяем имя
                if isinstance(child, DirNode):
                    name_to_check = child.original_name if child.encrypted else child.name
                else:
                    name_to_check = child.get_full_name()
                
                if search_term_lower in name_to_check.lower():
                    results.append({
                        'type': 'DIR' if isinstance(child, DirNode) else 'FILE',
                        'name': name_to_check,
                        'path': current_path,
                        'encrypted': child.encrypted if isinstance(child, DirNode) else False,
                        'size': child.size if not isinstance(child, DirNode) else 0
                    })
                
                # Рекурсивный поиск в поддиректориях
                if isinstance(child, DirNode):
                    search_recursive(child, current_path)
        
        # Начинаем поиск с корневой директории
        search_recursive(self.root, "VOID:\\")
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику файловой системы"""
        dirs, files = self.root.get_child_count()
        
        return {
            'seed': self.seed,
            'total_dirs': self.generation_stats['total_dirs'],
            'total_files': self.generation_stats['total_files'],
            'encrypted_dirs': self.generation_stats['encrypted_dirs'],
            'easter_eggs': self.generation_stats['easter_eggs'],
            'special_items': self.generation_stats['special_items'],
            'current_path': self.get_current_path_str(),
            'items_in_current_dir': len(self.current_dir.children)
        }


# Тестирование класса (если файл запущен напрямую)
if __name__ == "__main__":
    print("Тестирование VirtualFileSystem...")
    
    # Создаем VFS с фиксированным seed для тестирования
    vfs = VirtualFileSystem(seed=42)
    
    # Показываем корневую директорию
    print(f"\nКорневая директория: {vfs.get_current_path_str()}")
    print("Содержимое:")
    for item in vfs.list_directory(show_hidden=True):
        print(f"  {item}")
    
    # Пробуем перейти в директорию
    if vfs.root.children:
        first_dir = vfs.root.children[0]
        if isinstance(first_dir, DirNode):
            success, message = vfs.change_directory(first_dir.name)
            print(f"\n{message}")
            
            # Показываем содержимое новой директории
            print("Содержимое:")
            for item in vfs.list_directory(show_hidden=True):
                print(f"  {item}")
            
            # Возвращаемся назад
            success, message = vfs.change_directory("..")
            print(f"\n{message}")
    
    # Показываем статистику
    stats = vfs.get_stats()
    print(f"\nСтатистика VFS:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nТестирование завершено!")
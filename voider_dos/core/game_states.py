"""
Класс GameState: управление состоянием игры, счетом, статистикой и сохранениями
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional
import sys

# Добавляем путь для импорта config.py из корня проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from config import SAVES, SCORING

class GameState:
    """Класс для управления состоянием игры и сохранениями"""
    
    def __init__(self):
        """Инициализация состояния игры"""
        # Основные параметры
        self.score = 0
        self.session_score = 0
        self.total_score = 0
        
        # Статистика
        self.sessions_played = 0
        self.play_time = 0  # в минутах
        self.directories_decrypted = 0
        self.files_opened = 0
        self.easter_eggs_found = 0
        self.special_dirs_found = 0
        
        # Информация о сессии
        self.current_session_start = None
        self.last_session_seed = None
        self.last_played = None
        self.first_play_date = None
        
        # Прогресс и достижения
        self.achievements = {
            'first_decryption': False,
            'easter_egg_hunter': False,
            'void_explorer': False,
            'master_decryptor': False
        }
        
        # Флаги сессии
        self.first_decryption_done = False
        
        # Пути для сохранения
        self.save_dir = SAVES['save_dir']
        self.save_file = os.path.join(self.save_dir, SAVES['save_file'])
        
        # Создаем директорию для сохранений, если ее нет
        os.makedirs(self.save_dir, exist_ok=True)
    
    def add_score(self, points: int, reason: str = "") -> None:
        """Добавить очки за действие"""
        self.score += points
        self.session_score += points
        self.total_score += points
        
        # Логирование для отладки
        if reason:
            print(f"[DEBUG] +{points} очков за: {reason}")
    
    def add_stat(self, stat_name: str, value: int = 1) -> None:
        """Добавить значение к статистике"""
        if hasattr(self, stat_name):
            current = getattr(self, stat_name)
            setattr(self, stat_name, current + value)
            
            # Проверка достижений
            self._check_achievements()
    
    def start_new_session(self, seed: Optional[int] = None) -> None:
        """Начать новую игровую сессию"""
        self.session_score = 0
        self.current_session_start = time.time()
        self.last_session_seed = seed
        
        # Сбрасываем флаги сессии
        self.first_decryption_done = False
        
        self.sessions_played += 1
        
        print(f"[DEBUG] Начата новая сессия (Seed: {seed})")
    
    def end_session(self) -> None:
        """Завершить текущую сессию"""
        if self.current_session_start:
            session_time = time.time() - self.current_session_start
            self.play_time += session_time / 60  # конвертируем в минуты
            self.current_session_start = None
            
            print(f"[DEBUG] Сессия завершена. Очков заработано: {self.session_score}")
    
    def record_decryption(self, points: int = None) -> None:
        """Записать факт расшифровки директории"""
        self.directories_decrypted += 1
        
        if points is None:
            points = SCORING['directory_decrypted']
        
        # Бонус за первую расшифровку в сессии
        if not self.first_decryption_done:
            bonus = SCORING['first_decryption_bonus']
            self.add_score(bonus, "Бонус за первую расшифровку")
            self.first_decryption_done = True
            self.achievements['first_decryption'] = True
        
        self.add_score(points, "Расшифровка директории")
    
    def record_file_opened(self, is_easter_egg: bool = False, is_special: bool = False) -> None:
        """Записать факт открытия файла"""
        self.files_opened += 1
        
        if is_easter_egg:
            self.easter_eggs_found += 1
            points = SCORING['easter_egg_found']
            self.add_score(points, "Находка пасхалки")
        elif is_special:
            self.special_dirs_found += 1
            points = SCORING['special_dir_found']
            self.add_score(points, "Особая директория")
        else:
            points = SCORING['file_opened']
            self.add_score(points, "Открытие файла")
    
    def _check_achievements(self) -> None:
        """Проверить и разблокировать достижения"""
        # Охотник за пасхалками
        if self.easter_eggs_found >= 3 and not self.achievements['easter_egg_hunter']:
            self.achievements['easter_egg_hunter'] = True
            print("[ДОСТИЖЕНИЕ] Охотник за пасхалками: найдено 3 пасхалки!")
        
        # Исследователь пустоты
        if self.files_opened >= 20 and not self.achievements['void_explorer']:
            self.achievements['void_explorer'] = True
            print("[ДОСТИЖЕНИЕ] Исследователь пустоты: открыто 20 файлов!")
        
        # Мастер дешифровки
        if self.directories_decrypted >= 10 and not self.achievements['master_decryptor']:
            self.achievements['master_decryptor'] = True
            print("[ДОСТИЖЕНИЕ] Мастер дешифровки: расшифровано 10 директорий!")
    
    def save(self) -> bool:
        """Сохранить состояние игры в файл"""
        try:
            save_data = {
                # Основные данные
                'total_score': self.total_score,
                'score': self.score,
                
                # Статистика
                'sessions_played': self.sessions_played,
                'play_time': self.play_time,
                'directories_decrypted': self.directories_decrypted,
                'files_opened': self.files_opened,
                'easter_eggs_found': self.easter_eggs_found,
                'special_dirs_found': self.special_dirs_found,
                
                # Достижения
                'achievements': self.achievements,
                
                # Метаданные
                'last_played': datetime.now().isoformat(),
                'last_session_seed': self.last_session_seed,
                'first_play_date': self.first_play_date or datetime.now().isoformat(),
                'version': '0.1.0'  # Версия формата сохранения
            }
            
            # Создаем резервную копию, если файл уже существует
            if os.path.exists(self.save_file):
                self._create_backup()
            
            # Сохраняем данные
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            # Обновляем время последней игры
            self.last_played = save_data['last_played']
            
            print(f"[DEBUG] Игра сохранена в {self.save_file}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Ошибка при сохранении: {e}")
            return False
    
    def load(self) -> bool:
        """Загрузить состояние игры из файла"""
        try:
            if not os.path.exists(self.save_file):
                print(f"[DEBUG] Файл сохранения не найден: {self.save_file}")
                # Устанавливаем дату первого запуска
                self.first_play_date = datetime.now().isoformat()
                return False
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Загружаем основные данные
            self.total_score = save_data.get('total_score', 0)
            self.score = save_data.get('score', 0)
            
            # Загружаем статистику
            self.sessions_played = save_data.get('sessions_played', 0)
            self.play_time = save_data.get('play_time', 0)
            self.directories_decrypted = save_data.get('directories_decrypted', 0)
            self.files_opened = save_data.get('files_opened', 0)
            self.easter_eggs_found = save_data.get('easter_eggs_found', 0)
            self.special_dirs_found = save_data.get('special_dirs_found', 0)
            
            # Загружаем достижения
            self.achievements = save_data.get('achievements', {
                'first_decryption': False,
                'easter_egg_hunter': False,
                'void_explorer': False,
                'master_decryptor': False
            })
            
            # Загружаем метаданные
            self.last_played = save_data.get('last_played')
            self.last_session_seed = save_data.get('last_session_seed')
            self.first_play_date = save_data.get('first_play_date')
            
            print(f"[DEBUG] Игра загружена из {self.save_file}")
            print(f"[DEBUG] Общий счет: {self.total_score}, Сессий: {self.sessions_played}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке: {e}")
            return False
    
    def _create_backup(self) -> None:
        """Создать резервную копию файла сохранения"""
        try:
            import shutil
            from datetime import datetime
            
            # Создаем директорию для бэкапов, если ее нет
            backup_dir = os.path.join(self.save_dir, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Генерируем имя файла с временной меткой
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f'voider_save_backup_{timestamp}.json')
            
            # Копируем файл
            shutil.copy2(self.save_file, backup_file)
            
            # Удаляем старые бэкапы (оставляем только последние N)
            self._cleanup_old_backups(backup_dir)
            
        except Exception as e:
            print(f"[WARNING] Не удалось создать бэкап: {e}")
    
    def _cleanup_old_backups(self, backup_dir: str) -> None:
        """Удалить старые резервные копии"""
        try:
            import glob
            
            # Получаем все файлы бэкапов
            backup_files = glob.glob(os.path.join(backup_dir, 'voider_save_backup_*.json'))
            
            # Сортируем по времени модификации (новые в конце)
            backup_files.sort(key=os.path.getmtime)
            
            # Удаляем старые файлы, оставляя только последние N
            keep_count = SAVES['backup_count']
            if len(backup_files) > keep_count:
                for old_file in backup_files[:-keep_count]:
                    os.remove(old_file)
                    
        except Exception as e:
            print(f"[WARNING] Не удалось очистить старые бэкапы: {e}")
    
    def has_save(self) -> bool:
        """Проверить наличие файла сохранения"""
        return os.path.exists(self.save_file)
    
    def reset(self, keep_stats: bool = False) -> None:
        """Сбросить текущее состояние игры"""
        self.score = 0
        self.session_score = 0
        
        if not keep_stats:
            self.total_score = 0
            self.sessions_played = 0
            self.play_time = 0
            self.directories_decrypted = 0
            self.files_opened = 0
            self.easter_eggs_found = 0
            self.special_dirs_found = 0
            self.achievements = {
                'first_decryption': False,
                'easter_egg_hunter': False,
                'void_explorer': False,
                'master_decryptor': False
            }
        
        print("[DEBUG] Состояние игры сброшено")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получить статистику в виде словаря"""
        return {
            'total_score': self.total_score,
            'current_score': self.score,
            'sessions_played': self.sessions_played,
            'play_time': round(self.play_time, 1),
            'directories_decrypted': self.directories_decrypted,
            'files_opened': self.files_opened,
            'easter_eggs_found': self.easter_eggs_found,
            'special_dirs_found': self.special_dirs_found,
            'achievements_unlocked': sum(1 for v in self.achievements.values() if v),
            'last_session_seed': self.last_session_seed,
            'last_session_score': self.session_score,
            'last_played': self.last_played or 'Никогда',
            'first_play_date': self.first_play_date or 'Неизвестно'
        }
    
    def show_stats(self) -> None:
        """Показать статистику в консоли"""
        stats = self.get_statistics()
        
        print("\n" + "=" * 50)
        print("СТАТИСТИКА THE-VOIDER-DOS")
        print("=" * 50)
        
        print(f"\nОЧКИ:")
        print(f"  Текущие: {stats['current_score']}")
        print(f"  Всего заработано: {stats['total_score']}")
        print(f"  Последняя сессия: {stats['last_session_score']}")
        
        print(f"\nСТАТИСТИКА:")
        print(f"  Сыграно сессий: {stats['sessions_played']}")
        print(f"  Время в игре: {stats['play_time']} мин.")
        print(f"  Расшифровано директорий: {stats['directories_decrypted']}")
        print(f"  Открыто файлов: {stats['files_opened']}")
        print(f"  Найдено пасхалок: {stats['easter_eggs_found']}")
        print(f"  Особых директорий: {stats['special_dirs_found']}")
        
        print(f"\nДОСТИЖЕНИЯ: {stats['achievements_unlocked']}/4")
        for name, unlocked in self.achievements.items():
            status = "✓" if unlocked else "✗"
            print(f"  {status} {self._get_achievement_name(name)}")
        
        print(f"\nПОСЛЕДНЯЯ СЕССИЯ:")
        print(f"  Seed: {stats['last_session_seed'] or 'Неизвестно'}")
        print(f"  Последняя игра: {stats['last_played']}")
        print(f"  Первая игра: {stats['first_play_date']}")
        
        print("\n" + "=" * 50)
    
    def _get_achievement_name(self, key: str) -> str:
        """Получить читаемое название достижения"""
        names = {
            'first_decryption': 'Первая расшифровка',
            'easter_egg_hunter': 'Охотник за пасхалками',
            'void_explorer': 'Исследователь пустоты',
            'master_decryptor': 'Мастер дешифровки'
        }
        return names.get(key, key)


# Тестирование класса (если файл запущен напрямую)
if __name__ == "__main__":
    print("Тестирование класса GameState...")
    
    # Создаем экземпляр
    state = GameState()
    
    # Тестируем методы
    state.start_new_session(seed=12345)
    
    # Добавляем очки и статистику
    state.record_decryption()
    state.record_file_opened(is_easter_egg=True)
    state.record_file_opened()
    
    # Сохраняем
    state.save()
    
    # Загружаем
    state2 = GameState()
    state2.load()
    
    # Показываем статистику
    state2.show_stats()
    
    print("\nТестирование завершено!")
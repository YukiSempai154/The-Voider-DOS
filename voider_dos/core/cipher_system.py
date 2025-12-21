"""
Класс CipherSystem: система шифрования и дешифрования
Поддерживает: HEX, ASCII, Binary, Base64, ROT13, Caesar
"""

import base64
import random
from typing import Optional, Tuple, Dict, List
import sys

# Добавляем путь для импорта config.py из корня проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from config import CIPHERS

class CipherSystem:
    """Система шифрования и дешифрования для THE-VOIDER-DOS"""
    
    # Символы для Caesar шифра
    ALPHABET_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHABET_LOWER = 'abcdefghijklmnopqrstuvwxyz'
    ALPHABET_DIGITS = '0123456789'
    
    @staticmethod
    def encrypt(text: str, cipher_type: str) -> Tuple[str, Optional[int]]:
        """
        Зашифровать текст указанным методом
        
        Args:
            text: Текст для шифрования
            cipher_type: Тип шифра (hex, ascii, binary, base64, rot13, caesar)
            
        Returns:
            Кортеж (зашифрованный_текст, сдвиг_для_caesar или None)
        """
        if cipher_type == 'hex':
            return CipherSystem._encrypt_hex(text), None
        elif cipher_type == 'ascii':
            return CipherSystem._encrypt_ascii(text), None
        elif cipher_type == 'binary':
            return CipherSystem._encrypt_binary(text), None
        elif cipher_type == 'base64':
            return CipherSystem._encrypt_base64(text), None
        elif cipher_type == 'rot13':
            return CipherSystem._encrypt_rot13(text), None
        elif cipher_type == 'caesar':
            return CipherSystem._encrypt_caesar(text)
        else:
            raise ValueError(f"Неизвестный тип шифра: {cipher_type}")
    
    @staticmethod
    def decrypt(encrypted: str, cipher_type: str, shift: Optional[int] = None) -> str:
        """
        Расшифровать текст
        
        Args:
            encrypted: Зашифрованный текст
            cipher_type: Тип шифра
            shift: Сдвиг для Caesar шифра (опционально)
            
        Returns:
            Расшифрованный текст
        """
        if cipher_type == 'hex':
            return CipherSystem._decrypt_hex(encrypted)
        elif cipher_type == 'ascii':
            return CipherSystem._decrypt_ascii(encrypted)
        elif cipher_type == 'binary':
            return CipherSystem._decrypt_binary(encrypted)
        elif cipher_type == 'base64':
            return CipherSystem._decrypt_base64(encrypted)
        elif cipher_type == 'rot13':
            return CipherSystem._decrypt_rot13(encrypted)
        elif cipher_type == 'caesar':
            if shift is None:
                raise ValueError("Для Caesar шифра требуется параметр shift")
            return CipherSystem._decrypt_caesar(encrypted, shift)
        else:
            raise ValueError(f"Неизвестный тип шифра: {cipher_type}")
    
    @staticmethod
    def _encrypt_hex(text: str) -> str:
        """Шифрование в HEX"""
        # Вариант 1: Без разделителей
        # return text.encode().hex().upper()
        
        # Вариант 2: С разделителями каждые 2 символа (более читаемо)
        hex_str = text.encode().hex().upper()
        return ' '.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)])
    
    @staticmethod
    def _decrypt_hex(encrypted: str) -> str:
        """Дешифрование HEX"""
        # Удаляем пробелы и другие разделители
        clean_hex = encrypted.replace(' ', '').replace(':', '')
        try:
            return bytes.fromhex(clean_hex).decode('utf-8')
        except ValueError as e:
            raise ValueError(f"Неверный HEX формат: {e}")
    
    @staticmethod
    def _encrypt_ascii(text: str) -> str:
        """Шифрование в ASCII коды"""
        ascii_codes = [str(ord(char)) for char in text]
        return ' '.join(ascii_codes)
    
    @staticmethod
    def _decrypt_ascii(encrypted: str) -> str:
        """Дешифрование ASCII кодов"""
        try:
            codes = encrypted.split()
            chars = [chr(int(code)) for code in codes]
            return ''.join(chars)
        except ValueError as e:
            raise ValueError(f"Неверный ASCII формат: {e}")
    
    @staticmethod
    def _encrypt_binary(text: str) -> str:
        """Шифрование в двоичный код"""
        binary_codes = []
        for char in text:
            # Преобразуем в 8-битный двоичный код
            binary = format(ord(char), '08b')
            binary_codes.append(binary)
        return ' '.join(binary_codes)
    
    @staticmethod
    def _decrypt_binary(encrypted: str) -> str:
        """Дешифрование двоичного кода"""
        try:
            binaries = encrypted.split()
            chars = [chr(int(binary, 2)) for binary in binaries]
            return ''.join(chars)
        except ValueError as e:
            raise ValueError(f"Неверный двоичный формат: {e}")
    
    @staticmethod
    def _encrypt_base64(text: str) -> str:
        """Шифрование в Base64"""
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        return encoded
    
    @staticmethod
    def _decrypt_base64(encrypted: str) -> str:
        """Дешифрование Base64"""
        try:
            decoded = base64.b64decode(encrypted).decode('utf-8')
            return decoded
        except Exception as e:
            raise ValueError(f"Неверный Base64 формат: {e}")
    
    @staticmethod
    def _encrypt_rot13(text: str) -> str:
        """Шифрование ROT13"""
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                # Сдвиг для строчных букв
                result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                # Сдвиг для заглавных букв
                result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
            else:
                # Не-буквы остаются как есть
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def _decrypt_rot13(encrypted: str) -> str:
        """Дешифрование ROT13"""
        # ROT13 - самодвойственный шифр (дешифрование = шифрование)
        return CipherSystem._encrypt_rot13(encrypted)
    
    @staticmethod
    def _encrypt_caesar(text: str) -> Tuple[str, int]:
        """Шифрование Caesar с случайным сдвигом"""
        # Генерируем случайный сдвиг из диапазона в конфиге
        min_shift, max_shift = CIPHERS['caesar_shift_range']
        shift = random.randint(min_shift, max_shift)
        
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                # Сдвиг для строчных букв
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                result.append(new_char)
            elif 'A' <= char <= 'Z':
                # Сдвиг для заглавных букв
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                result.append(new_char)
            elif '0' <= char <= '9':
                # Сдвиг для цифр (по кругу 0-9)
                new_char = chr((ord(char) - ord('0') + shift) % 10 + ord('0'))
                result.append(new_char)
            else:
                # Остальные символы без изменений
                result.append(char)
        
        return ''.join(result), shift
    
    @staticmethod
    def _decrypt_caesar(encrypted: str, shift: int) -> str:
        """Дешифрование Caesar с известным сдвигом"""
        # Дешифрование = шифрование с обратным сдвигом
        result = []
        for char in encrypted:
            if 'a' <= char <= 'z':
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                result.append(new_char)
            elif 'A' <= char <= 'Z':
                new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                result.append(new_char)
            elif '0' <= char <= '9':
                new_char = chr((ord(char) - ord('0') - shift) % 10 + ord('0'))
                result.append(new_char)
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def get_random_cipher() -> str:
        """
        Получить случайный тип шифра с учетом весов
        
        Returns:
            Тип шифра (hex, ascii, binary, base64, rot13, caesar)
        """
        ciphers = list(CIPHERS['weights'].keys())
        weights = list(CIPHERS['weights'].values())
        
        # Выбираем случайный шифр с учетом весов
        return random.choices(ciphers, weights=weights, k=1)[0]
    
    @staticmethod
    def get_cipher_info(cipher_type: str) -> Dict[str, str]:
        """
        Получить информацию о шифре
        
        Args:
            cipher_type: Тип шифра
            
        Returns:
            Словарь с информацией о шифре
        """
        info = {
            'hex': {
                'name': 'HEX',
                'description': 'Шестнадцатеричное представление текста',
                'example': '48 65 6C 6C 6F → Hello',
                'hint': 'Каждые два символа HEX представляют один байт (символ ASCII)'
            },
            'ascii': {
                'name': 'ASCII',
                'description': 'Коды символов в десятичной системе',
                'example': '72 101 108 108 111 → Hello',
                'hint': 'Числа разделены пробелами, каждое число - код символа'
            },
            'binary': {
                'name': 'Binary',
                'description': 'Двоичное представление текста',
                'example': '01001000 01100101 01101100 01101100 01101111 → Hello',
                'hint': 'Каждый блок из 8 бит представляет один символ'
            },
            'base64': {
                'name': 'Base64',
                'description': 'Кодирование Base64',
                'example': 'SGVsbG8= → Hello',
                'hint': 'Использует символы A-Z, a-z, 0-9, +, / и = для дополнения'
            },
            'rot13': {
                'name': 'ROT13',
                'description': 'Шифр сдвига букв на 13 позиций',
                'example': 'Uryyb → Hello',
                'hint': 'A ↔ N, B ↔ O, C ↔ P и т.д. Самодвойственный шифр'
            },
            'caesar': {
                'name': 'Caesar',
                'description': 'Классический шифр Цезаря со случайным сдвигом',
                'example': 'Случайный сдвиг (1-25). Например, при сдвиге 3: Khoor → Hello',
                'hint': 'Все буквы сдвигаются на одинаковое количество позиций в алфавите'
            }
        }
        
        return info.get(cipher_type, {
            'name': 'Неизвестный',
            'description': 'Неизвестный тип шифра',
            'example': 'Нет примера',
            'hint': 'Нет подсказки'
        })
    
    @staticmethod
    def brute_force_caesar(encrypted: str) -> List[Dict[str, str]]:
        """
        Метод грубой силы для Caesar шифра
        Возвращает все возможные расшифровки
        
        Args:
            encrypted: Зашифрованный текст
            
        Returns:
            Список словарей с расшифровками и сдвигами
        """
        results = []
        
        # Пробуем все сдвиги от 1 до 25
        for shift in range(1, 26):
            try:
                decrypted = CipherSystem._decrypt_caesar(encrypted, shift)
                # Проверяем, содержит ли результат печатные символы
                if any(c.isprintable() and c.isalpha() for c in decrypted):
                    results.append({
                        'shift': shift,
                        'text': decrypted,
                        'confidence': CipherSystem._calculate_confidence(decrypted)
                    })
            except:
                continue
        
        # Сортируем по уверенности (чем больше похоже на реальные слова, тем выше)
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results
    
    @staticmethod
    def _calculate_confidence(text: str) -> float:
        """
        Рассчитать уверенность в том, что текст является правильной расшифровкой
        
        Args:
            text: Текст для анализа
            
        Returns:
            Уверенность от 0.0 до 1.0
        """
        confidence = 0.0
        
        # Проверяем наличие букв
        if any(c.isalpha() for c in text):
            confidence += 0.3
        
        # Проверяем наличие пробелов (признак слов)
        if ' ' in text:
            confidence += 0.2
        
        # Проверяем, начинается ли с заглавной буквы (часто имена директорий)
        if text and text[0].isupper():
            confidence += 0.2
        
        # Проверяем, содержит ли только печатные символы
        if all(c.isprintable() or c.isspace() for c in text):
            confidence += 0.3
        
        return min(confidence, 1.0)
    
    @staticmethod
    def validate_decryption(attempt: str, original: str, cipher_type: str, 
                          shift: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Проверить правильность расшифровки
        
        Args:
            attempt: Попытка расшифровки пользователя
            original: Оригинальный текст
            cipher_type: Тип шифра
            shift: Сдвиг для Caesar (опционально)
            
        Returns:
            Кортеж (успех, сообщение_об_ошибке)
        """
        # Нормализуем регистр для сравнения (имена директорий часто не чувствительны к регистру)
        attempt_norm = attempt.strip().lower()
        original_norm = original.lower()
        
        if cipher_type == 'caesar':
            # Для Caesar мы можем не знать сдвиг
            # Просто сравниваем с оригиналом
            if attempt_norm == original_norm:
                return True, None
            else:
                # Попробуем дать подсказку
                if shift is not None:
                    return False, f"Неверно. Попробуйте другой текст. Сдвиг был: {shift}"
                else:
                    return False, "Неверно. Попробуйте другой текст."
        else:
            # Для остальных шифров просто сравниваем
            if attempt_norm == original_norm:
                return True, None
            else:
                # Попробуем дать подсказку для HEX
                if cipher_type == 'hex':
                    # Покажем правильный HEX для сравнения
                    correct_hex = CipherSystem._encrypt_hex(original)
                    return False, f"Неверно. Правильный HEX: {correct_hex}"
                return False, "Неверная расшифровка. Попробуйте еще раз."
    
    @staticmethod
    def get_all_ciphers_info() -> List[Dict[str, str]]:
        """
        Получить информацию о всех доступных шифрах
        
        Returns:
            Список с информацией о каждом шифре
        """
        all_info = []
        for cipher_type in CIPHERS['enabled']:
            info = CipherSystem.get_cipher_info(cipher_type)
            info['type'] = cipher_type
            all_info.append(info)
        
        return all_info
    
    @staticmethod
    def practice_mode(text: str = "Hello") -> None:
        """
        Режим практики для изучения шифров
        
        Args:
            text: Текст для практики
        """
        print(f"\n{'='*60}")
        print(f"РЕЖИМ ПРАКТИКИ: '{text}'")
        print(f"{'='*60}\n")
        
        for cipher_type in CIPHERS['enabled']:
            if cipher_type == 'caesar':
                encrypted, shift = CipherSystem.encrypt(text, cipher_type)
                info = CipherSystem.get_cipher_info(cipher_type)
                print(f"{info['name']} (сдвиг {shift}):")
                print(f"  Зашифровано: {encrypted}")
                print(f"  Пример: {info['example']}")
            else:
                encrypted, _ = CipherSystem.encrypt(text, cipher_type)
                info = CipherSystem.get_cipher_info(cipher_type)
                print(f"{info['name']}:")
                print(f"  Зашифровано: {encrypted}")
                print(f"  Пример: {info['example']}")
            print(f"  Подсказка: {info['hint']}")
            print()


# Тестирование класса (если файл запущен напрямую)
if __name__ == "__main__":
    print("Тестирование CipherSystem...")
    
    # Тестовый текст
    test_text = "HelloWorld"
    
    # Тестируем все шифры
    for cipher_type in CIPHERS['enabled']:
        print(f"\n{cipher_type.upper()}:")
        print(f"  Оригинал: {test_text}")
        
        try:
            if cipher_type == 'caesar':
                encrypted, shift = CipherSystem.encrypt(test_text, cipher_type)
                print(f"  Зашифровано: {encrypted} (сдвиг: {shift})")
                decrypted = CipherSystem.decrypt(encrypted, cipher_type, shift)
                print(f"  Расшифровано: {decrypted}")
            else:
                encrypted, _ = CipherSystem.encrypt(test_text, cipher_type)
                print(f"  Зашифровано: {encrypted}")
                decrypted = CipherSystem.decrypt(encrypted, cipher_type)
                print(f"  Расшифровано: {decrypted}")
            
            # Проверяем
            if decrypted == test_text:
                print(f"  ✓ Корректно")
            else:
                print(f"  ✗ Ошибка: {decrypted} != {test_text}")
                
        except Exception as e:
            print(f"  ✗ Ошибка: {e}")
    
    # Тестируем получение случайного шифра
    print(f"\nСлучайный шифр: {CipherSystem.get_random_cipher()}")
    
    # Тестируем режим практики
    CipherSystem.practice_mode("Test")
    
    print("\nТестирование завершено!")
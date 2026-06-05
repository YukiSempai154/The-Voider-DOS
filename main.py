import os
import sys
import time
import random
from colorama import Fore, Back, Style, init

import world_gen

init(autoreset=True)

GREEN = Fore.GREEN + Style.BRIGHT
CYAN = Fore.CYAN + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT

def clear_screen():
    os.path.dirname
    os.system('cls' if os.name == 'nt' else 'clear')


def show_alpha_disclaimer():
    """Мигающее предупреждение перед запуском."""
    text = (
        "Приветствую тебя, дорогой тестировщик! Я Prunt. Единственный разработчик этого проекта.\n"
        "Прямо сейчас ты пробуешь мое детище в Alpha тестировании, и поэтому считаю должным тебя предупредить.\n"
        "Тут могут быть баги, гличи или вовсе какие-либо недоработки. Прошу тебя понять и простить\n"
        "мою грешную душу, поскольку в одно рыло пилить все это достаточно сложно, имея скудные познания в Python.\n\n"
        "Нажимая [y], ты соглашаешься с тем, что ты это прочитал и не имеешь ко мне претензий."
    )

    for _ in range(10):
        clear_screen()
        print(Back.RED + Fore.WHITE + Style.BRIGHT + " " * 80)
        print(Back.RED + Fore.WHITE + Style.BRIGHT + "ВНИМАНИЕ! КРИТИЧЕСКИЙ БУФЕР ТЕСТИРОВАНИЯ".center(80))
        print(Back.RED + Fore.WHITE + Style.BRIGHT + " " * 80)
        time.sleep(0.15)
        clear_screen()
        print(Back.WHITE + Fore.RED + Style.BRIGHT + " " * 80)
        print(Back.WHITE + Fore.RED + Style.BRIGHT + "ВНИМАНИЕ! КРИТИЧЕСКИЙ БУФЕР ТЕСТИРОВАНИЯ".center(80))
        print(Back.WHITE + Fore.RED + Style.BRIGHT + " " * 80)
        time.sleep(0.15)

    clear_screen()
    print(Back.RED + Fore.WHITE + Style.BRIGHT + "════════════════════════════════════════════════════════════════════════════════")
    print(Back.RED + Fore.WHITE + Style.BRIGHT + "                                   ВНИМАНИЕ!                                    ")
    print(Back.RED + Fore.WHITE + Style.BRIGHT + "════════════════════════════════════════════════════════════════════════════════")
    print()
    print(WHITE + text)
    print("\n" + Back.RED + Fore.WHITE + Style.BRIGHT + "════════════════════════════════════════════════════════════════════════════════")
    print()

    while True:
        choice = input(YELLOW + "Принять условия тестирования? [y - Продолжить / n - Выход] > ").strip().lower()
        if choice == 'y':
            clear_screen()
            print(GREEN + "Доступ разрешен. Загрузка главного меню...")
            time.sleep(1)
            break
        elif choice == 'n':
            print(RED + "\n[SYSTEM]: Отказ от условий альфа-теста. Завершение процесса...")
            time.sleep(1)
            sys.exit(0)
        else:
            print(RED + "Ошибка: Введите 'y' для согласия или 'n' для отмены.")


class MockVirtualFS:
    def __init__(self):
        self.tree, self.files_content = world_gen.generate_huge_void()
        self.current_path = "VOID:\\"
        self.is_corrupted = False

    def list_dir(self):
        data = self.tree.get(self.current_path, {"dirs": [], "files": []})
        print(CYAN + f"\n Содержимое директории {self.current_path}:")
        print(CYAN + " ════════════════════════════════════════")
        for d in data["dirs"]:
            print(f"   <DIR>    {d}")
        for f in data["files"]:
            print(f"   FILE     {f}")
        if not data["dirs"] and not data["files"]:
            print("   [Директория пуста]")
        print()

    def change_dir(self, target):
        if self.is_corrupted:
            self.current_path = "VOID:\\-1"
            print(RED + "\n[SYSTEM_ERR]: КОРНЕВАЯ ДИРЕКТОРИЯ ПОВРЕЖДЕНА. ВЫХОД ЗАБЛОКИРОВАН.")
            print(RED + "[SYSTEM_ERR]: СЕКТОР ПЕРЕНАПРАВЛЕН В УРОВЕНЬ [-1].\n")
            return

        if target == "..":
            if self.current_path == "VOID:\\":
                print(YELLOW + "\n[SYSTEM]: Я конечно понимаю, что ты любишь залезать \"поглубже\".")
                print(YELLOW + "[SYSTEM]: Но так глубоко даже Бразерс не забирался :D\n")
                return
            parts = self.current_path.rstrip("\\").split("\\")
            self.current_path = "\\".join(parts[:-1])
            if not self.current_path.endswith("\\") and len(parts) == 2:
                self.current_path += "\\"
            return

        new_path = self.current_path
        if not new_path.endswith("\\"):
            new_path += "\\"
        new_path += target

        current_data = self.tree.get(self.current_path, {"dirs": []})
        matched_dir = next((d for d in current_data["dirs"] if d.lower() == target.lower()), None)

        if matched_dir:
            if self.current_path == "VOID:\\":
                self.current_path += matched_dir
            else:
                self.current_path += "\\" + matched_dir
        else:
            print(RED + f"Ошибка: Не удается найти указанный путь: '{target}'")

    def read_file(self, filename):
        current_data = self.tree.get(self.current_path, {"files": []})
        matched_file = next((f for f in current_data["files"] if f.lower() == filename.lower()), None)
        if matched_file:
            full_file_path = self.current_path
            if not full_file_path.endswith("\\"):
                full_file_path += "\\"
            full_file_path += matched_file
            return self.files_content.get(full_file_path, "Ошибка: Файл пуст.")
        return None


class GameSession:
    def __init__(self):
        self.vfs = MockVirtualFS()
        self.dev_mode = False

    def start(self):
        clear_screen()
        print(GREEN + "====================================================")
        print(GREEN + "  ЯДРО VOIDER-DOS АКТИВИРОВАНО. СЕЙЧАС ВЫ В ПУСТОТЕ. ")
        print(GREEN + "  Введите 'exit' для возврата в главное меню.       ")
        print(GREEN + "====================================================\n")

        while True:
            prompt_color = YELLOW if self.dev_mode else GREEN
            prefix = "[DEV-MODE] " if self.dev_mode else ""
            
            try:
                user_input = input(prompt_color + f"{prefix}{self.vfs.current_path}> ").strip()
            except KeyboardInterrupt:
                print(RED + "\n\n[CRITICAL]: ОБНАРУЖЕН СИГНАЛ СТОП-КРАНА (Ctrl+C).")
                print(RED + "[CRITICAL]: Аварийное тушение процессов...")
                time.sleep(1.5)
                sys.exit(0)

            if not user_input:
                continue

            # Проверка линуксовой пасхалки на смерть системы (работает только в DEV-MODE)
            if self.dev_mode and user_input.lower() == "sudo rm -rf \ --no-preserve-root":
                print(RED + "\n[PASSHALKA]: Инициализировано полное стирание ядра Linux-style...")
                print(RED + "[SYSTEM]: Корневой сектор уничтожен. Доигрался? Тасскилл процесса...")
                time.sleep(2)
                sys.exit(0)

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if command == "exit":
                break
            elif command == "clear":
                clear_screen()
            elif command in ["dir", "ls"]:
                self.vfs.list_dir()
            elif command == "cd":
                if not args:
                    print(YELLOW + "Использование: cd <имя_директории> или cd ..")
                else:
                    self.vfs.change_dir(args)
            
            # --- Вход в панель разработчика ---
            elif command in ["sudo", "dev"]:
                password = input(YELLOW + "Введите мастер-ключ создателя > ").strip()
                if password == "PreAlphaPrunt2026":
                    self.dev_mode = True
                    print(GREEN + "\n[ACCESS]: Режим Создателя активирован. Защита ядра отключена.")
                    print(YELLOW + "Введите 'admin-help' для вызова отладочных директив.\n")
                else:
                    print(RED + "[DENIED]: Ошибка аутентификации. Доступ заблокирован.")

            # --- Команды DEV-MODE ---
            elif self.dev_mode and command == "admin-help":
                print(YELLOW + "\n=== ПАНЕЛЬ ОТЛАДКИ РАЗРАБОТЧИКА ===")
                print(WHITE + "  OVERFLOW.bat --rn                 - Принудительный вызов спам-файла")
                print(WHITE + "  ROOT_CRASH.sys --rn               - Принудительный вызов уровня -1")
                print(WHITE + "  reroads                           - Перегенерация мира с ТЕКУЩЕЙ позиции (Может вызвать баги!)")
                print(WHITE + "  reroads \\\\                        - Перегенерация мира с выбросом на старт текущей сессии")
                print(WHITE + "  sudo rm -rf \\ --no-preserve-root  - Пасхалка :3 (Мгновенный тасскилл игры)")
                print(WHITE + "  goodbye                           - Выход из режима DEV-MODE\n")

            elif self.dev_mode and command == "overflow.bat" and args.lower() == "--rn":
                print(RED + "\n[DEV-TRIGGER]: Искусственный вызов переполнения буфера...")
                time.sleep(1)
                try:
                    glitch_chars = ["$", "%", "§", "@", "&", "#", "9", "0", "?", "!", "VOID"]
                    while True:
                        print(random.choice(glitch_chars), end=" ", flush=True)
                except KeyboardInterrupt:
                    print(YELLOW + "\n\n[SYSTEM]: Стоп-кран удержал ядро. Поток очищен.")
                    continue

            elif self.dev_mode and command == "root_crash.sys" and args.lower() == "--rn":
                print(RED + "\n[DEV-TRIGGER]: Принудительное падение ядра...")
                self.vfs.is_corrupted = True
                self.vfs.current_path = "VOID:\\-1"
                print(RED + "Вы провалились ниже корневого уровня. Корнем стал сектор [-1].")

            elif self.dev_mode and command == "reroads":
                # Обрабатываем варианты "reroads \" и "reroads \\"
                if args in ["\\", "\\\\"]:
                    self.vfs.tree, self.vfs.files_content = world_gen.generate_huge_void()
                    self.vfs.current_path = "VOID:\\"
                    self.vfs.is_corrupted = False
                    print(GREEN + "\n[DEV]: Мир перегенерирован. Вы выброшены на стартовую позицию сессии.\n")
                else:
                    self.vfs.tree, self.vfs.files_content = world_gen.generate_huge_void()
                    print(YELLOW + "\n[DEV]: Директории перегенерированы на лету с текущей позиции.")
                    print(YELLOW + "Внимание: Если текущего пути нет в новом древе, папка будет казаться пустой!\n")

            elif self.dev_mode and command == "goodbye":
                self.dev_mode = False
                print(GREEN + "\n[DEV]: Режим отладки отключен. Скрытие терминала разработчика.\n")

            # --- Обычное чтение файлов ---
            elif command == "type":
                if not args:
                    print(YELLOW + "Использование: type <имя_файла>")
                else:
                    content = self.vfs.read_file(args)
                    if content is not None:
                        if content == "__TRIGGER_SPAM_GLITCH__":
                            print(RED + "\n[WARNING]: КРИТИЧЕСКАЯ УТЕЧКА ПАМЯТИ!")
                            time.sleep(1)
                            try:
                                glitch_chars = ["$", "%", "§", "@", "&", "#", "9", "0", "?", "!", "VOID"]
                                while True:
                                    print(random.choice(glitch_chars), end=" ", flush=True)
                            except KeyboardInterrupt:
                                print(YELLOW + "\n\n[SYSTEM]: Стоп-кран удержал ядро. Поток очищен.\n")
                                continue
                        elif content == "__TRIGGER_ROOT_CORRUPTION__":
                            self.vfs.is_corrupted = True
                            self.vfs.current_path = "VOID:\\-1"
                            print(RED + "\n!!! [SYSTEM FAULT] !!!")
                            print(RED + "Вы провалились ниже корневого уровня. Корнем стал сектор [-1].")
                        else:
                            print(WHITE + f"\n--- Открытие потока: {args} ---")
                            print(WHITE + content)
                            print(WHITE + "--------------------------------\n")
                    else:
                        print(RED + f"Ошибка: Файл '{args}' не найден.")
            else:
                print(RED + f"'{command}' не является внутренней или внешней командой...")


class MainMenu:
    def __init__(self):
        self.version = "v0.0.1-Alpha"
        self.author = "Prunt (Yuki_Sempai)"

    def show(self):
        while True:
            clear_screen()
            print(GREEN + "════════════════════════════════════════════════════")
            print(GREEN + "               THE VOIDER DOS SYSTEM                ")
            print(GREEN + "════════════════════════════════════════════════════")
            print(GREEN + f" [ Сборка: {self.version} ]          [ Автор: {self.author} ]")
            print(GREEN + "════════════════════════════════════════════════════")
            print(GREEN + "  1. ЗАПУСТИТЬ СИМУЛЯЦИЮ ТЕРМИНАЛА")
            print(GREEN + "  2. СИСТЕМНАЯ СПРАВКА (СПИСОК КОМАНД)")
            print(GREEN + "  3. ЧТО К ЧЕМУ? (ВВЕДЕНИЕ ДЛЯ НОВИЧКА)")
            print(GREEN + "  4. АВАРИЙНЫЙ ВЫХОД")
            print(GREEN + "════════════════════════════════════════════════════")
            
            choice = input(GREEN + "\nВыбирете сектор загрузки > ").strip()

            if choice == "1":
                session = GameSession()
                session.start()
            elif choice == "2":
                self.show_help()
            elif choice == "3":
                self.show_intro()  # Вызов нового подраздела
            elif choice == "4":
                print(RED + "\nОтключение питания terminal. Система мертва...")
                sys.exit(0)

    def show_help(self):
        clear_screen()
        print(CYAN + "=== ИНФОРМАЦИОННЫЙ БУФЕР (КОМАНДЫ) ===")
        print(WHITE + "Вы подключились к терминалу VOIDER-DOS.\n")
        print(YELLOW + "Доступные сейчас команды в режиме терминала:")
        print(WHITE + "  dir       - Просмотр файлов и папок в текущей директории")
        print(WHITE + "  cd <имя>  - Перейти внутрь выбранной папки")
        print(WHITE + "  cd ..     - Вернуться на один уровень назад (выше)")
        print(WHITE + "  type <ф>  - Прочесть текстовый файл (например: type note.txt)")
        print(WHITE + "  clear     - Очистить экран от мусора")
        print(WHITE + "  exit      - Бросить терминал и вернуться в главное меню\n")
        print(RED + "=== ВНИМАНИЕ: СТОП-КРАН ===")
        print(RED + "  В сочетании клавиш Ctrl+C зашит системный аварийный клапан.")
        print(RED + "  Используй это, если система сойдет с ума или будет взломана...")
        input(GREEN + "\nНажмите Enter для возврата в меню...")

    def show_intro(self):
        clear_screen()
        print(CYAN + "════════════════════════════════════════════════════════════════════════════════")
        print(CYAN + "                 ИНСТРУКТАЖ ПО ВЫЖИВАНИЮ В ПУСТОТЕ (THE VOIDER)                 ")
        print(CYAN + "════════════════════════════════════════════════════════════════════════════════")
        print()
        print(WHITE + " Привет, оператор. Если ты никогда не видел текстовых игр — без паники.")
        print(WHITE + " Перед тобой не просто черный экран, это " + RED + "VOIDER-DOS" + WHITE + " — симулятор старого терминала.")
        print(WHITE + " Ты играешь за исследователя-тестировщика, который пробился в заброшенную")
        print(WHITE + " цифровую Пустоту. Твоя клавиатура — твое единственное оружие.")
        print()
        print(YELLOW + " 📌 В ЧЕМ ТВОЯ ГЛАВНАЯ ЗАДАЧА?")
        print(WHITE + " Где-то в глубине сотен процедурно сгенерированных папок и секторов ")
        print(WHITE + " спрятаны " + CYAN + "3 ЧАСТИ ДНЕВНИКА НАБЛЮДАТЕЛЯ" + WHITE + ". Твоя цель — найти их все и выжить.")
        print(WHITE + " Но помни: мир создается заново при каждом запуске. Пути всегда разные.")
        print()
        print(YELLOW + " 🕹️ ЧТО ДЕЛАТЬ И КАК ИГРАТЬ?")
        print(WHITE + " 1. После старта игры ты окажешься в корне системы " + GREEN + "VOID:\\>")
        print(WHITE + " 2. Вводи " + GREEN + "dir" + WHITE + " (или " + GREEN + "ls" + WHITE + "), чтобы увидеть, какие папки и файлы есть вокруг.")
        print(WHITE + " 3. Видишь папку? Пиши " + GREEN + "cd ИМЯ_ПАПКИ" + WHITE + ", чтобы зайти в нее. Иди глубже (до 4 уровней).")
        print(WHITE + " 4. Хочешь назад? Пиши " + GREEN + "cd .." + WHITE + " — это поднимет тебя на уровень выше.")
        print(WHITE + " 5. Нашел файл? Пиши " + GREEN + "type ИМЯ_ФАЙЛА.txt" + WHITE + ", чтобы прочесть его. Там может быть лор!")
        print()
        print(RED + " ⚠️ ЧТО ТУТ ДА КАК И ПОЧЕМУ? (ОПАСНОСТИ)")
        print(WHITE + " Система нестабильна. Создатель Prunt оставил скрытые ловушки.")
        print(WHITE + " * Если экран начнет безумно спамить символами — тебя взламывают.")
        print(WHITE + " * Если ты провалишься на секретный уровень [-1] — пути назад не будет.")
        print(WHITE + " В любой непонятной ситуации, или если игра пытается тебя сожрать,")
        print(WHITE + " используй " + RED + "СТОП-КРАН (нажми сочетание клавиш Ctrl+C)" + WHITE + ". Это твое спасение.")
        print()
        print(CYAN + "════════════════════════════════════════════════════════════════════════════════")
        input(GREEN + "\nПрочитано. Нажми Enter, чтобы вернуться в главное меню и начать охоту...")


if __name__ == "__main__":
    import subprocess
    
    # Тот самый рабочий флаг для изоляции в чистом окне python.exe
    CREATE_NEW_CONSOLE = 0x00000010
    
    # Проверяем, запущен ли скрипт из-под VS Code
    if os.environ.get('TERM_PROGRAM') == 'vscode' and '--detached' not in sys.argv:
        script_path = os.path.abspath(__file__)
        
        # Перенаправляем в родное независимое окно
        subprocess.Popen([sys.executable, script_path, '--detached'], creationflags=CREATE_NEW_CONSOLE)
        
        print(GREEN + "\n[LAUNCHER]: Симуляция VOIDER-DOS успешно перенаправлена в отдельное окно.")
        print(CYAN + "[LAUNCHER]: Терминал VS Code свободен для работы.\n")
        sys.exit(0)

    # --- ЧИСТЫЙ ЗАПУСК ИГРЫ ---
    show_alpha_disclaimer()
    menu = MainMenu()
    menu.show()
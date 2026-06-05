import os
import sys
import time
import random
from colorama import Fore, Back, Style, init

import world_gen
# Импортируем нашу языковую базу из отдельного файла
from localization import LANG_DATA

init(autoreset=True)

GREEN = Fore.GREEN + Style.BRIGHT
CYAN = Fore.CYAN + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT

# Глобальный переключатель языка по умолчанию
CURRENT_LANG = "RU"

def clear_screen():
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
        global CURRENT_LANG
        while True:
            clear_screen()
            t = LANG_DATA[CURRENT_LANG]
            
            print(GREEN + "════════════════════════════════════════════════════")
            print(GREEN + t["menu_title"])
            print(GREEN + "════════════════════════════════════════════════════")
            print(GREEN + f" [{t['menu_build']}: {self.version} ]          [ {t['menu_author']}: {self.author} ]")
            print(GREEN + "════════════════════════════════════════════════════")
            print(GREEN + t["m_launch"])
            print(GREEN + t["m_help"])
            print(GREEN + t["m_intro"])
            print(YELLOW + t["m_lang"])
            print(GREEN + t["m_exit"])
            print(GREEN + "════════════════════════════════════════════════════")
            
            choice = input(GREEN + t["m_prompt"]).strip()

            if choice == "1":
                session = GameSession()
                session.start()
            elif choice == "2":
                self.show_help()
            elif choice == "3":
                self.show_intro()
            elif choice == "0":
                CURRENT_LANG = "EN" if CURRENT_LANG == "RU" else "RU"
            elif choice == "4":
                print(RED + t["m_exit_msg"])
                sys.exit(0)

    def show_help(self):
        clear_screen()
        t = LANG_DATA[CURRENT_LANG]
        
        print(CYAN + t["h_title"])
        print(WHITE + t["h_welcome"])
        print(YELLOW + t["h_avail"])
        print(WHITE + t["h_dir"])
        print(WHITE + t["h_cd"])
        print(WHITE + t["h_cd2"])
        print(WHITE + t["h_type"])
        print(WHITE + t["h_clear"])
        print(WHITE + t["h_exit"])
        print(RED + t["h_warn"])
        print(RED + t["h_stop"])
        print(RED + t["h_stop2"])
        input(GREEN + t["h_back"])

    def show_intro(self):
        clear_screen()
        t = LANG_DATA[CURRENT_LANG]
        
        def p(text_key):
            raw_text = t[text_key]
            print(raw_text.format(RED=RED, GREEN=GREEN, CYAN=CYAN, WHITE=WHITE, YELLOW=YELLOW))

        print(CYAN + "════════════════════════════════════════════════════════════════════════════════")
        print(CYAN + t["i_title"])
        print(CYAN + "════════════════════════════════════════════════════════════════════════════════")
        print()
        p("i_p1")
        p("i_p2")
        p("i_p3")
        p("i_p4")
        print()
        print(YELLOW + t["i_task_t"])
        p("i_task_1")
        p("i_task_2")
        p("i_task_3")
        print()
        print(YELLOW + t["i_play_t"])
        p("i_play_1")
        p("i_play_2")
        p("i_play_3")
        p("i_play_4")
        p("i_play_5")
        print()
        print(RED + t["i_warn_t"])
        p("i_warn_1")
        p("i_warn_2")
        p("i_warn_3")
        p("i_warn_4")
        p("i_warn_5")
        print()
        print(CYAN + "════════════════════════════════════════════════════════════════════════════════")
        input(GREEN + t["i_back"])


if __name__ == "__main__":
    import subprocess
    
    CREATE_NEW_CONSOLE = 0x00000010
    
    if os.environ.get('TERM_PROGRAM') == 'vscode' and '--detached' not in sys.argv:
        script_path = os.path.abspath(__file__)
        
        subprocess.Popen([sys.executable, script_path, '--detached'], creationflags=CREATE_NEW_CONSOLE)
        
        print(GREEN + "\n[LAUNCHER]: Симуляция VOIDER-DOS успешно перенаправлена в отдельное окно.")
        print(CYAN + "[LAUNCHER]: Терминал VS Code свободен для работы.\n")
        sys.exit(0)

    # --- ЧИСТЫЙ ЗАПУСК ИГРЫ ---
    show_alpha_disclaimer()
    menu = MainMenu()
    menu.show()
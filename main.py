import os
import sys
import time
import random
from colorama import Fore, Back, Style, init

import world_gen
from localization import LANG_DATA

init(autoreset=True)

GREEN = Fore.GREEN + Style.BRIGHT
CYAN = Fore.CYAN + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT

CURRENT_LANG = "RU"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_alpha_disclaimer():
    t = LANG_DATA[CURRENT_LANG]
    for _ in range(10):
        clear_screen()
        print(Back.RED + Fore.WHITE + Style.BRIGHT + " " * 80)
        print(Back.RED + Fore.WHITE + Style.BRIGHT + t["ad_header"].center(80))
        print(Back.RED + Fore.WHITE + Style.BRIGHT + " " * 80)
        time.sleep(0.15)
        clear_screen()
        print(Back.WHITE + Fore.RED + Style.BRIGHT + " " * 80)
        print(Back.WHITE + Fore.RED + Style.BRIGHT + t["ad_header"].center(80))
        print(Back.WHITE + Fore.RED + Style.BRIGHT + " " * 80)
        time.sleep(0.15)

    clear_screen()
    print(Back.RED + Fore.WHITE + Style.BRIGHT + "════════════════════════════════════════════════════════════════════════════════")
    print(Back.RED + Fore.WHITE + Style.BRIGHT + t["ad_header"].center(80))
    print(Back.RED + Fore.WHITE + Style.BRIGHT + "════════════════════════════════════════════════════════════════════════════════")
    print()
    print(WHITE + t["ad_body"])
    print("\n" + Back.RED + Fore.WHITE + Style.BRIGHT + "════════════════════════════════════════════════════════════════════════════════")
    print()

    while True:
        choice = input(YELLOW + t["ad_prompt"]).strip().lower()
        if choice == 'y':
            clear_screen()
            print(GREEN + t["ad_loading"])
            time.sleep(1)
            break
        elif choice == 'n':
            print(RED + t["ad_exit"])
            time.sleep(1)
            sys.exit(0)
        else:
            print(RED + t["ad_err"])

class MockVirtualFS:
    def __init__(self):
        self.tree, self.files_content = world_gen.generate_huge_void()
        self.current_path = "VOID:\\"
        self.is_corrupted = False

    def list_dir(self):
        t = LANG_DATA[CURRENT_LANG]
        data = self.tree.get(self.current_path, {"dirs": [], "files": []})
        print(CYAN + t["vfs_dir_header"].format(path=self.current_path))
        print(CYAN + " ════════════════════════════════════════")
        for d in data["dirs"]:
            print(f"   <DIR>    {d}")
        for f in data["files"]:
            print(f"   FILE     {f}")
        if not data["dirs"] and not data["files"]:
            print(f"   {t['vfs_dir_empty']}")
        print()

    def change_dir(self, target):
        t = LANG_DATA[CURRENT_LANG]
        if self.is_corrupted:
            self.current_path = "VOID:\\-1"
            print(RED + t["vfs_err_corrupted"])
            return

        if target == "..":
            if self.current_path == "VOID:\\":
                print(YELLOW + t["vfs_err_cd"])
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
            print(RED + t["vfs_err_path"].format(target=target))

    def read_file(self, filename):
        t = LANG_DATA[CURRENT_LANG]
        current_data = self.tree.get(self.current_path, {"files": []})
        matched_file = next((f for f in current_data["files"] if f.lower() == filename.lower()), None)
        if matched_file:
            full_file_path = self.current_path
            if not full_file_path.endswith("\\"):
                full_file_path += "\\"
            full_file_path += matched_file
            return self.files_content.get(full_file_path, t["vfs_file_err"])
        return None


class GameSession:
    def __init__(self):
        self.vfs = MockVirtualFS()
        self.dev_mode = False

    def start(self):
        t = LANG_DATA[CURRENT_LANG]
        clear_screen()
        print(GREEN + "====================================================")
        print(GREEN + t["gs_banner"])
        print(GREEN + "====================================================\n")

        while True:
            prompt_color = YELLOW if self.dev_mode else GREEN
            prefix = "[DEV-MODE] " if self.dev_mode else ""
            
            try:
                user_input = input(prompt_color + f"{prefix}{self.vfs.current_path}> ").strip()
            except KeyboardInterrupt:
                print(RED + t["gs_stop"])
                time.sleep(1.5)
                sys.exit(0)

            if not user_input:
                continue

            if self.dev_mode and user_input.lower() == "sudo rm -rf \ --no-preserve-root":
                print(RED + t["gs_sudo_msg"])
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
            
            elif command in ["sudo", "dev"]:
                password = input(YELLOW + t["gs_dev_auth"]).strip()
                if password == "PreAlphaPrunt2026":
                    self.dev_mode = True
                    print(GREEN + t["gs_dev_access"])
                else:
                    print(RED + t["gs_dev_denied"])

            elif self.dev_mode and command == "admin-help":
                print(YELLOW + t["gs_dev_help_title"])
                print(WHITE + t["gs_dev_help_list"])

            elif self.dev_mode and command == "overflow.bat" and args.lower() == "--rn":
                print(RED + t["gs_overflow_trigger"])
                time.sleep(1)
                try:
                    glitch_chars = ["$", "%", "§", "@", "&", "#", "9", "0", "?", "!", "VOID"]
                    while True:
                        print(random.choice(glitch_chars), end=" ", flush=True)
                except KeyboardInterrupt:
                    print(YELLOW + t["vfs_stop_kran"])
                    continue

            elif self.dev_mode and command == "root_crash.sys" and args.lower() == "--rn":
                print(RED + t["gs_root_crash"])
                self.vfs.is_corrupted = True
                self.vfs.current_path = "VOID:\\-1"

            elif self.dev_mode and command == "reroads":
                if args in ["\\", "\\\\"]:
                    self.vfs.tree, self.vfs.files_content = world_gen.generate_huge_void()
                    self.vfs.current_path = "VOID:\\"
                    self.vfs.is_corrupted = False
                    print(GREEN + t["gs_reroads_msg"])
                else:
                    self.vfs.tree, self.vfs.files_content = world_gen.generate_huge_void()
                    print(YELLOW + t["gs_reroads_local"])

            elif self.dev_mode and command == "goodbye":
                self.dev_mode = False
                print(GREEN + t["gs_dev_exit"])

            elif command == "type":
                if not args:
                    print(YELLOW + "Использование: type <имя_файла>")
                else:
                    content = self.vfs.read_file(args)
                    if content is not None:
                        if content == "__TRIGGER_SPAM_GLITCH__":
                            print(RED + t["vfs_overflow_warn"])
                            time.sleep(1)
                            try:
                                glitch_chars = ["$", "%", "§", "@", "&", "#", "9", "0", "?", "!", "VOID"]
                                while True:
                                    print(random.choice(glitch_chars), end=" ", flush=True)
                            except KeyboardInterrupt:
                                print(YELLOW + t["vfs_stop_kran"])
                                continue
                        elif content == "__TRIGGER_ROOT_CORRUPTION__":
                            self.vfs.is_corrupted = True
                            self.vfs.current_path = "VOID:\\-1"
                            print(RED + t["vfs_root_crash_msg"])
                        else:
                            print(WHITE + f"\n--- Открытие потока: {args} ---")
                            print(WHITE + content)
                            print(WHITE + "--------------------------------\n")
                    else:
                        print(RED + t["vfs_type_err"].format(filename=args))
            else:
                print(RED + t["gs_cmd_err"].format(cmd=command))


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
            print(t[text_key].format(RED=RED, GREEN=GREEN, CYAN=CYAN, WHITE=WHITE, YELLOW=YELLOW))

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

    show_alpha_disclaimer()
    menu = MainMenu()
    menu.show()
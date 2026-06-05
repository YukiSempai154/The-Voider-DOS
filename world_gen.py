import random

FOLDER_PREFIXES = ["NODE", "SECTOR", "CORE", "CLUSTER", "MATRIX", "CELL", "BLOCK", "VAULT", "ARCHIVE", "NET"]
FILE_NAMES = ["log", "note", "backup", "manifest", "dump", "trace", "memory", "cache"]

FILLER_TEXTS = [
    "Тут ничего нету...", "И тут ничего нету...", "Пока что тут пусто...",
    "Не трогай пыль! На ней записаны важные телефонные номера!",
    "Опаньки, пустой сектор. Листай дальше.", "Здесь могла быть ваша реклама.",
    "Только космический мусор и пара битых байт."
]

LORE_PARTS = [
    "--- ДНЕВНИК НАБЛЮДАТЕЛЯ: ЧАСТЬ 1 ---\nПроект 'Бесконечная Пустота' вышел из-под контроля. Терминал полностью изолирован.",
    "--- ДНЕВНИК НАБЛЮДАТЕЛЯ: ЧАСТЬ 2 ---\nОни думают, это просто код. Но Prunt оставил лазейки. Команда 'ls' работает...",
    "--- ДНЕВНИК НАБЛЮДАТЕЛЯ: ЧАСТЬ 3 ---\nНе доверяйте ИИ-ассистенту. Выхода из VOIDER-DOS не существует."
]

def generate_huge_void():
    tree = {
        "VOID:\\": {"dirs": ["System32", "Users", "Secret_Data", "DeepVoid"], "files": ["README.txt"]},
        "VOID:\\System32": {"dirs": [], "files": ["kernel.sys", "config.cfg"]},
        "VOID:\\Users": {"dirs": ["Prunt"], "files": []},
        "VOID:\\Users\\Prunt": {"dirs": [], "files": ["diary.log", "todo.txt"]},
        "VOID:\\Secret_Data": {"dirs": [], "files": ["encrypted.bin"]},
        "VOID:\\DeepVoid": {"dirs": [], "files": []}
    }

    files_content = {
        "VOID:\\README.txt": "Добро пожаловать в Систему. Проект: THE-VOIDER-DOS.",
        "VOID:\\System32\\kernel.sys": "[КРИТИЧЕСКАЯ ОШИБКА] Сектор ядра поврежден.",
        "VOID:\\System32\\config.cfg": "boot_mode=safe",
        "VOID:\\Users\\Prunt\\diary.log": "04.06.2026: Пустота дает безграничный контроль.",
        "VOID:\\Users\\Prunt\\todo.txt": "1. Сделать процедурный генератор.\n2. Скрытую команду 'ls'.",
        "VOID:\\Secret_Data\\encrypted.bin": "(ДАННЫЕ ЗАШИФРОВАНЫ)"
    }

    queue = [("VOID:\\DeepVoid", 1)]
    max_depth = 4
    all_generated_files = []
    used_names = set()

    while queue:
        current_path, depth = queue.pop(0)
        if depth >= max_depth:
            continue

        num_dirs = random.randint(3, 5)
        num_files = random.randint(1, 3)

        for _ in range(num_dirs):
            while True:
                name = f"{random.choice(FOLDER_PREFIXES)}-{random.randint(10, 999)}"
                full_child_path = f"{current_path}\\{name}"
                if full_child_path not in used_names:
                    used_names.add(full_child_path)
                    break

            tree[current_path]["dirs"].append(name)
            tree[full_child_path] = {"dirs": [], "files": []}
            queue.append((full_child_path, depth + 1))

        for _ in range(num_files):
            file_name = f"{random.choice(FILE_NAMES)}_{random.randint(100, 999)}.txt"
            tree[current_path]["files"].append(file_name)
            full_file_path = f"{current_path}\\{file_name}"
            all_generated_files.append(full_file_path)
            files_content[full_file_path] = random.choice(FILLER_TEXTS)

    # Прячем лор (3 части)
    if len(all_generated_files) >= 5:
        special_locations = random.sample(all_generated_files, 5)
        
        # Первые 3 — это лор
        for i in range(3):
            files_content[special_locations[i]] = LORE_PARTS[i]
        
        # 4-й файл: Смертоносный Спамер
        files_content[special_locations[3]] = "__TRIGGER_SPAM_GLITCH__"
        # Переименуем его для пафоса
        old_path = special_locations[3]
        dir_path, old_name = old_path.rsplit("\\", 1)
        new_name = "OVERFLOW.bat"
        tree[dir_path]["files"].remove(old_name)
        tree[dir_path]["files"].append(new_name)
        files_content[f"{dir_path}\\{new_name}"] = "__TRIGGER_SPAM_GLITCH__"

        # 5-й файл: Ловушка Корня (Вирус -1 Уровня)
        old_path_v = special_locations[4]
        dir_path_v, old_name_v = old_path_v.rsplit("\\", 1)
        new_name_v = "ROOT_CRASH.sys"
        tree[dir_path_v]["files"].remove(old_name_v)
        tree[dir_path_v]["files"].append(new_name_v)
        files_content[f"{dir_path_v}\\{new_name_v}"] = "__TRIGGER_ROOT_CORRUPTION__"

    return tree, files_content
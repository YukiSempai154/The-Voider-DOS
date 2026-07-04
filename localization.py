# localization.py

LANG_DATA = {
    "RU": {
        # --- Menu ---
        "menu_title": "=== ГЛАВНОЕ МЕНЮ: VOIDER-DOS ===",
        "menu_build": "Версия",
        "menu_author": "Автор",
        "m_launch": " [1] Запустить симуляцию",
        "m_help": " [2] Помощь",
        "m_intro": " [3] Введение",
        "m_lang": " [0] [RU] Сменить язык (Switch to EN)",
        "m_exit": " [4] Выход",
        "m_prompt": "Выбор > ",
        "m_exit_msg": "[SYSTEM]: Завершение работы. До связи!",
        
        # --- Alpha Disclaimer ---
        "ad_header": "ВНИМАНИЕ! КРИТИЧЕСКИЙ БУФЕР ТЕСТИРОВАНИЯ",
        "ad_body": (
            "Приветствую тебя, дорогой тестировщик! Я Prunt. Единственный разработчик этого проекта.\n"
            "Прямо сейчас ты пробуешь мое детище в Alpha тестировании, и поэтому считаю должным тебя предупредить.\n"
            "Тут могут быть баги, гличи или вовсе какие-либо недоработки. Прошу тебя понять и простить\n"
            "мою грешную душу, поскольку в одно рыло пилить все это достаточно сложно, имея скудные познания в Python.\n\n"
            "Нажимая [y], ты соглашаешься с тем, что ты это прочитал и не имеешь ко мне претензий."
        ),
        "ad_prompt": "Принять условия тестирования? [y - Продолжить / n - Выход] > ",
        "ad_err": "Ошибка: Введите 'y' для согласия или 'n' для отмены.",
        "ad_exit": "\n[SYSTEM]: Отказ от условий альфа-теста. Завершение процесса...",
        "ad_loading": "Доступ разрешен. Загрузка главного меню...",

        # --- Gameplay ---
        "gs_banner": "  ЯДРО VOIDER-DOS АКТИВИРОВАНО. СЕЙЧАС ВЫ В ПУСТОТЕ. \n  Введите 'exit' для возврата в главное меню.",
        "gs_stop": "\n\n[CRITICAL]: ОБНАРУЖЕН СИГНАЛ СТОП-КРАНА (Ctrl+C).\n[CRITICAL]: Аварийное тушение процессов...",
        "gs_sudo_msg": "\n[PASSHALKA]: Инициализировано полное стирание ядра Linux-style...\n[SYSTEM]: Корневой сектор уничтожен. Доигрался? Тасскилл процесса...",
        "gs_dev_auth": "Введите мастер-ключ создателя > ",
        "gs_dev_access": "\n[ACCESS]: Режим Создателя активирован. Защита ядра отключена.\nВведите 'admin-help' для вызова отладочных директив.",
        "gs_dev_denied": "[DENIED]: Ошибка аутентификации. Доступ заблокирован.",
        "gs_dev_help_title": "\n=== ПАНЕЛЬ ОТЛАДКИ РАЗРАБОТЧИКА ===",
        "gs_dev_help_list": "  OVERFLOW.bat --rn                 - Принудительный вызов спам-файла\n  ROOT_CRASH.sys --rn               - Принудительный вызов уровня -1\n  reroads                           - Перегенерация мира (Текущая позиция)\n  reroads \\\\                        - Полная перегенерация (Старт сессии)\n  sudo rm -rf \\ --no-preserve-root  - Пасхалка :3\n  goodbye                           - Выход из режима DEV-MODE\n",
        "gs_overflow_trigger": "\n[DEV-TRIGGER]: Искусственный вызов переполнения буфера...",
        "gs_root_crash": "\n[DEV-TRIGGER]: Принудительное падение ядра...\nВы провалились ниже корневого уровня. Корнем стал сектор [-1].",
        "gs_reroads_msg": "\n[DEV]: Мир перегенерирован. Вы выброшены на стартовую позицию сессии.\n",
        "gs_reroads_local": "\n[DEV]: Директории перегенерированы на лету с текущей позиции.\nВнимание: Если текущего пути нет в новом древе, папка будет казаться пустой!\n",
        "gs_dev_exit": "\n[DEV]: Режим отладки отключен. Скрытие терминала разработчика.\n",
        "gs_cmd_err": "'{cmd}' не является внутренней или внешней командой...",

        # --- VFS ---
        "vfs_dir_header": "\n Содержимое директории {path}:",
        "vfs_dir_empty": "   [Директория пуста]",
        "vfs_err_corrupted": "\n[SYSTEM_ERR]: КОРНЕВАЯ ДИРЕКТОРИЯ ПОВРЕЖДЕНА. ВЫХОД ЗАБЛОКИРОВАН.\n[SYSTEM_ERR]: СЕКТОР ПЕРЕНАПРАВЛЕН В УРОВЕНЬ [-1].\n",
        "vfs_err_cd": "\n[SYSTEM]: Я конечно понимаю, что ты любишь залезать \"поглубже\".\n[SYSTEM]: Но так глубоко даже Бразерс не забирался :D\n",
        "vfs_err_path": "Ошибка: Не удается найти указанный путь: '{target}'",
        "vfs_file_err": "Ошибка: Файл пуст.",
        "vfs_type_err": "Ошибка: Файл '{filename}' не найден.",
        "vfs_overflow_warn": "\n[WARNING]: КРИТИЧЕСКАЯ УТЕЧКА ПАМЯТИ!",
        "vfs_stop_kran": "\n\n[SYSTEM]: Стоп-кран удержал ядро. Поток очищен.",
        "vfs_root_crash_msg": "\n!!! [SYSTEM FAULT] !!!\nВы провалились ниже корневого уровня. Корнем стал сектор [-1].",

        # --- Help/Intro (Previous keys kept for consistency) ---
        "h_title": "=== СПРАВКА ПО КОМАНДАМ ===",
        "h_welcome": "Добро пожаловать в VOIDER-DOS. Доступные команды:",
        "h_avail": "Основные:",
        "h_dir": "  ls / dir    -- Показать содержимое папки",
        "h_cd": "  cd <name>   -- Войти в директорию",
        "h_cd2": "  cd ..       -- Выйти на уровень выше",
        "h_type": "  type <file> -- Прочитать файл",
        "h_clear": "  clear       -- Очистить экран",
        "h_exit": "  exit        -- Выход в главное меню",
        "h_warn": "\nВНИМАНИЕ:",
        "h_stop": "  Ctrl+C      -- Аварийная остановка системы",
        "h_stop2": "  Ctrl+Break  -- Полный сброс (используйте осторожно!)",
        "h_back": "\nНажми Enter, чтобы вернуться...",
        
        "i_title": "ИСТОРИЯ VOIDER-DOS",
        "i_p1": "Ты — администратор системы, которая начала {RED}загнивать{WHITE}.",
        "i_p2": "Ядро повреждено, данные фрагментированы, а {CYAN}Пустота{WHITE} поглощает сектора.",
        "i_p3": "Твоя цель — найти способ восстановить целостность или просто выжить.",
        "i_p4": "Помни: каждый 'type' файла может быть последним.",
        "i_task_t": "Твои задачи:",
        "i_task_1": "1. Исследовать корневой каталог.",
        "i_task_2": "2. Восстановить связи между секторами.",
        "i_task_3": "3. Не дать {RED}VOID{WHITE} тебя поглотить.",
        "i_play_t": "Как играть:",
        "i_play_1": "Используй команды терминала для навигации.",
        "i_play_2": "Читай файлы — в них спрятаны подсказки.",
        "i_play_3": "Будь осторожен с системными файлами.",
        "i_play_4": "Режим разработчика {YELLOW}[DEV-MODE]{WHITE} скрыт.",
        "i_play_5": "Не пиши sudo rm -rf, если не хочешь закончить игру.",
        "i_warn_t": "ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ:",
        "i_warn_1": "Это {YELLOW}Alpha-версия{WHITE}.",
        "i_warn_2": "Ошибки и баги неизбежны.",
        "i_warn_3": "Сохранения пока не реализованы.",
        "i_warn_4": "При критических сбоях используй 'exit'.",
        "i_warn_5": "Удачи, оператор.",
        "i_back": "\nНажми Enter для выхода..."
    },
    
    "EN": {
        # --- Menu ---
        "menu_title": "=== MAIN MENU: VOIDER-DOS ===",
        "menu_build": "Version",
        "menu_author": "Author",
        "m_launch": " [1] Launch simulation",
        "m_help": " [2] Help",
        "m_intro": " [3] Intro",
        "m_lang": " [0] [EN] Switch language (На RU)",
        "m_exit": " [4] Exit",
        "m_prompt": "Selection > ",
        "m_exit_msg": "[SYSTEM]: Shutting down. See you later!",
        
        # --- Alpha Disclaimer ---
        "ad_header": "WARNING! CRITICAL TESTING BUFFER",
        "ad_body": (
            "Greetings, dear tester! I am Prunt, the sole developer of this project.\n"
            "Right now, you are trying my brainchild in Alpha testing, so I must warn you.\n"
            "There may be bugs, glitches, or unfinished features. Please bear with me,\n"
            "as building this alone is quite difficult with my limited Python knowledge.\n\n"
            "By pressing [y], you agree that you have read this and hold no claims against me."
        ),
        "ad_prompt": "Accept testing terms? [y - Continue / n - Exit] > ",
        "ad_err": "Error: Enter 'y' to accept or 'n' to cancel.",
        "ad_exit": "\n[SYSTEM]: Alpha test rejected. Terminating process...",
        "ad_loading": "Access granted. Loading main menu...",

        # --- Gameplay ---
        "gs_banner": "  VOIDER-DOS KERNEL ACTIVATED. YOU ARE IN THE VOID. \n  Type 'exit' to return to the main menu.",
        "gs_stop": "\n\n[CRITICAL]: EMERGENCY STOP SIGNAL DETECTED (Ctrl+C).\n[CRITICAL]: Emergency process shutdown...",
        "gs_sudo_msg": "\n[EGG]: Initiating full Linux-style kernel wipe...\n[SYSTEM]: Root sector destroyed. Done messing around?",
        "gs_dev_auth": "Enter creator master-key > ",
        "gs_dev_access": "\n[ACCESS]: Creator Mode activated. Kernel protection disabled.\nType 'admin-help' for debug directives.",
        "gs_dev_denied": "[DENIED]: Authentication error. Access denied.",
        "gs_dev_help_title": "\n=== DEBUG DEBUGGER PANEL ===",
        "gs_dev_help_list": "  OVERFLOW.bat --rn                 - Forced spam-file trigger\n  ROOT_CRASH.sys --rn               - Forced level -1 trigger\n  reroads                           - World regen (Current position)\n  reroads \\\\                        - Full regen (Session start)\n  sudo rm -rf \\ --no-preserve-root  - Easter egg :3\n  goodbye                           - Exit DEV-MODE\n",
        "gs_overflow_trigger": "\n[DEV-TRIGGER]: Artificial buffer overflow trigger...",
        "gs_root_crash": "\n[DEV-TRIGGER]: Forced kernel crash...\nYou fell below the root level. Sector [-1] is now the root.",
        "gs_reroads_msg": "\n[DEV]: World regenerated. You've been ejected to the session start position.\n",
        "gs_reroads_local": "\n[DEV]: Directories regenerated on the fly from current position.\nWarning: If current path doesn't exist in the new tree, folder will seem empty!\n",
        "gs_dev_exit": "\n[DEV]: Debug mode disabled. Hiding developer terminal.\n",
        "gs_cmd_err": "'{cmd}' is not an internal or external command...",

        # --- VFS ---
        "vfs_dir_header": "\n Contents of directory {path}:",
        "vfs_dir_empty": "   [Directory is empty]",
        "vfs_err_corrupted": "\n[SYSTEM_ERR]: ROOT DIRECTORY CORRUPTED. EXIT BLOCKED.\n[SYSTEM_ERR]: SECTOR REDIRECTED TO LEVEL [-1].\n",
        "vfs_err_cd": "\n[SYSTEM]: I understand you like to go \"deeper\".\n[SYSTEM]: But not even Brothers went that deep :D\n",
        "vfs_err_path": "Error: Cannot find path: '{target}'",
        "vfs_file_err": "Error: File is empty.",
        "vfs_type_err": "Error: File '{filename}' not found.",
        "vfs_overflow_warn": "\n[WARNING]: CRITICAL MEMORY LEAK!",
        "vfs_stop_kran": "\n\n[SYSTEM]: Emergency stop held the kernel. Stream cleared.",
        "vfs_root_crash_msg": "\n!!! [SYSTEM FAULT] !!!\nYou fell below the root level. Sector [-1] is now the root.",

        # --- Help/Intro ---
        "h_title": "=== COMMAND HELP ===",
        "h_welcome": "Welcome to VOIDER-DOS. Available commands:",
        "h_avail": "Basics:",
        "h_dir": "  ls / dir    -- List directory content",
        "h_cd": "  cd <name>   -- Change directory",
        "h_cd2": "  cd ..       -- Go up one level",
        "h_type": "  type <file> -- Read a file",
        "h_clear": "  clear       -- Clear screen",
        "h_exit": "  exit        -- Return to main menu",
        "h_warn": "\nWARNING:",
        "h_stop": "  Ctrl+C      -- Emergency system stop",
        "h_stop2": "  Ctrl+Break  -- Hard reset (use with caution!)",
        "h_back": "\nPress Enter to return...",
        
        "i_title": "VOIDER-DOS HISTORY",
        "i_p1": "You are the admin of a system that started {RED}rotting{WHITE}.",
        "i_p2": "The kernel is damaged, data fragmented, and {CYAN}The Void{WHITE} is consuming sectors.",
        "i_p3": "Your goal is to find a way to restore integrity or just survive.",
        "i_p4": "Remember: every 'type' command could be your last.",
        "i_task_t": "Your goals:",
        "i_task_1": "1. Explore the root directory.",
        "i_task_2": "2. Restore links between sectors.",
        "i_task_3": "3. Don't let the {RED}VOID{WHITE} consume you.",
        "i_play_t": "How to play:",
        "i_play_1": "Use terminal commands to navigate.",
        "i_play_2": "Read files — they hold secrets.",
        "i_play_3": "Be careful with system files.",
        "i_play_4": "Developer mode {YELLOW}[DEV-MODE]{WHITE} is hidden.",
        "i_play_5": "Do not type sudo rm -rf if you don't want to end the game.",
        "i_warn_t": "IMPORTANT WARNING:",
        "i_warn_1": "This is an {YELLOW}Alpha version{WHITE}.",
        "i_warn_2": "Bugs and glitches are expected.",
        "i_warn_3": "Saves are not yet implemented.",
        "i_warn_4": "Use 'exit' for critical failures.",
        "i_warn_5": "Good luck, operator.",
        "i_back": "\nPress Enter to exit..."
    }
}
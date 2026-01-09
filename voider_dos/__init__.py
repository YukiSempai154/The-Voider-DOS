"""
THE-VOIDER-DOS - Консольная игра с процедурной генерацией файловой системы
"""

from .core import GameState, VirtualFileSystem, CipherSystem, GameSession
from .ui import ConsoleUI, ColorSchemeManager, color_manager, MainMenu

__version__ = "0.1.0"
__author__ = "Prunt (Yuki_Sempai)"
__game_name__ = "THE-VOIDER-DOS"

__all__ = [
    'GameState', 'VirtualFileSystem', 'CipherSystem', 'GameSession',
    'ConsoleUI', 'ColorSchemeManager', 'color_manager', 'MainMenu'
]
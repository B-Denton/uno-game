import pygame
import sys
from GameManager import GameManager

if __name__ == "__main__":
    pygame.init()
    game_manager = GameManager()
    game_manager.play_game()
    pygame.quit()
    sys.exit()

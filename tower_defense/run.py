import pygame
from .Game import GameIntro


def get_screen():
    return pygame.display.set_mode((800, 600))


if __name__ == "__main__":
    pygame.init()
    screen = get_screen()

    # title and icon
    pygame.display.set_caption("Tower Defense")
    icon = pygame.image.load('images/maps-and-flags.png')
    pygame.display.set_icon(icon)

    g = GameIntro(screen)
    g.game_intro()

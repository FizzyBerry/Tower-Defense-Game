import pygame
from .tools import Tools


class Enemy(Tools):
    alive = True

    def __init__(self, x, y, change, img, health, screen, player):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.change = change
        self.img = pygame.image.load(img)
        self.health = health
        self.screen = screen
        self.player = player

    def draw(self):
        self.text_display(str(self.health), 15, self.x + 32, self.y - 5, (0, 0, 0))
        self.screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.change
        if self.x >= 600:
            self.x = 600
            self.y += self.change

    def get_dmg(self, amount, special_effect):
        self.health -= amount
        if special_effect is not None:
            self.change -= 0.001
        if self.health <= 0:
            self.alive = False
            self.player.add_money(25)

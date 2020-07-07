import pygame
import math

from abc import abstractmethod


class Tower:
    width = 64
    height = 64

    def __init__(self, img, atack_range, x, y, dmg):
        self.level = 1
        self.img = pygame.image.load(img)
        self.atack_range = atack_range
        self.x = x
        self.y = y
        self.dmg = dmg

    @abstractmethod
    def atack_enemy(self):
        pass
    @abstractmethod
    def deal_dmg(self, enemy):
        pass

    def get_level(self):
        return self.level

    def draw(self, screen, enemies):
        enemy_in_range = None
        if enemies is not None:
            surface = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (0, 0, 0, 10), (self.x + 32, self.y + 32), self.atack_range)
            screen.blit(surface, (0, 0))
            for enemy in enemies:
                if math.sqrt(math.pow(self.x - enemy.x, 2) + math.pow(self.y - enemy.y, 2)) <= self.atack_range and enemy.alive:
                    enemy_in_range = enemy
                    break

        # shooting and pointing only first enemy in list
        if enemy_in_range is not None:
            self.point_on_enemy((enemy_in_range.x + 32, enemy_in_range.y + 32), screen)
            self.deal_dmg(enemy_in_range)
        else:
            screen.blit(self.img, (self.x, self.y))

    def rotate(self):
        self.img = pygame.transform.rotate(self.img, 180)

    def upgrade(self):
        self.atack_range += 50

    def point_on_enemy(self, pos, screen):
        angle = math.atan2(pos[1] - (self.y + 32), pos[0] - (self.x + 32))
        if self.y == 275:
            tower_rotation = pygame.transform.rotate(self.img, 270 - angle*57.29)
        else:
            tower_rotation = pygame.transform.rotate(self.img, 90 - angle * 57.29)
        tower_pos = (self.x - tower_rotation.get_rect().width/2 + 32,
                     self.y - tower_rotation.get_rect().height/2 + 32)
        screen.blit(tower_rotation, tower_pos)


class ShootingTower(Tower):

    def __init__(self, img, atack_range, x, y):
        super().__init__(img, atack_range, x, y, dmg=1)

    def atack_enemy(self):
        pass

    def deal_dmg(self, enemy):
        enemy.get_dmg(self.dmg, None)


class SlowingTower(Tower):
    def __init__(self, img, atack_range, x, y):
        super().__init__(img, atack_range, x, y, dmg=0)

    def atack_enemy(self):
        pass

    def deal_dmg(self, enemy):
        enemy.get_dmg(self.dmg, 1)


class ExtraDmg(Tower):
    def __init__(self, img, atack_range, x, y):
        super().__init__(img, atack_range, x, y, dmg=2)

    def atack_enemy(self):
        pass

    def deal_dmg(self, enemy):
        enemy.get_dmg(self.dmg, None)

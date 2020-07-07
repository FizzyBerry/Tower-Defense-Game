import pygame


class Earth:
    x = 560
    y = 380
    heart_x = 520
    heart_y = 560
    heart_diffrence = 40
    health = 5
    earthIMG = pygame.image.load('images/maps-and-flags.png')
    heartIMG = pygame.image.load('images/heart.png')

    def draw(self, screen):
        for i in range(0, self.health):
            screen.blit(self.heartIMG, (self.heart_x, self.heart_y - i*self.heart_diffrence))
        screen.blit(self.earthIMG, (self.x, self.y))

    def get_damage(self):
        self.health -= 1

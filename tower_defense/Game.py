import pygame
from .tools import Tools
from .earth import Earth
from .enemy import Enemy
from .Tower import Tower, ShootingTower, SlowingTower, ExtraDmg
from .Player import Player

from abc import abstractmethod


class Drawable:
    @abstractmethod
    def draw(self):
        ...


class Place(Drawable):
    def __init__(self, screen, x, y, occupied, rotated, game):
        self.x = x
        self.y = y
        self.screen = screen
        self.occupied = occupied
        self.rotated = rotated
        self.tower = None
        self.game = game

    def build_tower(self, tower: Tower):
        if self.occupied:
            return False
        self.occupied = True
        self.tower = tower
        if self.y == 150:
            self.tower.rotate()

    def draw(self):
        if self.tower is not None:
            if self.game.level < 3:
                self.tower.draw(self.screen, self.game.enemies[self.game.level])
            else:
                self.tower.draw(self.screen, None)


class BackgroundGraphics(Drawable):

    def __init__(self, screen, image_path: str, x, y):
        self.image_path = image_path
        self.x = x
        self.y = y
        self.screen = screen

    # drawing some background graphics
    def draw(self):
        self.screen.blit(pygame.image.load(self.image_path), (self.x, self.y))


class Path(Drawable, Tools):

    def __init__(self, screen, points, width, color=(30, 70, 130)):
        super().__init__(screen)
        self.points = points
        self.width = width
        self.color = color

    # drawing path to earth
    def draw(self):
        for prev_point, next_point in zip(self.points, self.points[1:]):
            if prev_point[0] == next_point[0]:
                # vertical line
                width = self.width
                height = next_point[1] - prev_point[1]
                self.draw_rect(prev_point[0] - self.width / 2, prev_point[1] - self.width / 2, width=width, height=height,
                               color=self.color)
            else:
                # horizontal line
                width = next_point[0] - prev_point[0]
                height = self.width
                self.draw_rect(prev_point[0] - self.width / 2, prev_point[1] - self.width / 2, width=width, height=height,
                               color=self.color)


class ShopItem:

    def __init__(self, cost: int, image: str, attack_range: int):
        self.cost = cost
        self.image_path = image
        self.image = pygame.image.load(image)
        self.attack_range = attack_range

    @abstractmethod
    def get_tower(self, x, y) -> Tower:
        ...


class ShootingTowerItem(ShopItem):

    def get_tower(self, x, y) -> Tower:
        return ShootingTower(self.image_path, self.attack_range, x, y)


class SlowingTowerItem(ShopItem):

    def get_tower(self, x, y) -> Tower:
        return SlowingTower(self.image_path, self.attack_range, x, y)


class ExtraDmgTowerItem(ShopItem):

    def get_tower(self, x, y) -> Tower:
        return ExtraDmg(self.image_path, self.attack_range, x, y)


class TowerShop(Drawable, Tools):

    def __init__(self, screen, shop_items, x, y, width, player: Player):
        super().__init__(screen)
        self.items = shop_items
        self.x = x
        self.y = y
        self.width = width
        self.spacing = 15
        self.player = player

    # drawing tower shop
    def draw(self):
        self.draw_rect(x=self.x, y=self.y, width=self.width, height=420, color=(30, 70, 130))
        self.text_display("MONEY:", font_size=13, width=self.x + self.width / 2, height=self.y + self.spacing,
                          color=(20, 20, 20))
        self.text_display(str(self.player.money), font_size=13, width=self.x + self.width / 2,
                          height=self.y + 2 * self.spacing, color=(20, 20, 20))
        self.draw_rect(x=self.x, y=self.y + 3 * self.spacing, width=self.width, height=2, color=(20, 20, 20))
        y_offset = self.y + 3 * self.spacing
        for item in self.items:
            self.text_display(str(item.cost), 13, self.x + self.width / 2, y_offset + self.spacing, color=(20, 20, 20))
            self.screen.blit(item.image, (self.x + 20, y_offset + 2 * self.spacing))
            y_offset += self.spacing * 3 + item.image.get_height()
            self.draw_rect(self.x, y_offset, self.width, 1, color=(20, 20, 20))


class Game(Tools):
    level = int  # level of the game

    def __init__(self, screen):
        super().__init__(screen)
        self.level = -1
        self.screen = screen
        self.player = Player()

        # (screen, x, y, occupied, rotated)
        self.places_for_spaceships = [Place(self.screen, 20, 275, False, False, self),
                                      Place(self.screen, 120, 275, False, False, self),
                                      Place(self.screen, 220, 275, False, False, self),
                                      Place(self.screen, 320, 275, False, False, self),
                                      Place(self.screen, 420, 275, False, False, self),
                                      Place(self.screen, 520, 275, False, False, self),
                                      Place(self.screen, 20, 150, False, False, self),
                                      Place(self.screen, 120, 150, False, False, self),
                                      Place(self.screen, 220, 150, False, False, self),
                                      Place(self.screen, 320, 150, False, False, self),
                                      Place(self.screen, 420, 150, False, False, self),
                                      Place(self.screen, 520, 150, False, False, self)]

        # list of enemies, on each level different group of enemies appear
        self.enemies = [[Enemy(-84, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-184, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-284, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-384, 214, 1, 'images/1.png', 100, self.screen, self.player)],
                        [Enemy(-84, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-184, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-284, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-384, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-484, 214, 1, 'images/2.png', 150, self.screen, self.player),
                         Enemy(-584, 214, 1, 'images/2.png', 150, self.screen, self.player)],
                        [Enemy(-84, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-184, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-284, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-384, 214, 1, 'images/1.png', 100, self.screen, self.player),
                         Enemy(-484, 214, 1, 'images/2.png', 150, self.screen, self.player),
                         Enemy(-584, 214, 1, 'images/2.png', 150, self.screen, self.player),
                         Enemy(-684, 214, 1, 'images/3.png', 300, self.screen, self.player)]]
        self.pressed = False
        self.paused = False
        self.allDied = False
        self.allAfterEarth = False

    def run(self):
        running = True
        moving_spaceships = [False, False, False]
        shop = TowerShop(self.screen,
                         [ShootingTowerItem(100, "images/4.png", 100), SlowingTowerItem(150, "images/5.png", 100),
                          ExtraDmgTowerItem(300, "images/6.png", 100)],
                         x=700, y=0, width=100, player=self.player)

        background_graphics = [
            BackgroundGraphics(self.screen, 'images/ursa-major (2).png', x=200, y=400),
            BackgroundGraphics(self.screen, 'images/star.png', x=100, y=70),
            BackgroundGraphics(self.screen, 'images/star (2).png', x=150, y=50),
            BackgroundGraphics(self.screen, 'images/star (1).png', x=400, y=530),
            BackgroundGraphics(self.screen, 'images/star (2).png', x=450, y=450),
            BackgroundGraphics(self.screen, 'images/star (2).png', x=150, y=460),
            BackgroundGraphics(self.screen, 'images/star.png', x=70, y=500),
        ]

        path = Path(self.screen, [(25, 245), (625, 245), (625, 520)], width=50)
        drawable_elements = [path, shop, *background_graphics, *self.places_for_spaceships]
        pause = pygame.image.load('images/pause.png')
        exit = pygame.image.load('images/exit.png')
        earth = Earth()

        # game loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((20, 60, 120))

            # displaying drawable elements
            for drawable in drawable_elements:
                drawable.draw()

            # displaying buttons
            if not self.pressed:
                self.button_function(200, 0, 250, 50, (0, 100, 120), (0, 130, 150), self.start_next_level)
            self.button_function(520, 0, 50, 50, (0, 100, 120), (0, 130, 150), self.quit)

            # displaying text and img on buttons
            self.text_display("Next Level", 28, 325, 25, (10, 10, 10))
            self.screen.blit(exit, (532, 10))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # checking if someone want to build spaceship
            if 720 + 64 > mouse[0] > 720 and 80 + 64 > mouse[1] > 80 and click[0] == 1 and self.player.money >= 100:
                moving_spaceships[0] = True
            if 720 + 64 > mouse[0] > 720 and 180 + 64 > mouse[1] > 180 and click[0] == 1 and self.player.money >= 150:
                moving_spaceships[1] = True
            if 720 + 64 > mouse[0] > 720 and 280 + 64 > mouse[1] > 280 and click[0] == 1 and self.player.money >= 300:
                moving_spaceships[2] = True

            # making spaceship follow the mouse and displaying placing boxes
            if moving_spaceships[0]:
                self.placing_spaceships('images/4.png', mouse)
            if moving_spaceships[1]:
                self.placing_spaceships('images/5.png', mouse)
            if moving_spaceships[2]:
                self.placing_spaceships('images/6.png', mouse)

            # building tower when they are placed in one of the placing boxes
            if click[0] == 0:
                for item_nr, item in enumerate(shop.items):
                    if moving_spaceships[item_nr]:
                        for place in self.places_for_spaceships:
                            if place.x + 64 > mouse[0] > place.x and place.y + 64 > mouse[1] > place.y:
                                if place.occupied:
                                    break
                                else:
                                    self.player.substract_money(item.cost)
                                    place.build_tower(item.get_tower(place.x, place.y))
                        moving_spaceships[item_nr] = False

            # displaying enemies based on level in game
            if self.pressed and self.level < 3:
                self.allDied = True
                self.allAfterEarth = True
                for i in self.enemies[self.level]:
                    if i.alive:
                        i.draw()
                        i.move()

                        self.allDied = False
                    if int(i.y) == 500:
                        earth.get_damage()
                    if i.y < 500 and i.alive:
                        self.allAfterEarth = False

                # if enemy is after earth or all of them died, active "next level" button
                if self.allAfterEarth or self.allDied:
                    self.pressed = False
            # you WON!
            elif self.pressed:
                self.text_display("You Won !", 40, 400, 250, (200, 70, 70))
                self.screen.blit(pygame.image.load('images/flowers (1).png'), (400, 300))

            # game over
            if earth.health <= 0:
                self.game_over()
                self.pressed = True

            earth.draw(self.screen)

            # pause button
            self.button_function(460, 0, 50, 50, (0, 100, 120), (0, 130, 150), self.pause)
            self.screen.blit(pause, (470, 10))
            pygame.display.update()

    def pause(self):
        self.paused = True
        pause = pygame.image.load('images/pause.png')
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.paused = False
            surface = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
            self.screen.blit(surface, (0, 0))
            self.text_display("Press 'c' to continue", 50, 400, 370, (20, 20, 20))
            self.screen.blit(pause, (470, 10))
            pygame.display.update()

    def quit(self):
        g = GameIntro(self.screen)
        g.game_intro()
        pygame.quit()
        quit()

    def start_next_level(self):
        self.pressed = True
        self.level += 1

    def save_score(self, nickname):
        pass

    def delete_tower(self) -> int:
        pass

    def placing_spaceships(self, img, mouse):
        for i in self.places_for_spaceships:
            if not i.occupied:
                self.draw_rect(i.x, i.y, 64, 64, (30, 70, 130))
        t = Tower(img, 100, mouse[0] - 32, mouse[1] - 32, 0)
        t.draw(self.screen, self.enemies[self.level])

    def game_over(self):
        self.text_display("Game Over !", 40, 400, 250, (200, 70, 70))


class ShowHelp(Tools):
    def show_help(self):
        running = True
        earth = Earth()
        while running:  # show help loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((20, 60, 120))

            # displaying earth and text to it
            earth.draw(self.screen)
            self.screen.blit(pygame.image.load('images/right.png'), (500, 500))
            self.text_display('this is earth, you need to protect it from aliens', 20, 260, 515, (0, 0, 0))

            # displaying enemies and text to them
            self.screen.blit(pygame.image.load('images/1.png'), (100, 100))
            self.screen.blit(pygame.image.load('images/2.png'), (100, 180))
            self.screen.blit(pygame.image.load('images/3.png'), (100, 260))
            self.text_display('these are aliens that you need to kill', 20, 200, 380, (0, 0, 0))
            arrow = pygame.image.load('images/right.png')
            arrow = pygame.transform.rotate(arrow, 90)
            self.screen.blit(arrow, (115, 330))

            # displaying spaceships and text to them
            self.screen.blit(pygame.image.load('images/4.png'), (700, 100))
            self.screen.blit(pygame.image.load('images/5.png'), (700, 180))
            self.screen.blit(pygame.image.load('images/6.png'), (700, 260))
            self.text_display('these are your spaceships', 20, 490, 170, (0, 0, 0))
            self.text_display('you are going to build them', 20, 490, 200, (0, 0, 0))
            self.text_display('to destroy the enemy.', 20, 490, 230, (0, 0, 0))
            self.text_display('Kind of spaceships from the top :', 20, 490, 260, (0, 0, 0))
            self.text_display('shooting, slowing, extra damage', 20, 490, 290, (0, 0, 0))
            self.screen.blit(pygame.image.load('images/right.png'), (650, 210))

            # button ' go back to the menu '
            self.button_function(250, 50, 250, 50, (0, 100, 120), (0, 130, 150), self.quit)
            self.text_display('Go back', 28, 375, 75, (170, 170, 170))
            pygame.display.update()

    def quit(self):
        g = GameIntro(self.screen)
        g.game_intro()
        pygame.quit()
        quit()


class GameIntro(Tools):
    running = False

    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen

    def game_intro(self):
        s = ShowHelp(self.screen)
        self.running = True
        while self.running:  # game intro loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((20, 60, 120))

            # displaying graphic objects
            self.screen.blit(pygame.image.load('images/ursa-major(5).png'), (300, 300))
            self.screen.blit(pygame.image.load('images/ursa-major(5).png'), (-150, -180))
            self.screen.blit(pygame.image.load('images/3.png'), (640, 150))
            spaceship = pygame.image.load('images/4.png')
            spaceship = pygame.transform.rotate(spaceship, 300)
            self.screen.blit(spaceship, (100, 430))

            # displaying welcome text
            self.text_display('Welcome to the game !', 50, 390, 100, (0, 0, 0))

            # displaying buttons and make them work
            self.button_function(275, 200, 250, 50, (0, 100, 120), (0, 130, 150), Menu.start_new_game)
            self.button_function(275, 280, 250, 50, (0, 100, 120), (0, 130, 150), Menu.show_score_board)
            self.button_function(275, 360, 250, 50, (0, 100, 120), (0, 130, 150), s.show_help)
            self.button_function(275, 440, 250, 50, (0, 100, 120), (0, 130, 150), Menu.quit)

            # displaying text on buttons
            self.text_display('New game', 28, 400, 225, (170, 170, 170))
            self.text_display('Scoreboard', 28, 400, 305, (170, 170, 170))
            self.text_display('Show help', 28, 400, 385, (170, 170, 170))
            self.text_display('Quit', 28, 400, 465, (170, 170, 170))

            pygame.display.update()


class Menu(Tools):
    @ staticmethod
    def start_new_game():
        screen = pygame.display.set_mode((800, 600))
        g = Game(screen)
        g.run()
        pygame.quit()
        quit()

    @ staticmethod
    def show_score_board():
        pass

    @ staticmethod
    def quit():
        pygame.quit()
        quit()

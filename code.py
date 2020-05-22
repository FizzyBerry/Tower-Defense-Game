import pygame

pygame.init()

class Tools:
    def text_objects(self, text, font, color):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def draw_rect(self, x, y, width, high, color):
        pygame.draw.rect(screen, color, [x, y, width, high])

    def text_display(self, text, font_size, width, high, color):
        display_text = pygame.font.Font('freesansbold.ttf', font_size)
        text_surface, text_rectangle = self.text_objects(text, display_text, color)
        text_rectangle.center = (width, high)
        screen.blit(text_surface, text_rectangle)

    def button_function(self, x, y, width, high, color_i, color_a, func):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + high > mouse[1] > y:
            self.draw_rect(x, y, width, high, color_a)
            if click[0] == 1:
                func()
        else:
            self.draw_rect(x, y, width, high, color_i)


class Menu(Tools):
    def game_intro(self):
        running = True
        while running:      # menu loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((20, 60, 120))

            # displaying graphic objects
            screen.blit(pygame.image.load('ursa-major(5).png'), (300, 300))
            screen.blit(pygame.image.load('ursa-major(5).png'), (-150, -180))
            screen.blit(pygame.image.load('3.png'), (640, 150))
            spaceship = pygame.image.load('4.png')
            spaceship = pygame.transform.rotate(spaceship, 300)
            screen.blit(spaceship, (100, 430))

            # displaying welcome text
            self.text_display('Welcome to the game !', 50, 390, 100, (0, 0, 0))

            # displaying buttons and make them work
            self.button_function(275, 200, 250, 50, (0, 100, 120), (0, 130, 150), self.start_new_game)
            self.button_function(275, 280, 250, 50, (0, 100, 120), (0, 130, 150), self.show_score_board)
            self.button_function(275, 360, 250, 50, (0, 100, 120), (0, 130, 150), self.show_help)
            self.button_function(275, 440, 250, 50, (0, 100, 120), (0, 130, 150), self.quit)

            # displaying text on buttons
            self.text_display('New game', 28, 400, 225, (170, 170, 170))
            self.text_display('Scoreboard', 28, 400, 305, (170, 170, 170))
            self.text_display('Show help', 28, 400, 385, (170, 170, 170))
            self.text_display('Quit', 28, 400, 465, (170, 170, 170))

            pygame.display.update()

    def start_new_game(self):
        G = Game()
        G.run()
        pygame.quit()
        quit()

    def show_help(self):
        running = True
        while running:  # show help loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((20, 60, 120))

            # displaying earth and text to it
            Earth()
            screen.blit(pygame.image.load('right.png'), (500, 500))
            self.text_display('this is earth, you need to protect it from aliens', 20, 260, 515, (0, 0, 0))

            # displaying enemies and text to them
            screen.blit(pygame.image.load('2.png'), (100, 100))
            screen.blit(pygame.image.load('1.png'), (100, 180))
            screen.blit(pygame.image.load('3.png'), (100, 260))
            self.text_display('these are aliens that you need to kill', 20, 200, 380, (0, 0, 0))
            arrow = pygame.image.load('right.png')
            arrow = pygame.transform.rotate(arrow, 90)
            screen.blit(arrow, (115, 330))

            # displaying spaceships and text to them
            screen.blit(pygame.image.load('4.png'), (700, 100))
            screen.blit(pygame.image.load('5.png'), (700, 180))
            screen.blit(pygame.image.load('6.png'), (700, 260))
            self.text_display('these are your spaceships', 20, 490, 170, (0, 0, 0))
            self.text_display('you are going to build them', 20, 490, 200, (0, 0, 0))
            self.text_display('to destroy the enemy.', 20, 490, 230, (0, 0, 0))
            self.text_display('Kind of spaceships from the top :', 20, 490, 260, (0, 0, 0))
            self.text_display('shooting, slowing, extra speed', 20, 490, 290, (0, 0, 0))
            screen.blit(pygame.image.load('right.png'), (650, 210))

            # button ' go back to the menu '
            self.button_function(250, 50, 250, 50, (0, 100, 120), (0, 130, 150), self.game_intro)
            self.text_display('Go back', 28, 375, 75, (170, 170, 170))
            pygame.display.update()

        pygame.quit()
        quit()

    def show_score_board(self):
        pass

    def quit(self):
        pygame.quit()
        quit()


class Scoreboard:
    def remove_score(self, nickname) -> bool:
        pass

    def go_back_to_menu(self):
        pass


class Enemy:
    X = int
    Y = int
    change = float
    path = []  # need to make path !!!

    def __init__(self, x, y, _change, img):
        self.X = x
        self.Y = y
        self.change = _change
        self.img = pygame.image.load(img)

    def draw(self):
        screen.blit(self.img, (self.X, self.Y))


class Player:
    money = int

    def __init__(self):
        self.money = 100

    def add_money(self):
        self.money += 100


class Game(Tools):
    level = int  # level of the game

    def __init__(self):
        self.level = 1

    def run(self):  # game loop
        running = True
        e = Enemy(0, 200, 0.1, '3.png')
        click1 = False
        shooting = Tower('4.png')
        slowing = Tower('5.png')
        extra_speed = Tower('6w  nm,.png')
        player = Player()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((20, 60, 120))

            # displaying some graphics
            screen.blit(pygame.image.load('ursa-major (2).png'), (200, 400))
            screen.blit(pygame.image.load('star.png'), (100, 70))
            screen.blit(pygame.image.load('star (2).png'), (150, 50))
            # screen.blit(pygame.image.load('sun (1).png'), (720, 60))
            screen.blit(pygame.image.load('star (1).png'), (400, 530))
            screen.blit(pygame.image.load('star (2).png'), (450, 450))
            screen.blit(pygame.image.load('star (2).png'), (150, 460))
            screen.blit(pygame.image.load('star.png'), (70, 500))

            # displaying path
            self.draw_rect(0, 220, 600, 50, (30, 70, 130))
            self.draw_rect(600, 220, 50, 300, (30, 70, 130))

            # displaying buttons
            self.button_function(200, 0, 250, 50, (0, 100, 120), (0, 130, 150), self.start_next_level)
            self.button_function(460, 0, 50, 50, (0, 100, 120), (0, 130, 150), player.add_money)
            self.button_function(520, 0, 50, 50, (0, 100, 120), (0, 130, 150), self.quit)

            # displaying text and img on buttons
            self.text_display("Next Level", 28, 325, 25, (10, 10, 10))
            screen.blit(pygame.image.load('pause.png'), (470, 10))
            screen.blit(pygame.image.load('exit.png'), (532, 10))

            # displaying right corner menu
            self.draw_rect(700, 0, 100, 420, (30, 70, 130))
            self.draw_rect(700, 50, 100, 2, (20, 20, 20))
            self.draw_rect(700, 150, 100, 1, (20, 20, 20))
            self.draw_rect(700, 250, 100, 1, (20, 20, 20))
            self.draw_rect(700, 350, 100, 1, (20, 20, 20))
            self.text_display("MONEY : ", 13, 750, 12, (20, 20, 20))
            self.text_display(str(player.money), 13, 750, 33, (20, 20, 20))
            self.text_display("100", 13, 750, 65, (20, 20, 20))
            self.text_display("150", 13, 750, 165, (20, 20, 20))
            self.text_display("300", 13, 750, 265, (20, 20, 20))
            screen.blit(pygame.image.load('4.png'), (720, 80))
            screen.blit(pygame.image.load('5.png'), (720, 180))
            screen.blit(pygame.image.load('6.png'), (720, 280))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if 720 + 64 > mouse[0] > 720 and 80 + 64 > mouse[1] > 80 and click[0] == 1:
                click1 = True
            if click1:
                t = Tower('4.png')
                t.draw(mouse[0], mouse[1])
            if click[0] == 0:
                click1 = False

            print(click1)
            Earth()
            e.draw()
            pygame.display.update()

    def pause(self):
        pass

    def quit(self):
        m = Menu()
        m.game_intro()

    def build_tower(self, tower, place) -> bool:
        pass

    def start_next_level(self):
        pass

    def save_score(self, nickname):
        pass

    def delete_tower(self) -> int:
        pass


class Tower:
    level = int   # tower level
    atack_speed = float
    dmg = int
    atack_range = int
    x = int
    y = int

    def __init__(self, img):
        self.level = 1
        self.img = img

    def atack_enemy(self):
        pass

    def upgrade(self):
        pass

    def get_level(self):
        return self.level

    def draw(self, x, y):
        screen.blit(pygame.image.load(self.img), (x, y))


class ShootingTower(Tower):
    pass


class SlowingTower(Tower):
    pass


class extra_speed(Tower):
    pass


class Earth:
    x = 560
    y = 380
    health = 1000
    earthIMG = pygame.image.load('maps-and-flags.png')

    def __init__(self):
        screen.blit(self.earthIMG, (self.x, self.y))


screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Tower Defense")
icon = pygame.image.load('maps-and-flags.png')
pygame.display.set_icon(icon)


M = Menu()
M.game_intro()

# E.set_x(E.get_x() + E.get_change())  # example of animation
# if E.get_x() >= 600:
#     E.set_x(600)
#     E.set_y(E.get_change() + E.get_y())
#     if E.get_y() >= 400:
#         E.set_y(400)

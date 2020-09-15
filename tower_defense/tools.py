import pygame


class Tools:
    def __init__(self, screen):
        self.screen = screen

    def text_objects(self, text, font, color):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def draw_rect(self, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, [x, y, width, height])

    def text_display(self, text, font_size, width, height, color):
        display_text = pygame.font.Font('freesansbold.ttf', font_size)
        text_surface, text_rectangle = self.text_objects(text, display_text, color)
        text_rectangle.center = (width, height)
        self.screen.blit(text_surface, text_rectangle)

    def button_function(self, x, y, width, height, color_i, color_a, func):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            self.draw_rect(x, y, width, height, color_a)
            if click[0] == 1:
                func()
        else:
            self.draw_rect(x, y, width, height, color_i)


import pygame

class TextObject:
    def __init__(self, x, y, width, height, font_size=36, colour=(0, 255, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.colour = colour
        self.text = ""
    
    def set_text(self, new_text):
        self.text = new_text
    
    def display_text(self, screen):
        screen.fill((0, 0, 0), rect=self.rect)
        text_surface = self.font.render(self.text, True, self.colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
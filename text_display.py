"""
Module for the TextDisplay class.
"""
import pygame

class TextDisplay:
    """
    Class representing a text display area in pygame.
    """
    def __init__(self, x: int, y: int, width: int, height: int, font_size: int = 36, colour: tuple = (0, 255, 0)) -> None:
        """
        Initializes the TextDisplay object.
        
        Args:
        - x (int): The x-coordinate of the text display area.
        - y (int): The y-coordinate of the text display area.
        - width (int): The width of the text display area.
        - height (int): The height of the text display area.
        - font_size (int, optional): The font size of the text. Defaults to 36.
        - colour (tuple, optional): The colour of the text. Defaults to green.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.colour = colour
        self.text = ""

    def set_text(self, new_text: str) -> None:
        """
        Sets the text to be displayed.
        
        Args:
        - new_text (str): The new text to display.
        """
        self.text = new_text

    def display_text(self, screen: pygame.Surface) -> None:
        """
        Displays the text on the given screen.
        
        Args:
        - screen (pygame.Surface): The screen on which to display the text.
        """
        screen.fill((0, 0, 0), rect=self.rect)
        text_surface = self.font.render(self.text, True, self.colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

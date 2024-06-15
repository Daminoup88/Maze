"""
Module for the Character class.
"""
import pygame

class Character:
    """
    Class representing a character in the maze.
    """
    def __init__(self, x: int, y: int, colour: tuple = (0, 0, 255)) -> None:
        """
        Initializes the Character object.
        
        Args:
        - x (int): The x-coordinate of the character's starting position.
        - y (int): The y-coordinate of the character's starting position.
        - colour (tuple, optional): The colour of the character. Defaults to blue.
        """
        self.x = x
        self.y = y
        self.colour = colour

    def set_colour(self, colour: tuple) -> None:
        """
        Sets the colour of the character.
        
        Args:
        - colour (tuple): The new colour of the character.
        """
        self.colour = colour

    def move(self, distance_map: list[list[int]]) -> None:
        """
        Moves the character based on the given distance map.
        The character will move to the adjacent cell with the lowest distance value to reach the end of the maze.
        
        Args:
        - distance_map (list[list[int]]): The distance map used to determine movement: each cell contains the distance to the end of the maze.
        """
        minimum = 1000
        move = (0, 0)
        if distance_map[self.x + 1][self.y] < minimum:
            minimum = distance_map[self.x + 1][self.y]
            move = (1, 0)
        if distance_map[self.x - 1][self.y] < minimum:
            minimum = distance_map[self.x - 1][self.y]
            move = (-1, 0)
        if distance_map[self.x][self.y + 1] < minimum:
            minimum = distance_map[self.x][self.y + 1]
            move = (0, 1)
        if distance_map[self.x][self.y - 1] < minimum:
            minimum = distance_map[self.x][self.y - 1]
            move = (0, -1)
        self.x += move[0]
        self.y += move[1]

    def display_character(self, screen: pygame.Surface, cell_size: int) -> None:
        """
        Displays the character on the given screen.
        
        Args:
        - screen (pygame.Surface): The screen on which to display the character.
        - cell_size (int): The size in pixels of each cell in the maze.
        """
        pygame.draw.circle(screen, self.colour,
                           (self.y * cell_size + cell_size // 2,
                            self.x * cell_size + cell_size // 2),
                           cell_size // 2)

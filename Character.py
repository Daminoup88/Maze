import pygame

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, distanceMap):
        min = 1000
        move = (0, 0)
        if distanceMap[self.x + 1][self.y] < min:
            min = distanceMap[self.x + 1][self.y]
            move = (1, 0)
        if distanceMap[self.x - 1][self.y] < min:
            min = distanceMap[self.x - 1][self.y]
            move = (-1, 0)
        if distanceMap[self.x][self.y + 1] < min:
            min = distanceMap[self.x][self.y + 1]
            move = (0, 1)
        if distanceMap[self.x][self.y - 1] < min:
            min = distanceMap[self.x][self.y - 1]
            move = (0, -1)
        self.x += move[0]
        self.y += move[1]

    def display_character(self, screen, cell_size):
        pygame.draw.circle(screen, (0, 0, 255), (self.y * cell_size + cell_size // 2, self.x * cell_size + cell_size // 2), cell_size // 2)
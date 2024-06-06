import random
import pygame

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def __str__(self):
        return str(self.start) + " -> " + str(self.end)
    
    def __repr__(self):
        return self.__str__()

class Maze:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.start = (0, 0)
        self.end = (n - 1, m - 1)
        self.edges = []
        self.maze_array = []
        self.generate_maze()
        self.transform_maze_to_array()
        self.distanceMap = self.init_distance_map()

    def init_distance_map(self):
        distanceMap = [[1000 for _ in range(len(self.maze_array))] for _ in range(len(self.maze_array[0]))]
        for i in range(self.n * 2 + 1):
            for j in range(self.m * 2 + 1):
                if self.maze_array[i][j] == 0:
                    distanceMap[i][j] = 100
        distanceMap[self.end[0]*2+1][self.end[1]*2+1] = 0
        return distanceMap
    
    def balayage(self):
        hasChanged = False
        for x in range(self.n * 2 + 1):
            for y in range(self.m * 2 + 1):
                if (self.distanceMap[x][y] != 1000 and self.distanceMap[x][y] != 0):

                    # determine le minimum des cases voisines
                    minCase = 1000
                    if (self.distanceMap[x-1][y] < minCase): minCase = self.distanceMap[x-1][y]
                    if (self.distanceMap[x+1][y] < minCase): minCase = self.distanceMap[x+1][y]
                    if (self.distanceMap[x][y-1] < minCase): minCase = self.distanceMap[x][y-1]
                    if (self.distanceMap[x][y+1] < minCase): minCase = self.distanceMap[x][y+1]

                    # si c'est la même ne pas changer
                    if (minCase + 1 != self.distanceMap[x][y] and minCase + 1 < 1000):
                        self.distanceMap[x][y] = minCase + 1
                        hasChanged = True
        
        if(hasChanged):
            self.balayage()

    def generate_maze(self):
        edgeArray = []
        sommets = [0 for _ in range(self.n * self.m)]
        sommets[self.start[0]] = 1
        border = []
        sommet = self.start[0]

        def get_neighbors(cell):
            x, y = divmod(cell, self.m)
            voisins = []
            if x > 0:  # North
                voisins.append(Edge(cell, cell - self.m))
            if x < self.n - 1:  # South
                voisins.append(Edge(cell, cell + self.m))
            if y > 0:  # West
                voisins.append(Edge(cell, cell - 1))
            if y < self.m - 1:  # East
                voisins.append(Edge(cell, cell + 1))
            return voisins

        while sommet >= 0:
            for neighbor in get_neighbors(sommet):
                if sommets[neighbor.end] == 0:
                    border.append(neighbor)

            sommet = -1

            while len(border) > 0:
                i = random.randint(0, len(border) - 1)
                edge = border[i]
                if sommets[edge.end] == 0:
                    edgeArray.append(edge)
                    sommets[edge.end] = 1
                    sommet = edge.end
                    break
                border.pop(i)
        self.edges = edgeArray

    def transform_maze_to_array(self):
        array = [[1 for _ in range(self.m * 2 + 1)] for _ in range(self.n * 2 + 1)]
        for i in range(self.n):
            for j in range(self.m):
                array[i * 2 + 1][j * 2 + 1] = 0
        for edge in self.edges:
            x1 = edge.start // self.m
            y1 = edge.start % self.m
            x2 = edge.end // self.m
            y2 = edge.end % self.m
            if x1 == x2:
                array[x1 * 2 + 1][(y1 + y2) + 1] = 0
            else:
                array[(x1 + x2) + 1][y1 * 2 + 1] = 0
        self.maze_array = array

    def display_maze(self, screen, cell_size=10, debug_array=[]):
        for y in range(len(self.maze_array)):
            for x in range(len(self.maze_array[y])):
                if self.maze_array[y][x] == 1:
                    color = (0, 0, 0)
                elif self.maze_array[y][x] == 2:
                    color = (0, 0, 255)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

        pygame.draw.rect(screen, (0, 255, 0), (cell_size, cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, (255, 0, 0), (screen.get_width() - 2 * cell_size, screen.get_height() - 2 * cell_size, cell_size, cell_size))

        if len(debug_array) == len(self.maze_array):
            font_size = cell_size // 2
            font = pygame.font.Font(None, font_size)
            for y in range(len(debug_array)):
                for x in range(len(debug_array[y])):
                    if debug_array[y][x] != -1:
                        text = font.render(str(debug_array[y][x]), True, (0, 0, 255))
                        text_rect = text.get_rect(center=((x * cell_size) + cell_size // 2, (y * cell_size) + cell_size // 2))
                        screen.blit(text, text_rect)

    def __str__(self):
        return "Maze of size " + str(self.n) + "x" + str(self.m)
    
    def __repr__(self):
        return self.__str__()
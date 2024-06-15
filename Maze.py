"""
Module containing the Maze class and Edge class for generating and displaying mazes.
"""
import random
import time
import pygame

class Edge:
    """
    Class representing an edge between two cells in the maze.
    """
    def __init__(self, start: int, end: int) -> None:
        """
        Initializes an Edge object representing a connection between two cells.
        
        Args:
        - start (int): The starting cell of the edge.
        - end (int): The ending cell of the edge.
        """
        self.start = start
        self.end = end

    def __str__(self):
        return str(self.start) + " -> " + str(self.end)

    def __repr__(self):
        return self.__str__()

class Maze:
    """
    Class representing a maze generated using Prim's algorithm.
    """
    def __init__(self, n: int, m: int) -> None:
        """
        Initializes the Maze object.
        Generates a new maze, transforms it into a 2D array, and computes the distance map.
        
        Args:
        - n (int): The number of rows in the maze.
        - m (int): The number of columns in the maze.
        """
        self.n = n
        self.m = m
        self.start = (0, 0)
        self.end = (n - 1, m - 1)
        self.edges = []
        self.maze_array = []
        self.generate_maze()
        self.transform_maze_to_array()
        self.distance_map = self.init_distance_map()
        self.balayage()

    def init_distance_map(self) -> list[list[int]]:
        """
        Initializes the distance map for the maze: end cell is 0, path cells are 100, wall cells are 1000.
        
        Returns:
        - list[list[int]]: The initialized distance map.
        """
        distance_map = [[1000 for _ in range(len(self.maze_array))] for _ in range(len(self.maze_array[0]))]
        for i in range(self.n * 2 + 1):
            for j in range(self.m * 2 + 1):
                if self.maze_array[i][j] == 0:
                    distance_map[i][j] = 100
        distance_map[self.end[0]*2+1][self.end[1]*2+1] = 0
        return distance_map

    def balayage(self) -> None:
        """
        Performs the sweep algorithm to compute distances in the distance map.
        Computes the distance from the end cell to all other cells in the maze.
        Only updates cells with a distance value of 100 (path cells).
        """
        has_changed = False
        for x in range(self.n * 2 + 1):
            for y in range(self.m * 2 + 1):
                if (self.distance_map[x][y] != 1000 and self.distance_map[x][y] != 0):

                    min_case = 1000
                    if self.distance_map[x-1][y] < min_case:
                        min_case = self.distance_map[x-1][y]
                    if self.distance_map[x+1][y] < min_case:
                        min_case = self.distance_map[x+1][y]
                    if self.distance_map[x][y-1] < min_case:
                        min_case = self.distance_map[x][y-1]
                    if self.distance_map[x][y+1] < min_case:
                        min_case = self.distance_map[x][y+1]

                    if (min_case + 1 != self.distance_map[x][y] and min_case + 1 < 1000):
                        self.distance_map[x][y] = min_case + 1
                        has_changed = True

        if has_changed:
            self.balayage()

    def generate_maze(self) -> None:
        """
        Generates a new maze using Prim's algorithm.
        At each step, expands the maze by adding a border cell of the current maze to the maze.
        """
        edge_array = []
        sommets = [0 for _ in range(self.n * self.m)]
        sommets[self.start[0]] = 1
        border = []
        sommet = self.start[0]

        def get_neighbours(cell: int) -> list[Edge]:
            """
            Returns the neighbours of the given cell.
            """
            x, y = divmod(cell, self.m)
            neighbours = []
            if x > 0:  # North
                neighbours.append(Edge(cell, cell - self.m))
            if x < self.n - 1:  # South
                neighbours.append(Edge(cell, cell + self.m))
            if y > 0:  # West
                neighbours.append(Edge(cell, cell - 1))
            if y < self.m - 1:  # East
                neighbours.append(Edge(cell, cell + 1))
            return neighbours

        while sommet >= 0:
            for neighbour in get_neighbours(sommet):
                if sommets[neighbour.end] == 0:
                    border.append(neighbour)

            sommet = -1

            while len(border) > 0:
                i = random.randint(0, len(border) - 1)
                edge = border[i]
                if sommets[edge.end] == 0:
                    edge_array.append(edge)
                    sommets[edge.end] = 1
                    sommet = edge.end
                    break
                border.pop(i)
        self.edges = edge_array

    def transform_maze_to_array(self) -> None:
        """
        Transforms the maze into a 2D array representation.
        Walls are represented by 1, paths by 0.
        """
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

    def display_maze(self, screen: pygame.Surface, cell_size: int = 10, debug: bool = False) -> None:
        """
        Displays the maze on the given screen.
        
        Args:
        - screen (pygame.Surface): The screen on which to display the maze.
        - cell_size (int, optional): The size of each cell in the maze. Defaults to 10.
        - debug (bool, optional): Whether to display the distance map. Defaults to False.
        """
        wall_colour = (0, 0, 0)
        path_colour = (255, 255, 255)
        for y in range(self.n * 2 + 1):
            for x in range(self.m * 2 + 1):
                if self.maze_array[y][x] == 1:
                    colour = wall_colour
                else:
                    colour = path_colour
                pygame.draw.rect(screen, colour, (x * cell_size, y * cell_size, cell_size, cell_size))
                if x == 1 and y == 1:
                    pygame.draw.rect(screen, (0, 255, 0), (x * cell_size, y * cell_size, cell_size, cell_size))
                elif x == self.m * 2 - 1 and y == self.n * 2 - 1:
                    pygame.draw.rect(screen, (255, 0, 0), (x * cell_size, y * cell_size, cell_size, cell_size))
        if debug:
            font_size = cell_size // 2
            font = pygame.font.Font(None, font_size)
            for y in range(self.n * 2 + 1):
                for x in range(self.m * 2 + 1):
                    if self.distance_map[y][x] != -1:
                        text = font.render(str(self.distance_map[y][x]), True, (0, 0, 255))
                        text_rect = text.get_rect(center=((x * cell_size) + cell_size // 2, (y * cell_size) + cell_size // 2))
                        screen.blit(text, text_rect)

    def regenerate_maze(self, character_x: int, character_y: int) -> None:
        """
        Regenerates the maze, the 2D array, and the distance map.
        If the character is in a wall cell, the cell is set to a path cell (can create a loop in the maze).
        Displays computation times for each step.
        
        Args:
        - character_x (int): The x-coordinate of the character's position.
        - character_y (int): The y-coordinate of the character's position.
        """
        self.edges = []
        t = time.time()
        self.generate_maze()
        print("Maze generation time:", time.time() - t)
        t = time.time()
        self.transform_maze_to_array()
        print("Maze transformation time:", time.time() - t)
        self.maze_array[character_x][character_y] = 0
        t = time.time()
        self.distance_map = self.init_distance_map()
        print("Distance map initialization time:", time.time() - t)
        t = time.time()
        self.balayage()
        print("Sweep time:", time.time() - t)

    def __str__(self):
        return "Maze of size " + str(self.n) + "x" + str(self.m)

    def __repr__(self):
        return self.__str__()

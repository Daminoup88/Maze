import pygame
import time
from Maze import Maze
from Character import Character

# Main
if __name__ == "__main__":
    n = 15  # Dimension of the maze
    cell_size = 20
    
    start_time = time.time()
    maze = Maze(n, n)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    start_time = time.time()
    maze.balayage()
    print("--- %s seconds ---" % (time.time() - start_time))
    character = Character(1, 1)

    pygame.init()
    width = len(maze.maze_array[0]) * cell_size
    height = len(maze.maze_array) * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Generator")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        if(character.x == n*2-1 and character.y == n*2-1):
            print("You won!")
            running = False
        maze.display_maze(screen, cell_size, maze.distanceMap)
        character.display_character(screen, cell_size)
        character.move(maze.distanceMap)
        time.sleep(0.1)

        pygame.display.flip()
    pygame.quit()
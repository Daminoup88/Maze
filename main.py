import pygame
import time
from Maze import Maze
from Character import Character

N = 15
CELL_SIZE = 25
MAZE = Maze(N, N)
CHARACTER = Character(1, 1)

PAUSE_FLAG = False
WON_FLAG = False
LOST_FLAG = False

# Create screen (the added height is for the information bar)
def CreateScreen(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height + 100))
    pygame.display.set_caption("Maze")
    return screen

SCREEN = CreateScreen(len(MAZE.maze_array[0]) * CELL_SIZE, len(MAZE.maze_array) * CELL_SIZE)

def handle_keydown(event):
    global PAUSE_FLAG, WON_FLAG, LOST_FLAG
    if event.key == pygame.K_p:
        PAUSE_FLAG = not PAUSE_FLAG
    elif event.key == pygame.K_r and not (WON_FLAG or LOST_FLAG or PAUSE_FLAG):
        MAZE.regenerate_maze(CHARACTER.x, CHARACTER.y)
        WON_FLAG = False
        LOST_FLAG = False

def check_win():
    global WON_FLAG
    if(CHARACTER.x == N*2-1 and CHARACTER.y == N*2-1):
        WON_FLAG = True

def play_one_turn():
    if not PAUSE_FLAG and not WON_FLAG and not LOST_FLAG:
        SCREEN.fill((0, 0, 0), rect=(0, 0, (N*2+1) * CELL_SIZE, (N*2+1) * CELL_SIZE))
        MAZE.display_maze(SCREEN, CELL_SIZE, MAZE.distanceMap)
        CHARACTER.move(MAZE.distanceMap)
        CHARACTER.display_character(SCREEN, CELL_SIZE)
        check_win()
        display("Press R to regenerate the maze, P to pause")
    elif WON_FLAG:
        display("You won!")
    elif LOST_FLAG:
        display("You lost!")
    elif PAUSE_FLAG:
        display("Paused")

def display(text):
    SCREEN.fill((0, 0, 0), rect=(0, (N*2+1) * CELL_SIZE, (N*2+1) * CELL_SIZE, 100))
    font = pygame.font.Font(None, 36)
    text = font.render(text, True, (0, 255, 0))
    text_rect = text.get_rect(center=(SCREEN.get_width() // 2, (N*2+1) * CELL_SIZE + 50))
    SCREEN.blit(text, text_rect)

# Main
if __name__ == "__main__":
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event)
        
        t = int(pygame.time.get_ticks())
        fps = 1
        if t % (1000 // fps) == 0:
            play_one_turn()
        
        pygame.display.flip()
    pygame.quit()
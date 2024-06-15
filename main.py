"""
Pygame maze game :
- Generates a maze using Prim's algorithm
- Moves the character to the end of the maze using a distance map
- P pauses the game
- R regenerates the maze
- The game ends when the character reaches the end of the maze
"""

import sys
import pygame
from maze import Maze
from character import Character
from text_display import TextDisplay

N = 15
FPS = 10
if len(sys.argv) == 3:
    N = int(sys.argv[1])
    FPS = int(sys.argv[2])
CELL_SIZE = 200//N*2
MAZE = Maze(N, N)
CHARACTER = Character(1, 1)

PAUSE_FLAG = False
WON_FLAG = False
LOST_FLAG = False

def create_screen(width: int, height: int) -> pygame.Surface:
    """
    Initializes a pygame screen with the specified width and height.
    
    Args:
    - width (int): The width of the screen.
    - height (int): The height of the screen.

    Returns:
    - pygame.Surface: The initialized screen surface.
    """
    pygame.init()
    screen = pygame.display.set_mode((width, height + 100))
    pygame.display.set_caption("Maze")
    return screen

SCREEN = create_screen(len(MAZE.maze_array[0]) * CELL_SIZE, len(MAZE.maze_array) * CELL_SIZE)

TEXT_DISPLAY = TextDisplay(0, (N*2+1) * CELL_SIZE, (N*2+1) * CELL_SIZE, 100)

def handle_keydown(e: pygame.event.Event) -> None:
    """
    Handles keydown events for pausing and regenerating the maze.
    
    Args:
    - e (pygame.event.Event): The keydown event.
    """
    global PAUSE_FLAG, WON_FLAG, LOST_FLAG
    if e.key == pygame.K_p:
        PAUSE_FLAG = not PAUSE_FLAG
    elif e.key == pygame.K_r and not (WON_FLAG or LOST_FLAG or PAUSE_FLAG):
        TEXT_DISPLAY.set_text("Regenerating the maze...")
        TEXT_DISPLAY.display_text(SCREEN)
        pygame.display.flip()
        MAZE.regenerate_maze(CHARACTER.x, CHARACTER.y)
        WON_FLAG = False
        LOST_FLAG = False
        TEXT_DISPLAY.set_text("Press R to regenerate the maze, P to pause")
        TEXT_DISPLAY.display_text(SCREEN)

def check_win() -> None:
    """
    Checks if the character has reached the end of the maze and sets the WON_FLAG.
    """
    global WON_FLAG
    if(CHARACTER.x == N*2-1 and CHARACTER.y == N*2-1):
        WON_FLAG = True

def play_one_turn() -> None:
    """
    Executes one turn of the game, updating the screen and checking game flags.
    """
    if not PAUSE_FLAG and not WON_FLAG and not LOST_FLAG:
        SCREEN.fill((0, 0, 0), rect=(0, 0, (N*2+1) * CELL_SIZE, (N*2+1) * CELL_SIZE))
        MAZE.display_maze(SCREEN, CELL_SIZE, True)
        CHARACTER.move(MAZE.distance_map)
        CHARACTER.display_character(SCREEN, CELL_SIZE)
        check_win()
        TEXT_DISPLAY.set_text("Press R to regenerate the maze, P to pause")
    elif WON_FLAG:
        TEXT_DISPLAY.set_text("You won!")
    elif LOST_FLAG:
        TEXT_DISPLAY.set_text("You lost!")
    elif PAUSE_FLAG:
        TEXT_DISPLAY.set_text("Paused")

    TEXT_DISPLAY.display_text(SCREEN)

RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event)

    t = int(pygame.time.get_ticks())
    if t % (1000 // FPS) == 0:
        play_one_turn()

    pygame.display.flip()
pygame.quit()

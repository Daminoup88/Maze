import pygame
from Maze import Maze
from Character import Character
from TextObject import TextObject

N = 45
CELL_SIZE = 10
MAZE = Maze(N, N)
CHARACTER = Character(1, 1)

PAUSE_FLAG = False
WON_FLAG = False
LOST_FLAG = False

# Create screen (the added height is for the information bar)
def create_screen(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height + 100))
    pygame.display.set_caption("Maze")
    return screen

SCREEN = create_screen(len(MAZE.maze_array[0]) * CELL_SIZE, len(MAZE.maze_array) * CELL_SIZE)

TEXT_DISPLAY = TextObject(0, (N*2+1) * CELL_SIZE, (N*2+1) * CELL_SIZE, 100)

def handle_keydown(e):
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

def check_win():
    global WON_FLAG
    if(CHARACTER.x == N*2-1 and CHARACTER.y == N*2-1):
        WON_FLAG = True

def play_one_turn():
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
        fps = 30
        if t % (1000 // fps) == 0:
            play_one_turn()

        pygame.display.flip()
    pygame.quit()

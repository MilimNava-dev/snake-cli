import curses
from curses import wrapper
from random import randint
import time

score = 0

def draw_game(screen, game_win, SNAKE_COLOR, BACKGROUND, APPLE):
    for row in range(len(screen)):
        for col in range(len(screen[row])):
            char = screen[row][col]
            if char == "+" or char == "-":
                game_win.addstr(row, col, char, SNAKE_COLOR)
            elif char == "x":
                game_win.addstr(row, col, char, APPLE)
            else:
                game_win.addstr(row, col, " ", BACKGROUND)


def game_next_step(screen, pos):
    rows = len(screen)
    cols = len(screen[0])

    new_screen = [row[:] for row in screen]

    head = [-1, -1]
    tail = [-1, -1]

    for row in range(rows):
        for col in range(cols):

            neighbors = 0

            if screen[row][col] == "+":
                head = [row, col]

            elif screen[row][col] == "-":

                directions = [
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1)
                ]

                for dy, dx in directions:
                    new_row = row + dy
                    new_col = col + dx

                    if 0 <= new_row < rows and 0 <= new_col < cols:
                        if screen[new_row][new_col] in ["-", "+"]:
                            neighbors += 1

                if neighbors == 1:
                    tail = [row, col]

    new_head_row = head[0] + pos[0]
    new_head_col = head[1] + pos[1]

    # COLISIÓN CON PAREDES
    if not (0 <= new_head_row < rows and 0 <= new_head_col < cols):
        return screen, True

    # COLISIÓN CON EL CUERPO
    if new_screen[new_head_row][new_head_col] == "-":
        return screen, True

    new_screen[head[0]][head[1]] = "-"

    if new_screen[new_head_row][new_head_col] == "x":
        new_screen = place_apple(new_screen)
        global score
        score += 1
    else:
        new_screen[tail[0]][tail[1]] = " "

    new_screen[new_head_row][new_head_col] = "+"

    return new_screen, False


def place_apple(screen):
    h, w = len(screen), len(screen[0])
    row, col = randint(0, h - 1), randint(0, w - 1)

    new_screen = [row[:] for row in screen]

    while new_screen[row][col] in ["+", "-", "x"]:
        row, col = randint(0, h - 1), randint(0, w - 1)

    new_screen[row][col] = "x"

    return new_screen



def main(stdcr):
    curses.start_color()
    stdcr.clear()

    # COLORS
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_BLUE, curses.COLOR_BLACK)
    SNAKE_COLOR = curses.color_pair(1)
    BACKGROUND = curses.color_pair(2)
    APPLE = curses.color_pair(3)

    WHITE_TEXT = curses.color_pair(4)
    GREEN_TEXT = curses.color_pair(6)
    RED_TEXT = curses.color_pair(7)
    CYAN_TEXT = curses.color_pair(8)
    BLUE_TEXT = curses.color_pair(9)

    # TERMINAL SIZE
    max_rows, max_cols = stdcr.getmaxyx()

    # create border
    stdcr.box()

    # WINDOWS
    game_win_h, game_win_w = max_rows - 2, max_cols - 2
    game_win = curses.newwin(game_win_h, game_win_w, 1, 1)
    stdcr.nodelay(True)

    # SCREEN
    s_rows, s_cols = game_win_h, game_win_w - 1
    screen = [[" " for j in range(s_cols)] for i in range(s_rows)]
    # create snake
    screen[10][10] = "+"
    screen[10][9] = "-"
    # create apple
    screen = place_apple(screen)

    # GAME LOOP
    # user input
    direction = [1, 0]
    game_over = False
    last_update = time.time()
    fps = 10
    while True:
        try:
            key = stdcr.getkey()
        except:
            key = None

        if not game_over:
            if key == "KEY_LEFT" or key == "h":
                if direction != [0, 1]:
                    direction = [0, -1]

            elif key == "KEY_RIGHT" or key == "l":
                if direction != [0, -1]:
                    direction = [0, 1]

            elif key == "KEY_UP" or key == "k":
                if direction != [1, 0]:
                    direction = [-1, 0]

            elif key == "KEY_DOWN" or key == "j":
                if direction != [-1, 0]:
                    direction = [1, 0]
        else:
            break
        if key == "\x1b":
            break

        # UPDATE SIMULATION
        current_time = time.time()

        if not game_over and current_time - last_update >= 1 / fps:
            screen, game_over = game_next_step(screen, direction)
            last_update = current_time

        game_win.clear()

        draw_game(screen, game_win, SNAKE_COLOR, BACKGROUND, APPLE)

        stdcr.refresh()
        game_win.refresh()


wrapper(main)
print("Your score is:", score)

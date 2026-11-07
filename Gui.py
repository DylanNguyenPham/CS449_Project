
import pygame
import random
from Classes import Button, Dropdown

pygame.init()

# Window settings
BG_WIDTH = 800
BG_HEIGHT = 600

# State variables
current_bg_color = (245, 245, 245)
current_text_color = (30, 30, 30)
current_peg_color = (30, 130, 230)

DOT_RADIUS = 18
DOT_SPACING = 50
DOT_COLOR_HOLE = (200, 200, 200)

# Automated game settings
AUTO_MOVE_INTERVAL = 350
auto_play_active = False
last_auto_move_time = 0

font_title = pygame.font.SysFont(None, 48)
font_label = pygame.font.SysFont(None, 28)
font_button = pygame.font.SysFont(None, 20)

# Game State
selected_peg = None
game_status_message = "Active Game"
show_reset_confirm = False
game_mode = "Manual"


# Function to dynamically build board matrices
def generate_board(size_str, board_type):
    size = int(size_str.split('x')[0])
    board = [[0 for _ in range(size)] for _ in range(size)]
    center = size // 2
    cutout = 1 if size == 5 else (2 if size == 7 else 3)

    for r in range(size):
        for c in range(size):

            if board_type == "English":
                if not (
                    (r < cutout or r >= size - cutout)
                    and (c < cutout or c >= size - cutout)
                ):
                    board[r][c] = 1

            elif board_type == "Diamond":
                if abs(r - center) + abs(c - center) <= center:
                    board[r][c] = 1

            elif board_type == "Hexagon":
                if abs(r - center) + abs(c - center) <= center + (cutout // 2):
                    board[r][c] = 1

    # Place center empty hole
    board[center][center] = 2

    return board


# UI Position Specs
_menu_w, _menu_h = 170, 32
_menu_x = BG_WIDTH - _menu_w - 30


# Dropdown Menus
size_dd = Dropdown(
    _menu_x, 150, _menu_w, _menu_h,
    "Board Size", ["7x7", "5x5", "9x9"], font_button
)

type_dd = Dropdown(
    _menu_x, 200, _menu_w, _menu_h,
    "Board Type", ["English", "Diamond", "Hexagon"], font_button
)

bg_dd = Dropdown(
    _menu_x, 250, _menu_w, _menu_h,
    "Background", ["Light Gray", "Red", "Blue", "Black"], font_button
)

peg_dd = Dropdown(
    _menu_x, 300, _menu_w, _menu_h,
    "Peg Color", ["Blue", "Green", "Gold", "Red"], font_button
)

dropdowns = [size_dd, type_dd, bg_dd, peg_dd]


# Initial Board State
board_layout = generate_board(
    size_dd.get_selected(),
    type_dd.get_selected()
)


# Action Buttons
new_game_btn = Button(
    _menu_x, 90, _menu_w, _menu_h,
    "New Game", font_button,
    (30, 30, 30), (230, 230, 230), (190, 190, 190)
)

randomize_btn = Button(
    _menu_x, 350, _menu_w, _menu_h,
    "Randomize", font_button,
    (30, 30, 30), (230, 230, 230), (190, 190, 190)
)

auto_play_btn = Button(
    _menu_x, 390, _menu_w, _menu_h,
    "Auto Play", font_button,
    (255, 255, 255), (40, 150, 80), (60, 190, 100)
)

stop_auto_btn = Button(
    _menu_x, 430, _menu_w, _menu_h,
    "Stop Auto Play", font_button,
    (255, 255, 255), (190, 60, 60), (230, 80, 80)
)


# Confirmation Dialog Buttons
confirm_yes_btn = Button(
    280, 320, 100, 40,
    "Confirm", font_button,
    (255, 255, 255), (200, 50, 50), (230, 80, 80)
)

confirm_no_btn = Button(
    400, 320, 100, 40,
    "Cancel", font_button,
    (255, 255, 255), (80, 80, 80), (120, 120, 120)
)


# --------------------------------------------------
# BOARD POSITION AND RESET FUNCTIONS
# --------------------------------------------------

def get_board_start_pos():
    size = len(board_layout)
    board_pixel_size = size * DOT_SPACING

    start_x = (_menu_x - board_pixel_size) // 2 + 20
    start_y = (BG_HEIGHT - board_pixel_size) // 2 + 20

    return max(40, start_x), max(40, start_y)


def reset_board():
    global board_layout
    global selected_peg
    global game_status_message
    global show_reset_confirm
    global auto_play_active
    global game_mode

    stop_auto_play()

    board_layout = generate_board(
        size_dd.get_selected(),
        type_dd.get_selected()
    )

    selected_peg = None
    game_status_message = "Active Game"
    show_reset_confirm = False
    game_mode = "Manual"


def count_pegs():
    return sum(row.count(1) for row in board_layout)


def count_playable_positions():
    return sum(
        1
        for row in board_layout
        for cell in row
        if cell != 0
    )


# --------------------------------------------------
# VALID MOVE FUNCTIONS
# --------------------------------------------------

def get_valid_moves():
    """
    Return every valid orthogonal peg jump.

    Each move contains:
    (starting_position, ending_position)
    """

    moves = []

    rows = len(board_layout)
    cols = len(board_layout[0])

    directions = [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2)
    ]

    for r in range(rows):
        for c in range(cols):

            if board_layout[r][c] != 1:
                continue

            for dr, dc in directions:

                nr = r + dr
                nc = c + dc

                mid_r = r + dr // 2
                mid_c = c + dc // 2

                if not (
                    0 <= nr < rows
                    and 0 <= nc < cols
                ):
                    continue

                if (
                    board_layout[mid_r][mid_c] == 1
                    and board_layout[nr][nc] == 2
                ):
                    moves.append(
                        ((r, c), (nr, nc))
                    )

    return moves


def has_valid_moves():
    return len(get_valid_moves()) > 0


# --------------------------------------------------
# GAME OVER AND VICTORY DETECTION
# --------------------------------------------------


def check_game_over():
    global game_status_message
    global auto_play_active

    pegs = count_pegs()

    # Victory: Exactly one peg remains anywhere on the board.
    if pegs == 1:

        game_status_message = "Victory!"
        auto_play_active = False

        return True

    # Loss: No valid moves remain.
    elif not has_valid_moves():

        game_status_message = "Game Over / Loss"
        auto_play_active = False

        return True

    game_status_message = "Active Game"

    return False



# --------------------------------------------------
# MANUAL GAME MODE
# --------------------------------------------------


def randomize_board():
    """
    Shuffle pegs across existing playable positions.

    Preserves the number of pegs and board dimensions.
    Ensures the randomized board has a valid move
    unless only one peg remains.
    """

    global selected_peg
    global game_status_message
    global game_mode
    global auto_play_active

    stop_auto_play()

    positions = []

    for r in range(len(board_layout)):
        for c in range(len(board_layout[r])):

            if board_layout[r][c] != 0:
                positions.append((r, c))

    peg_count = count_pegs()

    center = len(board_layout) // 2

    # Clear selected peg.
    selected_peg = None
    game_mode = "Manual"

    # Handle the final remaining peg.
    if peg_count == 1:

        for r, c in positions:
            board_layout[r][c] = 2

        board_layout[center][center] = 1

        check_game_over()
        return True

    # Randomize until a playable configuration is found.
    max_attempts = 1000

    for attempt in range(max_attempts):

        random.shuffle(positions)

        # Empty all playable positions.
        for r, c in positions:
            board_layout[r][c] = 2

        # Place the original number of pegs.
        for r, c in positions[:peg_count]:
            board_layout[r][c] = 1

        # Accept only configurations with valid moves.
        if has_valid_moves():

            game_status_message = "Board Randomized"
            return True

    # Restore the board if no playable arrangement is found.
    game_status_message = "Game Over / Loss"

    check_game_over()

    return False



def attempt_move(start_pos, end_pos):
    """
    Execute a valid orthogonal single-peg jump.

    The starting peg and jumped peg are removed.
    The destination becomes occupied.
    """

    global selected_peg

    r1, c1 = start_pos
    r2, c2 = end_pos

    size = len(board_layout)

    if not (
        0 <= r1 < size
        and 0 <= c1 < size
        and 0 <= r2 < size
        and 0 <= c2 < size
    ):
        return False

    if board_layout[r1][c1] != 1:
        return False

    if board_layout[r2][c2] != 2:
        return False

    dr = r2 - r1
    dc = c2 - c1

    # Only orthogonal jumps of exactly two positions.
    if not (
        (abs(dr) == 2 and dc == 0)
        or (abs(dc) == 2 and dr == 0)
    ):
        return False

    mid_r = r1 + dr // 2
    mid_c = c1 + dc // 2

    if board_layout[mid_r][mid_c] != 1:
        return False

    # Execute the jump.
    board_layout[r1][c1] = 2
    board_layout[mid_r][mid_c] = 2
    board_layout[r2][c2] = 1

    selected_peg = None

    check_game_over()

    return True


# --------------------------------------------------
# AUTOMATED GAME MODE
# --------------------------------------------------

def start_auto_play():
    """
    Start automated gameplay.

    The computer repeatedly selects random valid moves
    until the game is over or the user stops it.
    """

    global auto_play_active
    global last_auto_move_time
    global game_status_message
    global game_mode

    # Do not start an already completed game.
    if check_game_over():
        return False

    game_mode = "Automated"
    auto_play_active = True

    # Allow the first move immediately.
    last_auto_move_time = (
        pygame.time.get_ticks() - AUTO_MOVE_INTERVAL
    )

    game_status_message = "Auto Play: Running"

    return True


def auto_play_step():
    """
    Execute one randomly selected valid automated move.

    Returns True if a move was executed.
    Returns False if the game is over or no moves remain.
    """

    global game_status_message
    global auto_play_active

    if not auto_play_active:
        return False

    valid_moves = get_valid_moves()

    if not valid_moves:
        check_game_over()
        return False

    # Computer randomly selects one valid move.
    selected_move = random.choice(valid_moves)

    start_pos, end_pos = selected_move

    success = attempt_move(start_pos, end_pos)

    if success:

        if auto_play_active:
            game_status_message = "Auto Play: Running"

        return True

    return False


def stop_auto_play():
    """
    Stop automated gameplay.
    """

    global auto_play_active
    global game_status_message

    was_running = auto_play_active

    auto_play_active = False

    if was_running:
        game_status_message = "Auto Play Stopped"

    return was_running


def update_game(current_time=None):
    """
    Update automated gameplay.

    This function is called repeatedly by the main game loop.
    The computer waits between moves so the user can see
    the game being played.
    """

    global last_auto_move_time

    if not auto_play_active:
        return

    if current_time is None:
        current_time = pygame.time.get_ticks()

    if current_time - last_auto_move_time >= AUTO_MOVE_INTERVAL:

        last_auto_move_time = current_time

        auto_play_step()


# --------------------------------------------------
# UI DRAWING FUNCTIONS
# --------------------------------------------------

def draw_text_right_aligned(screen, text, font, color, y_pos):

    surface = font.render(text, True, color)

    x_pos = BG_WIDTH - surface.get_width() - 30

    screen.blit(surface, (x_pos, y_pos))


def draw_ui(screen, mouse_pos):

    draw_text_right_aligned(
        screen,
        "Peg Solitaire",
        font_title,
        current_text_color,
        15
    )

    draw_text_right_aligned(
        screen,
        f"Status: {game_status_message}",
        font_label,
        current_text_color,
        55
    )

    draw_text_right_aligned(
        screen,
        f"Mode: {game_mode}",
        font_label,
        current_text_color,
        475
    )

    # Draw action buttons.
    new_game_btn.draw(screen, mouse_pos)
    randomize_btn.draw(screen, mouse_pos)
    auto_play_btn.draw(screen, mouse_pos)
    stop_auto_btn.draw(screen, mouse_pos)

    # Draw closed dropdowns first.
    for dd in dropdowns:

        if not dd.is_open:
            dd.draw(screen, mouse_pos)

    # Draw open dropdowns on top.
    for dd in dropdowns:

        if dd.is_open:
            dd.draw(screen, mouse_pos)

    # Confirmation dialog.
    if show_reset_confirm:

        overlay = pygame.Surface(
            (BG_WIDTH, BG_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 180))

        screen.blit(overlay, (0, 0))

        dialog_rect = pygame.Rect(200, 200, 400, 200)

        pygame.draw.rect(
            screen,
            (240, 240, 240),
            dialog_rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (50, 50, 50),
            dialog_rect,
            width=2,
            border_radius=10
        )

        msg_surf = font_label.render(
            "Reset current game?",
            True,
            (30, 30, 30)
        )

        screen.blit(
            msg_surf,
            msg_surf.get_rect(center=(400, 250))
        )

        confirm_yes_btn.draw(screen, mouse_pos)
        confirm_no_btn.draw(screen, mouse_pos)


def draw_board(screen):

    start_x, start_y = get_board_start_pos()

    size = len(board_layout)

    for row in range(size):

        for col in range(size):

            val = board_layout[row][col]

            if val != 0:

                x = start_x + (col * DOT_SPACING)
                y = start_y + (row * DOT_SPACING)

                if val == 1:

                    color = (
                        (255, 215, 0)
                        if selected_peg == (row, col)
                        else current_peg_color
                    )

                    pygame.draw.circle(
                        screen,
                        color,
                        (x, y),
                        DOT_RADIUS
                    )

                    pygame.draw.circle(
                        screen,
                        (30, 30, 30),
                        (x, y),
                        DOT_RADIUS,
                        2
                    )

                elif val == 2:

                    pygame.draw.circle(
                        screen,
                        DOT_COLOR_HOLE,
                        (x, y),
                        DOT_RADIUS
                    )

                    pygame.draw.circle(
                        screen,
                        (150, 150, 150),
                        (x, y),
                        DOT_RADIUS,
                        2
                    )


# --------------------------------------------------
# EVENT HANDLING
# --------------------------------------------------

def handle_event(event):

    global current_bg_color
    global current_text_color
    global current_peg_color
    global selected_peg
    global show_reset_confirm

    if show_reset_confirm:

        if confirm_yes_btn.is_clicked(event):
            reset_board()

        elif confirm_no_btn.is_clicked(event):
            show_reset_confirm = False

        return

    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return

    # Handle open dropdown menus.
    for dd in dropdowns:

        if dd.is_open:

            for opt_rect, opt, idx in dd.option_rects:

                if opt_rect.collidepoint(event.pos):

                    dd.selected_index = idx
                    dd.is_open = False

                    if dd == bg_dd:

                        bg_colors = {
                            "Light Gray": ((245, 245, 245), (30, 30, 30)),
                            "Red": ((200, 50, 50), (255, 255, 255)),
                            "Blue": ((50, 150, 255), (255, 255, 255)),
                            "Black": ((30, 30, 30), (255, 255, 255))
                        }

                        current_bg_color, current_text_color = bg_colors[opt]

                    elif dd == peg_dd:

                        peg_colors = {
                            "Blue": (30, 130, 230),
                            "Green": (40, 200, 80),
                            "Gold": (230, 180, 30),
                            "Red": (220, 50, 50)
                        }

                        current_peg_color = peg_colors[opt]

                    elif dd == size_dd or dd == type_dd:

                        reset_board()

                    return

            dd.is_open = False

            return

    # Open a dropdown.
    for dd in dropdowns:

        if dd.rect.collidepoint(event.pos):

            dd.is_open = True

            for other_dd in dropdowns:

                if other_dd != dd:
                    other_dd.is_open = False

            return

    # New Game button.
    if new_game_btn.is_clicked(event):

        stop_auto_play()

        if count_pegs() < count_playable_positions() - 1:
            show_reset_confirm = True

        else:
            reset_board()

        return

    # Randomize button.
    if randomize_btn.is_clicked(event):

        randomize_board()
        return

    # Auto Play button.
    if auto_play_btn.is_clicked(event):

        start_auto_play()
        return

    # Stop Auto Play button.
    if stop_auto_btn.is_clicked(event):

        stop_auto_play()
        return

    # Do not allow manual moves after game over.
    if game_status_message in ("Victory!", "Game Over / Loss"):
        return

    # Manual board movements.
    mx, my = event.pos

    start_x, start_y = get_board_start_pos()

    size = len(board_layout)

    for r in range(size):

        for c in range(size):

            if board_layout[r][c] == 0:
                continue

            bx = start_x + (c * DOT_SPACING)
            by = start_y + (r * DOT_SPACING)

            if (mx - bx) ** 2 + (my - by) ** 2 <= DOT_RADIUS ** 2:

                # Manual interaction stops automated gameplay.
                stop_auto_play()

                if board_layout[r][c] == 1:

                    selected_peg = (r, c)

                elif board_layout[r][c] == 2 and selected_peg is not None:

                    attempt_move(selected_peg, (r, c))

                return

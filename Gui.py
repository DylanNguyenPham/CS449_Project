import pygame
from Classes import Button, Dropdown

pygame.init()

# Window settings
BG_WIDTH = 800
BG_HEIGHT = 600

# State variables
current_bg_color = (245, 245, 245)     # Default Light Gray
current_text_color = (30, 30, 30)      # Dark Text
current_peg_color = (30, 130, 230)     # Default Blue

DOT_RADIUS = 18
DOT_SPACING = 50
DOT_COLOR_HOLE = (200, 200, 200)

font_title = pygame.font.SysFont(None, 48)
font_label = pygame.font.SysFont(None, 28)
font_button = pygame.font.SysFont(None, 20)

# Game State
selected_peg = None
game_status_message = "Active Game"
show_reset_confirm = False

# Function to dynamically build board matrices based on size (5x5, 7x7, 9x9)
def generate_board(size_str, board_type):
    size = int(size_str.split('x')[0])
    board = [[1 for _ in range(size)] for _ in range(size)]
    
    # Calculate corner cutouts based on board dimension
    cutout = 1 if size == 5 else (2 if size == 7 else 3)
    
    for r in range(size):
        for c in range(size):
            if (r < cutout or r >= size - cutout) and (c < cutout or c >= size - cutout):
                board[r][c] = 0
                
    # Center hole
    center = size // 2
    board[center][center] = 2
    return board

# UI Position Specs
_menu_w, _menu_h = 170, 32
_menu_x = BG_WIDTH - _menu_w - 30

# Dropdown Menus
size_dd = Dropdown(_menu_x, 150, _menu_w, _menu_h, "Board Size", ["7x7", "5x5", "9x9"], font_button)
type_dd = Dropdown(_menu_x, 200, _menu_w, _menu_h, "Board Type", ["English", "Diamond", "Hexagon"], font_button)
bg_dd = Dropdown(_menu_x, 250, _menu_w, _menu_h, "Background", ["Light Gray", "Red", "Blue", "Black"], font_button)
peg_dd = Dropdown(_menu_x, 300, _menu_w, _menu_h, "Peg Color", ["Blue", "Green", "Gold", "Red"], font_button)

dropdowns = [size_dd, type_dd, bg_dd, peg_dd]

# Initial Board State
board_layout = generate_board(size_dd.get_selected(), type_dd.get_selected())

# Action Buttons
new_game_btn = Button(_menu_x, 90, _menu_w, _menu_h, "New Game", font_button, (30, 30, 30), (230, 230, 230), (190, 190, 190))

# Confirmation Dialog Buttons
confirm_yes_btn = Button(280, 320, 100, 40, "Confirm", font_button, (255,255,255), (200, 50, 50), (230, 80, 80))
confirm_no_btn = Button(400, 320, 100, 40, "Cancel", font_button, (255,255,255), (80, 80, 80), (120, 120, 120))

def get_board_start_pos():
    size = len(board_layout)
    board_pixel_size = size * DOT_SPACING
    start_x = (_menu_x - board_pixel_size) // 2 + 20
    start_y = (BG_HEIGHT - board_pixel_size) // 2 + 20
    return max(40, start_x), max(40, start_y)

def reset_board():
    global board_layout, selected_peg, game_status_message, show_reset_confirm
    board_layout = generate_board(size_dd.get_selected(), type_dd.get_selected())
    selected_peg = None
    game_status_message = "Active Game"
    show_reset_confirm = False

def count_pegs():
    return sum(row.count(1) for row in board_layout)

def has_valid_moves():
    rows = len(board_layout)
    cols = len(board_layout[0])
    for r in range(rows):
        for c in range(cols):
            if board_layout[r][c] == 1:
                directions = [(-2, 0, -1, 0), (2, 0, 1, 0), (0, -2, 0, -1), (0, 2, 0, 1)]
                for dr, dc, mr, mc in directions:
                    nr, nc = r + dr, c + dc
                    mid_r, mid_c = r + mr, c + mc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if board_layout[mid_r][mid_c] == 1 and board_layout[nr][nc] == 2:
                            return True
    return False

def check_game_over():
    global game_status_message
    pegs = count_pegs()
    center = len(board_layout) // 2
    if pegs == 1 and board_layout[center][center] == 1:
        game_status_message = "Victory!"
    elif not has_valid_moves():
        game_status_message = "Game Over / Loss"

def attempt_move(start_pos, end_pos):
    global selected_peg
    r1, c1 = start_pos
    r2, c2 = end_pos
    size = len(board_layout)

    if not (0 <= r1 < size and 0 <= c1 < size and 0 <= r2 < size and 0 <= c2 < size):
        return False

    if board_layout[r1][c1] != 1 or board_layout[r2][c2] != 2:
        return False

    dr = r2 - r1
    dc = c2 - c1

    if (abs(dr) == 2 and dc == 0) or (abs(dc) == 2 and dr == 0):
        mid_r = r1 + dr // 2
        mid_c = c1 + dc // 2
        
        if board_layout[mid_r][mid_c] == 1:
            board_layout[r1][c1] = 2
            board_layout[mid_r][mid_c] = 2
            board_layout[r2][c2] = 1
            selected_peg = None
            check_game_over()
            return True

    return False

def draw_text_right_aligned(screen, text, font, color, y_pos):
    surface = font.render(text, True, color)
    x_pos = BG_WIDTH - surface.get_width() - 30
    screen.blit(surface, (x_pos, y_pos))

def draw_ui(screen, mouse_pos):
    draw_text_right_aligned(screen, "Peg Solitaire", font_title, current_text_color, 15)
    draw_text_right_aligned(screen, f"Status: {game_status_message}", font_label, current_text_color, 55)

    new_game_btn.draw(screen, mouse_pos)

    for dd in dropdowns:
        if not dd.is_open:
            dd.draw(screen, mouse_pos)
            
    for dd in dropdowns:
        if dd.is_open:
            dd.draw(screen, mouse_pos)

    if show_reset_confirm:
        overlay = pygame.Surface((BG_WIDTH, BG_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        dialog_rect = pygame.Rect(200, 200, 400, 200)
        pygame.draw.rect(screen, (240, 240, 240), dialog_rect, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), dialog_rect, width=2, border_radius=10)

        msg_surf = font_label.render("Reset current game?", True, (30, 30, 30))
        screen.blit(msg_surf, msg_surf.get_rect(center=(400, 250)))

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
                    color = (255, 215, 0) if selected_peg == (row, col) else current_peg_color
                    pygame.draw.circle(screen, color, (x, y), DOT_RADIUS)
                    pygame.draw.circle(screen, (30, 30, 30), (x, y), DOT_RADIUS, 2)
                elif val == 2:
                    pygame.draw.circle(screen, DOT_COLOR_HOLE, (x, y), DOT_RADIUS)
                    pygame.draw.circle(screen, (150, 150, 150), (x, y), DOT_RADIUS, 2)

def handle_event(event):
    global current_bg_color, current_text_color, current_peg_color, selected_peg, show_reset_confirm

    if show_reset_confirm:
        if confirm_yes_btn.is_clicked(event):
            reset_board()
        elif confirm_no_btn.is_clicked(event):
            show_reset_confirm = False
        return

    # Handle Dropdown Menu Clicks
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for dd in dropdowns:
            if dd.is_open:
                for opt_rect, opt, idx in dd.option_rects:
                    if opt_rect.collidepoint(event.pos):
                        dd.selected_index = idx
                        dd.is_open = False
                        
                        if dd == bg_dd:
                            bg_colors = {"Light Gray": ((245,245,245),(30,30,30)), "Red": ((200,50,50),(255,255,255)), "Blue": ((50,150,255),(255,255,255)), "Black": ((30,30,30),(255,255,255))}
                            current_bg_color, current_text_color = bg_colors[opt]
                        elif dd == peg_dd:
                            peg_colors = {"Blue": (30,130,230), "Green": (40,200,80), "Gold": (230,180,30), "Red": (220,50,50)}
                            current_peg_color = peg_colors[opt]
                        elif dd == size_dd or dd == type_dd:
                            reset_board()
                        return
                dd.is_open = False

        for dd in dropdowns:
            if dd.rect.collidepoint(event.pos):
                dd.is_open = not dd.is_open
                for other_dd in dropdowns:
                    if other_dd != dd:
                        other_dd.is_open = False
                return

        # Handle Board Clicks for Peg Movements
        mx, my = event.pos
        start_x, start_y = get_board_start_pos()
        size = len(board_layout)
        
        for r in range(size):
            for c in range(size):
                if board_layout[r][c] != 0:
                    bx = start_x + (c * DOT_SPACING)
                    by = start_y + (r * DOT_SPACING)
                    if (mx - bx)**2 + (my - by)**2 <= DOT_RADIUS**2:
                        if board_layout[r][c] == 1:
                            selected_peg = (r, c)
                        elif board_layout[r][c] == 2 and selected_peg is not None:
                            attempt_move(selected_peg, (r, c))

    # Handle Button Click
    if new_game_btn.is_clicked(event):
        if count_pegs() < (len(board_layout)**2 - 1):
            show_reset_confirm = True
        else:
            reset_board()

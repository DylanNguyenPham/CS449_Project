
import pygame
import sys
import Gui

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode(
    (Gui.BG_WIDTH, Gui.BG_HEIGHT)
)

pygame.display.set_caption("Peg Solitaire - CS 449")

# Set up the game clock
clock = pygame.time.Clock()

# Main game loop
while True:

    # Get current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Fill background
    screen.fill(Gui.current_bg_color)

    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        # Pass events to GUI handler
        Gui.handle_event(event)

    # Update automated gameplay
    Gui.update_game()

    # Render board and UI
    Gui.draw_board(screen)
    Gui.draw_ui(screen, mouse_pos)

    # Update display
    pygame.display.flip()

    # Maintain 60 FPS
    clock.tick(60)


import pygame
import sys
import Gui  

# Initialize Pygame
pygame.init()

# Set up the game window using dimensions from Gui.py
screen = pygame.display.set_mode((Gui.BG_WIDTH, Gui.BG_HEIGHT))
pygame.display.set_caption("Peg Solitaire - CS 449")

# Set up the game clock
clock = pygame.time.Clock()

# Main game loop
while True:
    # Get current mouse position for UI button hover states
    mouse_pos = pygame.mouse.get_pos()

    # Fill background color dynamically based on user choice
    screen.fill(Gui.current_bg_color)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Pass event to GUI button click handler
        Gui.handle_event(event)



    # Render board and UI elements
    Gui.draw_board(screen)
    Gui.draw_ui(screen, mouse_pos)

    # Update the display
    pygame.display.flip()

    # Maintain 60 FPS
    clock.tick(60)
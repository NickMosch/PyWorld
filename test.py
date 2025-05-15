import pygame
import sys

# Initialize Pygame
pygame.init()

info = pygame.display.Info()
screen_width = min(1550, info.current_w)
screen_height = min(900, info.current_h)

screen = pygame.display.set_mode((screen_width, screen_height))
print(f"Detected resolution: {info.current_w}x{info.current_h}")
# Set a window title
pygame.display.set_caption("Pygame Window Test")
# Set fixed window size

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Optional: exit with ESC key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Fill the screen black
    screen.fill((0, 0, 0))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

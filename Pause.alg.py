import pygame 
import sys

# Αρχικοποίηση pygame
pygame.init()

# Ρυθμίσεις παραθύρου
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pause & Resume Example")

clock = pygame.time.Clock()
paused = False


# Βασική λούπα παιχνιδιού
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Έλεγχος πλήκτρων
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = True
            elif event.key == pygame.K_SPACE:
                paused = False

    # Αν δεν είναι παγωμένο, ενημέρωσε το παιχνίδι
    if not paused:
       continue

   

    pygame.display.flip()
    clock.tick(30)  # ρυθμός καρέ

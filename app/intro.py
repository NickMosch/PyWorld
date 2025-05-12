import pygame
import sys

class introScreen:
    def __init__(self,game):
        pygame.init()
        pygame.mixer.init()

        # Constants
        self.game = game
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 100)
        self.DARK_GRAY = (50, 50, 50)
        self.BLACK = (0, 0, 0)
        self.FONT = pygame.font.SysFont("consolas", 50)
        self.SMALL_FONT = pygame.font.SysFont("consolas", 27)

        # Display
        self.screen = pygame.display.set_mode((self.game.WIDTH, self.game.HEIGHT))
        pygame.display.set_caption("Welcome to PyWorld!")

        # Load background
        self.background = pygame.image.load("assets/matrix.png")
        self.background = pygame.transform.scale(self.background, (self.game.WIDTH, self.game.HEIGHT))

        # Sound
        self.background_music = pygame.mixer.Sound("assets/sound_effects/background_music.mp3")
        self.sound2 = pygame.mixer.Sound("assets/sound_effects/beep.mp3")
        self.background_music.set_volume(0.3)
        self.background_music.play(-1)

    def draw_instructions(self):
        self.screen.blit(self.background, (0, 0))
        title = self.FONT.render("Welcome to PyWorld!", True, self.YELLOW)
        self.screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 80))

        instructions = [
            "Menu Controls: Use the ARROW keys to navigate the menu.",
            "Press ENTER to select a menu option.",
            "To return to the main menu, press BACKSPACE.",
            "The questions will appear on the top of the screen, and 4 answers in the form of ",
            "submarines (in Chapter 1), tanks (in Chapter 2), helicopters (in Chapter 3) or UFO's (in Chapter 4)",
            "will appear, only ONE of which is correct.",
            "Shoot the answer you think is correct, if it's correct then you move on to the next question",
            "until all 9 questions are answered correctly. Then you proceed to the next chapter.",
            "If you answer a question wrong, the chapter restarts.",
            "Gameplay Controls: ",
            "Use the W A S D keys to move and the SPACE button to shoot. "
            "Before the main game starts, there will be a small chapter",
            "to determine your knowledge level."
        ]

        for i, line in enumerate(instructions):
            text = self.SMALL_FONT.render(line, True, self.WHITE)
            self.screen.blit(text, (self.game.WIDTH // 2 - text.get_width() // 2, 200 + i * 50))

        enter_text = self.FONT.render("Press ENTER to continue", True, self.DARK_GRAY)
        rect = enter_text.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT - 100))
        pygame.draw.rect(self.screen, self.YELLOW, rect.inflate(40, 20), border_radius=10)
        self.screen.blit(enter_text, rect)

    def display_intro(self):
        clock = pygame.time.Clock()
        self.game.fade("intro",0)

        running = True
        while running:
            self.draw_instructions()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.sound2.play()
                        self.game.fade("intro",1)
                        # Start the game here
                        self.game.gameLoopRun = True
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            clock.tick(60)

import pygame
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

assets_path = (BASE_DIR / "assets").resolve()

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
        self.FONT = pygame.font.SysFont("consolas", 35)
        self.SMALL_FONT = pygame.font.SysFont("consolas", 21)

        # Display
        self.screen = pygame.display.set_mode((self.game.WIDTH, self.game.HEIGHT))
        pygame.display.set_caption("Welcome to PyWorld!")

        # Load background
        self.bg_path = assets_path / "matrix.png"
        self.background = pygame.image.load(str(self.bg_path))
        self.background = pygame.transform.scale(self.background, (self.game.WIDTH, self.game.HEIGHT))

        # Sound
        self.background_music = self.game.menu.bg_music
        self.sound2 = self.game.menu.sound2
        self.background_music.set_volume(0.3)

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
            "to determine your knowledge level.",
            "Press 'P' to pause the game at any time"
        ]

        for i, line in enumerate(instructions):
            text = self.SMALL_FONT.render(line, True, self.WHITE)
            self.screen.blit(text, (self.game.WIDTH // 2 - text.get_width() // 2, 200 + i * 50))

        enter_text = self.FONT.render("Press ENTER to continue", True, self.DARK_GRAY)
        rect = enter_text.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT - 30))
        pygame.draw.rect(self.screen, self.YELLOW, rect.inflate(30, 10), border_radius=10)
        self.screen.blit(enter_text, rect)

    def display_intro(self):
        clock = pygame.time.Clock()
        self.game.fade("intro",0)

        running = True
        self.background_music.play(-1)
        while running:
            self.draw_instructions()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running,self.game.globalLoopRun,self.game.gameLoopRun,self.game.menu.run_display,self.game.tran_screen.isScreenRunning,self.game.lose_screen.isLoseRunning = False,False,False,False,False,False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.sound2.play()
                        self.game.fade("intro",1)
                        # Start the game here
                        self.background_music.stop()
                        self.game.gameLoopRun = True
                        running = False

            clock.tick(60)
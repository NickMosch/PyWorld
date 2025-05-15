import pygame
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

assets_path = (BASE_DIR / "assets").resolve()

class menu:
    def __init__(self,game):
        pygame.init()
        pygame.mixer.init()

        # Constants
        self.WIDTH, self.HEIGHT = 1550,900
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 100)
        self.DARK_GRAY = (50, 50, 50)
        self.BLACK = (0, 0, 0)
        self.FONT = pygame.font.SysFont("consolas", 40)
        self.SMALL_FONT = pygame.font.SysFont("consolas", 25)
        self.game = game

        # Load and scale background
        self.background_path = BASE_DIR / "assets" / "matrix.png"
        self.background = pygame.image.load(str(self.background_path))
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        # Sounds
        self.bg_music_path = BASE_DIR / "assets" / "sound_effects" / "background_music.mp3"
        self.bg_music = pygame.mixer.Sound(str(self.bg_music_path))
        self.sound2_path = BASE_DIR / "assets" / "sound_effects" / "beep.mp3"
        self.sound2 = pygame.mixer.Sound(str(self.sound2_path))
        self.bg_music.set_volume(0.3)

        # Display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Welcome to PyWorld!")

        # Menu state
        self.button_labels = ["Start", "Instructions", "Settings"]
        self.buttons = [pygame.Rect(self.WIDTH//2 - 150, self.HEIGHT//2 - 60 + i*80, 350, 65)
                        for i in range(len(self.button_labels))]
        self.selected_index = 0
        self.current_screen = "menu"
        self.run_display = False
        self.skillLevels = ["Beginner","Intermediate","Expert","Pro"]

        # Settings
        self.volume = 0.3
        self.brightness = 1.0

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        title_text = self.FONT.render(f"Welcome to PyWorld! Your level is {self.skillLevels[self.game.playerSkillLevel]}", True, self.YELLOW)
        self.screen.blit(title_text, (self.WIDTH//2 - title_text.get_width()//2, 100))

        for i, rect in enumerate(self.buttons):
            is_selected = (i == self.selected_index)
            color = self.YELLOW if is_selected else self.DARK_GRAY
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            label_color = self.BLACK if is_selected else self.YELLOW
            label = self.FONT.render(self.button_labels[i], True, label_color)
            self.screen.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

    def draw_instructions(self):
        self.screen.blit(self.background, (0, 0))
        title = self.FONT.render("Instructions", True, self.YELLOW)
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 80))

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
            "Use the W A S D keys to move and the SPACE button to shoot.",
            "Press 'P' to pause the game at any time"
        ]
        for i, line in enumerate(instructions):
            text = self.SMALL_FONT.render(line, True, self.WHITE)
            self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, 200 + i * 50))

    def draw_settings(self):
        self.screen.blit(self.background, (0, 0))
        title = self.FONT.render("Settings", True, self.YELLOW)
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 80))

        vol_text = self.SMALL_FONT.render(f"Music Volume: {int(self.volume * 100)}%", True, self.WHITE)
        self.screen.blit(vol_text, (self.WIDTH//2 - vol_text.get_width()//2, 250))

        bright_text = self.SMALL_FONT.render(f"Brightness: {int(self.brightness * 100)}%", True, self.WHITE)
        self.screen.blit(bright_text, (self.WIDTH//2 - bright_text.get_width()//2, 320))

        if self.brightness < 1.0:
            dim_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
            dim_surface.set_alpha(int((1 - self.brightness) * 255))
            dim_surface.fill((0, 0, 0))
            self.screen.blit(dim_surface, (0, 0))

        help_lines = [
            "Use ← → to adjust volume",
            "Use ↑ ↓ to adjust brightness",
            "Press BACKSPACE to return"
        ]
        for i, line in enumerate(help_lines):
            help_text = self.SMALL_FONT.render(line, True, self.WHITE)
            self.screen.blit(help_text, (30, self.HEIGHT - 100 + i * 30))

    def display_menu(self):
        clock = pygame.time.Clock()
        if self.run_display:
            self.game.fade("menu",0)
            self.bg_music.play(-1)
            self.game.isTutorial = False
            self.game.playerWon = False

        while self.run_display:
            self.screen.fill(self.BLACK)

            if self.current_screen == "menu":
                self.draw_menu()
            elif self.current_screen == "instructions":
                self.draw_instructions()
            elif self.current_screen == "settings":
                self.draw_settings()

            pygame.display.flip()
            #self.game.check_events()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.globalLoopRun,self.game.gameLoopRun,self.game.menu.run_display,self.game.tran_screen.isScreenRunning,self.game.lose_screen.isLoseRunning = False,False,False,False,False
                if event.type == pygame.KEYDOWN:
                    if self.current_screen == "menu":
                        if event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % len(self.buttons)
                            self.sound2.play()
                        elif event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % len(self.buttons)
                            self.sound2.play()
                        elif event.key == pygame.K_RETURN:
                            self.sound2.play()
                            selected = self.button_labels[self.selected_index]
                            if selected == "Start":
                                self.run_display = False
                                self.game.gameLoopRun = True
                                self.bg_music.stop()
                                self.game.fade("menu",1)
                                break
                            elif selected == "Instructions":
                                self.current_screen = "instructions"
                            elif selected == "Settings":
                                self.current_screen = "settings"

                    elif self.current_screen == "instructions":
                        if event.key == pygame.K_BACKSPACE:
                            self.current_screen = "menu"
                            self.sound2.play()

                    elif self.current_screen == "settings":
                        if event.key == pygame.K_LEFT:
                            self.volume = max(0.0, self.volume - 0.1)
                            self.bg_music.set_volume(self.volume)
                            for chapter_background_music_ in self.game.environment_sounds:
                                chapter_background_music_.set_volume(self.volume)
                            self.game.victory_sound.set_volume(self.volume)
                            self.game.defeat_sound.set_volume(self.volume)
                            self.game.laser_sound.set_volume(self.volume)
                            self.sound2.play()
                        elif event.key == pygame.K_RIGHT:
                            self.volume = min(1.0, self.volume + 0.1)
                            self.bg_music.set_volume(self.volume)
                            for chapter_background_music_ in self.game.environment_sounds:
                                chapter_background_music_.set_volume(self.volume)
                            self.game.victory_sound.set_volume(self.volume)
                            self.game.defeat_sound.set_volume(self.volume)
                            self.game.laser_sound.set_volume(self.volume)
                            self.sound2.play()
                        elif event.key == pygame.K_UP:
                            self.brightness = min(1.0, self.brightness + 0.1)
                            self.sound2.play()
                        elif event.key == pygame.K_DOWN:
                            self.brightness = max(0.1, self.brightness - 0.1)
                            self.sound2.play()
                        elif event.key == pygame.K_BACKSPACE:
                            self.current_screen = "menu"
                            self.sound2.play()

            clock.tick(60)
import pygame
import sys
from pathlib import Path

# Αν το script τρέχει από πακεταρισμένη μορφή (π.χ. μέσω PyInstaller), βρίσκει τη σωστή διαδρομή των assets
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# Ορισμός διαδρομής για τα assets
assets_path = (BASE_DIR / "assets").resolve()

class menu:
    """Κλάση για το κύριο μενού του παιχνιδιού"""
    
    def __init__(self, game):
        """Αρχικοποίηση του μενού"""
        pygame.init()
        pygame.mixer.init()

        # Σταθερές - διαστάσεις, χρώματα, γραμματοσειρές
        self.WIDTH, self.HEIGHT = 1550, 900  # Διαστάσεις παραθύρου
        self.WHITE = (255, 255, 255)  # Χρώμα λευκό
        self.YELLOW = (255, 255, 100)  # Χρώμα κίτρινο
        self.DARK_GRAY = (50, 50, 50)  # Χρώμα σκούρο γκρι
        self.BLACK = (0, 0, 0)  # Χρώμα μαύρο
        self.FONT = pygame.font.SysFont("consolas", 40)  # Γραμματοσειρά μεγέθους 40
        self.SMALL_FONT = pygame.font.SysFont("consolas", 25)  # Γραμματοσειρά μεγέθους 25
        self.game = game  # Αναφορά στο κύριο παιχνίδι

        # Φόρτωση και προσαρμογή φόντου
        self.background_path = BASE_DIR / "assets" / "matrix.png"  # Διαδρομή φόντου
        self.background = pygame.image.load(str(self.background_path))  # Φόρτωση εικόνας
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))  # Κλιμάκωση

        # Ήχοι με ρύθμιση έντασης
        self.bg_music_path = BASE_DIR / "assets" / "sound_effects" / "background_music.mp3"  # Μουσική φόντου
        self.bg_music = pygame.mixer.Sound(str(self.bg_music_path))  # Φόρτωση ήχου
        self.sound2_path = BASE_DIR / "assets" / "sound_effects" / "beep.mp3"  # Ηχητικό εφέ
        self.sound2 = pygame.mixer.Sound(str(self.sound2_path))  # Φόρτωση ήχου
        self.bg_music.set_volume(0.3)  # Ρύθμιση έντασης

        # Δημιουργία παραθύρου
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Δημιουργία οθόνης
        pygame.display.set_caption("Welcome to PyWorld!")  # Τίτλος παραθύρου

        # Ετικέτες και κουμπιά με τη θέση τους
        self.button_labels = ["Start", "Instructions", "Settings"]  # Ετικέτες κουμπιών
        # Δημιουργία ορθογωνίων για τα κουμπιά
        self.buttons = [pygame.Rect(self.WIDTH//2 - 150, self.HEIGHT//2 - 60 + i*80, 350, 65)
                        for i in range(len(self.button_labels))]
        self.selected_index = 0  # Επιλεγμένο κουμπί
        self.current_screen = "menu"  # Τρέχουσα οθόνη
        self.run_display = False  # Αν εμφανίζεται το μενού
        self.skillLevels = ["Beginner", "Intermediate", "Expert", "Pro"]  # Επίπεδα δυσκολίας

        # Ρυθμίσεις χρήστη
        self.volume = 0.3  # Ένταση ήχου (0-1)
        self.brightness = 1.0  # Φωτεινότητα (0.1-1.0)

    def draw_menu(self):
        """Σχεδίαση βασικού μενού"""
        self.screen.blit(self.background, (0, 0))  # Σχεδίαση φόντου
        
        # Τίτλος με το επίπεδο του παίκτη
        title_text = self.FONT.render(
            f"Welcome to PyWorld! Your level is {self.skillLevels[self.game.playerSkillLevel]}",
            True, self.YELLOW
        )
        self.screen.blit(title_text, (self.WIDTH//2 - title_text.get_width()//2, 100))

        # Δημιουργία κουμπιών
        for i, rect in enumerate(self.buttons):
            is_selected = (i == self.selected_index)  # Αν είναι επιλεγμένο το κουμπί
            color = self.YELLOW if is_selected else self.DARK_GRAY  # Χρώμα ανάλογα με την επιλογή
            pygame.draw.rect(self.screen, color, rect, border_radius=10)  # Σχεδίαση ορθογωνίου
            label_color = self.BLACK if is_selected else self.YELLOW  # Χρώμα κειμένου
            label = self.FONT.render(self.button_labels[i], True, label_color)  # Δημιουργία κειμένου
            self.screen.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))  # Σχεδίαση κειμένου

    def draw_instructions(self):
        """Οθόνη οδηγιών"""
        self.screen.blit(self.background, (0, 0))  # Σχεδίαση φόντου
        
        # Τίτλος οδηγιών
        title = self.FONT.render("Instructions", True, self.YELLOW)
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 80))

        # Λίστα με τις οδηγίες
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
        
        # Σχεδίαση κάθε γραμμής οδηγιών
        for i, line in enumerate(instructions):
            text = self.SMALL_FONT.render(line, True, self.WHITE)
            self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, 200 + i * 50))

    def draw_settings(self):
        """Οθόνη ρυθμίσεων"""
        self.screen.blit(self.background, (0, 0))  # Σχεδίαση φόντου
        
        # Τίτλος ρυθμίσεων
        title = self.FONT.render("Settings", True, self.YELLOW)
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 80))

        # Ένταση και φωτεινότητα
        vol_text = self.SMALL_FONT.render(f"Music Volume: {int(self.volume * 100)}%", True, self.WHITE)
        self.screen.blit(vol_text, (self.WIDTH//2 - vol_text.get_width()//2, 250))

        bright_text = self.SMALL_FONT.render(f"Brightness: {int(self.brightness * 100)}%", True, self.WHITE)
        self.screen.blit(bright_text, (self.WIDTH//2 - bright_text.get_width()//2, 320))

        # Μείωση φωτεινότητας με επιπλέον layer
        if self.brightness < 1.0:
            dim_surface = pygame.Surface((self.WIDTH, self.HEIGHT))  # Δημιουργία επιφάνειας
            dim_surface.set_alpha(int((1 - self.brightness) * 255))  # Ρύθμιση διαφάνειας
            dim_surface.fill((0, 0, 0))  # Μαύρο χρώμα
            self.screen.blit(dim_surface, (0, 0))  # Σχεδίαση επιφάνειας

        # Οδηγίες για τις ρυθμίσεις
        help_lines = [
            "Use ← → to adjust volume",
            "Use ↑ ↓ to adjust brightness",
            "Press BACKSPACE to return"
        ]
        for i, line in enumerate(help_lines):
            help_text = self.SMALL_FONT.render(line, True, self.WHITE)
            self.screen.blit(help_text, (30, self.HEIGHT - 100 + i * 30))

    def display_menu(self):
        """Κεντρική λούπα μενού"""
        clock = pygame.time.Clock()  # Χρονόμετρο για ελέγχου FPS
        
        # Εφέ εμφάνισης αν είναι ενεργό το μενού
        if self.run_display:
            self.game.fade("menu", 0)  # Εφέ εξαφάνισης
            self.bg_music.play(-1)  # Αναπαραγωγή μουσικής σε λούπα
            self.game.isTutorial = False  # Δεν είναι tutorial
            self.game.playerWon = False  # Επαναφορά κατάστασης νίκης

        while self.run_display:
            self.screen.fill(self.BLACK)  # Γέμισμα οθόνης με μαύρο

            # Ανάλογα με την τρέχουσα οθόνη σχεδιάζει την κατάλληλη
            if self.current_screen == "menu":
                self.draw_menu()
            elif self.current_screen == "instructions":
                self.draw_instructions()
            elif self.current_screen == "settings":
                self.draw_settings()

            pygame.display.flip()  # Ενημέρωση οθόνης

            # Χειρισμός γεγονότων
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Κλείσιμο παραθύρου
                    self.game.globalLoopRun = False
                    self.game.gameLoopRun = False
                    self.run_display = False
                    self.game.tran_screen.isScreenRunning = False
                    self.game.lose_screen.isLoseRunning = False

                elif event.type == pygame.KEYDOWN:  # Πάτημα πλήκτρου
                    if self.current_screen == "menu":  # Αν βρισκόμαστε στο κύριο μενού
                        if event.key == pygame.K_DOWN:  # Κάτω βέλος
                            self.selected_index = (self.selected_index + 1) % len(self.buttons)  # Επόμενο κουμπί
                            self.sound2.play()  # Ηχητικό εφέ
                        elif event.key == pygame.K_UP:  # Πάνω βέλος
                            self.selected_index = (self.selected_index - 1) % len(self.buttons)  # Προηγούμενο κουμπί
                            self.sound2.play()  # Ηχητικό εφέ
                        elif event.key == pygame.K_RETURN:  # Enter
                            self.sound2.play()  # Ηχητικό εφέ
                            selected = self.button_labels[self.selected_index]  # Επιλεγμένο κουμπί
                            if selected == "Start":  # Έναρξη παιχνιδιού
                                self.run_display = False
                                self.game.gameLoopRun = True
                                self.bg_music.stop()  # Σταμάτημα μουσικής
                                self.game.fade("menu", 1)  # Εφέ εμφάνισης
                                break
                            elif selected == "Instructions":  # Οθόνη οδηγιών
                                self.current_screen = "instructions"
                            elif selected == "Settings":  # Οθόνη ρυθμίσεων
                                self.current_screen = "settings"

                    elif self.current_screen == "instructions":  # Αν βρισκόμαστε στις οδηγίες
                        if event.key == pygame.K_BACKSPACE:  # Επιστροφή στο μενού
                            self.current_screen = "menu"
                            self.sound2.play()  # Ηχητικό εφέ

                    elif self.current_screen == "settings":  # Αν βρισκόμαστε στις ρυθμίσεις
                        if event.key == pygame.K_LEFT:  # Αριστερό βέλος - μείωση έντασης
                            self.volume = max(0.0, self.volume - 0.1)
                            # Εφαρμογή έντασης σε όλους τους ήχους
                            self.bg_music.set_volume(self.volume)
                            for chapter_music in self.game.environment_sounds:
                                chapter_music.set_volume(self.volume)
                            self.game.victory_sound.set_volume(self.volume)
                            self.game.defeat_sound.set_volume(self.volume)
                            self.game.laser_sound.set_volume(self.volume)
                            self.sound2.play()  # Ηχητικό εφέ
                        elif event.key == pygame.K_RIGHT:  # Δεξί βέλος - αύξηση έντασης
                            self.volume = min(1.0, self.volume + 0.1)
                            # Εφαρμογή έντασης σε όλους τους ήχους
                            self.bg_music.set_volume(self.volume)
                            for chapter_music in self.game.environment_sounds:
                                chapter_music.set_volume(self.volume)
                            self.game.victory_sound.set_volume(self.volume)
                            self.game.defeat_sound.set_volume(self.volume)
                            self.game.laser_sound.set_volume(self.volume)
                            self.sound2.play()  # Ηχητικό εφέ
                        elif event.key == pygame.K_UP:  # Πάνω βέλος - αύξηση φωτεινότητας
                            self.brightness = min(1.0, self.brightness + 0.1)
                            self.sound2.play()  # Ηχητικό εφέ
                        elif event.key == pygame.K_DOWN:  # Κάτω βέλος - μείωση φωτεινότητας
                            self.brightness = max(0.1, self.brightness - 0.1)
                            self.sound2.play()  # Ηχητικό εφέ
                        elif event.key == pygame.K_BACKSPACE:  # Επιστροφή στο μενού
                            self.current_screen = "menu"
                            self.sound2.play()  # Ηχητικό εφέ

            clock.tick(60)  # Περιορισμός στα 60 FPS

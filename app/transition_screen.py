import pygame
import sys 
from pathlib import Path

# Ορισμός του βασικού φακέλου (BASE_DIR) ανάλογα αν το πρόγραμμα τρέχει ως πακέτο (frozen) ή ως απλό script
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# Διαδρομή προς τον φάκελο assets
assets_path = (BASE_DIR / "assets").resolve()

# Χρώματα και αρχικοποίηση Pygame και γραμματοσειρών
YELLOW = (255, 255, 100)
DARK_GRAY = (50, 50, 50)
pygame.font.init()
pygame.init()
FONT = pygame.font.SysFont("consolas", 50)
SMALL_FONT = pygame.font.SysFont("consolas", 27)

class Screen():
    def __init__(self, game):
        self.game = game
        # Καταστάσεις για μετάβαση και ολοκλήρωση tutorial
        self.moveToNextChapter = False
        self.isTutorialComplete = False
        self.isScreenRunning = False
        self.clock = pygame.time.Clock()
        # Χρήση της μουσικής και ήχου από το μενού
        self.bg_music = self.game.menu.bg_music
        self.beep_sound = self.game.menu.sound2
        self.bg_music.set_volume(0.3)

    def draw_screen(self):
        # Ζωγραφίζει το background στην οθόνη του παιχνιδιού
        self.game.WINDOW.blit(self.bg_image, (0, 0))
        
        # Αν δεν είναι tutorial
        if not self.game.isTutorial:
            # Αν ο παίκτης κέρδισε το κεφάλαιο
            if self.game.playerWon:
                # Εμφάνιση συγχαρητηρίων και ευχαριστήριου μηνύματος
                title = FONT.render("Congratulations!", True, YELLOW)
                self.game.WINDOW.blit(title, (self.game.WIDTH//2 - title.get_width()//2, 80))
                message = [
                    "You answered all the questions correctly!",
                    "Thank you for playing PyWorld!",
                ]
                for i, line in enumerate(message):
                    text = SMALL_FONT.render(line, True, self.game.WHITE)
                    self.game.WINDOW.blit(text, (self.game.WIDTH//2 - text.get_width()//2, 200 + i * 50))

                # Κουμπί για να συνεχίσει ο παίκτης πατώντας ENTER
                enter_text = FONT.render("Press ENTER to continue", True, DARK_GRAY)
                rect = enter_text.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT - 100))
                pygame.draw.rect(self.game.WINDOW, YELLOW, rect.inflate(40, 20), border_radius=10)
                self.game.WINDOW.blit(enter_text, rect)
            else:
                # Αν δεν κέρδισε ακόμα αλλά ολοκλήρωσε σωστά την απάντηση
                if self.moveToNextChapter:
                    self.game.draw_text(30,"YOU BEAT THIS CHAPTER ",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
                    self.game.draw_text(20,"Press enter for next chapter",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
                    self.game.draw_text(20,"Press backspace for main menu",self.game.WIDTH/2,self.game.HEIGHT/2 + 80,self.game.WHITE)
                else:
                    self.game.draw_text(30,"CORRECT ANSWER",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
                    self.game.draw_text(20,"Press enter for next level",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
                    self.game.draw_text(20,"Press backspace for main menu",self.game.WIDTH/2,self.game.HEIGHT/2 + 80,self.game.WHITE)
        else:
            # Αν είναι tutorial
            if self.isTutorialComplete:
                self.game.draw_text(30,"YOU COMPLETED THE TUTORIAL",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
                self.game.draw_text(20,"Press enter to start the main game",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
            else:
                self.game.draw_text(30,"PRESS ENTER TO START THE NEXT TUTORIAL LEVEL",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
        
        pygame.display.update()  # Ενημέρωση οθόνης

    def display_transition_screen(self):
        # Επιλογή background ανάλογα αν ο παίκτης κέρδισε ή όχι
        if self.game.playerWon:
            self.bg_music.play(-1)
            self.bg_image_path = assets_path / "end.jpg"
            self.bg_image = pygame.image.load(str(self.bg_image_path))
        else:
            self.bg_image_path = assets_path / "transition.jpg"
            self.bg_image = pygame.image.load(str(self.bg_image_path))
        self.bg_image = pygame.transform.scale(self.bg_image,(self.game.WIDTH,self.game.HEIGHT))
        
        # Αν τρέχει η οθόνη μετάβασης, κάνε fade in
        if self.isScreenRunning:
            self.game.fade("transition",0)
        
        # Βρόχος λειτουργίας της οθόνης μετάβασης
        while self.isScreenRunning:
            self.draw_screen()
            self.game.check_events()  # Έλεγχος εισόδων από παίκτη
            self.checkEvents()        # Επεξεργασία δικών μας events
            self.game.reset_keys()    # Επαναφορά των πλήκτρων
            self.clock.tick(60)       # Περιορισμός 60 fps

    def checkEvents(self):
        # Όταν πατηθεί το κουμπί START (Enter)
        if self.game.START_KEY:
            # Αν είναι tutorial και ολοκληρώθηκε, επιστροφή στο μενού
            if self.game.isTutorial and self.isTutorialComplete:
                self.game.menu.run_display = True
            # Αν ο παίκτης κέρδισε το κεφάλαιο, επιστροφή στο μενού και παίξιμο ήχου beep
            elif self.game.playerWon:
                self.game.menu.run_display = True
                self.bg_music.stop()
                self.beep_sound.play()
            else:
                # Αλλιώς ξεκίνημα του κύριου παιχνιδιού και fade out
                self.game.gameLoopRun = True
                self.game.fade("transition",1)
            self.isScreenRunning = False  # Τερματισμός οθόνης μετάβασης
        
        # Αν πατηθεί το BACK (Backspace), και δεν είναι tutorial ή έχει κερδίσει
        if self.game.BACK_KEY and not self.game.isTutorial and not self.game.playerWon:
            self.game.menu.run_display = True
            self.isScreenRunning = False
            self.game.environment_sounds[self.game.chapter].stop()  # Σταμάτα τον ήχο περιβάλλοντος
            self.game.fade("transition",1)  # Fade out προς μενού

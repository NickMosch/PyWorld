import pygame

# Κλάση που χειρίζεται την οθόνη ήττας του παιχνιδιού
class LoseScreen():
    def __init__(self, game):
        self.game = game  # Αναφορά στο αντικείμενο του κύριου παιχνιδιού (για πρόσβαση σε μεθόδους και μεταβλητές)
        self.isLoseRunning = False  # Λογική σημαία για το αν η οθόνη ήττας είναι ενεργή
        self.clock = pygame.time.Clock()  # Ρολόι για τον έλεγχο των FPS

    # Συνάρτηση σχεδίασης της οθόνης ήττας
    def draw_screen(self):
        self.game.WINDOW.fill((0, 0, 0))  # Καθαρίζει την οθόνη με μαύρο φόντο

        # Προβολή των βασικών μηνυμάτων στην οθόνη
        self.game.draw_text(30, "YOU LOST", self.game.WIDTH / 2, self.game.HEIGHT / 2, self.game.WHITE)
        self.game.draw_text(20, "PRESS ENTER TO RESTART THE CHAPTER", self.game.WIDTH / 2, self.game.HEIGHT / 2 + 60, self.game.WHITE)
        self.game.draw_text(20, "PRESS BACKSPACE TO RETURN TO THE MAIN MENU", self.game.WIDTH / 2, self.game.HEIGHT / 2 + 80, self.game.WHITE)

        pygame.display.update()  # Ενημέρωση οθόνης με τα νέα στοιχεία

    # Συνάρτηση που ενεργοποιεί και "τρέχει" την οθόνη ήττας
    def display_lose_screen(self):
        if self.isLoseRunning:
            self.game.fade("lose", 0)  # Εκκίνηση με fade in εφέ

        while self.isLoseRunning:
            self.draw_screen()  # Σχεδίαση της οθόνης
            self.game.check_events()  # Έλεγχος βασικών events (π.χ. quit, keypress)
            self.checkEvents()  # Έλεγχος ειδικών κουμπιών (ENTER, BACKSPACE)
            self.game.reset_keys()  # Reset flags για τα πλήκτρα
            self.clock.tick(60)  # Περιορισμός στα 60 FPS

    # Συνάρτηση που ελέγχει τις ενέργειες του παίκτη στην οθόνη ήττας
    def checkEvents(self):
        if self.game.START_KEY:  # Αν πατήθηκε ENTER
            self.game.gameLoopRun = True  # Ξεκινάει το game loop (επαναλαμβάνει το κεφάλαιο)
            self.isLoseRunning = False  # Τερματίζει την lose screen
            self.game.fade("lose", 0)  # Fade effect κατά την έξοδο

        if self.game.BACK_KEY:  # Αν πατήθηκε BACKSPACE
            self.game.menu.run_display = True  # Επιστροφή στο μενού
            self.game.environment_sounds[self.game.chapter].stop()  # Σταματάει ο ήχος του κεφαλαίου
            self.isLoseRunning = False
            self.game.fade("lose", 0)  # Fade effect κατά την έξοδο

# Εισαγωγή των απαραίτητων βιβλιοθηκών
import pygame as pg
import json,random,os
import sys
from menu import menu
from transition_screen import Screen
from lose_screen import LoseScreen
from intro import introScreen
from pathlib import Path

# Καθορισμός του βασικού καταλόγου ανάλογα με το αν το πρόγραμμα τρέχει ως εκτελέσιμο ή ως script
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

print(BASE_DIR)
# Ορισμός διαδρομών για assets και ερωτήσεις
assets_path = (BASE_DIR / "assets").resolve()
questions_path = (BASE_DIR / "questions").resolve()

# Λίστες για την αποθήκευση assets και ερωτήσεων
chaptersAssets = []
chapterKeys = ["background","bullet","player","enemy"]
questions = []

# Αρχικοποίηση του mixer για ήχους
pg.mixer.init()

# Ορισμός διαδρομών για ήχους
victory_sound_path = (BASE_DIR / "assets" / "sound_effects" / "victory.mp3").resolve()
defeat_sound_path = (BASE_DIR / "assets" / "sound_effects" / "defeat.mp3").resolve()
shootlaser_sound_path = (BASE_DIR / "assets" / "sound_effects" / "laser_shot.mp3").resolve()
sea_environment_path = (BASE_DIR / "assets" / "sound_effects" / "Underwater.mp3").resolve()
nature_environment_path = (BASE_DIR / "assets" / "sound_effects" / "missle_shot.mp3").resolve()
sky_environment_path = (BASE_DIR / "assets" / "sound_effects" / "sky_jet.mp3").resolve()
space_environment_path = (BASE_DIR / "assets" / "sound_effects" / "space_ufo.mp3").resolve()

# Φόρτωση ήχων
victory_sound = pg.mixer.Sound(str(victory_sound_path))
defeat_sound = pg.mixer.Sound(str(defeat_sound_path))
shootlaser_sound = pg.mixer.Sound(str(shootlaser_sound_path))
sea_environment = pg.mixer.Sound(str(sea_environment_path))
nature_environment = pg.mixer.Sound(str(nature_environment_path))
sky_environment = pg.mixer.Sound(str(sky_environment_path))
space_environment = pg.mixer.Sound(str(space_environment_path))

# Ρύθμιση έντασης ήχου
sky_environment.set_volume(0.1)

def loadGameContent(playerSkillLevel):
    """Φόρτωση περιεχομένου παιχνιδιού (ερωτήσεις και assets) ανάλογα με το επίπεδο δεξιοτήτων του παίκτη"""
    questions.clear()
    chaptersAssets.clear()
    
    # Ορισμός εύρους ερωτήσεων ανάλογα με το επίπεδο
    if playerSkillLevel == 0:
        min = 0
        max = 4
    elif playerSkillLevel == 1:
        min = 1
        max = 5
    elif playerSkillLevel == 2:
        min = 2
        max = 6
    else:
        min = 3
        max = 7
    
    # Φόρτωση ερωτήσεων
    for currentFileIndex in range(min,max):
        questionsFile = sorted(questions_path.iterdir())[currentFileIndex]
        with open(str(questionsFile), 'r',encoding='utf-8') as file:    
            questions.append(json.load(file))

    # Φόρτωση assets για κάθε κεφάλαιο
    assetsLoaded = 0
    for assetsSubDir in sorted(assets_path.iterdir()):
        currentChapterAssets = [str(asset) for asset in sorted(assetsSubDir.iterdir())]
        formattedAsset = dict(zip(chapterKeys, currentChapterAssets))
        chaptersAssets.append(formattedAsset)
        assetsLoaded+=1
        if assetsLoaded == 4:  # Φόρτωσε μόνο τα assets για τα 4 πρώτα κεφάλαια
            break
    random.shuffle(questions[0])

# Φόρτωση ερωτήσεων για το tutorial
tutorial_questions_path = (BASE_DIR / "questions" / "tutorial.json").resolve()
with open(tutorial_questions_path, 'r') as file:    
    questions.append(json.load(file))

# Ειδική φόρτωση assets για το πρώτο κεφάλαιο
chapter_one_dir = BASE_DIR / "assets" / "C1_DeepSea"
chapterOneimgs = [str(chapter_one_dir / asset) for asset in os.listdir(chapter_one_dir)]
chaptersAssets.append(dict(zip(chapterKeys, chapterOneimgs)))

random.shuffle(questions[0])
pg.display.set_caption("Space Invaders")

# Φόρτωση αρχικών εικόνων
BG_IMAGE = pg.image.load(chaptersAssets[0]["background"])
LASER_BULET = pg.image.load(chaptersAssets[0]["bullet"])
PLAYER_IMG = pg.image.load(chaptersAssets[0]["player"])
ENEMY_IMG = pg.image.load(chaptersAssets[0]["enemy"])

# Αρχικοποίηση pygame
pg.init()
pg.font.init()

class Laser:
    """Κλάση για τις σφαίρες του παίκτη"""
    def __init__(self, x, y):
        self.image = LASER_BULET
        self.image = pg.transform.scale(self.image, (80, 30))
        self.mask = pg.mask.from_surface(self.image)  # Δημιουργία mask για collision detection
        self.x = x 
        self.y = y 

    def draw(self, window):
        """Σχεδίαση της σφαίρας"""
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        """Κίνηση της σφαίρας"""
        self.x -= vel

    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()
    
# Παράμετροι scale για τον παίκτη σε κάθε κεφάλαιο
PLAYER_SCALES = [0.2, 0.2, 2.0, 1.6] 

def scale_image(image, scale_factor):
    """Κλιμάκωση εικόνας με δεδομένο συντελεστή"""
    original_size = image.get_size()
    scaled_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
    return pg.transform.scale(image, scaled_size)

class Player:
    """Κλάση για τον παίκτη"""
    VELOCITY = 5  # Ταχύτητα κίνησης

    def __init__(self, game):
        self.game = game
        self.chapter = game.chapter  # Τρέχον κεφάλαιο (0-3)

        # Φόρτωση και κλιμάκωση εικόνας ανάλογα με το κεφάλαιο
        player_path = chaptersAssets[self.chapter]["player"]
        original_image = pg.image.load(player_path).convert_alpha()
        scale = PLAYER_SCALES[self.chapter]
        self.image = scale_image(original_image, scale)

        self.HEIGHT = self.game.HEIGHT
        self.x = 50  # Αρχική θέση X
        self.y = int(self.HEIGHT / 2)  # Αρχική θέση Y
        self.mask = pg.mask.from_surface(self.image)  # Mask για collision
        self.laser_power = 1  # Ισχύς σφαίρας
        self.lasers = []  # Λίστα με τις σφαίρες
        self.cooldown_timer = 0  # Χρόνος αναμονής μεταξύ βολών
        self.cooldown = 80  # Χρόνος cooldown

    def draw(self, window):
        """Σχεδίαση παίκτη και σφαιρών"""
        window.blit(self.image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        self.cooldown_timer -= 1  # Μείωση χρόνου cooldown

    def shoot(self):
        """Μέθοδος για πυροβολισμό"""
        if self.cooldown_timer <= 0:  # Έλεγχος αν μπορεί να πυροβολήσει
            laser_width = 80
            laser_height = 30

            # Υπολογισμός κέντρου παίκτη
            player_center_x = self.x + self.get_width() // 2
            player_center_y = self.y + self.get_height() // 2

            offset_y = 15  # Offset προς τα κάτω

            # Θέση σφαίρας
            laser_x = self.x + self.get_width() - 10
            laser_y = player_center_y - laser_height // 2 + offset_y

            new_laser = Laser(laser_x, laser_y)
            self.lasers.append(new_laser)
            self.cooldown_timer = self.cooldown

    def move(self, direction):
        """Μέθοδος για κίνηση παίκτη"""
        if direction == "left":
            self.x -= self.VELOCITY
        elif direction == "right":
            self.x += self.VELOCITY
        elif direction == "up":
            self.y -= self.VELOCITY
        elif direction == "down":
            self.y += self.VELOCITY

    def move_lasers(self, vel, objs):
        """Μέθοδος για κίνηση σφαιρών και έλεγχο συγκρούσεων"""
        for laser in self.lasers:
            laser.move(vel)
            if outOfScreen(laser,self):  # Έλεγχος αν η σφαίρα βγήκε εκτός οθόνης
                self.lasers.remove(laser)
            else:
                for obj in objs:  # Έλεγχος για σύγκρουση με εχθρούς
                    if checkCollision(laser, obj):                        
                        self.lasers.remove(laser)
                        shootlaser_sound.play()  # Αναπαραγωγή ήχου
                        if obj.isAnswer:  # Αν χτύπησε τη σωστή απάντηση
                            self.game.state = 1  # Νίκη
                        else:
                            self.game.state = -1  # Ήττα

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

class Alien:
    """Κλάση για τους εχθρούς/απαντήσεις"""
    def __init__(self, x, y):
        self.vel = 0.1  # Αρχική ταχύτητα
        self.x = x
        self.y = y
        self.image = ENEMY_IMG
        self.image = pg.transform.scale(self.image, (140, 100))
        self.mask = pg.mask.from_surface(self.image)
        self.isAnswer = False  # Αν είναι η σωστή απάντηση

    def draw(self, window):
        """Σχεδίαση εχθρού"""
        window.blit(self.image, (self.x, self.y))

    def move(self):
        """Κίνηση εχθρού"""
        self.x -= self.vel
        self.vel += 0.001  # Αύξηση ταχύτητας με το χρόνο

def checkCollision(obj1, obj2):
    """Έλεγχος για σύγκρουση μεταξύ δύο αντικειμένων"""
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def outOfScreen(obj,self):
    """Έλεγχος αν ένα αντικείμενο βγήκε εκτός οθόνης"""
    return obj.x < 0 
    
class Game():
    """Κύρια κλάση του παιχνιδιού"""
    def __init__(self):
        # Αρχικοποίηση μεταβλητών
        self.isTutorial = True  # Αν βρίσκεται στο tutorial
        self.font_name = pg.font.get_default_font()
        self.globalLoopRun = True  # Αν τρέχει το παιχνίδι
        self.gameLoopRun = True  # Αν τρέχει ο κύριος βρόχος
        # Μεταβλητές για πλήκτρα
        self.UP_KEY,self.DOWN_KEY,self.START_KEY,self.BACK_KEY = False,False,False,False
        self.FPS = 60  # Frames per second
        self.WIDTH, self.HEIGHT = 1550,900  # Διαστάσεις οθόνης
        self.border = self.WIDTH//2  # Όριο κίνησης παίκτη
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)  # Χρώματα
        self.WINDOW = pg.display.set_mode((self.WIDTH, self.HEIGHT))  # Παράθυρο
        self.BG_IMAGE = pg.transform.scale(BG_IMAGE, (self.WIDTH, self.HEIGHT))  # Background
        self.clock = pg.time.Clock()  # Χρονόμετρο
        # Οθόνες του παιχνιδιού
        self.menu = menu(self)
        self.tran_screen = Screen(self)
        self.lose_screen = LoseScreen(self)
        self.intro_screen = introScreen(self)
        # Λίστα με ήχους περιβάλλοντος
        self.environment_sounds = [sea_environment,nature_environment,sky_environment,space_environment]
        self.victory_sound = victory_sound
        self.defeat_sound = defeat_sound
        self.laser_sound = shootlaser_sound
        # Μεταβλητές προόδου
        self.correctTutorialAnswers = 0
        self.playerSkillLevel = 0  # Επίπεδο δεξιοτήτων (0-3)
        self.chapter = 0  # Τρέχον κεφάλαιο (0-3)
        self.level = 0  # Τρέχον επίπεδο
        self.state = 0  # Κατάσταση (0: κανονική, 1: νίκη, -1: ήττα)
        self.paused = False  # Αν το παιχνίδι είναι σε παύση
        self.playerWon = False  # Αν ο παίκτης κέρδισε

    def redraw_window(self):
        """Επανασχεδίαση της οθόνης"""
        self.WINDOW.blit(self.BG_IMAGE,(0,0))  # Background
        self.player.draw(self.WINDOW)  # Σχεδίαση παίκτη
        for i in range(len(self.aliens)):
            self.aliens[i].draw(self.WINDOW)  # Σχεδίαση εχθρών
            if not self.paused:
                self.aliens[i].move()  # Κίνηση εχθρών αν δεν είναι σε παύση
            # Σχεδίαση κειμένου απάντησης πάνω από κάθε εχθρό
            self.draw_text(20, questions[self.chapter][self.level]["answers"][i], self.aliens[i].x + 20, self.aliens[i].y - 3, self.WHITE)
        # Σχεδίαση πληροφοριών επιπέδου και ερώτησης
        self.draw_text(30,f"LEVEL {self.level + 1}",self.WIDTH/2,20,self.WHITE)
        self.draw_text(25,questions[self.chapter][self.level]["question"],self.WIDTH/2,100,self.WHITE)
        if self.paused:
            self.draw_pause_overlay()  # Σχεδίαση οθόνης παύσης
        pg.display.update()
    
    def check_events(self):
        """Έλεγχος για συμβάντα"""
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Κλείσιμο παιχνιδιού
                self.globalLoopRun,self.gameLoopRun,self.menu.run_display,self.tran_screen.isScreenRunning,self.lose_screen.isLoseRunning = False,False,False,False,False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Πλήκτρο Enter
                    self.START_KEY = True
                if event.key == pg.K_BACKSPACE:  # Πλήκτρο Backspace
                    self.BACK_KEY = True

    def draw_pause_overlay(self):
        """Σχεδίαση οθόνης παύσης"""
        overlay = pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Ημιδιαφανές μαύρο overlay
        self.WINDOW.blit(overlay, (0, 0))

        box_width, box_height = 500, 200
        box_rect = pg.Rect(
            (self.WIDTH - box_width) // 2,
            (self.HEIGHT - box_height) // 2,
            box_width,
            box_height
        )
        pg.draw.rect(self.WINDOW, (50, 50, 50), box_rect)
        pg.draw.rect(self.WINDOW, (200, 200, 200), box_rect, 2)

        font = pg.font.SysFont(None, 32)
        
        if not self.isTutorial:
            lines = [
                "Game Paused",
                "Press ESC to continue",
                "Press BACKSPACE to return to the main menu"
            ]
        else:
            lines = [
                "Game Paused",
               "Press ESC to continue"
            ]
        for i, line in enumerate(lines):
            self.draw_text(20,line,self.WIDTH // 2, box_rect.top + 40 + i * 50,self.WHITE)

    def reset_keys(self):
        """Επαναφορά των μεταβλητών πλήκτρων"""
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False                    

    def draw_text(self,size,text,x,y,color):
        """Σχεδίαση κειμένου"""
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.WINDOW.blit(text_surface,text_rect)
        
    def fade(self,module,mode):
        """Εφέ εξαφάνισης/εμφάνισης"""
        fade = pg.Surface((self.WIDTH, self.HEIGHT))
        fade.fill((0, 0, 0))
        clock = pg.time.Clock()
        myRange = [0,256,10] if mode else [255,-1,-10]  # Εύρος για fade in/out
        for alpha in range(*myRange):
            fade.set_alpha(alpha)
            if module == "game":
                self.redraw_window()
            elif module == "transition":
                self.tran_screen.draw_screen()
            elif module == "lose":
                self.lose_screen.draw_screen()
            elif module == "menu":
                self.menu.draw_menu()
            else:
                self.intro_screen.draw_instructions()
            self.WINDOW.blit(fade, (0, 0))
            pg.display.update()
            clock.tick(60)

    def handle_game_state(self):
        """Χειρισμός της κατάστασης του παιχνιδιού (νίκη/ήττα)"""
        if self.state==1:  # Νίκη
            self.level+=1
            if self.level==2:  # Αν ολοκληρώθηκε το κεφάλαιο
                global PLAYER_IMG
                global ENEMY_IMG
                global LASER_BULET
                self.environment_sounds[self.chapter].stop()
                self.chapter+=1  # Μετάβαση στο επόμενο κεφάλαιο
                self.level = 0
                self.tran_screen.moveToNextChapter = True
                if self.chapter == 4:  # Αν ολοκληρώθηκαν όλα τα κεφάλαια
                    self.playerWon = True
                    self.chapter = 0
                    self.tran_screen.moveToNextChapter = False
                # Φόρτωση νέων assets
                PLAYER_IMG = pg.image.load(chaptersAssets[self.chapter]["player"])
                ENEMY_IMG = pg.image.load(chaptersAssets[self.chapter]["enemy"])
                LASER_BULET= pg.image.load(chaptersAssets[self.chapter]["bullet"])
                transformedImage = pg.image.load(chaptersAssets[self.chapter]["background"])
                self.BG_IMAGE = pg.transform.scale(transformedImage,(self.WIDTH, self.HEIGHT))
                random.shuffle(questions[self.chapter])  # Ανακάτεμα ερωτήσεων
                victory_sound.play()  # Ηχητικό εφέ νίκης
            else:
                self.tran_screen.moveToNextChapter = False
            self.tran_screen.isScreenRunning = True
            self.gameLoopRun = False
        elif self.state == -1:  # Ήττα
            self.gameLoopRun = False
            self.level = 0
            random.shuffle(questions[self.chapter])
            self.lose_screen.isLoseRunning = True
            defeat_sound.play()  # Ηχητικό εφέ ήττας

    def handle_tutorial_state(self):
        """Χειρισμός κατάστασης tutorial"""
        if self.state == 1:  # Σωστή απάντηση
            self.correctTutorialAnswers +=1
            self.level+=1
            self.gameLoopRun = False
            self.tran_screen.isScreenRunning = True 
        elif self.state == -1:  # Λάθος απάντηση
            self.level+=1
            self.gameLoopRun = False
            self.tran_screen.isScreenRunning = True

        if self.level == 2:  # Ολοκλήρωση tutorial
            if self.correctTutorialAnswers <=2:
                self.playerSkillLevel = 0
            elif self.correctTutorialAnswers <= 5:
                self.playerSkillLevel = 1
            elif self.correctTutorialAnswers <= 9:
                self.playerSkillLevel = 2
            else:
                self.playerSkillLevel = 3
            self.tran_screen.isTutorialComplete = True
            self.level = 0
            self.environment_sounds[self.chapter].stop()
            loadGameContent(self.playerSkillLevel)  # Φόρτωση περιεχομένου ανάλογα με το επίπεδο

    def game_loop(self):
        """Κύριος βρόχος του παιχνιδιού"""
        ALIEN_ROW = 4  # Αριθμός σειρών εχθρών
        ALIEN_COL = 1  # Αριθμός στηλών εχθρών
        self.player = Player(self)
        self.player.image = pg.transform.rotate(self.player.image,-90)  # Περιστροφή εικόνας παίκτη
        self.state = 0  # Αρχική κατάσταση
        self.aliens = []  # Λίστα εχθρών

        # Δημιουργία εχθρών
        for i in range(ALIEN_ROW):
            cur_row = self.HEIGHT// 2 - ((ALIEN_ROW - 1) * 120 // 2) + (i * 120)
            for j in range(1, ALIEN_COL + 1):
                new_alien = Alien(self.WIDTH - 100 - (j * 200)/ (ALIEN_COL + 1), cur_row)
                if(questions[self.chapter][self.level]["correctAnswerIndex"] == i):
                    new_alien.isAnswer = True  # Ορισμός σωστής απάντησης
                self.aliens.append(new_alien)

        if self.gameLoopRun:
            self.environment_sounds[self.chapter].play(-1)  # Αναπαραγωγή ήχου περιβάλλοντος

        while self.gameLoopRun:
            self.clock.tick(self.FPS)  # Περιορισμός FPS
            self.redraw_window()                                                    
            self.check_events()
            keys = pg.key.get_pressed()

            if  keys[pg.K_p]:  # Πλήκτρο παύσης
                self.paused = True

            if self.paused:  # Αν το παιχνίδι είναι σε παύση
                if keys[pg.K_ESCAPE]:  # Συνέχεια
                    self.paused = False
                if not self.isTutorial:
                    if keys[pg.K_BACKSPACE]:  # Επιστροφή στο μενού
                        self.paused = False
                        self.gameLoopRun = False
                        self.environment_sounds[self.chapter].stop()
                        self.menu.run_display = True
                continue

            # Κίνηση παίκτη με πλήκτρα
            if keys[pg.K_a] and self.player.x - self.player.VELOCITY > 0:  # Αριστερά
                self.player.move("left")
            if keys[pg.K_d] and self.player.x + self.player.VELOCITY + self.player.get_width() < self.border:  # Δεξιά
                self.player.move("right")
            if keys[pg.K_w] and self.player.y - self.player.VELOCITY > 0: # Πάνω
                self.player.move("up")
            if keys[pg.K_s] and (self.player.y + self.player.VELOCITY + self.player.get_height() < self.HEIGHT): # Κάτω
                self.player.move("down")
            if keys[pg.K_SPACE]:  # Πυροβολισμός
                self.player.shoot()
            
            self.player.move_lasers(-20, self.aliens)  # Κίνηση σφαιρών

            # Έλεγχος για σύγκρουση παίκτη με εχθρό ή έξοδο εχθρού από οθόνη
            for alien in self.aliens:
                if checkCollision(alien, self.player) or outOfScreen(alien,self):
                    self.state = -1  # Ήττα

            # Χειρισμός κατάστασης ανάλογα με το αν είναι tutorial ή όχι
            if self.isTutorial:
                self.handle_tutorial_state()
            else:
                self.handle_game_state()
            self.reset_keys()  # Επαναφορά πλήκτρων

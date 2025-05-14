import pygame as pg
import json,random,os
import sys
from menu import menu
from transition_screen import Screen
from lose_screen import LoseScreen
from intro import introScreen
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

print(BASE_DIR)
assets_path = (BASE_DIR / "assets").resolve()
questions_path = (BASE_DIR / "questions").resolve()

chaptersAssets = []
chapterKeys = ["background","bullet","player","enemy"]

questions = []

pg.mixer.init()

collision_sound_path = (BASE_DIR / "assets" / "sound_effects" / "explosion.mp3")
victory_sound_path = (BASE_DIR / "assets" / "sound_effects" / "victory.mp3").resolve()
defeat_sound_path = (BASE_DIR / "assets" / "sound_effects" / "defeat.mp3").resolve()
shootlaser_sound_path = (BASE_DIR / "assets" / "sound_effects" / "laser_shot.mp3").resolve()
sea_environment_path = (BASE_DIR / "assets" / "sound_effects" / "Underwater.mp3").resolve()
nature_environment_path = (BASE_DIR / "assets" / "sound_effects" / "missle_shot.mp3").resolve()
sky_environment_path = (BASE_DIR / "assets" / "sound_effects" / "sky_jet.mp3").resolve()
space_environment_path = (BASE_DIR / "assets" / "sound_effects" / "space_ufo.mp3").resolve()

collision_sound = pg.mixer.Sound(str(collision_sound_path))
victory_sound = pg.mixer.Sound(str(victory_sound_path))
defeat_sound = pg.mixer.Sound(str(defeat_sound_path))
shootlaser_sound = pg.mixer.Sound(str(shootlaser_sound_path))
sea_environment = pg.mixer.Sound(str(sea_environment_path))
nature_environment = pg.mixer.Sound(str(nature_environment_path))
sky_environment = pg.mixer.Sound(str(sky_environment_path))
space_environment = pg.mixer.Sound(str(space_environment_path))

sky_environment.set_volume(0.1)

def loadGameContent(correctTutorialAnswers):
    questions.clear()
    chaptersAssets.clear()
    
    if correctTutorialAnswers == 0:
        min = 0
        max = 4
    elif correctTutorialAnswers == 1:
        min = 1
        max = 5
    elif correctTutorialAnswers == 2:
        min = 2
        max = 6
    else:
        min = 3
        max = 7
    
    for currentFileIndex in range(min,max):
        questionsFile = sorted(questions_path.iterdir())[currentFileIndex]
        with open(str(questionsFile), 'r') as file:    
            questions.append(json.load(file))

    assetsLoaded = 0
    for assetsSubDir in sorted(assets_path.iterdir()):
        currentChapterAssets = [str(asset) for asset in sorted(assetsSubDir.iterdir())]
        formattedAsset = dict(zip(chapterKeys, currentChapterAssets))
        chaptersAssets.append(formattedAsset)
        assetsLoaded+=1
        if assetsLoaded == 4:
            break
    random.shuffle(questions[0])

tutorial_questions_path = (BASE_DIR / "questions" / "tutorial.json").resolve()

with open(tutorial_questions_path, 'r') as file:    
    questions.append(json.load(file))

chapter_one_dir = BASE_DIR / "assets" / "C1_DeepSea"
chapterOneimgs = [str(chapter_one_dir / asset) for asset in os.listdir(chapter_one_dir)]
chaptersAssets.append(dict(zip(chapterKeys, chapterOneimgs)))

random.shuffle(questions[0])
pg.display.set_caption("Space Invaders")

# load images
BG_IMAGE = pg.image.load(chaptersAssets[0]["background"])
LASER_BULET = pg.image.load(chaptersAssets[0]["bullet"])
PLAYER_IMG = pg.image.load(chaptersAssets[0]["player"])
ENEMY_IMG = pg.image.load(chaptersAssets[0]["enemy"])

pg.init()
pg.font.init()

class Laser:
    def __init__(self, x, y):
        self.image = LASER_BULET
        self.image = pg.transform.scale(self.image, (80, 30))
        self.mask = pg.mask.from_surface(self.image)
        self.x = x + 20
        self.y = y + 10

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.x -= vel

    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()

class Player:

    VELOCITY = 5

    def __init__(self,game):
        self.game = game
        self.image = PLAYER_IMG
        #self.image = pg.transform.rotate(self.image, 0)
        self.image = pg.transform.scale(self.image, (150, 100))
        self.HEIGHT = self.game.HEIGHT
        self.x = 50
        self.y = int(self.HEIGHT/2)
        self.mask = pg.mask.from_surface(self.image)
        self.laser_power = 1
        self.lasers = []  # List of bullets in the screen shot by the player
        self.cooldown_timer = 0
        self.cooldown = 80

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        self.cooldown_timer -= 1

    def shoot(self):
        if self.cooldown_timer <= 0:
            new_laser = Laser(self.x + self.image.get_width() / 2, self.y)
            self.lasers.append(new_laser)
            self.cooldown_timer = self.cooldown

    def move(self, direction):
        if direction == "left":
            self.x -= self.VELOCITY
        elif direction == "right":
            self.x += self.VELOCITY
        elif direction == "up":
            self.y -= self.VELOCITY
        elif direction == "down":
            self.y += self.VELOCITY

    def move_lasers(self, vel, objs):
        for laser in self.lasers:
            laser.move(vel)
            if outOfScreen(laser,self):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if checkCollision(laser, obj):                        
                        self.lasers.remove(laser)
                        shootlaser_sound.play()
                        if obj.isAnswer:
                            self.game.state = 1
                        else:
                            self.game.state = -1

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

class Alien:
    def __init__(self, x, y):
        self.vel = 0.1
        self.x = x
        self.y = y
        self.image = ENEMY_IMG
        self.mask = pg.mask.from_surface(self.image)
        self.image = pg.transform.scale(self.image, (140, 100))
        self.isAnswer = False

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.x -= self.vel
        self.vel += 0.001

def checkCollision(obj1, obj2):
        offset_x = int(obj2.x - obj1.x)
        offset_y = int(obj2.y - obj1.y)
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def outOfScreen(obj,self):
    return obj.x < 0 
    
class Game():

    def __init__(self):
        self.isTutorial = True
        self.font_name = pg.font.get_default_font()
        self.globalLoopRun = True
        self.gameLoopRun = True
        self.UP_KEY,self.DOWN_KEY,self.START_KEY,self.BACK_KEY = False,False,False,False
        self.FPS = 60
        self.WIDTH, self.HEIGHT = 1550,900
        self.border = self.WIDTH//2
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.WINDOW = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.BG_IMAGE = pg.transform.scale(BG_IMAGE, (self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        self.menu = menu(self)
        #self.credits = CreditsMenu(self)
        self.tran_screen = Screen(self)
        self.lose_screen = LoseScreen(self)
        self.intro_screen = introScreen(self)
        self.environment_sounds = [sea_environment,nature_environment,sky_environment,space_environment]
        self.correctTutorialAnswers = 0
        self.chapter = 0
        self.level = 0
        self.state = 0  # default state
        self.paused = False
        self.playerWon = False

    def redraw_window(self):
        self.WINDOW.blit(self.BG_IMAGE,(0,0))
        self.player.draw(self.WINDOW)
        for i in range(len(self.aliens)):
            self.aliens[i].draw(self.WINDOW)
            if not self.paused:
                self.aliens[i].move()
            self.draw_text(20,questions[self.chapter][self.level]["answers"][i],self.aliens[i].x + 20,self.aliens[i].y - 20,self.WHITE)
        self.draw_text(30,f"LEVEL {self.level + 1}",self.WIDTH/2,20,self.WHITE)
        self.draw_text(25,questions[self.chapter][self.level]["question"],self.WIDTH/2,100,self.WHITE)
        if self.paused:
            self.draw_pause_overlay()
        pg.display.update()
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.globalLoopRun,self.gameLoopRun,self.menu.run_display,self.tran_screen.isScreenRunning,self.lose_screen.isLoseRunning = False,False,False,False,False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                if event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = True

    def draw_pause_overlay(self):
        overlay = pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  
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
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False                    

    def draw_text(self,size,text,x,y,color):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.WINDOW.blit(text_surface,text_rect)
        
    def fade(self,module,mode):
        fade = pg.Surface((self.WIDTH, self.HEIGHT))
        fade.fill((0, 0, 0))
        clock = pg.time.Clock()
        myRange = [0,256,10] if mode else [255,-1,-10]
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
        if self.state==1:
            self.level+=1
            if self.level==1:
                global PLAYER_IMG
                global ENEMY_IMG
                global LASER_BULET
                self.environment_sounds[self.chapter].stop()
                self.chapter+=1
                self.level = 0
                self.tran_screen.moveToNextChapter = True
                if self.chapter == 4:
                    self.playerWon = True
                    self.chapter = 0
                    self.tran_screen.moveToNextChapter = False
                PLAYER_IMG = pg.image.load(chaptersAssets[self.chapter]["player"])
                ENEMY_IMG = pg.image.load(chaptersAssets[self.chapter]["enemy"])
                LASER_BULET= pg.image.load(chaptersAssets[self.chapter]["bullet"])
                transformedImage = pg.image.load(chaptersAssets[self.chapter]["background"])
                self.BG_IMAGE = pg.transform.scale(transformedImage,(self.WIDTH, self.HEIGHT))
                random.shuffle(questions[self.chapter])
                victory_sound.play()
            else:
                self.tran_screen.moveToNextChapter = False
            self.tran_screen.isScreenRunning = True
            self.gameLoopRun = False
        elif self.state == -1:
            self.gameLoopRun = False
            self.level = 0
            random.shuffle(questions[self.chapter])
            self.lose_screen.isLoseRunning = True
            defeat_sound.play()

    def handle_tutorial_state(self):
        if self.state == 1:
            self.correctTutorialAnswers +=1
            self.level+=1
            self.gameLoopRun = False
            self.tran_screen.isScreenRunning = True 
        elif self.state == -1:
            self.level+=1
            self.gameLoopRun = False
            self.tran_screen.isScreenRunning = True

        if self.level == 2:
            self.tran_screen.isTutorialComplete = True
            self.level = 0
            self.environment_sounds[self.chapter].stop()
            loadGameContent(self.correctTutorialAnswers)

    def game_loop(self):

        ALIEN_ROW = 4
        ALIEN_COL = 1
        self.player = Player(self)
        self.player.image = pg.transform.rotate(self.player.image,-90)
        self.state = 0
        self.aliens = []

        for i in range(ALIEN_ROW):
            cur_row = self.HEIGHT// 2 - ((ALIEN_ROW - 1) * 120 // 2) + (i * 120)
            for j in range(1, ALIEN_COL + 1):
                new_alien = Alien(self.WIDTH - 100 - (j * 200)/ (ALIEN_COL + 1), cur_row)
                if(questions[self.chapter][self.level]["correctAnswerIndex"] == i):
                    new_alien.isAnswer = True
                self.aliens.append(new_alien)

        if self.gameLoopRun:
            self.environment_sounds[self.chapter].play(-1)

        while self.gameLoopRun:
            self.clock.tick(self.FPS)
            self.redraw_window()                                                    
            self.check_events()
            keys = pg.key.get_pressed()

            if  keys[pg.K_p]:
                self.paused = True

            if self.paused:
                if keys[pg.K_ESCAPE]:
                    self.paused = False
                if not self.isTutorial:
                    if keys[pg.K_BACKSPACE]:
                        self.paused = False
                        self.gameLoopRun = False
                        self.environment_sounds[self.chapter].stop()
                        self.menu.run_display = True
                continue

            if keys[pg.K_a] and self.player.x - self.player.VELOCITY > 0:  # left
                self.player.move("left")
            if keys[pg.K_d] and self.player.x + self.player.VELOCITY + self.player.get_width() < self.border:  # right
                self.player.move("right")
            if keys[pg.K_w] and self.player.y - self.player.VELOCITY > 0: #up
                self.player.move("up")
            if keys[pg.K_s] and (self.player.y + self.player.VELOCITY + self.player.get_height() < self.HEIGHT): #down
                self.player.move("down")
            if keys[pg.K_SPACE]:  # shoot
                #shootlaser_sound.play()
                self.player.shoot()
            
            self.player.move_lasers(-20, self.aliens)

            for alien in self.aliens:
                if checkCollision(alien, self.player) or outOfScreen(alien,self):
                    self.state = -1

            if self.isTutorial:
                self.handle_tutorial_state()
            else:
                self.handle_game_state()
            self.reset_keys()
import pygame as pg
import json,random,os
from menu import menu
from transition_screen import Screen
from lose_screen import LoseScreen
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

assets_path = BASE_DIR / "../assets"
questions_path  = BASE_DIR/"../questions"
chaptersAssets = []
chapterKeys = ["background","bullet","player","enemy"]

questions = []

def loadGameContent(correctTutorialAnswers):
    questions.clear()
    chaptersAssets.clear()
    
    if correctTutorialAnswers == 0:
        min = 0
        max = 3
    elif correctTutorialAnswers == 1:
        min = 1
        max = 4
    elif correctTutorialAnswers == 2:
        min = 2
        max = 5
    else:
        min = 3
        max = 6
    
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


with open("questions/tutorial.json", 'r') as file:    
    questions.append(json.load(file))
chapterOneimgs = [f"assets/C1_DeepSea/" + asset for asset in os.listdir("assets/C1_DeepSea")]
chaptersAssets.append(dict(zip(chapterKeys,chapterOneimgs)))
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
        self.correctTutorialAnswers = 0
        self.chapter = 0
        self.level = 0
        self.state = 0  # default state

    def redraw_window(self):
        self.WINDOW.blit(self.BG_IMAGE,(0,0))
        self.player.draw(self.WINDOW)
        for i in range(len(self.aliens)):
            self.aliens[i].draw(self.WINDOW)
            self.aliens[i].move()
            self.draw_text(20,questions[self.chapter][self.level]["answers"][i],self.aliens[i].x + 20,self.aliens[i].y - 20,self.WHITE)
        self.draw_text(30,f"LEVEL {self.level + 1}",self.WIDTH/2,20,self.WHITE)
        self.draw_text(25,questions[self.chapter][self.level]["question"],self.WIDTH/2,100,self.WHITE)
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

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False                    

    def draw_text(self,size,text,x,y,color):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.WINDOW.blit(text_surface,text_rect)

    #def loadAssets(self,chapter):
        

    def handle_game_state(self):
        if self.state==1:
            self.level+=1
            if self.level==3:
                global PLAYER_IMG
                global ENEMY_IMG
                global LASER_BULET
                self.chapter+=1
                self.level = 0
                PLAYER_IMG = pg.image.load(chaptersAssets[self.chapter]["player"])
                ENEMY_IMG = pg.image.load(chaptersAssets[self.chapter]["enemy"])
                LASER_BULET= pg.image.load(chaptersAssets[self.chapter]["bullet"])
                transformedImage = pg.image.load(chaptersAssets[self.chapter]["background"])
                self.BG_IMAGE = pg.transform.scale(transformedImage,(self.WIDTH, self.HEIGHT))
                self.tran_screen.moveToNextChapter = True
                random.shuffle(questions[self.chapter])
            else:
                self.tran_screen.moveToNextChapter = False
            self.tran_screen.isScreenRunning = True
            self.gameLoopRun = False
        elif self.state == -1:
            self.gameLoopRun = False
            self.level = 0
            random.shuffle(questions[self.chapter])
            self.lose_screen.isLoseRunning = True

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
        
        if self.level == 4:
            self.tran_screen.isTutorialComplete = True
            self.level = 0
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

        while self.gameLoopRun:
            self.clock.tick(self.FPS)
            self.redraw_window()                                                    
            self.check_events()
            keys = pg.key.get_pressed()
            if keys[pg.K_a] and self.player.x - self.player.VELOCITY > 0:  # left
                self.player.move("left")
            if keys[pg.K_d] and self.player.x + self.player.VELOCITY + self.player.get_width() < self.border:  # right
                self.player.move("right")
            if keys[pg.K_w] and self.player.y - self.player.VELOCITY > 0: #up
                self.player.move("up")
            if keys[pg.K_s] and (self.player.y + self.player.VELOCITY + self.player.get_height() < self.HEIGHT): #down
                self.player.move("down")
            if keys[pg.K_SPACE]:  # shoot
                self.player.shoot()

            self.player.move_lasers(-20, self.aliens)

            for alien in self.aliens:
                if checkCollision(alien, self.player) or outOfScreen(alien,self):
                    self.state = -1

            if self.isTutorial:
                self.handle_tutorial_state()
            else:
                self.handle_game_state()

            if self.BACK_KEY and not self.isTutorial:
                self.gameLoopRun = False
                self.menu.run_display = True
                self.tran_screen.isScreenRunning = False    
                self.menu.display_menu()

            self.reset_keys()
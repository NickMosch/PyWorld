import pygame
import sys 
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

assets_path = (BASE_DIR / "assets").resolve()

YELLOW = (255, 255, 100)
DARK_GRAY = (50, 50, 50)
pygame.font.init()
pygame.init()
FONT = pygame.font.SysFont("consolas", 50)
SMALL_FONT = pygame.font.SysFont("consolas", 27)

class Screen():
    def __init__(self,game):
        self.game = game
        self.moveToNextChapter = False
        self.isTutorialComplete = False
        self.isScreenRunning = False
        self.clock = pygame.time.Clock()
        self.bg_music = self.game.menu.bg_music
        self.beep_sound = self.game.menu.sound2
        self.bg_music.set_volume(0.3)

    def draw_screen(self):
        self.game.WINDOW.blit(self.bg_image,(0,0))
        if not self.game.isTutorial:
            if self.game.playerWon:
                title = FONT.render("Congratulations!", True, YELLOW)
                self.game.WINDOW.blit(title, (self.game.WIDTH//2 - title.get_width()//2, 80))
                message = [
                    "You answered all the questions correctly!",
                    "Thank you for playing PyWorld!",
                ]
                for i, line in enumerate(message):
                    text = SMALL_FONT.render(line, True, self.game.WHITE)
                    self.game.WINDOW.blit(text, (self.game.WIDTH//2 - text.get_width()//2, 200 + i * 50))

                enter_text = FONT.render("Press ENTER to continue", True, DARK_GRAY)
                rect = enter_text.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT - 100))
                pygame.draw.rect(self.game.WINDOW, YELLOW, rect.inflate(40, 20), border_radius=10)
                self.game.WINDOW.blit(enter_text, rect)
            else:
                if self.moveToNextChapter:
                    self.game.draw_text(30,"YOU BEAT THIS CHAPTER ",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
                    self.game.draw_text(20,"Press enter for next chapter",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
                    self.game.draw_text(20,"Press backspace for main menu",self.game.WIDTH/2,self.game.HEIGHT/2 + 80,self.game.WHITE)
                else:
                    self.game.draw_text(30,"CORRECT ANSWER",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
                    self.game.draw_text(20,"Press enter for next level",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
                    self.game.draw_text(20,"Press backspace for main menu",self.game.WIDTH/2,self.game.HEIGHT/2 + 80,self.game.WHITE)
        else:
            if self.isTutorialComplete:
                self.game.draw_text(30,"YOU COMPLETED THE TUTORIAL",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
                self.game.draw_text(20,"Press enter to start the main game",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
            else:
                self.game.draw_text(30,"NEXT TUTORIAL LEVEL STARTS IN...",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
                self.game.draw_text(20,"Press enter to actually start it, there is no timer yet",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
        
        pygame.display.update()
    
    def display_transition_screen(self):
        if self.game.playerWon:
            self.bg_music.play(-1)
            self.bg_image_path = assets_path / "end.jpg"
            self.bg_image = pygame.image.load(str(self.bg_image_path))
        else:
            self.bg_image_path = assets_path / "transition.jpg"
            self.bg_image = pygame.image.load(str(self.bg_image_path))
        self.bg_image = pygame.transform.scale(self.bg_image,(self.game.WIDTH,self.game.HEIGHT))
        if self.isScreenRunning:
            self.game.fade("transition",0)
        while self.isScreenRunning:
            self.draw_screen()
            self.game.check_events()
            self.checkEvents()
            self.game.reset_keys()
            self.clock.tick(60)

    def checkEvents(self):
        if self.game.START_KEY:
            if self.game.isTutorial and self.isTutorialComplete:
                self.game.menu.run_display = True
            elif self.game.playerWon:
                self.game.menu.run_display = True
                self.bg_music.stop()
                self.beep_sound.play()
            else:
                self.game.gameLoopRun = True
                self.game.fade("transition",1)
            self.isScreenRunning = False
        if self.game.BACK_KEY and not self.game.isTutorial and not self.game.playerWon:
            self.game.menu.run_display = True
            self.isScreenRunning = False
            self.game.environment_sounds[self.game.chapter].stop()
            self.game.fade("transition",1)
import pygame

class Screen():
    def __init__(self,game):
        self.game = game
        self.moveToNextChapter = False
        self.isTutorialComplete = False
        self.isScreenRunning = False
        self.clock = pygame.time.Clock()

    def draw_screen(self):
        self.game.WINDOW.fill((0,0,0))
        if not self.game.isTutorial and self.isTutorialComplete:
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
                self.isScreenRunning = False
                self.game.isTutorial = False
                self.game.fade("transition",1)
            else:
                self.game.gameLoopRun = True
                self.isScreenRunning = False
                self.game.fade("transition",1)
        if self.game.BACK_KEY and not self.game.isTutorial:
            self.game.menu.run_display = True
            self.isScreenRunning = False
            self.game.fade("transition",1)
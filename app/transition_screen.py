import pygame

class Screen():
    def __init__(self,game):
        self.game = game
        self.moveToNextChapter = False
        self.isScreenRunning = False
        self.clock = pygame.time.Clock()

    def draw_screen(self):
        self.game.WINDOW.fill((0,0,0))
        self.game.check_events()
        self.checkEvents()
        self.game.reset_keys()
        if self.moveToNextChapter:
            self.game.draw_text_directly(30,"YOU BEAT THIS CHAPTER ",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
            self.game.draw_text_directly(20,"Press enter for next chapter",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
            self.game.draw_text_directly(20,"Press backspace for main menu",self.game.WIDTH/2,self.game.HEIGHT/2 + 80,self.game.WHITE)
        else:
            self.game.draw_text_directly(30,"CORRECT ANSWER",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
            self.game.draw_text_directly(20,"Press enter for next level",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
            self.game.draw_text_directly(20,"Press backspace for main menu",self.game.WIDTH/2,self.game.HEIGHT/2 + 80,self.game.WHITE)
        pygame.display.update()
    
    def display_transition_screen(self):
        while self.isScreenRunning:
            self.draw_screen()
            self.clock.tick(60)

    def checkEvents(self):
        if self.game.START_KEY:
            self.game.gameLoopRun = True
            self.isScreenRunning = False
        if self.game.BACK_KEY:
            self.game.menu.run_display = True
            self.isScreenRunning = False

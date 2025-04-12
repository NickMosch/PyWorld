import pygame

class LoseScreen():
    def __init__(self,game):
        self.game = game
        self.isLoseRunning = False
        self.clock = pygame.time.Clock()

    def draw_screen(self):
        self.game.WINDOW.fill((0,0,0))
        self.game.check_events()
        self.checkEvents()
        self.game.reset_keys() 
        self.game.draw_text_directly(30,"YOU LOST",self.game.WIDTH/2,self.game.HEIGHT/2,self.game.WHITE)
        self.game.draw_text_directly(20,"PRESS ENTER TO RESTART THE CHAPTER",self.game.WIDTH/2,self.game.HEIGHT/2 + 60,self.game.WHITE)
        self.game.draw_text_directly(20,"PRESS BACKSPACE TO RETURN TO THE MAIN MENU",self.game.WIDTH/2,self.game.HEIGHT/2 + 80,self.game.WHITE)
        pygame.display.update()
    
    def display_lose_screen(self):
        while self.isLoseRunning:
            self.draw_screen()
            self.clock.tick(60)

    def checkEvents(self):
        if self.game.START_KEY:
            self.game.gameLoopRun = True
            self.isLoseRunning = False
        if self.game.BACK_KEY:
            self.game.menu.run_display = True
            self.isLoseRunning = False

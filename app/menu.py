import pygame

class Menu():
    def __init__(self,game):
        self.game = game
        self.statdre = "Start"
        self.run_display = True
        self.display = pygame.Surface((self.game.WIDTH,self.game.HEIGHT))
        self.window = pygame.display.set_mode(((game.WIDTH,self.game.HEIGHT)))
        self.clock = pygame.time.Clock()
        self.mid_w = self.game.WIDTH/2
        self.mid_h = self.game.HEIGHT/2
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()

    def display_menu(self):
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.display.fill(self.game.BLACK)
            self.game.draw_text('PRESS ENTER TO SELECT AN OPTION', 20, self.game.WIDTH / 2, 100)
            self.game.draw_text('Main Menu', 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()
            self.clock.tick(60)

    def check_input(self):
        if self.game.START_KEY:
            self.run_display = False
            self.game.gameLoopRun = True
            
"""class CreditsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.WIDTH / 2, self.HEIGHT / 2 - 20)
            self.game.draw_text('Made by me', 15, self.WIDTH / 2, self.HEIGHT / 2 + 10)
            self.blit_screen()   """
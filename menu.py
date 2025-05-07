import pygame

class Menu():
    def __init__(self,game):
        self.game = game
        self.run_display = False
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
        self.game.draw_text(15,"*", self.cursor_rect.x, self.cursor_rect.y,self.game.WHITE)

    def display_menu(self):
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.WINDOW.fill(self.game.BLACK)
            self.game.draw_text(20,'PRESS ENTER TO SELECT AN OPTION', self.game.WIDTH / 2, 100,self.game.WHITE)
            self.game.draw_text(20,'Main Menu', self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20,self.game.WHITE)
            self.game.draw_text(20,"Start Game", self.startx, self.starty,self.game.WHITE)
            self.game.draw_text(20,"Options", self.optionsx, self.optionsy,self.game.WHITE)
            self.game.draw_text(20,"Credits", self.creditsx, self.creditsy,self.game.WHITE)
            self.draw_cursor()
            pygame.display.update()
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
from game import Game

g = Game()
g.intro_screen.display_intro()

while g.globalLoopRun:
    g.menu.display_menu()
    g.game_loop()
    g.tran_screen.display_transition_screen()
    g.lose_screen.display_lose_screen()
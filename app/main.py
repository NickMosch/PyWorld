from game import Game

# Δημιουργία αντικειμένου Game που περιέχει όλη τη λογική και τις οθόνες του παιχνιδιού
g = Game()

# Προβολή της εισαγωγικής οθόνης (intro)
g.intro_screen.display_intro()

# Κεντρικός βρόχος του παιχνιδιού που τρέχει όσο το globalLoopRun είναι True
while g.globalLoopRun:
    # Εμφάνιση μενού
    g.menu.display_menu()

    # Εκτέλεση κύριου game loop (χειρίζεται gameplay, κίνησεις, συγκρούσεις κ.λπ.)
    g.game_loop()

    # Προβολή οθόνης μετάβασης (μεταξύ κεφαλαίων / quiz)
    g.tran_screen.display_transition_screen()

    # Προβολή οθόνης ήττας αν χάθηκε το παιχνίδι
    g.lose_screen.display_lose_screen()

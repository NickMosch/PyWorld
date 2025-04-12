import pygame as pg

pg.font.init()

FPS = 120

# Swap width and height for 90-degree rotation
WIDTH, HEIGHT = 1550, 900

WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("PyWorld")

# Load images
SPACESHIP_IMG = pg.image.load("assets/C1_DeepSea/03_submarine_1.png")
ALIEN_IMG = pg.image.load("assets/C2_Land/04_tank_2.png")
LASER_BULLET = pg.image.load("assets/C2_Land/02_Missile_2.png")

# Load background image
BACKGROUND_IMG = pg.image.load("assets/C2_Land/01_forest_land.jpg")  # Replace with your background image path
BACKGROUND_IMG = pg.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))  # Scale to fit the window

class Player:

    VELOCITY = 5

    def __init__(self):  # First instantiation of the player
        self.image = SPACESHIP_IMG  # Player Sprite
        self.image = pg.transform.rotate(self.image, -90)
        self.image = pg.transform.scale(self.image, (150, 100))
        self.mask = pg.mask.from_surface(self.image)  # Player mask for collisions
        self.x = 50 # Starting x position
        self.y = int(HEIGHT/2) # Starting y position
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
            new_laser = Laser(self.x + self.image.get_width() / 2, self.y, self.laser_power)
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

    def move_lasers(self, vel, objs_Alien):
        for laser in self.lasers[:]:  # Iterate over a copy of the list
            laser.move(vel)
            if outOfScreen(laser):
                self.lasers.remove(laser)
                print("Laser removed (out of screen)")
            else:
                for alien in objs_Alien[:]:  # Iterate over a copy of the list
                    if checkCollision(laser, alien):
                        print(f"Collision detected with alien at ({alien.x}, {alien.y})")
                        alien.hp -= laser.power
                        if alien.hp <= 0:
                            print(f"Alien at ({alien.x}, {alien.y}) removed")
                            objs_Alien.remove(alien)
                        self.lasers.remove(laser)
                        print("Laser removed (collision)")
                        break  # Exit the inner loop after handling the collision

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

# Rotate player spaceship to face right
#SPACESHIP_IMG = pg.transform.rotate(SPACESHIP_IMG, -90)  # Rotate 90 degrees left

class Alien:
    def __init__(self, x, y, hp):
        self.vel = 0.1 # Velocity of the aliens
        self.hp = hp
        self.x = x
        self.y = y
        self.image = ALIEN_IMG
        self.mask = pg.mask.from_surface(self.image)
        self.image = pg.transform.scale(self.image, (140, 100))

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.x -= self.vel
        self.vel += 0.001

class Laser:

    def __init__(self, x, y, power):
        self.image = LASER_BULLET
        self.image = pg.transform.scale(self.image, (80, 30))
        self.mask = pg.mask.from_surface(self.image)
        self.x = x + 20
        self.y = y + 10
        self.power = power

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
    def move(self, vel):
        self.x -= vel

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

def checkCollision(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y= int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def outOfScreen(obj):
    return obj.y < 0 or obj.y > HEIGHT

def main():
    font = pg.font.SysFont("comicsans", 60)
    run = True
    clock = pg.time.Clock()
    wave = 0
    lives = 0
    # Define the vertical border position
    BORDER_X = WIDTH // 2  # Middle of the screen
    ALIEN_ROW = 4
    ALIEN_COL = 1

    MAP_STATE = {1: "You Win!!", -1: "You lost!!"}
    state = 0  # default state
    print(MAP_STATE[-1])

    player = Player()

    aliens = []
    def spawn_aliens(wave):
        for i in range(ALIEN_ROW):
            cur_row = HEIGHT// 2 - ((ALIEN_ROW - 1) * 120 // 2) + (i * 120)
            for j in range(1, ALIEN_COL + 1):
                new_alien = Alien(WIDTH - 100 - (j * 200)/ (ALIEN_COL + 1), cur_row, 1)
                aliens.append(new_alien)

    def redraw_window():
        game_surface = pg.Surface((WIDTH, HEIGHT))
        game_surface.blit(BACKGROUND_IMG, (0, 0))

        player.draw(game_surface)
        for alien in aliens:
            alien.draw(game_surface)
            alien.move()

        if state != 0:
            lost_label = font.render(MAP_STATE[state], 1, (255, 255, 255))
            game_surface.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        lost_label = font.render("Wave " + str(wave), 1, (255, 255, 255))
        game_surface.blit(lost_label, (WIDTH - lost_label.get_width() - 10, 10))

        lost_label = font.render(" " + str(lives), 1, (255, 255, 255))
        game_surface.blit(lost_label, (10, 10))

        WINDOW.blit(game_surface, (0, 0))
        pg.display.update()

    spawn_aliens(wave)
    while run:  # Main game loop
        clock.tick(FPS)
        redraw_window()

        # check for any event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

        keys = pg.key.get_pressed()
        if keys[pg.K_a] and player.x - player.VELOCITY > 0:  # left
            player.move("left")
        if keys[pg.K_d] and player.x + player.VELOCITY + player.get_width() < BORDER_X:  # right
            player.move("right")
        if keys[pg.K_w] and player.y - player.VELOCITY > 0: #up
            player.move("up")
        if keys[pg.K_s] and player.y + player.VELOCITY + player.get_height() < HEIGHT: #down
            player.move("down")
        if keys[pg.K_SPACE]:  # shoot
            player.shoot()


        player.move_lasers(-20, aliens)

        for alien in aliens:  # Check if any alien collides with player
            if checkCollision(alien, player):
                state = -1
            elif outOfScreen(alien):
                aliens.remove(alien)
                if lives == 0:
                    state = -1
                else:
                    lives -= 1

        if len(aliens) == 0:  # Check if there are any aliens left
            if wave == 2:
                state = 1
            else:
                wave += 1
                spawn_aliens(wave)


main()
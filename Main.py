import pygame
import sys

# Initialise pygame
pygame.init()

# Create the Screen.
screen = pygame.display.set_mode((500, 1080), pygame.RESIZABLE)

# Set max frames to 60
clock = pygame.time.Clock()
fps = 60

text_font = pygame.font.Font(None, 150)
button_text_font = pygame.font.Font(None, 50)
fps_font = pygame.font.Font(None, 30)

class Button():
    def __init__(self, text, x_pos, y_pos, enabled, action=None):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.action = action
        self.width, self.height = 200, 50
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def draw(self):
        # Button color change on hover
        color = "Dark Grey" if self.check_hover() else "Light Grey"
        pygame.draw.rect(screen, color, self.rect, 0, 5)
        pygame.draw.rect(screen, "black", self.rect, 2, 5)

        button_text = button_text_font.render(self.text, True, "White")
        screen.blit(button_text, (self.x_pos + 10, self.y_pos + 10))

    def check_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]  # Left mouse button

        if click and self.rect.collidepoint(mouse_pos) and self.enabled:
            if self.action:
                self.action()
            return True
        return False

def get_image(sheet, x, y, width, height):
    #Extracts a frame from a sprite sheet

    image = pygame.Surface((width, height), pygame.SRCALPHA)  
    image.blit(sheet, (0, 0), (x, y, width, height))
    return image


def select_level_window():
    select_level_screen = True
    while select_level_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                select_level_screen = False  # Press ESC to return to main menu
        

        screen.fill((50, 50, 50))
        text_surface = text_font.render("Level select:", True, "White")
        screen.blit(text_surface, (100, 100))

        Level_1_button = Button("Level 1", 150, 400, True, Level_1)
        Level_1_button.draw()

        back_button = Button("Back",50,1000, True)
        back_button.draw()

        Level_1_button.check_click()

        draw_fps()
        pygame.display.update()
        clock.tick(fps)


class Player:
    def __init__(self, x, y):
        self.image = get_image(pygame.image.load("assets/sprite_baboonMonk_strip8.png"), 0, 0, 70, 80)
        self.rect = self.image.get_rect(midbottom=(x, y))  
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 8
        self.jump_power = -20
        self.gravity = 1.0
        self.on_ground = False
        
    def apply_gravity(self):
        if not self.on_ground:
            self.velocity.y += self.gravity

    def jump(self):
        if self.on_ground:
            self.velocity.y = self.jump_power
            self.on_ground = False

    def move(self, platforms):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_d]:
            self.velocity.x = self.speed

        self.rect.x += self.velocity.x
        self.check_collisions_x(platforms)

        self.apply_gravity()
        self.rect.y += self.velocity.y
        self.check_collisions_y(platforms)

        # Check if the player falls off the screen
        if self.rect.top > screen.get_height():
            self.respawn()

    def check_collisions_x(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity.y > 0:  # Falling down
                    self.rect.bottom = platform.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:  # Hitting ceiling
                    self.rect.top = platform.bottom
                    self.velocity.y = 0


    def check_collisions_y(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = platform.bottom
                    self.velocity.y = 0

    def respawn(self):
        self.rect.midbottom = (100, 600)
        self.velocity = pygame.Vector2(0, 0)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)


def Level_1():
    platforms = [
        pygame.Rect((100, 620), (300, 20)),
        pygame.Rect((500, 520), (200, 20)),
        pygame.Rect((500,720),(200,20)),
        pygame.Rect((500,300),(200,20)),
        pygame.Rect((800,400),(200,20))

    ]


    coins = []
    for platform in platforms:
        coin_x = platform.centerx - coin_image.get_width() // 2
        coin_y = platform.top - coin_image.get_height()
        coins.append(pygame.Rect(coin_x, coin_y, coin_image.get_width(), coin_image.get_height()))


    player = Player(100, 600)  

    level_1 = True
    while level_1:
        screen.fill((0, 0, 0))
        screen.blit(forest_background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level_1 = False
                elif event.key == pygame.K_SPACE:
                    player.jump()
        
        player.move(platforms)
        player.draw()

        for platform in platforms:
            pygame.draw.rect(screen, (100, 100, 100), platform)

        coins = [coin for coin in coins if not player.rect.colliderect(coin)]

        # Draw coins
        for coin in coins:
            screen.blit(coin_image, (coin.x, coin.y))

        draw_fps()
        pygame.display.update()
        clock.tick(fps)






def quit_game():
    pygame.quit()
    sys.exit()

# Load background image
forest_background = pygame.image.load("assets/Background/forest_background.png")


# Load and scale coin image
original_coin_image = pygame.image.load("assets/Items/7b7be946-8479-4be9-a792-3e705bdad2c8.png")
coin_image = pygame.transform.scale(original_coin_image, (30, 30))  # Resize to 30x30 pixels


# Load background music
pygame.mixer.music.load("assets/Music/playful-catch-254930.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

def draw_fps():
    """Displays the FPS counter on the screen."""
    fps_value = str(int(clock.get_fps()))  
    fps_surface = fps_font.render(f"FPS: {fps_value}", True, "White")
    screen.blit(fps_surface, (10, 10)) 


text_surface = text_font.render("Welcome", 1, "White")


# Create buttons once, instead of inside the loop
start_button = Button("Start Game", 150, 300, True, select_level_window)
option_button = Button("Options", 150, 400, True)
quit_button = Button("Quit", 150, 500, True, quit_game)




# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(forest_background, (0, 0))
    screen.blit(text_surface, (150, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_button.check_click()
            option_button.check_click()
            quit_button.check_click()

    # Draw buttons
    start_button.draw()
    option_button.draw()
    quit_button.draw()

    draw_fps()

    pygame.display.update()
    clock.tick(fps)

    clock.get_fps()


import pygame
import sys

# Initialise pygame
pygame.init()

# Create the Screen.
screen = pygame.display.set_mode((500, 1080), pygame.RESIZABLE)

# Set max frames to 60
clock = pygame.time.Clock()
fps = 30

# Load fonts
text_font = pygame.font.Font(None, 150)
button_text_font = pygame.font.Font(None, 50)
fps_font = pygame.font.Font(None, 30)

# Load background image
forest_background = pygame.image.load("assets/Background/forest_background.png")

# Load background music
pygame.mixer.music.load("assets/Music/playful-catch-254930.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

class Button:
    def __init__(self, text, x_pos, y_pos, enabled, action=None):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.action = action
        self.width, self.height = 200, 50
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def draw(self):
        color = "Dark Grey" if self.check_hover() else "Light Grey"
        pygame.draw.rect(screen, color, self.rect, 0, 5)
        pygame.draw.rect(screen, "black", self.rect, 2, 5)

        button_text = button_text_font.render(self.text, True, "White")
        screen.blit(button_text, (self.x_pos + 10, self.y_pos + 10))

    def check_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def check_click(self):
        if pygame.mouse.get_pressed()[0] and self.enabled and self.check_hover():
            if self.action:
                self.action()

def get_image(sheet, x, y, width, height):
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
                select_level_screen = False  

        screen.fill((50, 50, 50))
        screen.blit(forest_background, (0, 0))

        text_surface = text_font.render("Level select:", True, "White")
        screen.blit(text_surface, (100, 100))

        level_1_button = Button("Level 1", 150, 400, True, Level_1)
        back_button = Button("Back", 50, 1000, True, lambda: exit_select_level())

        level_1_button.draw()
        back_button.draw()

        level_1_button.check_click()
        back_button.check_click()

        draw_fps()
        pygame.display.update()
        clock.tick(fps)

def exit_select_level():
    global running
    running = False

class Player:
    def __init__(self, x, y):
        self.sprite_sheet = pygame.image.load("assets/sprite_baboonMonk_strip8.png")
        self.image = get_image(self.sprite_sheet, 0, 0, 70, 80)
        self.rect = self.image.get_rect(midbottom=(x, y))  
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.9
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

        if self.rect.top > screen.get_height():
            self.respawn()

    def check_collisions_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity.x > 0:  
                    self.rect.right = platform.left
                elif self.velocity.x < 0:  
                    self.rect.left = platform.right

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
        pygame.Rect(100, 620, 300, 20),
        pygame.Rect(400, 520, 200, 20),
        pygame.Rect(50, 720, 400, 20)
    ]

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

        draw_fps()
        pygame.display.update()
        clock.tick(fps)

def quit_game():
    pygame.quit()
    sys.exit()

def draw_fps():
    fps_value = str(int(clock.get_fps()))  
    fps_surface = fps_font.render(f"FPS: {fps_value}", True, "White")
    screen.blit(fps_surface, (10, 10)) 

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(forest_background, (0, 0))

    start_button = Button("Start Game", 150, 300, True, select_level_window)
    quit_button = Button("Quit", 150, 500, True, quit_game)

    start_button.draw()
    quit_button.draw()

    start_button.check_click()
    quit_button.check_click()

    draw_fps()
    pygame.display.update()
    clock.tick(fps)

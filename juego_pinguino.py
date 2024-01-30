# Librerías
import pygame
import random

# Inicio de pygame
pygame.init()

# Paleta de colores
Black = (0, 0, 0)
White = (255,255,255)

# Configuración de ventana
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Penguin")
clock = pygame.time.Clock()
fondo = pygame.image.load("Paisaje.jpg").convert()

# Fuente de texto
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, White)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Pantalla de inicio
def start_screen():
    screen.blit(fondo, [0, 0])
    draw_text(screen, "PENGUIN", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Press SPACE to continue", 17, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                waiting = False

# Definición de jugador
class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("pinguino.png").convert(), (60, 60))
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 0

    def changespeed(self, x):
        self.speed_x += x

    def update(self):
        self.rect.x += self.speed_x
        player.rect.y = 450

# Definición de enemigo
class Enemigo (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("destello.png").convert(), (40, 40))
        self.image.set_colorkey(White)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25 :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-130, -70)
            self.speedy = 3

# Definición de recompensa
class Pastel (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("torta.png").convert(), (40, 40))
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25 :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-130, -70)
            self.speedy = 3

# Seteo de aparición de objetos
ADDENEMY = pygame.USEREVENT + 1
ADDPASTEL = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, 2000)
pygame.time.set_timer(ADDPASTEL, 2000)

# Pantalla de juego finalizado
def gameover_screen():
    screen.fill(Black)
    draw_text(screen, "GAME OVER", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Score = ", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, str(score), 27, 470, HEIGHT // 2)
    draw_text(screen, "Press SPACE to restart", 17, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                waiting = False

# Bucle principal de juego
game_state = "start_menu"

if game_state:
    start_screen()
    
game_over = True
done = False

while not done:
    if game_over:
        player = Player()
        all_sprite_list = pygame.sprite.Group()
        rayo_list = pygame.sprite.Group()
        pastel_list = pygame.sprite.Group()
        all_sprite_list.add(player)
        
        for i in range(3):
            rayo = Enemigo()
            rayo_list.add(rayo)
            all_sprite_list.add(rayo)
            
        for i in range(3):
            pastel = Pastel()
            pastel_list.add(pastel)
            all_sprite_list.add(pastel)
        
        game_over = False
        lives = 5
        score = 0
        
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == ADDENEMY:
            new_enemy = Enemigo()
            rayo_list.add(new_enemy)
            all_sprite_list.add(new_enemy)
        elif event.type == ADDPASTEL:
            new_pastel = Pastel()
            pastel_list.add(new_pastel)
            all_sprite_list.add(new_pastel)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3)
            if event.key == pygame.K_RIGHT:
                player.changespeed(3)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-3)


    all_sprite_list.update() 

    
    pastel_hit_list = pygame.sprite.spritecollide(player, pastel_list, True)
    for pastel in pastel_hit_list:
        score += 1

        
    rayo_hit_list = pygame.sprite.spritecollide(player, rayo_list, True)
    for rayo in rayo_hit_list:
        lives -= 1
        if lives <= 0:
            game_over = True
            gameover_screen()


    screen.blit(fondo, [0, 0])

    all_sprite_list.draw(screen)
    draw_text(screen, "Score = ", 25, 50, 10)
    draw_text(screen, str(score), 25, 100, 10)
    life = pygame.image.load("corazon.png").convert()
    life.set_colorkey(White)
    screen.blit(life, (565, 10))
    draw_text(screen, str(lives), 25, 600, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
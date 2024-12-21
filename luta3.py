import pygame
import random
import math

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ARENA_RADIUS = 250

# Configurações dos personagens
CHARACTER_RADIUS = 20
SPEED = 2
PUSH_FORCE = 3  # Força de empurrão normal
SPECIAL_PUSH_FORCE = 10  # Força do ataque especial
ATTACK_COOLDOWN = 1000  # Tempo entre ataques especiais (em milissegundos)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Luta de Personagens")
clock = pygame.time.Clock()

# Classe para o Personagem
class Character:
    def __init__(self, x, y, color, is_ai=False):
        self.x = x
        self.y = y
        self.color = color
        self.is_ai = is_ai
        self.last_attack_time = 0  # Para controlar o cooldown do ataque especial

    def move(self, target=None):
        if self.is_ai and target:
            # Movimento da IA em direção ao alvo
            dx = target.x - self.x
            dy = target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.x += (dx / dist) * SPEED
                self.y += (dy / dist) * SPEED
        else:
            # Controle manual (WASD)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.y -= SPEED
            if keys[pygame.K_s]:
                self.y += SPEED
            if keys[pygame.K_a]:
                self.x -= SPEED
            if keys[pygame.K_d]:
                self.x += SPEED

    def attack(self, opponent):
        # Resolve colisão como ataque especial
        dx = opponent.x - self.x
        dy = opponent.y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:  # Evita divisão por zero
            push_x = (dx / distance) * SPECIAL_PUSH_FORCE
            push_y = (dy / distance) * SPECIAL_PUSH_FORCE

            # Aplica a força do ataque especial no oponente
            opponent.x += push_x
            opponent.y += push_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), CHARACTER_RADIUS)

# Função para verificar colisão entre dois personagens
def check_collision(char1, char2):
    dx = char2.x - char1.x
    dy = char2.y - char1.y
    distance = math.hypot(dx, dy)
    return distance < (CHARACTER_RADIUS * 2)

# Função para resolver colisão (empurrão normal)
def resolve_collision(char1, char2):
    dx = char2.x - char1.x
    dy = char2.y - char1.y
    distance = math.hypot(dx, dy)

    if distance > 0:  # Evita divisão por zero
        overlap = (CHARACTER_RADIUS * 2 - distance) / 2
        push_x = (dx / distance) * overlap * PUSH_FORCE
        push_y = (dy / distance) * overlap * PUSH_FORCE

        # Empurra os personagens em direções opostas
        char1.x -= push_x
        char1.y -= push_y
        char2.x += push_x
        char2.y += push_y

# Função para verificar se o personagem está dentro da arena
def is_inside_arena(x, y):
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    dist = math.hypot(x - center_x, y - center_y)
    return dist <= ARENA_RADIUS

# Configuração inicial
player = Character(300, 300, BLUE, is_ai=False)
opponent = Character(500, 300, RED, is_ai=True)
running = True

while running:
    screen.fill(WHITE)
    pygame.draw.circle(screen, GRAY, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), ARENA_RADIUS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento dos personagens
    player.move()
    opponent.move(player)

    # Verifica colisão entre os personagens
    if check_collision(player, opponent):
        resolve_collision(player, opponent)

    # Verifica cooldown para ataque especial
    current_time = pygame.time.get_ticks()
    if current_time - player.last_attack_time > ATTACK_COOLDOWN:
        player.attack(opponent)
        player.last_attack_time = current_time

    if current_time - opponent.last_attack_time > ATTACK_COOLDOWN:
        opponent.attack(player)
        opponent.last_attack_time = current_time

    # Verifica se os personagens ainda estão dentro da arena
    if not is_inside_arena(player.x, player.y):
        print("Oponente venceu!")
        running = False
    if not is_inside_arena(opponent.x, opponent.y):
        print("Você venceu!")
        running = False

    # Desenho dos personagens
    player.draw(screen)
    opponent.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

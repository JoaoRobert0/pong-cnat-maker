import pygame
import sys
import random

# Configura├º├úo geral do Pygame
pygame.init()
clock = pygame.time.Clock()

# Janela principal (tela cheia)
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Pong - Dois Jogadores")

# Cores
light_grey = (200, 200, 200)
bg_color = pygame.Color("grey12")

# Ret├óngulos do jogo
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)  # Jogador 1
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)  # Jogador 2

# Vari├íveis do jogo
ball_speed_x = 10 * random.choice((1, -1))
ball_speed_y = 10 * random.choice((1, -1))
num_houses = 10
house_height = screen_height // num_houses

# Posi├º├Áes dos jogadores
player_current_house = num_houses // 2  # Come├ºa no meio
opponent_current_house = num_houses // 2

# Pontua├º├Áes
player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None, 36)

# Controle do jogo
game_active = True
vencedor = None  # Define o vencedor

# Definindo uma constante para velocidade do movimento
MOVE_SPEED = 0.25  # Mude esse valor para ajustar a velocidade

# Fun├º├Áes do jogo
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, game_active, vencedor
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        player_score += 1
        ball_start()
    if ball.right >= screen_width:
        opponent_score += 1
        ball_start()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    if player_score >= 10:
        game_active = False
        vencedor = "Jogador 2"
    elif opponent_score >= 10:
        game_active = False
        vencedor = "Jogador 1"

def ball_start():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))

def update_positions():
    player.top = player_current_house * house_height
    player.top = max(0, min(player.top, screen_height - player.height))
    opponent.top = opponent_current_house * house_height
    opponent.top = max(0, min(opponent.top, screen_height - opponent.height))

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controle do movimento dos jogadores
    keys = pygame.key.get_pressed()

    # Jogador 1 (esquerda)
    if keys[pygame.K_UP]:
        opponent_current_house = max(0, opponent_current_house - MOVE_SPEED)
    elif keys[pygame.K_DOWN]:
        opponent_current_house = min(num_houses - 1, opponent_current_house + MOVE_SPEED)

    # Jogador 2 (direita)
    if keys[pygame.K_LEFT]:
        player_current_house = max(0, player_current_house - MOVE_SPEED)
    elif keys[pygame.K_RIGHT]:
        player_current_house = min(num_houses - 1, player_current_house + MOVE_SPEED)

    if game_active:
        ball_animation()
        update_positions()
    else:
        screen.fill(bg_color)
        vencedor_text = game_font.render(f"{vencedor} venceu!", True, light_grey)
        screen.blit(vencedor_text, (screen_width / 2 - vencedor_text.get_width() / 2, screen_height / 2))
        pygame.display.flip()
        continue

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    player_text = game_font.render(f"{player_score}", True, light_grey)
    opponent_text = game_font.render(f"{opponent_score}", True, light_grey)
    screen.blit(player_text, (screen_width / 2 + 20, 20))
    screen.blit(opponent_text, (screen_width / 2 - 40, 20))

    pygame.display.flip()
    clock.tick(60)

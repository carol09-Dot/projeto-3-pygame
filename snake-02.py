import pygame
import random
import sys

pygame.init()

# --- 1. CONFIGURAÇÕES ---
LARGURA, ALTURA = 600, 400
TAMANHO_BLOCO = 20
FPS = 12

# Cores do Arquivo das Sombras
COR_FUNDO = (15, 0, 5)
COR_CABECA = (179, 0, 45)
COR_CORPO = (100, 0, 20)
COR_COMIDA = (255, 215, 0)
COR_TEXTO = (200, 200, 200)

# Inicialização da Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("O Despertar da Serpente")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("georgia", 25)

# --- 2. ESTADO INICIAL DO JOGO ---
x, y = LARGURA // 2, ALTURA // 2
vel_x, vel_y = 0, 0
cobra = [[x, y]]
pontos = 0

# Função simples para gerar comida
comida = [random.randrange(0, LARGURA, TAMANHO_BLOCO), 
          random.randrange(0, ALTURA, TAMANHO_BLOCO)]

# --- 3. LOOP PRINCIPAL ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and vel_y == 0:
                vel_x, vel_y = 0, -TAMANHO_BLOCO
            elif evento.key == pygame.K_DOWN and vel_y == 0:
                vel_x, vel_y = 0, TAMANHO_BLOCO
            elif evento.key == pygame.K_LEFT and vel_x == 0:
                vel_x, vel_y = -TAMANHO_BLOCO, 0
            elif evento.key == pygame.K_RIGHT and vel_x == 0:
                vel_x, vel_y = TAMANHO_BLOCO, 0

    # Movimentação
    x += vel_x
    y += vel_y

    # --- NOVIDADE: ATRAVESSAR PAREDES ---
    if x < 0: x = LARGURA - TAMANHO_BLOCO
    elif x >= LARGURA: x = 0
    if y < 0: y = ALTURA - TAMANHO_BLOCO
    elif y >= ALTURA: y = 0

    # Adiciona nova cabeça
    cobra.insert(0, [x, y])

    # Sistema de Comida / Crescimento
    if x == comida[0] and y == comida[1]:
        pontos += 10
        comida = [random.randrange(0, LARGURA, TAMANHO_BLOCO), 
                  random.randrange(0, ALTURA, TAMANHO_BLOCO)]
    else:
        if vel_x != 0 or vel_y != 0: # Só remove a cauda se a cobra estiver andando
            cobra.pop()

    # Colisão com o Próprio Corpo
    for seg in cobra[1:]:
        if seg == [x, y] and (vel_x != 0 or vel_y != 0):
            print(f"Game Over! Almas coletadas: {pontos}")
            pygame.quit()
            sys.exit()

    # --- 4. DESENHO ---
    tela.fill(COR_FUNDO)

    # Desenha Comida
    pygame.draw.rect(tela, COR_COMIDA, (comida[0], comida[1], TAMANHO_BLOCO, TAMANHO_BLOCO))
    
    # Desenha Cobra
    for i, seg in enumerate(cobra):
        cor = COR_CABECA if i == 0 else COR_CORPO
        # O -1 cria um contorno escuro entre os gomos da cobra
        pygame.draw.rect(tela, cor, (seg[0], seg[1], TAMANHO_BLOCO - 1, TAMANHO_BLOCO - 1))

    # Placar
    texto = fonte.render(f"Almas Coletadas: {pontos}", True, COR_TEXTO)
    tela.blit(texto, [10, 10])

    pygame.display.update()
    relogio.tick(FPS)
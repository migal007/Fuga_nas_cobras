import pygame
import random
import math
import sys
import os

pygame.init()
pygame.mixer.init()

# --------------------
# FUNÇÃO CAMINHO (EXE)
# --------------------
def caminho(rel):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, rel)

# --------------------
# CONFIG
# --------------------
LARGURA, ALTURA = 1000, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobra Game")
clock = pygame.time.Clock()

# --------------------
# CORES
# --------------------
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 200, 0)
VERMELHO = (200, 50, 50)

# --------------------
# IMAGENS
# --------------------
inicio_img = pygame.transform.scale(
    pygame.image.load(caminho("inicio.png")).convert(), (LARGURA, ALTURA)
)

player_img = pygame.transform.scale(
    pygame.image.load(caminho("player.png")).convert_alpha(), (50, 50)
)

cobra_base_img = pygame.transform.scale(
    pygame.image.load(caminho("cobra.png")).convert_alpha(), (80, 40)
)

boss_img = pygame.transform.scale(
    pygame.image.load(caminho("boss.png")).convert_alpha(), (160, 120)
)

missil_img = pygame.transform.scale(
    pygame.image.load(caminho("missil.png")).convert_alpha(), (40, 20)
)

anticobra_img = pygame.transform.scale(
    pygame.image.load(caminho("anticobra.png")).convert_alpha(), (60, 60)
)

# --------------------
# SONS E MÚSICAS
# --------------------
som_anticobra = pygame.mixer.Sound(caminho("som_anticobra.ogg"))

def musica_normal():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(caminho("musica1.ogg"))
    pygame.mixer.music.play(-1)

def musica_boss():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(caminho("musica2.ogg"))
    pygame.mixer.music.play(-1)

# --------------------
# FONTES
# --------------------
fonte_grande = pygame.font.SysFont(None, 80)
fonte_media = pygame.font.SysFont(None, 40)
fonte_pequena = pygame.font.SysFont(None, 28)

# --------------------
# FUNÇÕES
# --------------------
def criar_cobras(qtd):
    return [
        pygame.Rect(
            random.randint(400, 900),
            random.randint(50, 550),
            80, 40
        ) for _ in range(qtd)
    ]

def resetar_fase():
    global cobras, boss_vivo, boss_rect, boss_vida
    global misseis, anticobras, boss_sentido, tempo_fase

    cobras = []
    misseis = []
    anticobras = []
    tempo_fase = pygame.time.get_ticks()

    if nivel % 10 == 0:
        boss_vivo = True
        boss_rect = pygame.Rect(800, 200, 160, 120)
        boss_vida = 150
        boss_sentido = 1
        musica_boss()

        for _ in range(6):
            anticobras.append(
                pygame.Rect(
                    random.randint(100, 600),
                    random.randint(50, 500),
                    60, 60
                )
            )
    else:
        boss_vivo = False
        musica_normal()
        cobras.extend(criar_cobras(nivel))

# --------------------
# VARIÁVEIS
# --------------------
estado = "inicio"

player = pygame.Rect(100, 300, 50, 50)
vel_player = 5

nivel = 1
tempo_fase = 0

# ⏱️ TEMPO 2x MAIS RÁPIDO (30s)
DURACAO_FASE = 30000  

# 🐍 VELOCIDADE DAS COBRAS (mais rápido)
VEL_COBRA = 4

resetar_fase()

# --------------------
# LOOP PRINCIPAL
# --------------------
while True:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if estado == "inicio":
                if botao_start.collidepoint(evento.pos):
                    estado = "jogo"
                    nivel = 1
                    resetar_fase()

        if evento.type == pygame.KEYDOWN:
            if estado == "gameover" and evento.key == pygame.K_r:
                estado = "inicio"

    # ====================
    # TELA INICIAL
    # ====================
    if estado == "inicio":
        tela.blit(inicio_img, (0, 0))

        titulo = fonte_grande.render("COBRA GAME", True, BRANCO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 120))

        texto_start = fonte_media.render("START", True, BRANCO)
        botao_start = texto_start.get_rect(center=(LARGURA // 2, 320))
        tela.blit(texto_start, botao_start)

        tela.blit(
            fonte_pequena.render("Clique em START para jogar", True, BRANCO),
            (LARGURA // 2 - 140, 380)
        )

        pygame.display.update()
        continue

    # ====================
    # GAME OVER
    # ====================
    if estado == "gameover":
        tela.fill(PRETO)
        tela.blit(fonte_grande.render("GAME OVER", True, BRANCO), (320, 220))
        tela.blit(
            fonte_media.render("Pressione R para voltar", True, BRANCO),
            (300, 300)
        )
        pygame.display.update()
        continue

    # ====================
    # JOGO
    # ====================
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        player.y -= vel_player
    if teclas[pygame.K_s]:
        player.y += vel_player
    if teclas[pygame.K_a]:
        player.x -= vel_player
    if teclas[pygame.K_d]:
        player.x += vel_player

    player.clamp_ip(tela.get_rect())

    if pygame.time.get_ticks() - tempo_fase >= DURACAO_FASE:
        nivel += 1
        resetar_fase()

    cobras_desenho = []
    for cobra in cobras[:]:
        dx = player.centerx - cobra.centerx
        dy = player.centery - cobra.centery
        dist = math.hypot(dx, dy)

        if dist != 0:
            cobra.x += int(VEL_COBRA * dx / dist)
            cobra.y += int(VEL_COBRA * dy / dist)

        angulo = math.degrees(math.atan2(-dy, dx))
        img = pygame.transform.rotate(cobra_base_img, angulo)
        rect = img.get_rect(center=cobra.center)
        cobras_desenho.append((img, rect))

        if cobra.colliderect(player):
            estado = "gameover"

    if boss_vivo:
        boss_rect.y += 2 * boss_sentido
        if boss_rect.top <= 0 or boss_rect.bottom >= ALTURA:
            boss_sentido *= -1

        if random.randint(0, 50) == 0:
            misseis.append(
                pygame.Rect(boss_rect.left - 20, boss_rect.centery, 40, 20)
            )

    for missil in misseis[:]:
        missil.x -= 7
        if missil.colliderect(player):
            estado = "gameover"
        if not tela.get_rect().colliderect(missil):
            misseis.remove(missil)

    for anti in anticobras[:]:
        if player.colliderect(anti):
            som_anticobra.play()
            boss_vida -= 5
            anticobras.remove(anti)

    if boss_vivo and boss_vida <= 0:
        nivel += 1
        resetar_fase()

    tela.fill(PRETO)
    tela.blit(player_img, player)

    for img, rect in cobras_desenho:
        tela.blit(img, rect)

    if boss_vivo:
        tela.blit(boss_img, boss_rect)
        pygame.draw.rect(tela, VERMELHO, (boss_rect.x, boss_rect.y - 12, 160, 10))
        pygame.draw.rect(
            tela, VERDE,
            (boss_rect.x, boss_rect.y - 12, int(160 * boss_vida / 150), 10)
        )

    for missil in misseis:
        tela.blit(missil_img, missil)

    for anti in anticobras:
        tela.blit(anticobra_img, anti)

    tela.blit(
        fonte_pequena.render(f"Fase {nivel}", True, BRANCO),
        (20, 20)
    )

    tempo_restante = max(
        0, (DURACAO_FASE - (pygame.time.get_ticks() - tempo_fase)) // 1000
    )
    tela.blit(
        fonte_pequena.render(f"Tempo: {tempo_restante}s", True, BRANCO),
        (20, 45)
    )

    pygame.display.update()

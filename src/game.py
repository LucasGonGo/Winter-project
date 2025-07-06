import os
import random
import pygame
import math
import settings
from card import Carta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSET_DIR = os.path.join(BASE_DIR, 'assets')
IMG_DIR = os.path.join(ASSET_DIR, 'images')
DATA_DIR = os.path.join(ASSET_DIR, 'data')
SOUND_DIR = os.path.join(ASSET_DIR, 'sounds')

def desenhar_botao_voltar(screen, font):
    botao_cor = (200, 50, 50) 
    botao_cor_hover = (255, 80, 80)
    texto_cor = (255, 255, 255)

    botao_rect = pygame.Rect(1180, 665, 90, 50)  # posição fixa no canto superior direito

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicado = pygame.mouse.get_pressed()[0]

    # Muda cor se o mouse estiver sobre o botão
    if botao_rect.collidepoint(mouse_pos):
        cor_atual = botao_cor_hover
        clicado = mouse_clicado
    else:
        cor_atual = botao_cor
        clicado = False

    pygame.draw.rect(screen, cor_atual, botao_rect, border_radius=5)

    texto_sair = font.render("Voltar", True, texto_cor)
    texto_rect = texto_sair.get_rect(center=botao_rect.center)
    screen.blit(texto_sair, texto_rect)

    return clicado and botao_rect.collidepoint(mouse_pos)


pygame.mixer.init()
hit_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'acerto.wav'))

def play(sound):
    if settings.sound_on:
        sound.play()

tam_carta = (179, 256)
linhas = 2
espaco = 20

def carregar_desafios():
    desafios = []
    caminho = os.path.join(DATA_DIR, 'desafios.txt')
    with open(caminho, encoding='utf-8') as f:
        for linha in f:
            if linha.strip():
                try:
                    texto, nome_arquivo = linha.strip().split(';')
                    desafios.append({'frase': texto, 'correta': nome_arquivo})
                except ValueError:
                    print(f"Linha ignorada por formato incorreto: {linha}")
    return desafios

MAX_COLS = 2
MAX_CARDS = 4

def criar_cartas(nomes_cartas):
    total = min(len(nomes_cartas), MAX_CARDS)

    colunas = min(MAX_COLS, total)
    linhas = math.ceil(total/colunas)
    
    largura_grade = colunas * tam_carta[0] + (colunas - 1) * espaco
    altura_grade = linhas * tam_carta[1] + (linhas - 1) * espaco

    start_x = (1280 - largura_grade) // 2
    start_y = ((720 - altura_grade) // 2) + 40

    cartas = []

    idx = 0

    for idx, nome in enumerate(nomes_cartas[:total]):
        coluna = idx % colunas
        linha  = idx // colunas

        img_path = os.path.join(IMG_DIR, nome)
        imagem   = pygame.image.load(img_path).convert_alpha()

        x = start_x + coluna * (tam_carta[0] + espaco)
        y = start_y + linha  * (tam_carta[1] + espaco)

        cartas.append(Carta(imagem, (x, y), escala=tam_carta, id=nome))

    return cartas

def rodar_jogo(screen, clock):
    desafios = carregar_desafios()
    todas_imagens = [f for f in os.listdir(IMG_DIR) if f.endswith('.png')]
    font = pygame.font.SysFont('couriernew', 34)

    player_wins = 0
    running = True

    while running:
        # — Escolhe desafio e monta 4 cartas —
        desafio_atual     = random.choice(desafios)
        frase_para_mostrar = desafio_atual['frase']
        carta_correta_nome = desafio_atual['correta']

        # 3 distrações diferentes da correta
        distracoes = random.sample([f for f in todas_imagens
                                    if f != carta_correta_nome], 3)
        nomes_cartas_round = [carta_correta_nome] + distracoes
        random.shuffle(nomes_cartas_round)

        cartas = criar_cartas(nomes_cartas_round)

        rodada_finalizada = False
        tempo_rodada_finalizado = None

        # ----- loop principal da rodada -----
        while True:
            screen.fill((163, 177, 138))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif (event.type == pygame.MOUSEBUTTONDOWN
                      and not rodada_finalizada):
                    for carta in cartas:
                        if carta.colidiu_com_ponto(event.pos):
                            carta.selecionada = True
                            rodada_finalizada = True
                            tempo_rodada_finalizado = pygame.time.get_ticks()

                            if carta.id == carta_correta_nome:
                                carta.resultado = "correta"
                                play(hit_sound)
                                player_wins += 1
                            else:
                                carta.resultado = "errada"
                                for c in cartas:
                                    if c.id == carta_correta_nome:
                                        c.resultado = "correta"
                            break

            # Sai do laço interno quando for hora da próxima rodada
            if not running:
                break
            if (rodada_finalizada
                and (pygame.time.get_ticks() - tempo_rodada_finalizado) > 1000):
                break   # próxima rodada

            # Desenha textos, cartas e botão:
            texto_render = font.render(frase_para_mostrar, True, 'black')
            screen.blit(texto_render,
                        texto_render.get_rect(center=(640,40)))

            vitorias_render = font.render(f"Vitórias: {player_wins}",
                                          True, 'black')
            screen.blit(vitorias_render, (10,680))

            for carta in cartas:
                carta.desenhar(screen)

            if desenhar_botao_voltar(screen, pygame.font.SysFont('couriernew', 20 )):
                return 'voltar_menu'

            pygame.display.flip()
            clock.tick(60)

    return 'sair'


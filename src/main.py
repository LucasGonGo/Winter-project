import os
import pygame
import random
from card import Carta

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSET_DIR = os.path.join(BASE_DIR, 'assets')
IMG_DIR = os.path.join(ASSET_DIR, 'images')
DATA_DIR = os.path.join(ASSET_DIR, 'data')

# Carrega desafios do arquivo
def carregar_desafios(caminho):
    desafios = []
    with open(caminho, encoding='utf-8') as f:
        for linha in f:
            if linha.strip():
                texto, nome_arquivo = linha.strip().split(';')
                desafios.append({'frase': texto, 'correta': nome_arquivo})
    return desafios

desafios = carregar_desafios(os.path.join(DATA_DIR, 'desafios.txt'))

tam_carta = (100, 140)
linhas = 2
espaco = 20

# Função para criar as cartas e posicionar na tela
def criar_cartas(nomes_cartas):
    colunas = len(nomes_cartas) // 2 + len(nomes_cartas) % 2
    largura_grade = colunas * tam_carta[0] + (colunas - 1) * espaco
    altura_grade = linhas * tam_carta[1] + (linhas - 1) * espaco

    start_x = (1280 - largura_grade) // 2
    start_y = (720 - altura_grade) // 2

    cartas = []
    idx = 0

    for linha in range(linhas):
        for coluna in range(colunas):
            if idx >= len(nomes_cartas):
                break
            nome = nomes_cartas[idx]
            img_path = os.path.join(IMG_DIR, nome)
            imagem = pygame.image.load(img_path).convert_alpha()

            x = start_x + coluna * (tam_carta[0] + espaco)
            y = start_y + linha * (tam_carta[1] + espaco)

            carta = Carta(imagem, (x, y), escala=tam_carta, id=nome)
            cartas.append(carta)
            idx += 1
    return cartas

# Escolhe desafio inicial
desafio_atual = random.choice(desafios)
frase_para_mostrar = desafio_atual['frase']
carta_correta_nome = desafio_atual['correta']

# Lista de cartas
nomes_cartas = [f for f in os.listdir(IMG_DIR) if f.endswith('.png')]
random.shuffle(nomes_cartas)
cartas = criar_cartas(nomes_cartas)

rodada_finalizada = False

# Fonte para mostrar a frase
font = pygame.font.SysFont(None, 36)

while running:
    screen.fill((157, 141, 241))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not rodada_finalizada:
            for carta in cartas:
                if carta.colidiu_com_ponto(event.pos):
                    carta.selecionada = True
                    rodada_finalizada = True
                    if carta.id == carta_correta_nome:
                        carta.resultado = "correta"
                    else:
                        carta.resultado = "errada"
                        # Mostra a carta correta também
                        for c in cartas:
                            if c.id == carta_correta_nome:
                                c.resultado = "correta"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and rodada_finalizada:
                rodada_finalizada = False
                for carta in cartas:
                    carta.selecionada = False
                    carta.resultado = None

                # Novo desafio aleatório
                desafio_atual = random.choice(desafios)
                frase_para_mostrar = desafio_atual['frase']
                carta_correta_nome = desafio_atual['correta']

                # Embaralhar cartas e recriar
                random.shuffle(nomes_cartas)
                cartas = criar_cartas(nomes_cartas)

    # Desenhar frase no topo da tela
    texto_render = font.render(frase_para_mostrar, True, (255, 255, 255))
    texto_rect = texto_render.get_rect(center=(1280 // 2, 40))
    screen.blit(texto_render, texto_rect)

    for carta in cartas:
        carta.desenhar(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

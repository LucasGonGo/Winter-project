import pygame

pygame.font.init()
FONT = pygame.font.SysFont('arial', 30)

LARGURA_BOTAO = 300
ALTURA_BOTAO = 60
ESPACO = 20
COR_BOTAO = (100, 150, 250)
COR_BOTAO_HOVER = (120, 180, 255)
COR_BORDA = (255, 255, 255)
COR_TEXTO = (255, 255, 255)
ESPESSURA_BORDA = 3

def mostrar_menu(screen):
    largura_tela, altura_tela = screen.get_size()

    total_altura = 3 * ALTURA_BOTAO + 2 * ESPACO
    start_y = (altura_tela - total_altura) // 2
    x = (largura_tela - LARGURA_BOTAO) // 2

    botoes = []
    textos = ['Jogar', 'Opções', 'Sair']

    mouse_pos = pygame.mouse.get_pos()

    for i in range(3):
        y = start_y + i * (ALTURA_BOTAO + ESPACO)
        botao_rect = pygame.Rect(x, y, LARGURA_BOTAO, ALTURA_BOTAO)
        botoes.append(botao_rect)

        if botao_rect.collidepoint(mouse_pos):
            cor = COR_BOTAO_HOVER
        else:
            cor = COR_BOTAO

        pygame.draw.rect(screen, cor, botao_rect)
        pygame.draw.rect(screen, COR_BORDA, botao_rect, ESPESSURA_BORDA)

        texto_render = FONT.render(textos[i], True, COR_TEXTO)
        texto_rect = texto_render.get_rect(center=botao_rect.center)
        screen.blit(texto_render, texto_rect)

    return botoes

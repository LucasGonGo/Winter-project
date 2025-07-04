import pygame
import sys
import menu
import game

pygame.init()
screen = pygame.display.set_mode((1280, 720), (pygame.RESIZABLE | pygame.SCALED))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24)

estado = 'menu'

while True:
    if estado == 'menu':
        rodando_menu = True
        while rodando_menu:
            screen.fill((250, 250, 255))
            botoes = menu.mostrar_menu(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, botao in enumerate(botoes):
                        if botao.collidepoint(event.pos):
                            if i == 0:
                                rodando_menu = False
                                estado = 'jogo'
                            elif i == 2:
                                pygame.quit()
                                exit()

            pygame.display.flip()
            clock.tick(60)

    elif estado == 'jogo':
        resultado = game.rodar_jogo(screen, clock)
        if resultado == 'voltar_menu':
            estado = 'menu'
        else:
            pygame.quit()
            exit()

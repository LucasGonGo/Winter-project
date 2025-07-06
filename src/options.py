import pygame, settings, sys

def mostrar_opcoes(screen, clock, fonte):
    largura_tela, altura_tela = screen.get_size()

    fonte_opcao = pygame.font.SysFont('couriernew', 40)

    botao_som = pygame.Rect(largura_tela//2 - 150, altura_tela//2 - 60, 300, 60)

    botao_voltar = pygame.Rect(largura_tela//2 - 150, altura_tela//2 + 30, 300, 60)

    rodando = True
    while rodando:
        screen.fill((163,177,138))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        cor_btn = (80, 180, 100) if settings.sound_on else (180, 80, 80)
        cor_hover = (120, 220, 140) if settings.sound_on else (220, 120, 120)
        cor = cor_hover if botao_som.collidepoint(mouse) else cor_btn
        pygame.draw.rect(screen, cor, botao_som, border_radius=8)
        txt = "Som: ON" if settings.sound_on else "Som: OFF"
        text_render = fonte_opcao.render(txt, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=botao_som.center)
        screen.blit(text_render, text_rect)

        cor2 = (200, 50, 50) if not botao_voltar.collidepoint(mouse) else (255, 80, 80)
        pygame.draw.rect(screen, cor2, botao_voltar, border_radius=8)
        text_voltar = fonte_opcao.render("Voltar", True, (255,255,255))
        text_voltar_rect = text_voltar.get_rect(center=botao_voltar.center)
        screen.blit(text_voltar, text_voltar_rect)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if botao_som.collidepoint(e.pos):
                    settings.sound_on = not settings.sound_on
                    if settings.sound_on:
                        pygame.mixer.unpause()
                    else:
                        pygame.mixer.pause()
                elif botao_voltar.collidepoint(e.pos):
                    rodando = False

        pygame.display.flip()
        clock.tick(60)
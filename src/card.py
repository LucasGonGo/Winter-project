import pygame
import os

class Carta:
    def __init__(self, imagem, pos, escala=(179, 256), id = None):
        self.imagem = pygame.transform.scale(imagem, escala)
        self.rect = self.imagem.get_rect(topleft=pos)
        self.id = id
        self.selecionada = False  # você pode usar isso para realce, etc.
        self.resultado = None # correta, errada ou none

    def desenhar(self, surface):
        surface.blit(self.imagem, self.rect.topleft)

        if self.resultado == "correta":
            pygame.draw.rect(surface, (0, 255, 0), self.rect, 5)
        elif self.resultado == "errada":
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 5)

    def colidiu_com_ponto(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)

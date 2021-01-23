import sys
from enum import Enum

import pygame
from pygame.locals import *

FPS = 240  # frames per second setting
fpsClock = pygame.time.Clock()


class Direcao(Enum):
    ESQUERDA = 1
    CIMA = 2
    DIREITA = 3
    BAIXO = 4


direcao_atual = Direcao.ESQUERDA


def muda_direcao(key, direcao_atual):
    valoratual = direcao_atual.value
    incremento = 0
    if key == K_LEFT:
        incremento = -1
    elif key == K_RIGHT:
        incremento = +1
    valoratual = valoratual + incremento
    if valoratual > 4:
        valoratual = 1
    if valoratual < 1:
        valoratual = 4
    return Direcao(valoratual)


def movimenta(x, y, direcao_atual):
    velocidade = 1
    if direcao_atual == Direcao.CIMA:
        y -= velocidade
    elif direcao_atual == Direcao.BAIXO:
        y += velocidade
    elif direcao_atual == Direcao.ESQUERDA:
        x -= velocidade
    elif direcao_atual == Direcao.DIREITA:
        x += velocidade
    return x, y

def crashed(x, y):
    if x < 1 or x >= 800 or y < 1 or y >= 600:
        return True
    if screen.get_at((x, y)) != (0, 0, 0):
        print(screen.get_at((x, y)))
        return True


pygame.init()
screen = pygame.display.set_mode((800, 600))
x = 400
y = 300
pygame.display.set_caption('- | T R O N  | -')
while True:  # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            direcao_atual = muda_direcao(event.key, direcao_atual)
        #   print(direcao_atual)
    x, y = movimenta(x, y, direcao_atual)
    # print(x, y)
    if crashed(x, y):
        pygame.quit()
        sys.exit()
    screen.set_at((x, y), (200, 0, 0))
    pygame.display.update()
    fpsClock.tick(FPS)

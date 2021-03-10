import sys
from enum import Enum
import pygame
import time
from pygame.locals import *

i = 0
FPS = 65  # frames per second setting
fpsClock = pygame.time.Clock()


class Direcao(Enum):
    ESQUERDA = 1
    CIMA = 2
    DIREITA = 3
    BAIXO = 4


direcao_atual = Direcao.ESQUERDA


class Moto:
    def __init__(self, nome, cor,
                 x_inicial=10, y_inicial=200,
                 tecla_direita=K_RIGHT, tecla_esquerda=K_LEFT,
                 direcao_inicial=Direcao.DIREITA):
        self.nome = nome
        self.cor = cor
        self.x = x_inicial
        self.y = y_inicial
        self.tecla_esquerda = tecla_esquerda
        self.tecla_direita = tecla_direita
        self.velocidade = 1
        self.direcao_atual = direcao_inicial

    def muda_direcao(self, key):
        valoratual = self.direcao_atual.value
        incremento = 0
        if key == self.tecla_esquerda:
            incremento = -1
        elif key == self.tecla_direita:
            incremento = +1
        valoratual = valoratual + incremento
        if valoratual > 4:
            valoratual = 1
        if valoratual < 1:
            valoratual = 4
        self.direcao_atual = Direcao(valoratual)

    def proximo_xy(self):
        proximo_x = self.x
        proximo_y = self.y
        if self.direcao_atual == Direcao.CIMA:
            proximo_y = self.y - self.velocidade
        elif self.direcao_atual == Direcao.BAIXO:
            proximo_y = self.y + self.velocidade
        elif self.direcao_atual == Direcao.ESQUERDA:
            proximo_x = self.x - self.velocidade
        elif self.direcao_atual == Direcao.DIREITA:
            proximo_x = self.x + self.velocidade
        return proximo_x, proximo_y

    def movimenta(self):
        self.x, self.y = self.proximo_xy()

    def piloto_automatico(self):
        if crashed(*self.proximo_xy()):
            self.muda_direcao(self.tecla_direita)


def crashed(x, y):
    if x < 1 or x >= 800 or y < 1 or y >= 800:
        return True
    #print(screen.get_at((x, y)))
    if sum(screen.get_at((x, y))[:3]) != 0:
        # print(screen.get_at((x, y)))
        return True
    return False


pygame.init()
screen = pygame.display.set_mode((800, 800))
AZUL = (0, 0, 100)
VERMELHA = (100, 0, 0)
moto_azul = Moto(nome='Azul', cor=AZUL)
moto_vermelha = Moto(nome='Vermelha', cor=VERMELHA,
                     tecla_direita=K_d, tecla_esquerda=K_a,
                     x_inicial=790, direcao_inicial=Direcao.ESQUERDA)
pygame.display.set_caption('- | T R O N  | -')
while True:  # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            moto_azul.muda_direcao(event.key)
            moto_vermelha.muda_direcao(event.key)
            FPS += 5
            print("Velocidade", FPS)
            # direcao_atual = muda_direcao(event.key, direcao_atual)
            # print(direcao_atual)

    screen.set_at((moto_azul.x, moto_azul.y), moto_azul.cor)
    screen.set_at((moto_vermelha.x, moto_vermelha.y), moto_vermelha.cor)
    moto_azul.movimenta()
    moto_vermelha.piloto_automatico()
    moto_vermelha.movimenta()
    # x, y = movimenta(x, y, direcao_atual)
    if crashed(moto_azul.x, moto_azul.y):
        print(f'{moto_azul.nome} mooooorreeeeeu!!!!')
        pygame.quit()
        print(FPS)
        fpsClock.tick(5)
        sys.exit()
    if crashed(moto_vermelha.x, moto_vermelha.y):
        print(f'{moto_vermelha.nome} mooooorreeeeeu!!!!')
        pygame.quit()
        sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)

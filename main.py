import sys
import pygame
from pygame.locals import *
import os


FPS = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('resources/img', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = load_image('start_fon.jpg')
    screen.blit(fon, (0, 0))
    play_button = pygame.Rect(145, 580, 180, 180)
    pygame.draw.rect(screen, pygame.Color('black'), play_button, 10, 15)
    pygame.draw.polygon(screen, pygame.Color('black'), ((190, 620), (190, 720), (295, 670)))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_SPACE:
                    pygame.time.delay(150)
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    pygame.time.delay(150)
                    return
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 480, 854
    pygame.display.set_caption('SWAY')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_screen()
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)
        pygame.display.flip()
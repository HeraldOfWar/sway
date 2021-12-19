import sys
import pygame
import os


FRACTION = 0
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
                    return choose_fraction()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    pygame.time.delay(150)
                    return choose_fraction()
        pygame.display.flip()


def choose_fraction():
    global FRACTION
    fon = load_image('choose_fraction_fon.jpg')
    konohagakure, ivagakure = load_image('konohagakure_fon.jpg'), load_image('ivagakure_fon.jpg')
    info_1, info_2 = load_image('info_1.png'), load_image('info_2.png')
    k_rect, i_rect = konohagakure.get_rect(), ivagakure.get_rect()
    inf_rect1, inf_rect2 = info_1.get_rect(), info_2.get_rect()
    k_rect.x, k_rect.y = width - 390, 0
    i_rect.x, i_rect.y = 0, height - 285
    inf_rect1.x, inf_rect1.y = 0, 0
    inf_rect2.x, inf_rect2.y = width - 80, height - 285
    screen.blit(fon, (0, 0))
    screen.blit(info_1, (inf_rect1.x, inf_rect1.y))
    screen.blit(info_2, (inf_rect2.x, inf_rect2.y))
    screen.blit(konohagakure, (k_rect.x, k_rect.y))
    screen.blit(ivagakure, (i_rect.x, i_rect.y))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if k_rect.collidepoint(event.pos):
                    FRACTION = 0
                    pygame.time.delay(150)
                    return
                if i_rect.collidepoint(event.pos):
                    FRACTION = 1
                    pygame.time.delay(150)
                    return
                elif inf_rect1.collidepoint(event.pos):
                    FRACTION = 0
                    pygame.time.delay(150)
                    return
                elif inf_rect2.collidepoint(event.pos):
                    FRACTION = 1
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
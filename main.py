import sys
import os
import pygame
import cards
from cards import PLAYCARDS, BONUSCARDS

FRACTION = None
KONOHAGAKURE = 'KONOHAGAKURE'
IVAGAKURE = 'IVAGAKURE'
FPS = 60


def load_image(*names, colorkey=None):
    fullname = os.path.join('resources', '')
    for name in names:
        fullname = os.path.join(fullname, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_cardlist(surf, group, cards):
    sprites = group.sprites()
    group.empty()
    sprites[0].image, sprites[1].image = pygame.transform.scale(sprites[0].image, (183, 95)), \
                                         pygame.transform.scale(sprites[1].image, (183, 95))
    sprites[0].rect, sprites[1].rect = sprites[0].image.get_rect(), sprites[1].image.get_rect()
    sprites[0].rect.x, sprites[0].rect.y = 49, height - 110
    sprites[1].rect.x, sprites[1].rect.y = 248, height - 110
    group.add(sprites[0])
    group.add(sprites[1])
    exit_button = pygame.Rect(width - 70, 15, 50, 50)
    pygame.draw.rect(surf, pygame.Color('black'), exit_button, 3)
    pygame.draw.line(surf, pygame.Color('black'), (width - 60, 25), (width - 30, 55), 5)
    pygame.draw.line(surf, pygame.Color('black'), (width - 30, 25), (width - 60, 55), 5)
    if cards:
        for i in range(len(BONUSCARDS)):
            if BONUSCARDS[i].fraction == FRACTION:
                BONUSCARDS[i].image = pygame.transform.scale(BONUSCARDS[i].image, (150, 225))
                BONUSCARDS[i].rect.x = 5 + 160 * ((i % 5) % 3)
                BONUSCARDS[i].rect.y = 200 + 275 * ((i % 5) // 3)
                group.add(BONUSCARDS[i])
    else:
        for i in range(len(PLAYCARDS)):
            if PLAYCARDS[i].fraction == FRACTION:
                PLAYCARDS[i].image = pygame.transform.scale(PLAYCARDS[i].image, (150, 225))
                PLAYCARDS[i].rect.x = 5 + 160 * ((i % 6) % 3)
                PLAYCARDS[i].rect.y = 200 + 275 * ((i % 6) // 3)
                group.add(PLAYCARDS[i])


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = load_image('back_and_buttons', 'start_background.jpg')
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
                    pygame.time.wait(150)
                    return choose_fraction()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if play_button.collidepoint(event.pos):
                        pygame.time.wait(150)
                        return choose_fraction()
        pygame.display.flip()


def choose_fraction():
    global FRACTION
    fon = load_image('back_and_buttons', 'cf_background.jpg')
    konohagakure, ivagakure = load_image('back_and_buttons', 'konoha_background.jpg'), \
                              load_image('back_and_buttons', 'iva_background.jpg')
    info_1, info_2 = load_image('back_and_buttons', 'info_1.png'), \
                     load_image('back_and_buttons', 'info_2.png')
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
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return start_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if k_rect.collidepoint(event.pos):
                        FRACTION = KONOHAGAKURE
                        pygame.time.wait(150)
                        return
                    elif i_rect.collidepoint(event.pos):
                        FRACTION = IVAGAKURE
                        pygame.time.wait(150)
                        return
                    elif inf_rect1.collidepoint(event.pos):
                        FRACTION = KONOHAGAKURE
                        pygame.time.wait(150)
                        return cards_info()
                    elif inf_rect2.collidepoint(event.pos):
                        FRACTION = IVAGAKURE
                        pygame.time.wait(150)
                        return cards_info()
        pygame.display.flip()


def cards_info():
    info_sprites = pygame.sprite.Group()
    fon = load_image('back_and_buttons', 'basic_background.jpg')
    screen.blit(fon, (0, 0))
    exit_button = pygame.Rect(width - 70, 15, 50, 50)
    pygame.draw.rect(screen, pygame.Color('black'), exit_button, 3)
    pygame.draw.line(screen, pygame.Color('black'), (width - 60, 25), (width - 30, 55), 5)
    pygame.draw.line(screen, pygame.Color('black'), (width - 30, 25), (width - 60, 55), 5)
    playcards, bonuscards = pygame.sprite.Sprite(), pygame.sprite.Sprite()
    playcards.image, bonuscards.image = load_image('back_and_buttons', 'playcards.png'), \
                                        load_image('back_and_buttons', 'bonuscards.png')
    playcards.rect, bonuscards.rect = playcards.image.get_rect(), bonuscards.image.get_rect()
    playcards.rect.x, playcards.rect.y = 102, 285
    bonuscards.rect.x, bonuscards.rect.y = 102, 500
    info_sprites.add(playcards)
    info_sprites.add(bonuscards)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    pygame.time.wait(150)
                    return choose_fraction()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if exit_button.collidepoint(event.pos):
                        pygame.time.wait(150)
                        return choose_fraction()
                    elif playcards.rect.collidepoint(event.pos):
                        pygame.time.wait(150)
                        screen2 = pygame.Surface(screen.get_size())
                        screen2.blit(fon, (0, 0))
                        load_cardlist(screen2, info_sprites, 0)
                        screen.blit(screen2, (0, 0))
                    elif bonuscards.rect.collidepoint(event.pos):
                        pygame.time.wait(150)
                        screen2 = pygame.Surface(screen.get_size())
                        screen2.blit(fon, (0, 0))
                        load_cardlist(screen2, info_sprites, 1)
                        screen.blit(screen2, (0, 0))
        info_sprites.draw(screen)
        pygame.display.flip()


def main():
    start_screen()
    screen.blit(load_image('back_and_buttons', 'main_battlefield.jpg'), (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)
        pygame.display.flip()
    return start_screen()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 480, 854
    pygame.display.set_caption('SWAY')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    main()
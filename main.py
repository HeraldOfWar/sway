import sys
import os
import pygame
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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.blit(start_fon, (0, 0))
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
    screen.blit(cf_fon, (0, 0))
    cf_sprites.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return start_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if konohagakure.rect.collidepoint(event.pos):
                        FRACTION = KONOHAGAKURE
                        pygame.time.wait(150)
                        return
                    elif ivagakure.rect.collidepoint(event.pos):
                        FRACTION = IVAGAKURE
                        pygame.time.wait(150)
                        return
                    elif info_1.rect.collidepoint(event.pos):
                        FRACTION = KONOHAGAKURE
                        pygame.time.wait(150)
                        return cards_info()
                    elif info_2.rect.collidepoint(event.pos):
                        FRACTION = IVAGAKURE
                        pygame.time.wait(150)
                        return cards_info()
        pygame.display.flip()


def cards_info():
    screen.blit(cinf_fon, (0, 0))
    pygame.draw.rect(screen, pygame.Color('black'), exit_button, 3)
    pygame.draw.line(screen, pygame.Color('black'), (width - 60, 25), (width - 30, 55), 5)
    pygame.draw.line(screen, pygame.Color('black'), (width - 30, 25), (width - 60, 55), 5)
    playcards.image, bonuscards.image = pc_img, bc_img
    playcards.rect, bonuscards.rect = playcards.image.get_rect(), bonuscards.image.get_rect()
    playcards.rect.x, playcards.rect.y = 102, 285
    bonuscards.rect.x, bonuscards.rect.y = 102, 500
    info_sprites.add(playcards)
    info_sprites.add(bonuscards)
    info_sprites.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    pygame.time.wait(150)
                    info_sprites.empty()
                    return choose_fraction()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if exit_button.collidepoint(event.pos):
                        pygame.time.wait(150)
                        info_sprites.empty()
                        return choose_fraction()
                    elif playcards.rect.collidepoint(event.pos):
                        pygame.time.wait(150)
                        screen2 = pygame.Surface(screen.get_size())
                        screen2.blit(cinf_fon, (0, 0))
                        load_cardlist(screen2, 0)
                        screen.blit(screen2, (0, 0))
                        info_sprites.draw(screen)
                    elif bonuscards.rect.collidepoint(event.pos):
                        pygame.time.wait(150)
                        screen2 = pygame.Surface(screen.get_size())
                        screen2.blit(cinf_fon, (0, 0))
                        load_cardlist(screen2, 1)
                        screen.blit(screen2, (0, 0))
                        info_sprites.draw(screen)
                    info_sprites.update(event)
        pygame.display.flip()


def load_cardlist(surf, cards):
    info_sprites.empty()
    pygame.draw.rect(surf, pygame.Color('black'), exit_button, 3)
    pygame.draw.line(surf, pygame.Color('black'), (width - 60, 25), (width - 30, 55), 5)
    pygame.draw.line(surf, pygame.Color('black'), (width - 30, 25), (width - 60, 55), 5)
    playcards.image, bonuscards.image = pygame.transform.scale(playcards.image, (183, 95)), \
                                         pygame.transform.scale(bonuscards.image, (183, 95))
    playcards.rect, bonuscards.rect = playcards.image.get_rect(), bonuscards.image.get_rect()
    playcards.rect.x,  playcards.rect.y = 49, height - 110
    bonuscards.rect.x, bonuscards.rect.y = 248, height - 110
    info_sprites.add(playcards)
    info_sprites.add(bonuscards)
    if cards:
        for i in range(len(BONUSCARDS)):
            if BONUSCARDS[i].fraction == FRACTION:
                info_sprites.add(BONUSCARDS[i])
    else:
        for i in range(len(PLAYCARDS)):
            if PLAYCARDS[i].fraction == FRACTION:
                info_sprites.add(PLAYCARDS[i])


def sprites_initialization():
    konohagakure.image, ivagakure.image = load_image('back_and_buttons', 'konoha_background.jpg'), \
                                          load_image('back_and_buttons', 'iva_background.jpg')
    info_1.image, info_2.image = load_image('back_and_buttons', 'info_1.png'), \
                                 load_image('back_and_buttons', 'info_2.png')
    konohagakure.rect, ivagakure.rect = konohagakure.image.get_rect(), ivagakure.image.get_rect()
    info_1.rect, info_2.rect = info_1.image.get_rect(), info_2.image.get_rect()
    konohagakure.rect.x, konohagakure.rect.y = width - 390, 0
    ivagakure.rect.x, ivagakure.rect.y = 0, height - 285
    info_1.rect.x, info_1.rect.y = 0, 0
    info_2.rect.x, info_2.rect.y = width - 80, height - 285

    for i in range(len(BONUSCARDS)):
        BONUSCARDS[i].image = pygame.transform.scale(BONUSCARDS[i].image, (150, 225))
        BONUSCARDS[i].rect.x = 5 + 160 * ((i % 5) % 3)
        BONUSCARDS[i].rect.y = 200 + 275 * ((i % 5) // 3)
    for i in range(len(PLAYCARDS)):
        PLAYCARDS[i].image = pygame.transform.scale(PLAYCARDS[i].image, (150, 225))
        PLAYCARDS[i].rect.x = 5 + 160 * ((i % 6) % 3)
        PLAYCARDS[i].rect.y = 200 + 275 * ((i % 6) // 3)


def main():
    sprites_initialization()
    start_screen()
    screen.blit(load_image('back_and_buttons', 'main_battlefield.jpg'), (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)
        pygame.display.flip()
    return main()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 480, 854
    pygame.display.set_caption('SWAY')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    cf_sprites = pygame.sprite.Group()
    info_sprites = pygame.sprite.Group()

    start_fon = load_image('back_and_buttons', 'start_background.jpg')
    cf_fon = load_image('back_and_buttons', 'cf_background.jpg')
    cinf_fon = load_image('back_and_buttons', 'basic_background.jpg')

    pc_img, bc_img = load_image('back_and_buttons', 'playcards.png'), \
                     load_image('back_and_buttons', 'bonuscards.png')

    play_button = pygame.Rect(145, 580, 180, 180)
    exit_button = pygame.Rect(width - 70, 15, 50, 50)

    konohagakure, ivagakure = pygame.sprite.Sprite(cf_sprites), pygame.sprite.Sprite(cf_sprites)
    info_1, info_2 = pygame.sprite.Sprite(cf_sprites), pygame.sprite.Sprite(cf_sprites)
    playcards, bonuscards = pygame.sprite.Sprite(info_sprites), pygame.sprite.Sprite(info_sprites)
    main()
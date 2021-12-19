import sys
import pygame
import os


FRACTION = 0
KONOHAGAKURE = 0
IVAGAKURE = 1
FPS = 60


def load_image(*names, colorkey=None):
    fullname = os.path.join('resources', '')
    for name in names:
        fullname = os.path.join(fullname, name)
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


def load_cardlist(cards):
    pass


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
                    pygame.time.delay(150)
                    return choose_fraction()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if play_button.collidepoint(event.pos):
                        pygame.time.delay(150)
                        return choose_fraction()
        pygame.display.flip()


def choose_fraction():
    global FRACTION
    fon = load_image('back_and_buttons', 'cf_background.jpg')
    konohagakure, ivagakure = load_image('back_and_buttons', 'konoha_background.jpg'), \
                              load_image('back_and_buttons', 'iva_background.jpg')
    info_1, info_2 = load_image('back_and_buttons', 'info_1.png'), load_image('back_and_buttons', 'info_2.png')
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
                        pygame.time.delay(150)
                        return
                    elif i_rect.collidepoint(event.pos):
                        FRACTION = IVAGAKURE
                        pygame.time.delay(150)
                        return
                    elif inf_rect1.collidepoint(event.pos):
                        FRACTION = KONOHAGAKURE
                        pygame.time.delay(150)
                        return cards_info()
                    elif inf_rect2.collidepoint(event.pos):
                        FRACTION = IVAGAKURE
                        pygame.time.delay(150)
                        return cards_info()
        pygame.display.flip()


def cards_info():
    fon = load_image('back_and_buttons', 'basic_background.jpg')
    screen.blit(fon, (0, 0))
    exit_button = pygame.Rect(width - 70, 15, 50, 50)
    pygame.draw.rect(screen, pygame.Color('black'), exit_button, 3)
    pygame.draw.line(screen, pygame.Color('black'), (width - 60, 25), (width - 30, 55), 5)
    pygame.draw.line(screen, pygame.Color('black'), (width - 30, 25), (width - 60, 55), 5)
    player_cards, bonus_cards = load_image('back_and_buttons', 'player_cards.png'), \
                                load_image('back_and_buttons', 'bonus_cards.png')
    pc_rect, bc_rect = player_cards.get_rect(), bonus_cards.get_rect()
    pc_rect.x, pc_rect.y = 102, 285
    bc_rect.x, bc_rect.y = 102, 500
    screen.blit(player_cards, (pc_rect.x, pc_rect.y))
    screen.blit(bonus_cards, (bc_rect.x, bc_rect.y))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    pygame.time.delay(150)
                    return choose_fraction()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if exit_button.collidepoint(event.pos):
                        pygame.time.delay(150)
                        return choose_fraction()
                    elif pc_rect.collidepoint(event.pos):
                        pygame.time.delay(150)
                        load_cardlist(0)
                    elif bc_rect.collidepoint(event.pos):
                        pygame.time.delay(150)
                        load_cardlist(1)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 480, 854
    pygame.display.set_caption('SWAY')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_screen()
    screen.blit(load_image('back_and_buttons', 'main_battlefield.jpg'), (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)
        pygame.display.flip()
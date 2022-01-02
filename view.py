import pygame
from system_func import terminate, load_image
from constants import *
import cards


"""Предварительная инициализация спрайтов"""
def sprites_init():
    konohagakure.image, ivagakure.image = load_image(BACKGROUND, 'konoha_background.jpg'), \
                                          load_image(BACKGROUND, 'iva_background.jpg')
    info_1.image, info_2.image = load_image(BACKGROUND, 'info_1.png'), load_image(BACKGROUND, 'info_2.png')
    konohagakure.rect, ivagakure.rect = konohagakure.image.get_rect(), ivagakure.image.get_rect()
    info_1.rect, info_2.rect = info_1.image.get_rect(), info_2.image.get_rect()
    konohagakure.rect.x, konohagakure.rect.y = width - 390, 0
    ivagakure.rect.x, ivagakure.rect.y = 0, height - 285
    info_1.rect.x, info_1.rect.y = 0, 0
    info_2.rect.x, info_2.rect.y = width - 80, height - 285
    playcards.image, bonuscards.image = pygame.transform.scale(pc_img, (183, 95)), \
                                        pygame.transform.scale(bc_img, (183, 95))
    playcards.rect, bonuscards.rect = playcards.image.get_rect(), bonuscards.image.get_rect()
    playcards.rect.x, playcards.rect.y = 49, height - 110
    bonuscards.rect.x, bonuscards.rect.y = 248, height - 110

    for i in range(len(PLAYCARDS_DATA)):
        data = PLAYCARDS_DATA[i]
        PLAYCARDS.append(cards.PlayCard(f'{data[3]}.jpg', data[0], data[1], data[2], data[3], data[4],
                                        data[5], data[6], data[7], data[8], data[9], data[10]))
    for i in range(len(BONUSCARDS_DATA)):
        data = BONUSCARDS_DATA[i]
        BONUSCARDS.append(cards.BonusCard(f'{data[3]}.jpg', data[0], data[1], data[2], data[3]))

    for card in PLAYCARDS:
        second_info = sqlite3.connect(DATABASE).cursor().execute(f"""SELECT technic_info, passive_ability_info 
                                                                    FROM playcards
                                                                    WHERE id = '{card.id}'""")
        second_info = [list(i) for i in second_info]
        P_SECOND_INFO.append(second_info)
    for card in BONUSCARDS:
        second_info = sqlite3.connect(DATABASE).cursor().execute(f"""SELECT ability_info FROM bonuscards
                                                                     WHERE id = '{card.id}'""")
        second_info = [list(i) for i in second_info]
        B_SECOND_INFO.append(second_info)

    for i in range(len(BONUSCARDS)):
        BONUSCARDS[i].image = pygame.transform.scale(BONUSCARDS[i].image, (150, 225))
        BONUSCARDS[i].rect = BONUSCARDS[i].image.get_rect()
        BONUSCARDS[i].rect.x = 5 + 160 * ((i % 5) % 3)
        BONUSCARDS[i].rect.y = 200 + 275 * ((i % 5) // 3)
    for i in range(len(PLAYCARDS)):
        PLAYCARDS[i].image = pygame.transform.scale(PLAYCARDS[i].image, (150, 225))
        PLAYCARDS[i].rect = PLAYCARDS[i].image.get_rect()
        PLAYCARDS[i].rect.x = 5 + 160 * ((i % 6) % 3)
        PLAYCARDS[i].rect.y = 200 + 275 * ((i % 6) // 3)


class BasicActivity():

    def __init__(self, background, buttons=[], sprites=[], old_activity=None):
        self.background = background
        self.buttons = buttons
        self.sprites = sprites
        self.old_activity = old_activity
        self.previous_activity = None
        self.next_activity = None

    def run(self, card=None):
        self.output()
        if card:
            card.get_info()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    return self.key_click(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        for button in self.buttons:
                            if button.collidepoint(event.pos):
                                return self.mouse_click(button)
                        for sprite in self.sprites:
                            if sprite.rect.collidepoint(event.pos):
                                return self.mouse_click(sprite)
            pygame.display.flip()

    def output(self):
        screen.blit(self.background, (0, 0))
        for button in self.buttons:
            self.draw_button(button)
        if self.sprites:
            self.sprites.draw(screen)

    def draw_button(self, button, ishovered=False):
        if button == play_button:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('white'), play_button, 10, 15)
                pygame.draw.polygon(screen, pygame.Color('white'), ((190, 620), (190, 720), (295, 670)))
            else:
                pygame.draw.rect(screen, pygame.Color('black'), play_button, 10, 15)
                pygame.draw.polygon(screen, pygame.Color('black'), ((190, 620), (190, 720), (295, 670)))
        if button == exit_button:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('white'), exit_button, 3)
                pygame.draw.line(screen, pygame.Color('white'), (width - 60, 25), (width - 30, 55), 5)
                pygame.draw.line(screen, pygame.Color('white'), (width - 30, 25), (width - 60, 55), 5)
            else:
                pygame.draw.rect(screen, pygame.Color('black'), exit_button, 3)
                pygame.draw.line(screen, pygame.Color('black'), (width - 60, 25), (width - 30, 55), 5)
                pygame.draw.line(screen, pygame.Color('black'), (width - 30, 25), (width - 60, 55), 5)
        if button == escape_button:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('white'), escape_button, 3)
                pygame.draw.rect(screen, pygame.Color('white'), (45, 32, 45, 16))
                pygame.draw.polygon(screen, pygame.Color('white'), ((30, 40), (55, 25), (55, 55)))
            else:
                pygame.draw.rect(screen, pygame.Color('black'), escape_button, 3)
                pygame.draw.rect(screen, pygame.Color('black'), (45, 32, 45, 16))
                pygame.draw.polygon(screen, pygame.Color('black'), ((30, 40), (55, 25), (55, 55)))

    def mouse_motion(self, event):
        pygame.time.wait(50)
        for button in self.buttons:
            if button.collidepoint(event.pos):
                self.draw_button(button, True)
            else:
                self.draw_button(button)

    def key_click(self, event):
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
            if self.old_activity:
                pygame.time.wait(150)
                return self.old_activity.run()
            else:
                terminate()

    def mouse_click(self, view):
        global FRACTION
        pygame.time.wait(150)
        if view == play_button:
            self.next_activity.run()
        if view == exit_button:
            info_sprites.empty()
            self.old_activity.run()
        if view == escape_button:
            self.previous_activity.run()
        if view == konohagakure:
            FRACTION = KONOHAGAKURE
        if view == ivagakure:
            FRACTION = IVAGAKURE
        if view == info_1:
            FRACTION = KONOHAGAKURE
            self.next_activity.load_cardlist(0)
            self.next_activity.run()
        if view == info_2:
            FRACTION = IVAGAKURE
            self.next_activity.load_cardlist(0)
            self.next_activity.run()
        if view == playcards:
            self.load_cardlist(0)
            self.run()
        if view == bonuscards:
            self.load_cardlist(1)
            self.run()
        for sprite in info_sprites:
            if view == sprite:
                sprite.get_info()
                self.next_activity.run(card=sprite)

    def load_cardlist(self, cards):
        self.sprites.empty()
        self.sprites.add(playcards)
        self.sprites.add(bonuscards)
        if cards:
            for card in BONUSCARDS:
                if card.fraction == FRACTION[0]:
                    self.sprites.add(card)
        else:
            for card in PLAYCARDS:
                if card.fraction == FRACTION[0]:
                    self.sprites.add(card)

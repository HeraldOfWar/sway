import pygame
from system_func import terminate, load_image
from constants import *


class BasicActivity():
    """Класс стандартного окна (активности)"""

    def __init__(self, background, buttons=[], sprites=[], old_activity=None):
        """Инициализация основных параметров окна"""
        self.background = background  # фон
        self.buttons = buttons  # список кнопок
        self.sprites = sprites  # спрайты
        self.old_activity = old_activity  # предыдущая активность
        self.previous_activity = None  # ещё одна предыдущая активность... (escape_button)
        self.next_activity = None  # следующая активность
        self.start_game_activity = None  # активность для запуска игры

    def run(self, card=None, rules=False):
        """Запуск основного цикла"""
        self.output()  # предварительная отрисовка окна
        if card:
            card.get_info()  # при нажатии на карту выдаётся информация о ней
        if rules:
            title_rules = b_font.render('Правила', 1, pygame.Color('black'))
            title_rules_rect = title_rules.get_rect()
            title_rules_rect.centerx = pygame.Rect(0, 0, width, height).centerx
            screen.blit(title_rules, (title_rules_rect.x, 45))
        while True:  # а вот и цикл!
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    terminate()
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши на клавиатуре
                    return self.key_click(event)
                elif event.type == pygame.MOUSEMOTION:  # движение мыши
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # клик мыши
                    if event.button == pygame.BUTTON_LEFT:  # только левая кнопка!
                        for button in self.buttons:
                            if button.collidepoint(event.pos):  # проверка пересечения мыши и кнопки
                                return self.mouse_click(button)
                        for sprite in self.sprites:
                            if sprite.rect.collidepoint(event.pos):  # проверка пересечения мыши и спрайта
                                return self.mouse_click(sprite)
            pygame.display.flip()  # смена кадров

    def output(self):
        """Отрисовка всех элементов"""
        screen.blit(self.background, (0, 0))  # отрисовка фона
        for button in self.buttons:
            self.draw_button(button)  # отрисовка кнопок
        if self.sprites:
            self.sprites.draw(screen)  # отрисовка прайтов

    def draw_button(self, button, ishovered=False):
        """Отрисовка всех кнопок"""
        if button == play_button:
            if ishovered:  # если пользователь наводит мышь на кнопку, она становится белой
                pygame.draw.rect(screen, pygame.Color('white'), play_button, 10, 15)
                pygame.draw.polygon(screen, pygame.Color('white'), ((190, 620), (190, 720), (295, 670)))
            else:  # иначе она снова становится чёрной
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
        if button == ok_button:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('white'), ok_button, 10)
                ok_text = b_font.render('OK', 1, pygame.Color('white'))
            else:
                pygame.draw.rect(screen, pygame.Color('black'), ok_button, 10)
                ok_text = b_font.render('OK', 1, pygame.Color('black'))
            ok_text_coord = ok_text.get_rect()
            ok_text_coord.center = ok_button.center
            screen.blit(ok_text, ok_text_coord)

    def mouse_motion(self, event):
        """Проверка наведения пользователем мыши на кнопку"""
        pygame.time.wait(50)  # искуственная задержка (50 мс)
        for button in self.buttons:
            if button.collidepoint(event.pos):
                self.draw_button(button, True)
            else:
                self.draw_button(button)

    def key_click(self, event):
        """Проверка нажатия клавиши клавиатуры"""
        if event.key == pygame.K_ESCAPE:
            if self.old_activity:
                pygame.time.wait(150)
                return self.old_activity.run()
            else:
                terminate()

    def mouse_click(self, view):
        """Проверка нажатия клавиши мыши"""
        global FRACTION
        pygame.time.wait(150)
        if view == play_button or view == ok_button:
            self.next_activity.run()  # отрисовка следующей активности
        if view == exit_button:
            self.old_activity.run()  # отрисовка предыдушей активности
        if view == escape_button:
            self.previous_activity.run()
        if view == konohagakure:
            FRACTION = KONOHAGAKURE  # выбрана фракция Конохагакуре
            self.start_game_activity.run(rules=True)
        if view == ivagakure:
            FRACTION = IVAGAKURE  # выбрана фракция Ивагакуре
            self.start_game_activity.run(rules=True)
        if view == info_1:
            FRACTION = KONOHAGAKURE
            self.next_activity.load_cardlist(0)  # загрузка списка карт
            self.next_activity.run()
        if view == info_2:
            FRACTION = IVAGAKURE
            self.next_activity.load_cardlist(0)
            self.next_activity.run()
        if view == playcards:
            self.load_cardlist(0)
            self.run()
        if view == bonuscards:
            self.load_cardlist(1)  # загрузка списка карт-бонусов
            self.run()
        for sprite in info_sprites:
            if view == sprite:
                self.next_activity.run(card=sprite)

    def load_cardlist(self, cards):
        """Загрузка списка карт"""
        self.sprites.empty()
        self.sprites.add(playcards)  # добавление 1 кнопки (Игровые карты)
        self.sprites.add(bonuscards)  # добавление 2 кнопки (Бонусные карты)
        if cards:
            """Добавление всех бонусных карт выбранной фракции"""
            for card in BONUSCARDS:
                if card.fraction == FRACTION:
                    self.sprites.add(card)
        else:
            """Добавление всех игровых карт выбранной фракции"""
            for card in PLAYCARDS:
                if card.fraction == FRACTION:
                    if card.image != card.info_image:
                        card.image = card.info_image
                    self.sprites.add(card)


class GameActivity(BasicActivity):
    """Класс игрового окна (активности), наследуемый от стандартного окна"""

    def __init__(self, background, buttons, decks, battlepoints):
        """Инициализация основных параметров игровой активности"""
        super().__init__(background, buttons=buttons)
        self.konoha_cards = decks[0]  # колода игровых карт Конохагакуре
        self.iva_cards = decks[1]  # колода игровых карт Ивагакуре
        self.battlepoints = battlepoints  # список боевых точек

    def run(self):
        "Запуск игрового цикл"
        if FRACTION == IVAGAKURE:  # если выбрана фракция Ивагакуре
            self.background = i_battlefield  # переворачиваем фон
        self.konoha_cards.main_fraction = FRACTION  # передаём колодам выбранную фракцию
        self.iva_cards.main_fraction = FRACTION
        self.output()
        while True:
            for event in pygame.event.get():  # pygame ждёт, чтобы пользователь что-то сделал
                if event.type == pygame.QUIT:  # ты куда???... (выход при нажатии на системный крестик)
                    terminate()
                elif event.type == pygame.KEYDOWN:  # нажатие клавиши на клавиатуре
                    return self.key_click(event)
                elif event.type == pygame.MOUSEMOTION:  # движение мыши
                    self.mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # клик мыши
                    if event.button == pygame.BUTTON_LEFT:  # только левая кнопка!
                        for button in self.buttons:
                            if button.collidepoint(event.pos):  # проверка пересечения мыши и кнопки
                                self.mouse_click(button)
                        for sprites in self.sprites:
                            for sprite in sprites:
                                if sprite.rect.collidepoint(event.pos):  # проверка пересечения мыши и спрайта
                                    self.mouse_click(sprite)
            pygame.display.flip()

    def output(self):
        """Отрисовка всех элементов"""
        screen.blit(self.background, (0, 0))
        self.konoha_cards.output()
        self.iva_cards.output()
        for button in self.buttons:
            self.draw_button(button)
        for battlepoint in self.battlepoints:
            battlepoint.output()

    def draw_button(self, button, ishovered=False):
        """Отрисовка всех элементов"""
        if button == endstep_button1:
            for i in range(len('Конец хода'.split())):
                if ishovered:
                    line = b_font2.render('Конец хода'.split()[i], 1, pygame.Color('white'))
                else:
                    line = b_font2.render('Конец хода'.split()[i], 1, pygame.Color('black'))
                line_coord= line.get_rect()
                line_coord.centerx = pygame.Rect(width - 125, height - 140, 90, 55).centerx
                screen.blit(line, (line_coord.x, height - 135 + 20 * i))
        if button == endstep_button2:
            for i in range(len('Конец хода'.split())):
                if ishovered:
                    line = b_font2.render('Конец хода'.split()[i], 1, pygame.Color('white'))
                else:
                    line = b_font2.render('Конец хода'.split()[i], 1, pygame.Color('black'))
                line_coord= line.get_rect()
                line_coord.centerx = pygame.Rect(35, 85, 90, 55).centerx
                screen.blit(line, (line_coord.x, 90 + 20 * i))
        if button == bonus_button1:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), bonus_button1, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), bonus_button1, 3)
        if button == bonus_button2:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), bonus_button2, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), bonus_button2, 3)
        if button == leftslide1:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('black'), leftslide1, 3)
                pygame.draw.polygon(screen, pygame.Color('black'), ((175, height - 93), (175, height - 53),
                                                                    (140, height - 73)))
            else:
                pygame.draw.rect(screen, pygame.Color('white'), leftslide1, 3)
                pygame.draw.polygon(screen, pygame.Color('white'), ((175, height - 93), (175, height - 53),
                                                                    (140, height - 73)))
        if button == rightslide1:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('black'), rightslide1, 3)
                pygame.draw.polygon(screen, pygame.Color('black'), ((width - 174, height - 93),
                                                                    (width - 174, height - 53),
                                                                    (width - 139, height - 73)))
            else:
                pygame.draw.rect(screen, pygame.Color('white'), rightslide1, 3)
                pygame.draw.polygon(screen, pygame.Color('white'), ((width - 174, height - 93),
                                                                    (width - 174, height - 53),
                                                                    (width - 139, height - 73)))
        if button == leftslide2:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('black'), leftslide2, 3)
                pygame.draw.polygon(screen, pygame.Color('black'), ((175, 53), (175, 93), (140, 73)))
            else:
                pygame.draw.rect(screen, pygame.Color('white'), leftslide2, 3)
                pygame.draw.polygon(screen, pygame.Color('white'), ((175, 53), (175, 93), (140, 73)))
        if button == rightslide2:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('black'), rightslide2, 3)
                pygame.draw.polygon(screen, pygame.Color('black'), ((width - 174, 53), (width - 174, 93),
                                                                    (width - 139, 73)))
            else:
                pygame.draw.rect(screen, pygame.Color('white'), rightslide2, 3)
                pygame.draw.polygon(screen, pygame.Color('white'), ((width - 174, 53), (width - 174, 93),
                                                                    (width - 139, 73)))
        if button == b_pass1:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass1, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass1, 3)
        if button == b_pass2:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass2, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass2, 3)
        if button == b_pass3:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass3, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass3, 3)
        if button == b_pass4:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass4, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass4, 3)
        if button == b_pass5:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass5, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass5, 3)
        if button == b_pass6:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_pass6, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_pass6, 3)
        if button == b_bridge1:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_bridge1, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_bridge1, 3)
        if button == b_bridge2:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_bridge2, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_bridge2, 3)
        if button == b_horanpass:
            if ishovered:
                pygame.draw.rect(screen, pygame.Color('red'), b_horanpass, 3)
            else:
                pygame.draw.rect(screen, pygame.Color('white'), b_horanpass, 3)

    def mouse_click(self, view):
        """Проверка нажатия клавиши мыши"""
        if view == leftslide1:
            if FRACTION == KONOHAGAKURE:
                if self.konoha_cards.current == 0:
                    self.konoha_cards.current = len(self.konoha_cards.sprites()) - 1
                else:
                    self.konoha_cards.current -= 1
            else:
                if self.iva_cards.current == 0:
                    self.iva_cards.current = len(self.iva_cards.sprites()) - 1
                else:
                    self.iva_cards.current -= 1
            self.output()
        if view == rightslide1:
            if FRACTION == KONOHAGAKURE:
                if self.konoha_cards.current == len(self.konoha_cards.sprites()) - 1:
                    self.konoha_cards.current = 0
                else:
                    self.konoha_cards.current += 1
            else:
                if self.iva_cards.current == len(self.iva_cards.sprites()) - 1:
                    self.iva_cards.current = 0
                else:
                    self.iva_cards.current += 1
            self.output()
        if view == leftslide2:
            if FRACTION == IVAGAKURE:
                if self.konoha_cards.current == 0:
                    self.konoha_cards.current = len(self.konoha_cards.sprites()) - 1
                else:
                    self.konoha_cards.current -= 1
            else:
                if self.iva_cards.current == 0:
                    self.iva_cards.current = len(self.iva_cards.sprites()) - 1
                else:
                    self.iva_cards.current -= 1
            self.output()
        if view == rightslide2:
            if FRACTION == IVAGAKURE:
                if self.konoha_cards.current == len(self.konoha_cards.sprites()) - 1:
                    self.konoha_cards.current = 0
                else:
                    self.konoha_cards.current += 1
            else:
                if self.iva_cards.current == len(self.iva_cards.sprites()) - 1:
                    self.iva_cards.current = 0
                else:
                    self.iva_cards.current += 1
            self.output()

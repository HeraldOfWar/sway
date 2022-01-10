from constants import *
from activities import BattleFragment


class BattlePoint(pygame.sprite.Group):
    """Класс боевой точки, наследуемый от sprite.Group"""

    def __init__(self, view, score):
        """Инициализация боевой точки"""
        super().__init__()
        self.view = view  # вид боевой точки на игровом поле
        self.info_fragment = BattleFragment('battlepoint', battlepoint_back, b_battlepoint,
                                            self)  # информация о точке
        self.score = score  # количество ОЗ, которое генерируется точкой
        self.points, self.first_points, self.second_points = [], [], []  # позиции на боевой точке
        self.title, self.type = '', ''  # название и тип
        self.point1_cards, self.point2_cards = [], []  # список союзных и вражеских карт на точке

    def output(self):
        """Отрисовка боевой точки"""
        for point in self.points:  # отрисовка всех точкек
            pygame.draw.rect(screen, pygame.Color('white'), point, 3)
        if self.type == 'Перевал Хорана':
            for i in range(2):
                name = b_font2.render(self.title.split()[i], 1, pygame.Color('white'))
                name_coord = name.get_rect()
                name_coord.center = self.view.center
                name_coord.y = height // 2 - 25
                name_coord.y += 22 * i
                screen.blit(name, name_coord)
        else:
            name = b_font4.render(self.title, 1, pygame.Color('white'))
            name_coord = name.get_rect()
            name_coord.center = self.view.center
            screen.blit(name, name_coord)  # вывод названия точки
        self.draw(screen)  # отрисовка всех карт на точке на игровом поле

    def update_points(self):
        """Обновление союзных и вражеских позиций"""
        self.first_points = self.points[:3]
        self.second_points = self.points[3:]

    def update_card_draw(self):
        for card in self.sprites():
            card.image = card.battle_image  # замена изображения карты
            card.rect = card.image.get_rect()  # изменение координат карты
            if card in self.point1_cards:
                card.rect.center = self.points[self.point1_cards.index(card)].center
            else:
                card.rect.center = self.points[self.point2_cards.index(card) + 3].center

    def get_info(self):
        """Выдача информации о боевой точке"""

        """Установка позиций всех карт на точке"""
        for i in range(len(self.point1_cards)):  # союзных
            self.point1_cards[i].image = self.point1_cards[i].battle_info_image
            self.point1_cards[i].rect = self.point1_cards[i].image.get_rect()
            if i == 0:
                self.point1_cards[i].rect.center = point1.center
            if i == 1:
                self.point1_cards[i].rect.center = point2.center
            if i == 2:
                self.point1_cards[i].rect.center = point3.center
        for i in range(len(self.point2_cards)):  # и вражеских
            self.point2_cards[i].image = self.point2_cards[i].battle_info_image
            self.point2_cards[i].rect = self.point2_cards[i].image.get_rect()
            if i == 0:
                self.point2_cards[i].rect.center = point4.center
            if i == 1:
                self.point2_cards[i].rect.center = point5.center
            if i == 2:
                self.point2_cards[i].rect.center = point6.center
        self.draw(screen)  # отрисовка карт


class Deck(pygame.sprite.Group):
    """Класс игровой колоды, наследуемый от sprite.Group"""

    def __init__(self, fraction):
        """Инициализация игровой колоды"""
        super().__init__()
        self.main_fraction = None  # выбранная в меню фракция
        self.fraction = fraction  # фракция колоды
        self.score = 0  # количество ОЗ
        self.step = 0  # ход
        self.current = 0  # индекс текущей карты
        self.hand = self.sprites()
        self.konoha_bonus_rect = konoha_bonus.get_rect()  # колода карт-бонусов Конохагакуре (размеры)
        self.iva_bonus_rect = iva_bonus.get_rect()  # колода карт-бонусов Ивагакуре (размеры)
        self.state = True  # состояние игровой колоды
        self.is_moved = 0  # количество перемещённых карт (для 1 хода)

    def load(self):
        """Загрузка изображений карт игровой колоды"""
        if self.fraction == self.main_fraction:
            for i in range(self.__len__()):
                self.sprites()[i].image = self.sprites()[i].deck_image
                self.sprites()[i].rect = self.sprites()[i].image.get_rect()
                self.sprites()[i].rect.center = pygame.Rect(126, height - 140, 229, 135).center
        else:
            for i in range(self.__len__()):
                self.sprites()[i].image = self.sprites()[i].deck_image
                self.sprites()[i].rect = self.sprites()[i].image.get_rect()
                self.sprites()[i].rect.center = pygame.Rect(126, 5, 229, 135).center

    def output(self):
        """Отрисовка игровой колоды"""
        if self.fraction == self.main_fraction:
            pygame.draw.rect(screen, pygame.Color('white'), (125, height - 140, 231, 135), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (width - 125, height - 140, 90, 135), 3)
            pygame.draw.rect(screen, pygame.Color('white'), endstep_button1, 3)
            """Установка колоды бонусных карт"""
            if self.fraction == KONOHAGAKURE:
                self.konoha_bonus_rect.center = bonus_button1.center
                screen.blit(konoha_bonus, self.konoha_bonus_rect)
            else:
                pass
                self.iva_bonus_rect.center = bonus_button1.center
                screen.blit(iva_bonus, self.iva_bonus_rect)
        else:
            pygame.draw.rect(screen, pygame.Color('white'), (124, 5, 231, 135), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (35, 5, 90, 135), 3)
            pygame.draw.rect(screen, pygame.Color('white'), endstep_button2, 3)
            if self.fraction == KONOHAGAKURE:
                self.konoha_bonus_rect.center = bonus_button2.center
                screen.blit(konoha_bonus, self.konoha_bonus_rect)
            else:
                self.iva_bonus_rect.center = bonus_button2.center
                screen.blit(iva_bonus, self.iva_bonus_rect)

        """Вывод изображения текущей карты"""
        if self.hand:
            if self.current > len(self.hand) - 1:
                self.current = len(self.hand) - 1
            screen.blit(self.hand[self.current].image, self.hand[self.current].rect)

        """Вывод информации о количестве ходов, ОЗ и карт"""
        for i in range(len('Ход: ОЗ: Карты:'.split())):
            if i == 0:
                line = font1.render(f"{'Ход: ОЗ: Карты:'.split()[i]} {self.step}", 1, pygame.Color('black'))
            elif i == 1:
                line = font1.render(f"{'Ход: ОЗ: Карты:'.split()[i]} {self.score}", 1, pygame.Color('black'))
            else:
                line = font1.render(f"{'Ход: ОЗ: Карты:'.split()[i]} {self.__len__()}", 1,
                                    pygame.Color('black'))
            if self.fraction != self.main_fraction:
                screen.blit(line, (42, 15 + 22 * i))
            else:
                screen.blit(line, (width - 118, height - 75 + 22 * i))

    def set_hand(self):
        """Заполнение карт в руке"""
        self.hand = self.sprites()

    def update_hand(self, cards):
        """Добавление карт в руку"""
        for card in cards:
            self.hand.insert(self.current, card)

    def set_state(self, state):
        """Установка состояния игровой колоды"""
        if state:  # если активна
            if self.fraction == self.main_fraction:
                self.state = True
                bonus_button1.is_enabled = True
                endstep_button1.is_enabled = True
                for card in self.sprites():
                    card.is_enabled = True
                point1.is_enabled = True
                point2.is_enabled = True
                point3.is_enabled = True
            else:
                self.state = True
                bonus_button2.is_enabled = True
                endstep_button2.is_enabled = True
                for card in self.sprites():
                    card.is_enabled = True
                point4.is_enabled = True
                point5.is_enabled = True
                point6.is_enabled = True
        else:  # если неактивна
            if self.fraction == self.main_fraction:
                self.state = False
                bonus_button1.is_enabled = False
                endstep_button1.is_enabled = False
                for card in self.sprites():
                    card.is_enabled = False
                point1.is_enabled = False
                point2.is_enabled = False
                point3.is_enabled = False
            else:
                self.state = False
                bonus_button2.is_enabled = False
                endstep_button2.is_enabled = False
                for card in self.sprites():
                    card.is_enabled = False
                point4.is_enabled = False
                point5.is_enabled = False
                point6.is_enabled = False

    def get_state(self):
        """Выдача состояния игровой колоды"""
        return self.state

    def update_pace(self):
        for card in self.sprites():
            card.update_pace()

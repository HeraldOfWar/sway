from constants import *
from activities import BattleFragment


class BattlePoint(pygame.sprite.Group):
    """Класс боевой точки, наследуемый от sprite.Group"""

    def __init__(self, view, score):
        """Инициализация боевой точки"""
        super().__init__()
        self.view = view  # кнопка боевой точки на игровом поле
        self.score = score  # количество ОЗ, которое генерируется точкой
        self.points, self.first_points, self.second_points = [], [], []  # позиции на боевой точке
        self.title, self.type = '', ''  # название и тип
        self.point1_cards, self.point2_cards = [], []  # список союзных и вражеских карт на точке
        self.info_fragment = BattleFragment('battlepoint', basic_back, b_points,
                                            self)  # фрагмент с информацией о точке
        self.is_under = None  # контролирующая фракция

    def output(self, color):
        """Отрисовка боевой точки"""
        for point in self.points:  # отрисовка всех позиций
            pygame.draw.rect(screen, pygame.Color(color), point, 3)
        if self.type == 'Перевал Хорана':
            for i in range(2):
                name = g_font1.render(self.title.split()[i], 1, pygame.Color(color))
                name_coord = name.get_rect()
                name_coord.center = self.view.center
                name_coord.y = height // 2 - 25
                name_coord.y += 22 * i
                screen.blit(name, name_coord)  # вывод названия Перевала Хорана
        else:
            name = g_font3.render(self.title, 1, pygame.Color(color))
            name_coord = name.get_rect()
            name_coord.center = self.view.center
            screen.blit(name, name_coord)  # вывод названия точки
        self.draw(screen)  # отрисовка всех карт на точке на игровом поле

    def update_points(self):
        """Обновление союзных и вражеских позиций"""
        self.first_points = [point1, point2, point3]  # позиции для первого игрока
        self.second_points = [point4, point5, point6]  # для второго игрока

    def update_card_draw(self):
        """Обновление позиций и размеров карт под игровое поле"""
        for card in self.sprites():
            card.image = card.battle_image  # замена изображения карты
            card.rect = card.image.get_rect()  # изменение координат карты
            if card in self.point1_cards:
                card.rect.center = self.points[self.point1_cards.index(card)].center
            else:
                card.rect.center = self.points[self.point2_cards.index(card) + 3].center

    def set_get_info_mode(self):
        """Установка позиций всех карт на точке (для информативного фрагмента)"""
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

    @staticmethod
    def set_battle_mode(friend, enemy):
        """Установка позиций карт для поединка"""
        friend.rect.centery = pygame.Rect(0, 327, width, 233).centery
        friend.rect.x = pygame.Rect(0, 327, width, 233).x + 20
        enemy.rect.centery = pygame.Rect(0, 327, width, 233).centery
        enemy.rect.right = pygame.Rect(0, 327, width, 233).right - 20

    @staticmethod
    def battle(friend, enemy):
        """Сражение между картами"""
        friend.attack(enemy)  # сначала атакует первая
        if enemy.is_alive and (enemy.point == friend.point):
            enemy.attack(friend)  # а потом вторая, если выжила и осталась на точке


class Deck(pygame.sprite.Group):
    """Класс игровой колоды, наследуемый от sprite.Group"""

    def __init__(self, fraction):
        """Инициализация игровой колоды"""
        super().__init__()
        self.main_fraction = None  # выбранная в меню фракция
        self.fraction = fraction  # фракция колоды
        self.score = 0  # количество ОЗ
        self.step = 0  # ход
        self.hand = self.sprites()  # "рука"
        self.current = 0  # индекс текущей карты в "руке"
        self.state = True  # состояние игровой колоды
        self.is_moved = 0  # количество перемещённых карт (для 1 хода)
        if self.fraction == KONOHAGAKURE:
            self.bonus_deck = konoha_bonusdeck  # передача колоды карт-бонусов
        else:
            self.bonus_deck = iva_bonusdeck
        self.konoha_bonus_rect = konoha_bonus.get_rect()  # колода карт-бонусов Конохагакуре (размеры)
        self.iva_bonus_rect = iva_bonus.get_rect()  # колода карт-бонусов Ивагакуре (размеры)

    def output(self, color):
        """Отрисовка игровой колоды"""
        if self.fraction == self.main_fraction:
            pygame.draw.rect(screen, pygame.Color(color), (125, height - 140, 231, 135), 3)
            pygame.draw.rect(screen, pygame.Color(color), (width - 125, height - 140, 90, 135), 3)
            pygame.draw.rect(screen, pygame.Color(color), endstep_button1, 3)
            """Установка колоды бонусных карт"""
            if self.fraction == KONOHAGAKURE:
                if self.bonus_deck:
                    self.konoha_bonus_rect.center = bonus_button1.center
                    screen.blit(konoha_bonus, self.konoha_bonus_rect)
            else:
                if self.bonus_deck:
                    self.iva_bonus_rect.center = bonus_button1.center
                    screen.blit(iva_bonus, self.iva_bonus_rect)
        else:
            pygame.draw.rect(screen, pygame.Color(color), (124, 5, 231, 135), 3)
            pygame.draw.rect(screen, pygame.Color(color), (35, 5, 90, 135), 3)
            pygame.draw.rect(screen, pygame.Color(color), endstep_button2, 3)
            if self.fraction == KONOHAGAKURE:
                if self.bonus_deck:
                    self.konoha_bonus_rect.center = bonus_button2.center
                    screen.blit(konoha_bonus, self.konoha_bonus_rect)
            else:
                if self.bonus_deck:
                    self.iva_bonus_rect.center = bonus_button2.center
                    screen.blit(iva_bonus, self.iva_bonus_rect)

        """Вывод изображения текущей карты в руке"""
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

    def update_pace(self):
        """Обновление скорости для всех союзных карт"""
        for card in self.sprites():
            card.update_pace()

    def set_hand(self):
        """Заполнение руки всеми доступными картами"""
        self.hand = self.sprites()

    def update_hand(self):
        """Обновление позиций карт в руке"""
        if self.fraction == self.main_fraction:
            for i in range(len(self.hand)):
                self.hand[i].image = self.hand[i].deck_image
                self.hand[i].rect = self.hand[i].image.get_rect()
                self.hand[i].rect.center = pygame.Rect(126, height - 140, 229, 135).center
        else:
            for i in range(len(self.hand)):
                self.hand[i].image = self.hand[i].deck_image
                self.hand[i].rect = self.hand[i].image.get_rect()
                self.hand[i].rect.center = pygame.Rect(126, 5, 229, 135).center

    def add_card(self, cards):
        """Добавление карт в руку"""
        for card in cards:
            card.point = self
            if len(self.hand) > 0:
                self.hand.insert(self.current, card)
            else:
                self.hand.append(card)

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

    def get_bonus(self):
        """Выпадение бонусной карты"""
        card = random.choice(self.bonus_deck.sprites())  # случайный выбор карты из колоды
        card.bonus()  # активация эффекта карты
        self.bonus_deck.remove(card)
        return card

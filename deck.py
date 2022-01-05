import pygame, thorpy
from constants import *


class Deck(pygame.sprite.Group):
    """Класс игровой колоды, наследуемый от sprite.Group"""

    def __init__(self, fraction):
        """Инициализация колоды"""
        super().__init__()
        self.main_fraction = None  # выбранная в меню фракция
        self.fraction = fraction  # фракция колоды
        self.score = 0  # количество ОЗ
        self.step = 0  # ход
        self.current = 0  # индекс текущей карты
        self.konoha_bonus_rect = konoha_bonus.get_rect()  # колода карт-бонусов Конохагакуре (размеры)
        self.iva_bonus_rect = iva_bonus.get_rect()  # колода карт-бонусов Ивагакуре (размеры)

    def output(self):
        """Отрисовка игровой колоды"""
        if self.fraction == self.main_fraction:
            pygame.draw.rect(screen, pygame.Color('white'), (126, height - 140, 229, 135), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (width - 125, height - 140, 90, 135), 3)
            pygame.draw.rect(screen, pygame.Color('white'), endstep_button1, 3)
            """Установка колоды бонусных карт"""
            if self.fraction == KONOHAGAKURE:
                self.konoha_bonus_rect.center = bonus_button1.center
                screen.blit(konoha_bonus, self.konoha_bonus_rect)
            else:
                self.iva_bonus_rect.center = bonus_button1.center
                screen.blit(iva_bonus, self.iva_bonus_rect)
            for i in range(self.__len__()):
                self.sprites()[i].image = self.sprites()[i].deck_image
                self.sprites()[i].rect = self.sprites()[i].image.get_rect()
                self.sprites()[i].rect.center = pygame.Rect(126, height - 140, 229, 135).center
            screen.blit(self.sprites()[self.current].image, self.sprites()[self.current].rect)
        else:
            pygame.draw.rect(screen, pygame.Color('white'), (126, 5, 229, 135), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (35, 5, 90, 135), 3)
            pygame.draw.rect(screen, pygame.Color('white'), endstep_button2, 3)
            if self.fraction == KONOHAGAKURE:
                self.konoha_bonus_rect.center = bonus_button2.center
                screen.blit(konoha_bonus, self.konoha_bonus_rect)
            else:
                self.iva_bonus_rect.center = bonus_button2.center
                screen.blit(iva_bonus, self.iva_bonus_rect)
            for i in range(self.__len__()):
                self.sprites()[i].image = self.sprites()[i].deck_image
                self.sprites()[i].rect = self.sprites()[i].image.get_rect()
                self.sprites()[i].rect.center = pygame.Rect(126, 5, 229, 135).center
            screen.blit(self.sprites()[self.current].image, self.sprites()[self.current].rect)

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
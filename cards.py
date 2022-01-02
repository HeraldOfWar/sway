import sys, os
import pygame
from system_func import load_image
from constants import *

"""Класс игровой карты"""
class PlayCard(pygame.sprite.Sprite):

    def __init__(self, image, id, fraction, name, short_name, spec, pace, chakra,
                 resist, health, technic, synergy):
        super().__init__()
        self.image = load_image(CARDS, image)
        self.id = id
        self.fraction = fraction
        self.name = name
        self.short_name = short_name
        self.spec = spec
        self.pace = pace
        self.chakra = chakra
        self.resist = resist
        self.health = health
        self.technic = technic.split()
        self.synergy = synergy
        self.damage = self.pace + self.chakra + int(self.technic[0])
        self.rect = self.image.get_rect()


    def update(self, *args):
        pass

    """Выдача информации о карте"""
    def get_info(self, *args):
        pygame.draw.rect(screen, pygame.Color('black'), (8, 160, 464, 246), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 405, 464, 45), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 449, 232, 44), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (238, 449, 233, 44), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 492, 232, 45), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (238, 492, 233, 45), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 536, 232, 44), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (238, 536, 233, 44), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 405, 464, 444), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 405, 464, 290), 3)

        img_coord = self.rect.copy()
        img_coord.center = pygame.Rect((8, 160, 465, 245)).center
        title = b_font2.render(f'{self.name}, ({self.spec})', 1, pygame.Color('black'))
        title_coord = title.get_rect()
        title_coord.center = pygame.Rect((8, 405, 464, 45)).center
        pace = font.render(f'Скорость: {self.pace}', 1, pygame.Color('black'))
        pace_coord = pace.get_rect()
        pace_coord.center = pygame.Rect((8, 449, 232, 44)).center
        chakra = font.render(f'Чакра: {self.chakra}', 1, pygame.Color('black'))
        chakra_coord = chakra.get_rect()
        chakra_coord.center = pygame.Rect((238, 449, 233, 44)).center
        resist = font.render(f'Стойкость: {self.resist}', 1, pygame.Color('black'))
        resist_coord = resist.get_rect()
        resist_coord.center = pygame.Rect((8, 492, 232, 45)).center
        health = font.render(f'Здоровье: {self.health}', 1, pygame.Color('black'))
        health_coord = health.get_rect()
        health_coord.center = pygame.Rect(238, 492, 233, 45).center
        damage = font.render(f'Урон: {self.damage}', 1, pygame.Color('black'))
        damage_coord = damage.get_rect()
        damage_coord.center = pygame.Rect((8, 536, 232, 44)).center
        if len(self.synergy) > 10:
            synergy = font1.render(f'Синергия: {self.synergy}', 1, pygame.Color('black'))
        else:
            synergy = font.render(f'Синергия: {self.synergy}', 1, pygame.Color('black'))
        synergy_coord = synergy.get_rect()
        synergy_coord.center = pygame.Rect((238, 536, 233, 44)).center
        technic = b_font2.render('Техника:', 1, pygame.Color('black'))
        passive_ability = b_font2.render('Пассивная способность:', 1, pygame.Color('black'))
        old_technic_info, old_passive_ability_info = P_SECOND_INFO[self.id - 1][0][0], \
                                                     P_SECOND_INFO[self.id - 1][0][1]
        technic_info1, passive_ability_info1 = '', ''
        technic_info, passive_ability_info = [], []

        for i in range(len(old_technic_info)):
            technic_info1 += old_technic_info[i]
            if len(technic_info1) % 57 == 0:
                technic_info.append(technic_info1.strip())
                technic_info1 = ''
            elif i == len(old_technic_info) - 1:
                technic_info.append(technic_info1.strip())

        for i in range(len(old_passive_ability_info)):
            passive_ability_info1 += old_passive_ability_info[i]
            if len(passive_ability_info1) % 57 == 0:
                passive_ability_info.append(passive_ability_info1.strip())
                passive_ability_info1 = ''
            elif i == len(old_passive_ability_info) - 1:
                passive_ability_info.append(passive_ability_info1.strip())

        screen.blit(self.image, img_coord)
        screen.blit(title, title_coord)
        screen.blit(pace, pace_coord)
        screen.blit(chakra, chakra_coord)
        screen.blit(resist, resist_coord)
        screen.blit(health, health_coord)
        screen.blit(damage, damage_coord)
        screen.blit(synergy, synergy_coord)
        screen.blit(technic, (16, 586))
        screen.blit(passive_ability, (16, 700))
        for i in range(len(technic_info)):
            line = font2.render(technic_info[i], 1, pygame.Color('black'))
            y = 615 + 20 * i
            screen.blit(line, (16, y))
        for i in range(len(passive_ability_info)):
            line = font2.render(passive_ability_info[i], 1, pygame.Color('black'))
            y = 729 + 20 * i
            screen.blit(line, (16, y))

    def __str__(self):
        return self.short_name


"""Класс бонусной карты"""
class BonusCard(pygame.sprite.Sprite):

    def __init__(self, image, id, fraction, name, short_name):
        super().__init__()
        self.image = load_image(CARDS, image)
        self.id = id
        self.fraction = fraction
        self.name = name
        self.short_name = short_name
        self.rect = self.image.get_rect()

    def update(self):
        pass

    """Выдача информации о карте"""
    def get_info(self):
        pygame.draw.rect(screen, pygame.Color('black'), (8, 160, 464, 245), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 404, 464, 50), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 453, 464, 393), 3)

        img_coord = self.rect.copy()
        img_coord.center = pygame.Rect((8, 160, 465, 245)).center
        title = b_font1.render(f'{self.name}', 1, pygame.Color('black'))
        title_coord = title.get_rect()
        title_coord.center = pygame.Rect((8, 404, 465, 50)).center
        ability = b_font1.render('Эффект:', 1, pygame.Color('black'))
        old_ability_info = B_SECOND_INFO[self.id - 1][0][0]
        ability_info1, ability_info = '', []

        for i in range(len(old_ability_info)):
            ability_info1 += old_ability_info[i]
            if len(ability_info1) % 40 == 0:
                ability_info.append(ability_info1.strip())
                ability_info1 = ''
            elif i == len(old_ability_info) - 1:
                ability_info.append(ability_info1.strip())

        screen.blit(self.image, img_coord)
        screen.blit(title, title_coord)
        screen.blit(ability, (18, 462))
        for i in range(len(ability_info)):
            line = font.render(ability_info[i], 1, pygame.Color('black'))
            y = 500 + 22 * i
            screen.blit(line, (16, y))

    def __str__(self):
        return self.short_name


"""Классы игровых карт Конохагакуре"""
class Shu(PlayCard):
    def update(self, *args):
        pass


class Pashke(PlayCard):
    def update(self, *args):
        pass

class Akemi(PlayCard):
    def update(self, *args):
        pass


class Raik(PlayCard):
    def update(self, *args):
        pass


class Kentaru(PlayCard):
    def update(self, *args):
        pass


class Hiruko(PlayCard):
    def update(self, *args):
        pass


"""Классы игровых карт Ивагакуре"""
class Keiko(PlayCard):
    def update(self, *args):
        pass


class Akito(PlayCard):
    def update(self, *args):
        pass


class Ryu(PlayCard):
    def update(self, *args):
        pass


class Kitsu(PlayCard):
    def update(self, *args):
        pass


class Benkei(PlayCard):
    def update(self, *args):
        pass


class Teeru(PlayCard):
    def update(self, *args):
        pass


"""Классы бонусных карт Конохагакуре"""
class BarKonoha(BonusCard):
    def update(self, *args):
        pass


class Himera(BonusCard):
    def update(self, *args):
        pass


class Tsunami(BonusCard):
    def update(self, *args):
        pass


class KingOfMouse(BonusCard):
    def update(self, *args):
        pass


class Ren(BonusCard):
    def update(self, *args):
        pass


"""Классы бонусных карт Ивагакуре"""
class HymnIva(BonusCard):
    def update(self, *args):
        pass


class Turtle(BonusCard):
    def update(self, *args):
        pass


class Kin(BonusCard):
    def update(self, *args):
        pass


class TrueMedic(BonusCard):
    def update(self, *args):
        pass


class Ambitions(BonusCard):
    def update(self, *args):
        pass

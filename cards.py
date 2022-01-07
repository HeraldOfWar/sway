import pygame
from system_func import load_image
from constants import *


class PlayCard(pygame.sprite.Sprite):
    """Класс игровой карты, наследуемый от sprite.Sprite"""

    def __init__(self, image, args, *group):
        """Инициализация основных характеристик карты"""
        super().__init__(group)  # инициализация родительского класса спрайта
        self.image = load_image(CARDS, image)  # изображение карты
        self.id = args[0]  # идентификатор
        self.fraction = args[1]  # принадлежность фракции
        self.name = args[2]  # имя
        self.short_name = args[3]  # короткое имя
        self.spec = args[4]  # специализация
        self.pace = args[5]  # скорость
        self.chakra = args[6]  # запасы чакры (энергии)
        self.resist = args[7]  # стойкость (сопротивление)
        self.health = args[8]  # здоровье
        self.technic = args[9].split()  # техника (урон и вид)
        self.synergy = args[10]  # связь с другими картами (увеличивает урон)
        self.damage = self.pace + self.chakra + int(self.technic[0])  # урон складывается из трёх показателей
        self.isalive = True  # параметр, отвечающий за то, жива ли карта или нет
        self.rect = self.image.get_rect()  # размеры карты
        self.info_image = self.image  # изображение для выдачи информации о карте
        self.deck_image = load_image(CARDS, f'deck_{self.short_name}.jpg')  # изображение "в руке"
        self.battle_image = load_image(CARDS, f'battle_{self.short_name}.jpg')  # изображение на боевой точке
        self.is_enabled = True

    def update(self, *args):
        """Реализация пассивной способности"""
        pass

    def get_info(self, *args):
        """Выдача информации о карте"""

        """Предварительная отрисовка всех границ и прямоугольников"""
        pygame.draw.rect(screen, pygame.Color('black'), (8, 160, 464, 248), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 405, 464, 47), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 449, 232, 46), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (238, 449, 233, 46), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 492, 232, 47), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (238, 492, 233, 47), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 536, 232, 46), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (238, 536, 233, 46), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 405, 464, 444), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 405, 464, 290), 3)

        """Создание текста и установка координат"""
        img_coord = self.info_image.get_rect()
        img_coord.center = pygame.Rect((8, 160, 465, 248)).center
        title = b_font3.render(f'{self.name}, ({self.spec})', 1, pygame.Color('black'))
        title_coord = title.get_rect()
        title_coord.center = pygame.Rect((8, 405, 464, 47)).center
        pace = font.render(f'Скорость: {self.pace}', 1, pygame.Color('black'))
        pace_coord = pace.get_rect()
        pace_coord.center = pygame.Rect((8, 449, 232, 46)).center
        chakra = font.render(f'Чакра: {self.chakra}', 1, pygame.Color('black'))
        chakra_coord = chakra.get_rect()
        chakra_coord.center = pygame.Rect((238, 449, 233, 46)).center
        resist = font.render(f'Стойкость: {self.resist}', 1, pygame.Color('black'))
        resist_coord = resist.get_rect()
        resist_coord.center = pygame.Rect((8, 492, 232, 47)).center
        health = font.render(f'Здоровье: {self.health}', 1, pygame.Color('black'))
        health_coord = health.get_rect()
        health_coord.center = pygame.Rect(238, 492, 233, 47).center
        damage = font.render(f'Урон: {self.damage}', 1, pygame.Color('black'))
        damage_coord = damage.get_rect()
        damage_coord.center = pygame.Rect((8, 536, 232, 46)).center
        if len(self.synergy) > 10:  # установка размера в зависимости от длины текста
            synergy = font1.render(f'Синергия: {self.synergy}', 1, pygame.Color('black'))
        else:
            synergy = font.render(f'Синергия: {self.synergy}', 1, pygame.Color('black'))
        synergy_coord = synergy.get_rect()
        synergy_coord.center = pygame.Rect((238, 536, 233, 46)).center
        technic = b_font3.render('Техника:', 1, pygame.Color('black'))
        passive_ability = b_font3.render('Пассивная способность:', 1, pygame.Color('black'))
        old_technic_info, old_passive_ability_info = P_SECOND_INFO[self.id - 1][0][0], \
                                                     P_SECOND_INFO[self.id - 1][0][1]
        technic_info1, passive_ability_info1 = '', ''
        technic_info, passive_ability_info = [], []

        for i in range(len(old_technic_info)):  # разделение описания техники по строкам
            technic_info1 += old_technic_info[i]
            if len(technic_info1) % 57 == 0:
                technic_info.append(technic_info1.strip())
                technic_info1 = ''
            elif i == len(old_technic_info) - 1:
                technic_info.append(technic_info1.strip())

        for i in range(len(old_passive_ability_info)):  # разделение описания пассивной способности по строкам
            passive_ability_info1 += old_passive_ability_info[i]
            if len(passive_ability_info1) % 57 == 0:
                passive_ability_info.append(passive_ability_info1.strip())
                passive_ability_info1 = ''
            elif i == len(old_passive_ability_info) - 1:
                passive_ability_info.append(passive_ability_info1.strip())

        "Вывод всей информации в окне"
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
        for i in range(len(technic_info)):  # построчный вывод описания техники
            line = font2.render(technic_info[i], 1, pygame.Color('black'))
            y = 615 + 20 * i
            screen.blit(line, (16, y))
        for i in range(len(passive_ability_info)):  # посторочный вывод описания пассивной способности
            line = font2.render(passive_ability_info[i], 1, pygame.Color('black'))
            y = 729 + 20 * i
            screen.blit(line, (16, y))

    def __str__(self):
        """Представление объекта карты в виде строки"""
        return self.name


class BonusCard(pygame.sprite.Sprite):
    """Класс бонусной карты, наследуемый от sprite.Sprite"""

    def __init__(self, image, args, *group):
        """Инициализация основных характеристик карты"""
        super().__init__(group)
        self.image = load_image(CARDS, image)
        self.id = args[0]
        self.fraction = args[1]
        self.name = args[2]
        self.short_name = args[3]
        self.rect = self.image.get_rect()
        self.is_enabled = True

    def update(self):
        """Реализация эффекта карты"""
        pass

    def get_info(self):
        """Выдача информации о карте"""
        pygame.draw.rect(screen, pygame.Color('black'), (8, 160, 464, 247), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 404, 464, 52), 3)
        pygame.draw.rect(screen, pygame.Color('black'), (8, 453, 464, 393), 3)

        img_coord = self.rect.copy()
        img_coord.center = pygame.Rect((8, 160, 465, 247)).center
        title = b_font2.render(f'{self.name}', 1, pygame.Color('black'))
        title_coord = title.get_rect()
        title_coord.center = pygame.Rect((8, 404, 465, 52)).center
        ability = b_font2.render('Эффект:', 1, pygame.Color('black'))
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
        return self.name


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

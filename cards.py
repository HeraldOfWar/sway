import pygame
import random
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
        self.synergy = args[10].split()  # связь с другими картами (увеличивает урон)
        self.damage = self.pace + self.chakra + int(self.technic[0])
        self.rect = self.image.get_rect()  # размеры карты
        self.info_image = self.image  # изображение для выдачи информации о карте
        self.deck_image = load_image(CARDS, f'deck_{self.short_name}.jpg')  # изображение "в руке"
        self.battle_image = load_image(CARDS, f'battle_{self.short_name}.jpg')  # изображение на игровом поле
        self.battle_info_image = load_image(CARDS,
                                            f'b_inf_{self.short_name}.jpg')  # изображение на боевой точке
        self.is_alive = True  # параметр, отвечающий за то, жива ли карта или нет
        self.is_enabled = True  # проверка карты, заблокирована ли она или нет
        self.is_attacked = False
        self.passive_is_used = False
        self.default_pace, self.default_chakra, self.default_health = self.pace, self.chakra, self.health
        self.default_rect = self.rect
        self.point = self.groups()[0]
        self.pieces = pygame.sprite.Group()

    def can_attack(self):
        if self.chakra == 0:
            return 'chakra'
        if self.is_attacked:
            return 'is_attacked'
        if self.fraction == self.groups()[0].main_fraction:
            if len(self.point.point2_cards) == 0:
                return 'len_cards'
        else:
            if len(self.point.point1_cards) == 0:
                return 'len_cards'
        return True

    def attack(self, enemy):
        self.damage = self.set_damage()
        enemy.get_damage(self.damage)
        self.chakra -= 1

    def can_move(self, new_point=None):
        if self.pace == 0:
            return 'pace'
        if self.groups()[0].step == 0 and self.groups()[0].is_moved >= 3:
            return 'step'
        if self.fraction == self.groups()[0].main_fraction and new_point:
            if len(new_point.point1_cards) == 3:
                return 'len_cards'
        elif self.fraction != self.groups()[0].main_fraction and new_point:
            if len(new_point.point2_cards) == 3:
                return 'len_cards'
        return True

    def move(self, last_point, new_point):
        if self.groups()[0].main_fraction == self.fraction:
            if last_point != self.groups()[0]:
                last_point.point1_cards.remove(self)
                last_point.remove(self)
                last_point.update_card_draw()
            else:
                last_point.hand.remove(self)
            if new_point != self.groups()[0]:
                new_point.point1_cards.append(self)
                new_point.add(self)
                new_point.update_card_draw()
            else:
                new_point.update_hand([self])
                new_point.load()
        else:
            if last_point != self.groups()[0]:
                last_point.point2_cards.remove(self)
                last_point.remove(self)
                last_point.update_card_draw()
            else:
                last_point.hand.remove(self)
            if new_point != self.groups()[0]:
                new_point.point2_cards.append(self)
                new_point.add(self)
                new_point.update_card_draw()
            else:
                new_point.update_hand([self])
                new_point.load()
        self.point = new_point
        self.pace -= 1

    def recover(self):
        if self.health < self.default_health:
            self.health += 1
        if self.chakra < self.default_chakra:
            self.chakra += 1

    def update_pace(self, *args):
        """Обновление cкорости"""
        self.pace = self.default_pace

    def set_damage(self):
        damage = self.pace + self.chakra + int(self.technic[0])
        if self.groups():
            if self.point != self.groups()[0]:
                if self.fraction == self.groups()[0].main_fraction:
                    if len(self.point.point1_cards) > 1 and self.synergy == 'Все':
                        return damage + 1
                    for card in self.point.point1_cards:
                        if card.name.split()[0] in self.synergy:
                            return damage + 1
                else:
                    if len(self.point.point2_cards) > 1 and self.synergy == 'Все':
                        return damage + 1
                    for card in self.point.point2_cards:
                        if card.name.split()[0] in self.synergy:
                            return damage + 1
        return damage

    def get_damage(self, damage):
        if self.health + self.resist <= damage:
            self.is_alive = False
            if self.fraction == self.groups()[0].main_fraction:
                self.point.point1_cards.remove(self)
            else:
                self.point.point2_cards.remove(self)
            self.kill()
            self.death()
        else:
            if self.resist <= damage:
                self.health -= damage - self.resist

    def get_passive(self):
        return False

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
        damage = font.render(f'Урон: {self.set_damage()}', 1, pygame.Color('black'))
        damage_coord = damage.get_rect()
        damage_coord.center = pygame.Rect((8, 536, 232, 46)).center
        if self.synergy == 'Все':
            synergy = font.render(f'Синергия: {self.synergy}', 1, pygame.Color('black'))
        elif len(", ".join(self.synergy)) > 10:  # установка размера в зависимости от длины текста
            synergy = font1.render(f'Синергия: {", ".join(self.synergy)}', 1, pygame.Color('black'))
        else:
            synergy = font.render(f'Синергия: {", ".join(self.synergy)}', 1, pygame.Color('black'))
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
        screen.blit(self.info_image, img_coord)
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

    def death(self):
        for x in range(0, self.rect.width, self.rect.width // 5):
            for y in range(0, self.rect.height, self.rect.height // 5):
                piece = CardPiece(self.image, (self.rect.x, self.rect.y), x, y, random.choice(range(-5, 6)),
                                  random.choice(range(-5, 10)), self.pieces)

    def update(self):
        self.rect = self.rect.move(random.randrange(3) - 1, random.randrange(3) - 1)
        if self.rect.x - self.default_rect.x > 2:
            self.rect = self.rect.move(-1, 0)
        elif self.default_rect.x - self.rect.x > 2:
            self.rect = self.rect.move(1, 0)
        elif self.rect.y - self.default_rect.y > 2:
            self.rect = self.rect.move(0, -1)
        elif self.default_rect.y - self.rect.y > 2:
            self.rect = self.rect.move(0, 1)

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

    def bonus(self):
        pass

    def update(self):
        self.rect.centerx = screen.get_rect().centerx
        if self.rect.centery != pygame.Rect((8, 160, 465, 247)).centery:
            if (self.rect.centery - pygame.Rect((8, 160, 465, 247)).centery) // 10 < 1:
                self.rect.centery = pygame.Rect((8, 160, 465, 247)).centery
            self.rect.y -= (self.rect.centery - pygame.Rect((8, 160, 465, 247)).centery) // 10
        else:
            return 'ready'
        return

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


class CardPiece(pygame.sprite.Sprite):

    def __init__(self, image, pos, x, y, dx, dy, *group):
        super().__init__(group)
        self.image = image.subsurface(x, y, image.get_rect().width // 5, image.get_rect().height // 5)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos[0] + x, pos[1] + y
        self.gravity = 1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen.get_rect()):
            self.kill()


"""Классы игровых карт Конохагакуре"""
class Shu(PlayCard):
    pass


class Pashke(PlayCard):
    pass


class Akemi(PlayCard):

    def get_passive(self):
        if self.fraction == self.groups()[0].main_fraction:
            for card in self.point.point1_cards:
                if card.short_name == 'shu' and len(self.point.point1_cards) == 2:
                    return True
        else:
            for card in self.point.point2_cards:
                if card.short_name == 'shu' and len(self.point.point2_cards) == 2:
                    return True
        return False



class Raik(PlayCard):

    def move(self, last_point, new_point):
        if self.groups()[0].main_fraction == self.fraction:
            if last_point != self.groups()[0]:
                last_point.point1_cards.remove(self)
                last_point.remove(self)
                last_point.update_card_draw()
            else:
                last_point.hand.remove(self)
            if new_point != self.groups()[0]:
                new_point.point1_cards.append(self)
                new_point.add(self)
                new_point.update_card_draw()
            else:
                new_point.update_hand([self])
                new_point.load()
        else:
            if last_point != self.groups()[0]:
                last_point.point2_cards.remove(self)
                last_point.remove(self)
                last_point.update_card_draw()
            else:
                last_point.hand.remove(self)
            if new_point != self.groups()[0]:
                new_point.point2_cards.append(self)
                new_point.add(self)
                new_point.update_card_draw()
            else:
                new_point.update_hand([self])
                new_point.load()
        self.point = new_point
        self.pace -= 1


class Kentaru(PlayCard):
    pass


class Hiruko(PlayCard):

    def get_passive(self):
        if self.passive_is_used:
            return False
        return True



"""Классы игровых карт Ивагакуре"""
class Keiko(PlayCard):

    def get_passive(self):
        return True


class Akito(PlayCard):

    def get_passive(self):
        return True


class Ryu(PlayCard):

    def get_passive(self):
        if self.passive_is_used:
            return False
        return True


class Kitsu(PlayCard):
    pass


class Benkei(PlayCard):
    pass


class Teeru(PlayCard):
    pass


"""Классы бонусных карт Конохагакуре"""
class BarKonoha(BonusCard):

    def bonus(self):
        for card in PLAYCARDS:
            if card.fraction == KONOHAGAKURE:
                card.synergy = 'Все'

class Himera(BonusCard):
    pass


class Tsunami(BonusCard):
    pass


class KingOfMouse(BonusCard):
    pass


class Ren(BonusCard):
    pass


"""Классы бонусных карт Ивагакуре"""
class HymnIva(BonusCard):
    pass


class Turtle(BonusCard):
    pass


class Kin(BonusCard):
    pass


class TrueMedic(BonusCard):
    pass


class Ambitions(BonusCard):
    pass

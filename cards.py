import random
import pygame_gui.elements
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
        self.current_health = args[8]  # здоровье
        self.technic = args[9].split()  # техника (урон и вид)
        self.synergy = args[10].split()  # связь с другими картами (увеличивает урон)
        self.damage = self.pace + self.chakra + int(self.technic[0])  # значение урона карты
        self.is_damaged = 0  # полученный урон
        self.rect = self.image.get_rect()  # размеры карты
        self.info_image = self.image  # изображение для выдачи информации о карте
        self.deck_image = load_image(CARDS, f'deck_{self.short_name}.jpg')  # изображение "в руке"
        self.battle_image = load_image(CARDS, f'battle_{self.short_name}.jpg')  # изображение на игровом поле
        self.battle_info_image = load_image(CARDS,
                                            f'b_inf_{self.short_name}.jpg')  # изображение на боевой точке
        self.is_alive = True  # карта жива?
        self.is_enabled = True  # карта заблокирована?
        self.is_attacked, self.is_healed = False, False  # карта сражалась в этом ходу, лечила кого-нибудь?
        self.is_blocked = False  # карта обездвижена?
        self.passive_is_used, self.passive_is_active = False, False  # карта использовала пассивную способность?
        self.default_pace, self.default_chakra = self.pace, self.chakra  # стандартные значения показателей
        self.health_capacity = self.current_health
        self.default_rect = self.rect  # стандартное положение и размер
        self.point = None  # местонахождение карты
        if self.groups():
            self.point = self.groups()[0]  # в начале игры это база ("рука")
        self.pieces = pygame.sprite.Group()  # "куски" карты (для уничтожения)
        self.sounds = []  # озвучка появления/выхода
        self.attack_sounds = []  # озвучка атаки
        self.death_sounds = []  # озвучка смерти

    def can_attack(self):
        """Проверка на возможность атаковать противника"""
        if self.chakra <= 0:  # если закончилась чакра
            return 'chakra'
        if self.is_attacked:  # если карта уже принимала участие в поединке в этом ходу
            return 'is_attacked'
        if self.fraction == self.groups()[0].main_fraction:  # если нет противников
            if len(self.point.point2_cards) == 0:
                return 'len_cards'
        else:
            if len(self.point.point1_cards) == 0:
                return 'len_cards'
        return True

    def attack(self, enemy):
        """Атака"""
        self.damage = self.set_damage()  # передаём урон
        """Проверка на виды техник"""
        if self.technic[1] == 'Ниндзюцу' and enemy.technic[1] == 'Гендзюцу':
            self.damage += 1
        if self.technic[1] == 'Гендзюцу' and (enemy.technic[1] == 'Тайдзюцу' or
                                              enemy.technic[1] == 'Кендзюцу'):
            self.damage += 1
        if (self.technic[1] == 'Тайдзюцу' or self.technic[1] == 'Кендзюцу') and \
                enemy.technic[1] == 'Ниндзюцу':
            self.damage += 1
        enemy.get_damage(self.damage, self)  # наносим урон противнику
        if self.chakra > 0:
            self.chakra -= 1  # тратим чакру

    def can_heal(self):
        """Проверка на возможность вылечить союзника"""
        if self.chakra <= 0:  # если закончилась чакра
            return 'chakra'
        if self.is_healed:  # если карта уже принимала участие в поединке в этом ходу
            return 'is_healed'

    def heal(self, friend):
        """Лечение"""
        if friend.current_health + int(self.technic[0]) > friend.health_capacity:
            friend.current_health = friend.health_capacity
        else:
            friend.current_health += int(self.technic[0])
        self.is_healed = True
        if self.chakra > 0:
            self.chakra -= 1

    def can_move(self, new_point=None):
        "Проверка на возможность переместить карту"
        if self.pace <= 0:  # если закончилась скорость
            return 'pace'
        if self.is_blocked:
            return 'block'
        if self.short_name != 'raik':
            if self.fraction == self.groups()[0].main_fraction:  # если есть противники и недостаточно скорости
                if self.point != self.groups()[0] and self.point.point2_cards and self.pace == 1:
                    return 'pace1'
            elif self.fraction != self.groups()[0].main_fraction:
                if self.point != self.groups()[0] and self.point.point1_cards and self.pace == 1:
                    return 'pace1'
        if self.groups()[0].step == 0 and self.groups()[0].is_moved >= 3:  # если в первом ходу уже перемещено
            return 'step'  # 3 карты
        if self.groups()[0].step == 0 and self.point != self.groups()[0]:
            return 'step1'
        if self.fraction == self.groups()[0].main_fraction and new_point:  # если на точке уже 3 союзных карты
            if len(new_point.point1_cards) == 3:
                return 'len_cards'
        elif self.fraction != self.groups()[0].main_fraction and new_point:
            if len(new_point.point2_cards) == 3:
                return 'len_cards'
        return True

    def move(self, last_point, new_point):
        """Перемещение карты"""
        if last_point == self.groups()[0]:  # если текущая точка это база
            last_point.hand.remove(self)  # удаляем из руки и добавляем в новую точку
            if self.fraction == self.groups()[0].main_fraction:
                new_point.point1_cards.append(self)
            else:
                new_point.point2_cards.append(self)
            new_point.add(self)
            new_point.update_card_draw()
            self.pace -= 1
        else:
            last_point.remove(self)
            if self.fraction == self.groups()[0].main_fraction:
                last_point.point1_cards.remove(self)
                if last_point.point2_cards:  # если на точке были противники
                    self.pace -= 2  # тратим дополнительную единицу скорости
                else:
                    self.pace -= 1
            else:
                last_point.point2_cards.remove(self)
                if last_point.point1_cards:
                    self.pace -= 2
                else:
                    self.pace -= 1
            if new_point == self.groups()[0]:  # если новая точка это база
                new_point.add_card([self])  # добавляем её в руку
            else:
                if self.fraction == self.groups()[0].main_fraction:
                    new_point.point1_cards.append(self)
                else:
                    new_point.point2_cards.append(self)
                new_point.add(self)
        self.point = new_point  # установка нового местоположения

    def recover(self):
        """Восстановление карты"""
        if self.current_health < self.health_capacity:
            self.current_health += 1  # восстановление здоровья
        if self.chakra < self.default_chakra:
            self.chakra += 1  # восстановление чакры

    def update_pace(self, *args):
        """Обновление cкорости"""
        self.pace = self.default_pace

    def set_damage(self):
        """Установка урона"""
        if self.spec != 'Медик':
            damage = self.pace + self.chakra + int(self.technic[0])  # урон складывается из 3 показателей
        else:
            damage = self.pace + self.chakra  # но не у медиков
        if self.chakra <= 0:  # если закончилась чакра
            return 0  # карта не наносит урон
        if self.groups():
            if self.point != self.groups()[0]:  # если срабатывает синергия
                if self.fraction == self.groups()[0].main_fraction:
                    if len(self.point.point1_cards) > 1 and self.synergy == 'Все':
                        damage += 1  # добавляем 1 к урону
                    for card in self.point.point1_cards:
                        if card.name.split()[0] in self.synergy:
                            damage += 1
                    for card in self.point.point1_cards:
                        if self.short_name != 'benkei' and card.short_name == 'benkei' and \
                                not card.passive_is_used:  # Бенкей ослабляет союзников
                            return damage - 2
                        if card.short_name == 'benkei' and card.passive_is_used:  # но с Иватой усиляет
                            return damage + 1
                        if card.short_name == 'hiruko' and card.himera_is_used:  # Хируко может украсть
                            if self.short_name != 'hiruko' and card.himera_card.short_name == 'benkei' and \
                                    not card.himera_card.passive_is_used:  # эту способность у Бенкея
                                return damage - 2
                            if card.himera_card.short_name == 'benkei' and card.himera_card.passive_is_used:
                                return damage + 1
                else:
                    if len(self.point.point2_cards) > 1 and self.synergy == 'Все':
                        damage += 1
                    for card in self.point.point2_cards:
                        if card.name.split()[0] in self.synergy:
                            damage += 1
                    for card in self.point.point2_cards:
                        if self.short_name != 'benkei' and card.short_name == 'benkei' and \
                                not card.passive_is_used:
                            return damage - 2
                        if card.short_name == 'benkei' and card.passive_is_used:
                            return damage + 1
                        if card.short_name == 'hiruko' and card.himera_is_used:
                            if self.short_name != 'hiruko' and card.himera_card.short_name == 'benkei' and \
                                    not card.himera_card.passive_is_used:
                                return damage - 2
                            if card.himera_card.short_name == 'benkei' and card.himera_card.passive_is_used:
                                return damage + 1
        return damage  # возвращаем урон

    def get_damage(self, damage, *enemy):
        """Получение урона"""
        if self.is_alive:  # если карта жива
            if damage >= self.resist:
                self.is_damaged = damage - self.resist
            else:
                self.is_damaged = 0  # если урон меньше стойкости, то он не наносится
            if self.current_health <= self.is_damaged:  # если урон больше чем здоровье + стойкость
                self.current_health = 0
                self.is_alive = False  # карта погибает
                if self.fraction == self.groups()[0].main_fraction:  # отосвюду удаляется
                    self.point.point1_cards.remove(self)
                else:
                    self.point.point2_cards.remove(self)
                self.kill()
                self.death()  # а также срабатывает анимация уничтожения
            else:
                self.current_health -= self.is_damaged  # наносим урон карте

    def get_ability(self):
        """Проверка наличия способности карты"""
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
        img_coord = self.info_image.get_rect()  # изображение (координаты)
        img_coord.center = pygame.Rect((8, 160, 465, 248)).center
        title = b_font3.render(f'{self.name}, ({self.spec})', 1, pygame.Color('black'))
        title_coord = title.get_rect()  # название (координаты)
        title_coord.center = pygame.Rect((8, 405, 464, 47)).center
        pace = font.render(f'Скорость: {self.pace}', 1, pygame.Color('black'))
        pace_coord = pace.get_rect()  # показатель скорости (координаты)
        pace_coord.center = pygame.Rect((8, 449, 232, 46)).center
        chakra = font.render(f'Чакра: {self.chakra}', 1, pygame.Color('black'))
        chakra_coord = chakra.get_rect()  # показатель чакры (координаты)
        chakra_coord.center = pygame.Rect((238, 449, 233, 46)).center
        resist = font.render(f'Стойкость: {self.resist}', 1, pygame.Color('black'))
        resist_coord = resist.get_rect()  # показатель стойкости (координаты)
        resist_coord.center = pygame.Rect((8, 492, 232, 47)).center
        health = font.render(f'Здоровье: {self.current_health}', 1, pygame.Color('black'))
        health_coord = health.get_rect()  # показатель здоровья (координаты)
        health_coord.center = pygame.Rect(238, 492, 233, 47).center
        damage = font.render(f'Урон: {self.set_damage()}', 1, pygame.Color('black'))
        damage_coord = damage.get_rect()  # показатель урона (координаты)
        damage_coord.center = pygame.Rect((8, 536, 232, 46)).center
        if self.synergy == 'Все':  # синергия (координаты)
            synergy = font.render(f'Синергия: {self.synergy}', 1, pygame.Color('black'))
        elif len(", ".join(self.synergy)) > 10:  # установка размера в зависимости от длины текста
            synergy = font1.render(f'Синергия: {", ".join(self.synergy)}', 1, pygame.Color('black'))
        else:
            synergy = font.render(f'Синергия: {", ".join(self.synergy)}', 1, pygame.Color('black'))
        synergy_coord = synergy.get_rect()  # синергия (координаты)
        synergy_coord.center = pygame.Rect((238, 536, 233, 46)).center

        "Вывод всей информации в окне"
        screen.blit(self.info_image, img_coord)  # вывод изображения
        screen.blit(title, title_coord)  # вывод названия
        screen.blit(pace, pace_coord)  # вывод скорости
        screen.blit(chakra, chakra_coord)  # вывод чакры
        screen.blit(resist, resist_coord)  # вывод стойкости
        screen.blit(health, health_coord)  # вывод здоровья
        screen.blit(damage, damage_coord)  # вывод урона
        screen.blit(synergy, synergy_coord)  # вывод синергии

    def get_abilities_info(self):
        "Возвращение информации о способностях карты"
        return '<b>Техника:</b><br />' + P_SECOND_INFO[self.id - 1][0][0], \
               '<b>Способность:</b><br />' + P_SECOND_INFO[self.id - 1][0][1]

    def death(self):
        """Подготовка к анимации уничтожения карты"""
        for x in range(0, self.rect.width, self.rect.width // 5):
            for y in range(0, self.rect.height, self.rect.height // 5):
                piece = CardPiece(self.image, (self.rect.x, self.rect.y), x, y, random.choice(range(-5, 6)),
                                  random.choice(range(-5, 10)), self.pieces)
        if self.death_sounds:
            if self.point.info_fragment.channel and self.point.info_fragment.channel.get_busy():
                self.point.info_fragment.channel.stop()
            my_sound = random.choice(self.death_sounds)
            self.point.info_fragment.channel = my_sound.play()
            self.point.info_fragment.channel.set_volume(CARD_VOLUME)

    def update(self):
        """Анимация тряски"""
        self.rect = self.rect.move(random.randrange(3) - 1, random.randrange(3) - 1)
        if self.rect.x - self.default_rect.x > 2:
            self.rect = self.rect.move(-1, 0)
        elif self.default_rect.x - self.rect.x > 2:
            self.rect = self.rect.move(1, 0)
        elif self.rect.y - self.default_rect.y > 2:
            self.rect = self.rect.move(0, -1)
        elif self.default_rect.y - self.rect.y > 2:
            self.rect = self.rect.move(0, 1)

    def rise(self):
        """Анимация появления карты"""
        self.rect.centerx = screen.get_rect().centerx
        if self.rect.centery != pygame.Rect((8, 160, 465, 247)).centery:
            if (self.rect.centery - pygame.Rect((8, 160, 465, 247)).centery) // 10 < 1:
                self.rect.centery = pygame.Rect((8, 160, 465, 247)).centery
            self.rect.y -= (self.rect.centery - pygame.Rect((8, 160, 465, 247)).centery) // 10
        else:  # когда карта достигнет нужной точки, выводится информация о карте
            return 'ready'
        return

    def get_sound(self):
        if self.sounds:
            my_sound = random.choice(self.sounds)
            return my_sound
        return None

    def get_attack_sound(self):
        if self.attack_sounds:
            my_sound = random.choice(self.attack_sounds)
            return my_sound
        return None

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
        self.main_activity = None  # главная игровая активность
        self.sounds = []  # озвучка появления

    def bonus(self):
        """Активация эффекта бонусной карты"""
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
        ability = g_font2.render('Эффект:', 1, pygame.Color('black'))
        ability_info = B_SECOND_INFO[self.id - 1][0][0]

        screen.blit(self.image, img_coord)
        screen.blit(title, title_coord)

    def get_ability_info(self):
        """Возвращение информации об эффекте бонусной карты"""
        return '<b>Эффект:</b><br />' + B_SECOND_INFO[self.id - 1][0][0]

    def rise(self):
        """Анимация появление бонусной карты"""
        self.rect.centerx = screen.get_rect().centerx
        if self.rect.centery != pygame.Rect((8, 160, 465, 247)).centery:
            if (self.rect.centery - pygame.Rect((8, 160, 465, 247)).centery) // 10 < 1:
                self.rect.centery = pygame.Rect((8, 160, 465, 247)).centery
            self.rect.y -= (self.rect.centery - pygame.Rect((8, 160, 465, 247)).centery) // 10
        else:  # когда карта достигнет нужной точки, выводится информация о карте
            return 'ready'
        return

    def get_sound(self):
        if self.sounds:
            my_sound = random.choice(self.sounds)
            my_sound.set_volume(CARD_VOLUME)
            return my_sound
        return None

    def __str__(self):
        return self.name


class KickedCard(pygame.sprite.Sprite):
    """Класс выброшенной карты, наследуемый от pygame.Sprite (для Кентару и Икетани)"""

    def __init__(self, card, direction):
        super().__init__()
        self.image = card.image  # изображение карты
        self.rect = card.rect  # размеры и координаты карты
        self.direction = direction  # направление движения

    def update(self):
        """Анимация выброса карты"""
        if self.direction == 'right':  # вправо
            self.rect.right += 50
        if self.direction == 'left':  # влево
            self.rect.x -= 50
        if not self.rect.colliderect(screen.get_rect()):
            self.kill()  # как только карта вылетает за пределы экрана, она уничтожается


class CardPiece(pygame.sprite.Sprite):
    """Класс осколков карты, наследуемый от pygame.Sprite (уничожение)"""

    def __init__(self, image, pos, x, y, dx, dy, *group):
        """Инициализация осколка карты"""
        super().__init__(group)
        # изображение осколка карты
        self.image = image.subsurface(x, y, image.get_rect().width // 5, image.get_rect().height // 5)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]  # направление движения осколков по оси x и y
        self.rect.x, self.rect.y = pos[0] + x, pos[1] + y  # позиция
        self.gravity = 1  # гравитация

    def update(self):
        """Анимация разрушения"""
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen.get_rect()):
            self.kill()  # как только осколок вылетает за пределы экрана, он уничтожается


class Kamikaze(pygame.sprite.Sprite):
    """Класс мышей-камикадзе, наследуемый от pygame.Sprite (для способности Джерри)"""

    def __init__(self, point, *group):
        super().__init__(group)
        self.image = load_image(CARDS, 'kamikaze.jpg')  # изображение карты "Мыши-камикадзе"
        self.boom_image = load_image(BACK_N_BUT, 'boom.png')  # изображение взрыва
        self.rect = self.image.get_rect()
        self.point = point  # атакуемая точка
        self.rect.right = 0  # перед началом анимации устанавливаем карту за пределами экрана
        self.rect.centery = self.point.centery  # и точно перпендикулярно атакуемой точке

    def update(self):
        """Анимация появления, движения и взрыва мышей-камикадзе"""
        if self.rect.centerx != self.point.centerx:
            if (self.point.centerx - self.rect.centerx) // 60 < 1:
                self.rect.centerx = self.point.centerx
            self.rect.x += (self.point.centerx - self.rect.centerx) // 60
        else:
            self.image = self.boom_image  # при достижении цели карта взрывается
            return 'ready'
        return


"""Классы игровых карт Конохагакуре"""


class Shu(PlayCard):
    """Класс игровой карты Шу"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'shu.wav'), load_sound(C_VOICES, 'shu1.wav')]

    def set_damage(self):
        """Установка урона"""
        if self.spec != 'Медик':
            damage = self.pace + self.chakra + int(self.technic[0])  # урон складывается из 3 показателей
            if self.passive_is_used:
                damage += 4
        else:
            damage = self.pace + self.chakra  # но не у медиков
        if self.chakra == 0:  # если закончилась чакра
            return 0  # карта не наносит урон
        if self.groups():
            if self.point != self.groups()[0]:  # если срабатывает синергия
                if self.fraction == self.groups()[0].main_fraction:
                    if len(self.point.point1_cards) > 1 and self.synergy == 'Все':
                        damage += 1  # добавляем 1 к урону
                    for card in self.point.point1_cards:
                        if card.name.split()[0] in self.synergy:
                            damage += 1
                    for card in self.point.point1_cards:
                        if self.short_name != 'benkei' and card.short_name == 'benkei' and \
                                not card.passive_is_used:  # Бенкей ослабляет союзников
                            return damage - 2
                        if card.short_name == 'benkei' and card.passive_is_used:  # но с Иватой усиляет
                            return damage + 1
                        if card.short_name == 'hiruko' and card.himera_is_used:  # Хируко может украсть
                            if self.short_name != 'hiruko' and card.himera_card.short_name == 'benkei' and \
                                    not card.himera_card.passive_is_used:  # эту способность у Бенкея
                                return damage - 2
                            if card.himera_card.short_name == 'benkei' and card.himera_card.passive_is_used:
                                return damage + 1
                else:
                    if len(self.point.point2_cards) > 1 and self.synergy == 'Все':
                        damage += 1
                    for card in self.point.point2_cards:
                        if card.name.split()[0] in self.synergy:
                            damage += 1
                    for card in self.point.point2_cards:
                        if self.short_name != 'benkei' and card.short_name == 'benkei' and \
                                not card.passive_is_used:
                            return damage - 2
                        if card.short_name == 'benkei' and card.passive_is_used:
                            return damage + 1
                        if card.short_name == 'hiruko' and card.himera_is_used:
                            if self.short_name != 'hiruko' and card.himera_card.short_name == 'benkei' and \
                                    not card.himera_card.passive_is_used:
                                return damage - 2
                            if card.himera_card.short_name == 'benkei' and card.himera_card.passive_is_used:
                                return damage + 1
        return damage  # возвращаем урон

    def get_damage(self, damage, *enemy):
        """Реализация пассивной способности: 50% шанс избежать урона в бою"""
        self.passive_is_used = random.choice([True, False, False])
        if self.passive_is_used:
            self.is_damaged = 0
            return
        if damage >= self.resist:
            self.is_damaged = damage - self.resist
        else:
            self.is_damaged = 0
        if self.current_health <= self.is_damaged:  # если урон больше чем здоровье + стойкость
            self.current_health = 0
            self.is_alive = False  # карта погибает
            if self.fraction == self.groups()[0].main_fraction:  # отосвюду удаляется
                self.point.point1_cards.remove(self)
            else:
                self.point.point2_cards.remove(self)
            self.kill()
            self.death()  # а также срабатывает анимация уничтожения
        else:
            self.current_health -= self.is_damaged  # наносим урон карте

    def attack(self, enemy):
        """Атака"""
        self.damage = self.set_damage()  # передаём урон
        """Проверка на виды техник"""
        if self.technic[1] == 'Ниндзюцу' and enemy.technic[1] == 'Гендзюцу':
            self.damage += 1
        if self.technic[1] == 'Гендзюцу' and (enemy.technic[1] == 'Тайдзюцу' or
                                              enemy.technic[1] == 'Кендзюцу'):
            self.damage += 1
        if (self.technic[1] == 'Тайдзюцу' or self.technic[1] == 'Кендзюцу') and \
                enemy.technic[1] == 'Ниндзюцу':
            self.damage += 1
        enemy.get_damage(self.damage, self)  # наносим урон противнику
        if self.chakra > 0:
            self.chakra -= 1  # тратим чакру
        self.passive_is_used = False


class Pashke(PlayCard):
    """Класс игровой карты Пашке"""

    def get_damage(self, damage, *enemy):
        """Реализация пассивной способности: после смерти Пашке в руке появляется карта Ваштэ"""
        if damage >= self.resist:
            self.is_damaged = damage - self.resist
        else:
            self.is_damaged = 0
        if self.current_health <= self.is_damaged:  # если урон больше чем здоровье + стойкость
            self.create_vashte()
            self.current_health = 0
            self.is_alive = False  # карта погибает
            if self.fraction == self.groups()[0].main_fraction:  # отосвюду удаляется
                self.point.point1_cards.remove(self)
            else:
                self.point.point2_cards.remove(self)
            self.kill()
            self.death()  # а также срабатывает анимация уничтожения
        else:
            self.current_health -= self.is_damaged  # наносим урон карте

    def create_vashte(self):
        """Cоздание Ваштэ"""
        for card in OTHER_PCARDS:
            if card.short_name == 'vashte':
                self.groups()[0].add(card)  # добавление в колоду карт
                self.groups()[0].add_card([card])  # и в руку

    def rise_vashte(self):
        """Анимация появления Ваштэ"""
        for card in OTHER_PCARDS:
            if card.short_name == 'vashte':
                self.point.info_fragment.close()
                self.point.info_fragment.main_activity.set_static_mode()
                self.point.info_fragment.main_activity.set_card_rise(card)


class Akemi(PlayCard):
    """Класс игровой карты Акеми"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, *group)
        self.enemies = []  # список врагов, получивших урон в последнем сражении
        self.sounds = [load_sound(C_VOICES, 'akemi.wav')]

    def attack(self, enemy):
        """Атака"""
        self.enemies.clear()
        self.damage = self.set_damage()  # передаём урон
        if self.technic[1] == 'Ниндзюцу' and enemy.technic[1] == 'Гендзюцу':
            self.damage += 1
        if self.technic[1] == 'Гендзюцу' and (enemy.technic[1] == 'Тайдзюцу' or
                                              enemy.technic[1] == 'Кендзюцу'):
            self.damage += 1
        if (self.technic[1] == 'Тайдзюцу' or self.technic[1] == 'Кендзюцу') and \
                enemy.technic[1] == 'Ниндзюцу':
            self.damage += 1
        enemy.get_damage(self.damage, self)  # наносим урон противнику
        """Акеми наносит урон всем врагам на точке"""
        if self.fraction == self.groups()[0].main_fraction:
            for card in self.point.point2_cards:
                if card != enemy:
                    self.enemies.append(card)
                    card.get_damage(card.resist + 1, self)
        else:
            for card in self.point.point1_cards:
                if card != enemy:
                    self.enemies.append(card)
                    card.get_damage(card.resist + 1, self)
        if self.chakra != 0:
            self.chakra -= 1  # тратим чакру

    def get_enemies(self):
        """Возвращение списка противников, получивших урон"""
        return self.enemies

    def get_ability(self):  # способность доступна, если на точке из союзных карт есть только Шу и Акеми
        if not self.passive_is_used and self.chakra > 0:
            if self.fraction == self.groups()[0].main_fraction:
                for card in self.point.point1_cards:
                    if card.short_name == 'shu' and len(self.point.point1_cards) == 2:
                        return True
            else:
                for card in self.point.point2_cards:
                    if card.short_name == 'shu' and len(self.point.point2_cards) == 2:
                        return True
        return False

    def ability(self):
        """Реализация пассивной способности: создание карты Куби Номи"""
        self.passive_is_used = True
        self.is_attacked = True
        self.chakra -= 1
        for card in OTHER_PCARDS:
            if card.short_name == 'kubi':
                self.groups()[0].add(card)
                card.point = self.point
                if self.fraction == self.groups()[0].main_fraction:
                    self.point.point1_cards.append(card)
                else:
                    self.point.point2_cards.append(card)
                self.point.add(card)
                self.point.info_fragment.close()
                self.point.info_fragment.main_activity.set_card_rise(card)


class Raik(PlayCard):
    """Класс игровой карты Райка"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'raik.wav')]

    def move(self, last_point, new_point):
        """Реализация пассивной способности: Райк не тратит дополнительные очки скорости
        при перемещении с боевой точки, на которой были противники."""
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
                new_point.add_card([self])
                new_point.update_hand()
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
                new_point.add_card([self])
                new_point.update_hand()
        self.point = new_point
        self.pace -= 1


class Kentaru(PlayCard):
    """Класс игровой карты Кентару"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.kicked = pygame.sprite.Group()  # группа для анимации вылетания карты
        self.sounds = [load_sound(C_VOICES, 'kentaru.wav')]
        self.attack_sounds = [load_sound(C_VOICES, 'attack_kentaru.wav'),
                              load_sound(C_VOICES, 'attack_kentaru1.wav')]
        self.death_sounds = [load_sound(C_VOICES, 'death_kentaru.wav')]

    def attack(self, enemy):
        """Реализация пассивной способности: 50% шанс во время атаки
         выбросить противника на случайную соседнюю точку."""
        self.kicked.empty()
        self.damage = self.set_damage()  # передаём урон
        if self.technic[1] == 'Ниндзюцу' and enemy.technic[1] == 'Гендзюцу':
            self.damage += 1
        if self.technic[1] == 'Гендзюцу' and (enemy.technic[1] == 'Тайдзюцу' or
                                              enemy.technic[1] == 'Кендзюцу'):
            self.damage += 1
        if (self.technic[1] == 'Тайдзюцу' or self.technic[1] == 'Кендзюцу') and \
                enemy.technic[1] == 'Ниндзюцу':
            self.damage += 1
        enemy.get_damage(self.damage, self)  # наносим урон противнику
        if self.chakra > 0:
            self.chakra -= 1  # тратим чакру

        self.passive_is_used = random.randint(0, 1)
        if self.passive_is_used and enemy.is_alive:  # если противник жив!
            points = []  # список доступных точек
            for i in range(len(play_board)):
                for j in range(len(play_board)):
                    if self.point.view == play_board[i][j]:  # подсвечиваем все ближайшие точки
                        if i - 1 >= 0:  # cлева
                            play_board[i - 1][j].is_hovered = True
                            play_board[i - 1][j].is_enabled = True
                        if i + 1 < len(play_board):  # справа
                            play_board[i + 1][j].is_hovered = True
                            play_board[i + 1][j].is_enabled = True
                        if j - 1 >= 0:  # сверху
                            play_board[i][j - 1].is_hovered = True
                            play_board[i][j - 1].is_enabled = True
                        if j + 1 < len(play_board):  # и снизу
                            play_board[i][j + 1].is_hovered = True
                            play_board[i][j + 1].is_enabled = True
                    elif not play_board[i][j].is_hovered:  # остальные блокируем
                        play_board[i][j].is_enabled = False
            for point in self.point.info_fragment.main_activity.battlepoints:
                if point.view.is_enabled and point != self.point:
                    if self.fraction == self.groups()[0].main_fraction:
                        if len(point.point2_cards) < 3:
                            points.append(point)
                    else:
                        if len(point.point1_cards) < 3:
                            points.append(point)
            if points:
                self.kicked.add(KickedCard(enemy, 'right'))  # создаём вылетевшую карту
                enemy.move(self.point, random.choice(points))  # перемещение вражеской карты на случайную точку


class Hiruko(PlayCard):
    """Класс игровой карты Хируко"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.passive_is_used1 = False  # использована ли основная способность?
        self.himera_is_active = False  # активна ли Химера?
        self.himera_is_used = False  # использована ли Химера?
        self.himera_card = None  # карта с украденной способностью
        self.kicked = pygame.sprite.Group()
        self.kamikazes = pygame.sprite.Group()
        self.sounds = [load_sound(C_VOICES, 'hiruko.wav'), load_sound(C_VOICES, 'hiruko1.wav')]

    def get_ability(self):  # основная способность доступна всего 1 раз за игру
        if self.passive_is_used1 or self.chakra <= 0:
            return False
        return True

    def ability(self):
        """Активация пассивной способности"""
        self.passive_is_used1 = True
        self.chakra -= 1
        for card in OTHER_BCARDS:
            if card.short_name == 'i_leave':  # добавление карты "Я ухожу!" в колоду бонусов противника
                if self.groups()[0].main_fraction == self.fraction:
                    self.point.info_fragment.main_activity.second_cards.bonus_deck.add(card)
                else:
                    self.point.info_fragment.main_activity.first_cards.bonus_deck.add(card)
                self.point.info_fragment.close()
                self.point.info_fragment.main_activity.set_card_rise(card)  # анимация появления

    def get_himera(self):
        """Активация режима Химеры"""
        self.point.info_fragment.set_static_mode()
        self.point.info_fragment.set_attack_mode()
        self.point.info_fragment.mode = 'himera'

    def himera(self, enemy):
        """Реализация химеры: кража способности"""
        self.himera_card = enemy  # добавление способности вражеской карты
        P_SECOND_INFO[self.id - 1][0][1] += '<br /><br />' + enemy.get_abilities_info()[1][35:]
        self.himera_is_active = False  # деактивация Химеры
        self.himera_is_used = True  # подтверждение использования Химеры

    def get_new_ability(self):  # новая пассивная способность доступна при тех же условиях, что и для
        if self.himera_card.short_name == 'keiko':  # родной карты
            if not self.is_attacked:
                if self.fraction == self.groups()[0].main_fraction:
                    if len(self.point.point2_cards) > 0:
                        return True
                else:
                    if len(self.point.point1_cards) > 0:
                        return True
            return False
        if self.himera_card.short_name == 'akito':
            if not self.passive_is_used and self.chakra > 0:
                if self.fraction == self.groups()[0].main_fraction:
                    if len(self.point.point1_cards) > 1:
                        return True
                else:
                    if len(self.point.point2_cards) > 1:
                        return True
            return False
        if self.himera_card.short_name == 'ryu':
            if not self.is_attacked and not self.passive_is_used and self.chakra > 0:
                if self.fraction == self.groups()[0].main_fraction:
                    if len(self.point.point2_cards) > 0:
                        return True
                else:
                    if len(self.point.point1_cards) > 0:
                        return True
            return False
        if self.himera_card.short_name == 'akemi':
            if not self.passive_is_used and self.chakra > 0:
                if self.fraction == self.groups()[0].main_fraction:
                    for card in self.point.point1_cards:
                        if card.short_name == 'shu' and len(self.point.point1_cards) == 2:
                            return True
                else:
                    for card in self.point.point2_cards:
                        if card.short_name == 'shu' and len(self.point.point2_cards) == 2:
                            return True
            return False
        if self.himera_card.short_name == 'jerry':
            if not self.is_attacked and self.chakra > 0:  # также необходимо иметь чакру
                if self.fraction == self.groups()[0].main_fraction:
                    for card in self.point.point1_cards:
                        if card.short_name == 'shu' and self.point.point2_cards:
                            return True
                else:
                    for card in self.point.point2_cards:
                        if card.short_name == 'shu' and self.point.point1_cards:
                            return True
            return False
        return False

    def new_ability(self):
        """Реализация украденной способности"""
        if self.himera_card.short_name == 'keiko':
            self.point.info_fragment.set_static_mode()
            self.passive_is_used = True
            self.point.info_fragment.set_attack_mode()
        elif self.himera_card.short_name == 'akito':
            self.point.info_fragment.set_static_mode()
            self.passive_is_active = True
            self.point.info_fragment.set_heal_mode()
        elif self.himera_card.short_name == 'ryu':
            self.point.info_fragment.set_static_mode()
            self.passive_is_active = True
            self.point.info_fragment.set_attack_mode()
        elif self.himera_card.short_name == 'akemi':
            self.passive_is_used = True
            self.is_attacked = True
            self.chakra -= 1
            for card in OTHER_PCARDS:
                if card.short_name == 'kubi':
                    self.groups()[0].add(card)
                    card.point = self.point
                    if self.fraction == self.groups()[0].main_fraction:
                        self.point.point1_cards.append(card)
                    else:
                        self.point.point2_cards.append(card)
                    self.point.add(card)
                    self.point.info_fragment.close()
                    self.point.info_fragment.main_activity.set_card_rise(card)
        elif self.himera_card.short_name == 'jerry':
            self.point.info_fragment.set_static_mode()
            self.passive_is_active = True
            self.point.info_fragment.set_attack_mode()

    def attack(self, enemy):
        """Реализация украденной способности во время атаки"""
        self.kicked.empty()
        self.damage = self.set_damage()  # передаём урон
        if self.technic[1] == 'Ниндзюцу' and enemy.technic[1] == 'Гендзюцу':
            self.damage += 1
        if self.technic[1] == 'Гендзюцу' and (enemy.technic[1] == 'Тайдзюцу' or
                                              enemy.technic[1] == 'Кендзюцу'):
            self.damage += 1
        if (self.technic[1] == 'Тайдзюцу' or self.technic[1] == 'Кендзюцу') and \
                enemy.technic[1] == 'Ниндзюцу':
            self.damage += 1
        if self.chakra > 0:
            self.chakra -= 1  # тратим чакру
        if self.himera_is_used and self.himera_card.short_name == 'keiko':
            if self.passive_is_used:
                enemy.get_damage(enemy.current_health + enemy.resist, self)  # наносим урон противнику
                self.current_health = 0
                self.is_alive = False  # карта погибает
                if self.fraction == self.groups()[0].main_fraction:  # отосвюду удаляется
                    self.point.point1_cards.remove(self)
                else:
                    self.point.point2_cards.remove(self)
                self.kill()
                self.death()  # а также срабатывает анимация уничтожения
                return
            else:
                enemy.get_damage(self.damage, self)
                return
        if self.himera_is_used and self.himera_card.short_name == 'ryu':
            if self.passive_is_active:
                self.passive_is_used = True
                enemy.is_blocked = True
                enemy.get_damage(self.damage, self)
            return
        if self.himera_is_used and self.himera_card.short_name == 'teeru':
            enemy.get_damage(self.damage, self)
            if not enemy.is_alive:
                if self.groups()[0].main_fraction == self.fraction:
                    if self.point.info_fragment.main_activity.second_cards.bonus_deck.sprites():
                        bonus = random.choice(self.point.info_fragment.main_activity.
                                              second_cards.bonus_deck.sprites())
                        self.point.info_fragment.main_activity.second_cards.bonus_deck.remove(bonus)
                else:
                    if self.point.info_fragment.main_activity.first_cards.bonus_deck.sprites():
                        bonus = random.choice(self.point.info_fragment.main_activity.
                                              first_cards.bonus_deck.sprites())
                        self.point.info_fragment.main_activity.first_cards.bonus_deck.remove(bonus)
            return
        if self.himera_is_used and self.himera_card.short_name == 'kentaru':
            self.passive_is_used = random.randint(0, 1)
            if self.passive_is_used and enemy.is_alive:  # если противник жив!
                points = []  # список доступных точек
                for i in range(len(play_board)):
                    for j in range(len(play_board)):
                        if self.point.view == play_board[i][j]:  # подсвечиваем все ближайшие точки
                            if i - 1 >= 0:  # cлева
                                play_board[i - 1][j].is_hovered = True
                                play_board[i - 1][j].is_enabled = True
                            if i + 1 < len(play_board):  # справа
                                play_board[i + 1][j].is_hovered = True
                                play_board[i + 1][j].is_enabled = True
                            if j - 1 >= 0:  # сверху
                                play_board[i][j - 1].is_hovered = True
                                play_board[i][j - 1].is_enabled = True
                            if j + 1 < len(play_board):  # и снизу
                                play_board[i][j + 1].is_hovered = True
                                play_board[i][j + 1].is_enabled = True
                        elif not play_board[i][j].is_hovered:  # остальные блокируем
                            play_board[i][j].is_enabled = False
                for point in self.point.info_fragment.main_activity.battlepoints:
                    if point.view.is_enabled and point != self.point:
                        if self.fraction == self.groups()[0].main_fraction:
                            if len(point.point2_cards) < 3:
                                points.append(point)
                        else:
                            if len(point.point1_cards) < 3:
                                points.append(point)
                if points:
                    self.kicked.add(KickedCard(enemy, 'right'))  # создаём вылетевшую карту
                    enemy.move(self.point,
                               random.choice(points))  # перемещение вражеской карты на случайную точку
        if self.himera_is_used and self.himera_card.short_name == 'iketani':
            if enemy.is_alive:
                points = []
                for i in range(len(play_board)):
                    for j in range(len(play_board)):
                        if self.point.view == play_board[i][j]:  # подсвечиваем все ближайшие точки
                            if i - 1 >= 0:  # cлева
                                play_board[i - 1][j].is_hovered = True
                                play_board[i - 1][j].is_enabled = True
                            if i + 1 < len(play_board):  # справа
                                play_board[i + 1][j].is_hovered = True
                                play_board[i + 1][j].is_enabled = True
                            if j - 1 >= 0:  # сверху
                                play_board[i][j - 1].is_hovered = True
                                play_board[i][j - 1].is_enabled = True
                            if j + 1 < len(play_board):  # и снизу
                                play_board[i][j + 1].is_hovered = True
                                play_board[i][j + 1].is_enabled = True
                        elif not play_board[i][j].is_hovered:  # остальные блокируем
                            play_board[i][j].is_enabled = False
                for point in self.point.info_fragment.main_activity.battlepoints:
                    if point.view.is_enabled and point != self.point:
                        if self.fraction == self.groups()[0].main_fraction:
                            if len(point.point2_cards) < 3:
                                points.append(point)
                        else:
                            if len(point.point1_cards) < 3:
                                points.append(point)
                if points:
                    self.kicked.add(KickedCard(enemy, 'right'))  # создаём вылетевшую карту
                    enemy.move(self.point,
                               random.choice(points))  # перемещение вражеской карты на случайную точку
        enemy.get_damage(self.damage, self)

    def heal(self, friend):
        """Реализация украденной способности поддержки"""
        if self.himera_is_used:
            if self.himera_card.short_name == 'akito':
                if self.passive_is_active:
                    self.passive_is_used = True
                    friend.pace += 2
                    self.chakra -= 1
                    self.point.info_fragment.close()
                    self.point.info_fragment.main_activity.set_static_mode()
                    self.point.info_fragment.main_activity.card_is_moving = friend
                    self.point.info_fragment.main_activity.set_move_mode(self.point)
                    self.point.info_fragment.set_static_mode()

    def get_damage(self, damage, *enemy):
        """Реализация украденной способности, связанной с получением урона"""
        if self.himera_is_used:
            if self.himera_card.short_name == 'kitsu':
                if enemy[0].spec == 'Боец Ближнего боя':
                    self.passive_is_used = random.randint(0, 9)
                    if self.passive_is_used:
                        self.is_damaged = 0
                        self.passive_is_used = False
                        return
            if self.himera_card.short_name == 'ryu':
                if self.passive_is_active:
                    self.passive_is_active = False
                    self.is_damaged = 0
                    return
            if self.himera_card.short_name == 'shu':
                self.passive_is_used = random.choice([True, False, False])
                if self.passive_is_used:
                    self.is_damaged = 0
                    self.passive_is_used = False
                    return
        if damage >= self.resist:
            self.is_damaged = damage - self.resist
        else:
            self.is_damaged = 0
        if self.himera_is_used and self.himera_card.short_name == 'pashke':
            if self.current_health <= self.is_damaged:  # если урон больше чем здоровье + стойкость
                self.create_vashte()
                self.current_health = 0
                self.is_alive = False  # карта погибает
                if self.fraction == self.groups()[0].main_fraction:  # отосвюду удаляется
                    self.point.point1_cards.remove(self)
                else:
                    self.point.point2_cards.remove(self)
                self.kill()
                self.death()  # а также срабатывает анимация уничтожения
        else:
            if self.current_health <= self.is_damaged:  # если урон больше чем здоровье + стойкость
                self.current_health = 0
                self.is_alive = False  # карта погибает
                if self.fraction == self.groups()[0].main_fraction:  # отосвюду удаляется
                    self.point.point1_cards.remove(self)
                else:
                    self.point.point2_cards.remove(self)
                self.kill()
                self.death()  # а также срабатывает анимация уничтожения
            else:
                self.current_health -= self.is_damaged  # наносим урон карте

    def move(self, last_point, new_point):
        if self.himera_is_used and self.himera_card.short_name == 'raik':
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
                    new_point.add_card([self])
                    new_point.update_hand()
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
                    new_point.add_card([self])
                    new_point.update_hand()
            self.point = new_point
            self.pace -= 1
        else:
            if last_point == self.groups()[0]:  # если текущая точка это база
                last_point.hand.remove(self)  # удаляем из руки и добавляем в новую точку
                if self.fraction == self.groups()[0].main_fraction:
                    new_point.point1_cards.append(self)
                else:
                    new_point.point2_cards.append(self)
                new_point.add(self)
                new_point.update_card_draw()
                self.pace -= 1
            else:
                last_point.remove(self)
                if self.fraction == self.groups()[0].main_fraction:
                    last_point.point1_cards.remove(self)
                    if last_point.point2_cards:  # если на точке были противники
                        self.pace -= 2  # тратим дополнительную единицу скорости
                    else:
                        self.pace -= 1
                else:
                    last_point.point2_cards.remove(self)
                    if last_point.point1_cards:
                        self.pace -= 2
                    else:
                        self.pace -= 1
                if new_point == self.groups()[0]:  # если новая точка это база
                    new_point.add_card([self])  # добавляем её в руку
                else:
                    if self.fraction == self.groups()[0].main_fraction:
                        new_point.point1_cards.append(self)
                    else:
                        new_point.point2_cards.append(self)
                    new_point.add(self)
            self.point = new_point  # установка нового местоположения

    def create_vashte(self):
        """Cоздание Ваштэ"""
        for card in OTHER_PCARDS:
            if card.short_name == 'vashte':
                self.groups()[0].add(card)  # добавление в колоду карт
                self.groups()[0].add_card([card])  # и в руку

    def rise_vashte(self):
        """Анимация появления Ваштэ"""
        for card in OTHER_PCARDS:
            if card.short_name == 'vashte':
                self.point.info_fragment.close()
                self.point.info_fragment.main_activity.set_static_mode()
                self.point.info_fragment.main_activity.set_card_rise(card)

    def get_kamikaze(self, enemy, point):
        """Создание мышей-камикадзе"""
        self.is_attacked, self.passive_is_active = True, False
        self.kamikazes.add(Kamikaze(point))  # создаём мышь-камикадзе
        if enemy.resist - 2 < 0:  # отнимаем у противника 2 единицы стойкости
            enemy.resist = 0
        else:
            enemy.resist -= 2
        if self.chakra > 0:
            self.chakra -= 1


class Iketani(Kentaru):
    """Класс игровой карты Икетани"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'iketani.wav')]
        self.attack_sounds = [load_sound(C_VOICES, 'attack_iketani.wav'),
                              load_sound(C_VOICES, 'attack_iketani1.wav')]
        self.death_sounds = [load_sound(C_VOICES, 'death_iketani.wav')]

    def attack(self, enemy):
        """Реализация пассивной способности: во время атаки Икетани со 100% вероятностью
        выбрасывает противника на случайную соседнюю точку."""
        self.kicked.empty()
        self.damage = self.set_damage()  # передаём урон
        if self.technic[1] == 'Ниндзюцу' and enemy.technic[1] == 'Гендзюцу':
            self.damage += 1
        if self.technic[1] == 'Гендзюцу' and (enemy.technic[1] == 'Тайдзюцу' or
                                              enemy.technic[1] == 'Кендзюцу'):
            self.damage += 1
        if (self.technic[1] == 'Тайдзюцу' or self.technic[1] == 'Кендзюцу') and \
                enemy.technic[1] == 'Ниндзюцу':
            self.damage += 1
        enemy.get_damage(self.damage, self)  # наносим урон противнику
        if self.chakra > 0:
            self.chakra -= 1  # тратим чакру

        if enemy.is_alive:
            points = []
            for i in range(len(play_board)):
                for j in range(len(play_board)):
                    if self.point.view == play_board[i][j]:  # подсвечиваем все ближайшие точки
                        if i - 1 >= 0:  # cлева
                            play_board[i - 1][j].is_hovered = True
                            play_board[i - 1][j].is_enabled = True
                        if i + 1 < len(play_board):  # справа
                            play_board[i + 1][j].is_hovered = True
                            play_board[i + 1][j].is_enabled = True
                        if j - 1 >= 0:  # сверху
                            play_board[i][j - 1].is_hovered = True
                            play_board[i][j - 1].is_enabled = True
                        if j + 1 < len(play_board):  # и снизу
                            play_board[i][j + 1].is_hovered = True
                            play_board[i][j + 1].is_enabled = True
                    elif not play_board[i][j].is_hovered:  # остальные блокируем
                        play_board[i][j].is_enabled = False
            for point in self.point.info_fragment.main_activity.battlepoints:
                if point.view.is_enabled and point != self.point:
                    if self.fraction == self.groups()[0].main_fraction:
                        if len(point.point2_cards) < 3:
                            points.append(point)
                    else:
                        if len(point.point1_cards) < 3:
                            points.append(point)
            if points:
                self.kicked.add(KickedCard(enemy, 'right'))  # создаём вылетевшую карту
                enemy.move(self.point, random.choice(points))  # перемещение вражеской карты на случайную точку


class Jerry(PlayCard):
    """Класс игровой карты Джерри"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.kamikazes = pygame.sprite.Group()  # группа для отрисовки мышей-камикадзе
        self.sounds = [load_sound(C_VOICES, 'jerry.wav')]
        self.attack_sounds = [load_sound(C_VOICES, 'attack_jerry.wav'),
                              load_sound(C_VOICES, 'attack_jerry1.wav')]

    def get_ability(self):  # способность доступна, если на точке есть Шу и противники
        if not self.is_attacked and self.chakra > 0:  # также необходимо иметь чакру
            if self.fraction == self.groups()[0].main_fraction:
                for card in self.point.point1_cards:
                    if card.short_name == 'shu' and self.point.point2_cards:
                        return True
            else:
                for card in self.point.point2_cards:
                    if card.short_name == 'shu' and self.point.point1_cards:
                        return True
        return False

    def ability(self):
        """Активация способности, включение атакующего состояния боевой точки"""
        self.point.info_fragment.set_static_mode()
        self.passive_is_active = True
        self.point.info_fragment.set_attack_mode()

    def get_kamikaze(self, enemy, point):
        """Создание мышей-камикадзе"""
        self.is_attacked, self.passive_is_active = True, False
        self.kamikazes.add(Kamikaze(point))  # создаём мышь-камикадзе
        if enemy.resist - 2 < 0:  # отнимаем у противника 2 единицы стойкости
            enemy.resist = 0
        else:
            enemy.resist -= 2
        if self.chakra > 0:
            self.chakra -= 1


"""Классы игровых карт Ивагакуре"""


class Keiko(PlayCard):
    """Класс игровой карты Кеико"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'keiko.wav')]
        self.attack_sounds = [load_sound(C_VOICES, 'attack_keiko.wav'),
                              load_sound(C_VOICES, 'attack_keiko1.wav')]
        self.death_sounds = [load_sound(C_VOICES, 'death_keiko.wav')]

    def get_ability(self):  # способность доступна, если на точке есть противники
        if not self.is_attacked and self.chakra > 0:
            if self.fraction == self.groups()[0].main_fraction:
                if len(self.point.point2_cards) > 0:
                    return True
            else:
                if len(self.point.point1_cards) > 0:
                    return True
        return False

    def ability(self):
        self.point.info_fragment.set_static_mode()
        self.passive_is_used = True
        self.point.info_fragment.set_attack_mode()

    def attack(self, enemy):
        """Атака"""
        self.damage = self.set_damage()  # передаём урон
        if self.technic[1] == 'Ниндзюцу' and enemy.technic[1] == 'Гендзюцу':
            self.damage += 1
        if self.technic[1] == 'Гендзюцу' and (enemy.technic[1] == 'Тайдзюцу' or
                                              enemy.technic[1] == 'Кендзюцу'):
            self.damage += 1
        if (self.technic[1] == 'Тайдзюцу' or self.technic[1] == 'Кендзюцу') and \
                enemy.technic[1] == 'Ниндзюцу':
            self.damage += 1
        if self.chakra > 0:
            self.chakra -= 1
        if self.passive_is_used:
            enemy.get_damage(enemy.current_health + enemy.resist, self)  # наносим урон противнику
            self.current_health = 0
            self.is_alive = False  # карта погибает
            if self.fraction == self.groups()[0].main_fraction:  # отосвюду удаляется
                self.point.point1_cards.remove(self)
            else:
                self.point.point2_cards.remove(self)
            self.kill()
            self.death()  # а также срабатывает анимация уничтожения
        else:
            enemy.get_damage(self.damage, self)


class Akito(PlayCard):
    """Класс игровой карты Акито"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.new_technic = None  # новая техника (при выпадении "Я Медик, честно!")
        self.sounds = [load_sound(C_VOICES, 'akito.wav')]
        self.attack_sounds = [load_sound(C_VOICES, 'attack_akito.wav')]
        self.death_sounds = [load_sound(C_VOICES, 'death_akito.wav')]
        self.heal_sounds = [load_sound(C_VOICES, 'heal_akito.wav')]
        self.owl_sound = [load_sound(C_VOICES, 'owl.wav')]

    def get_ability(self):  # способность доступна 1 раз за ход
        if not self.passive_is_used and self.chakra > 0:
            if self.fraction == self.groups()[0].main_fraction:
                if len(self.point.point1_cards) > 1:
                    return True
            else:
                if len(self.point.point2_cards) > 1:
                    return True
        return False

    def ability(self):
        """Активация способности, включение режима лечения"""
        self.point.info_fragment.set_static_mode()
        self.passive_is_active = True
        self.point.info_fragment.set_heal_mode()

    def heal(self, friend):
        """Реализация пассивной способности: перемещение союзника без затрат скорости"""
        if self.passive_is_active:
            self.passive_is_used = True
            friend.pace += 2
            self.chakra -= 1
            self.point.info_fragment.close()
            self.point.info_fragment.main_activity.set_static_mode()
            self.point.info_fragment.main_activity.card_is_moving = friend
            self.point.info_fragment.main_activity.set_move_mode(self.point)
            self.point.info_fragment.set_static_mode()
            my_sound = random.choice(self.owl_sound)
            if self.point.info_fragment.channel and self.point.info_fragment.channel.get_busy():
                self.point.info_fragment.channel.stop()
            self.point.info_fragment.channel = my_sound.play()
            self.point.info_fragment.channel.set_volume(CARD_VOLUME)
        else:
            if friend.current_health + int(self.technic[0]) > friend.health_capacity:
                friend.current_health = friend.health_capacity
            else:
                friend.current_health += int(self.technic[0])
            self.is_healed = True
            self.chakra -= 1
            my_sound = random.choice(self.heal_sounds)
            if self.point.info_fragment.channel and self.point.info_fragment.channel.get_busy():
                self.point.info_fragment.channel.stop()
            self.point.info_fragment.channel = my_sound.play()
            self.point.info_fragment.channel.set_volume(CARD_VOLUME)

    def set_damage(self):
        """Установка урона"""
        if self.spec != 'Медик' or self.new_technic:  # если доступна атакующая технкиа
            damage = self.pace + self.chakra + int(self.new_technic[0])  # урон складывается из 3 показателей
        else:
            damage = self.pace + self.chakra  # иначе из двух (т.к. медик)
        if self.chakra <= 0:
            return 0
        if self.groups():
            if self.point != self.groups()[0]:  # если срабатывает синергия
                if self.fraction == self.groups()[0].main_fraction:
                    if len(self.point.point1_cards) > 1 and self.synergy == 'Все':
                        damage += 1  # добавляем 1 к урону
                    for card in self.point.point1_cards:
                        if card.name.split()[0] in self.synergy:
                            damage += 1
                    for card in self.point.point1_cards:
                        if card.short_name == 'benkei' and not card.passive_is_used:
                            return damage - 2
                        if card.short_name == 'benkei' and card.passive_is_used:
                            return damage + 1
                        if card.short_name == 'hiruko' and card.himera_is_used:
                            if card.himera_card.short_name == 'benkei' and \
                                    not card.himera_card.passive_is_used:
                                return damage - 2
                            if card.himera_card.short_name == 'benkei' and card.himera_card.passive_is_used:
                                return damage + 1
                else:
                    if len(self.point.point2_cards) > 1 and self.synergy == 'Все':
                        damage += 1
                    for card in self.point.point2_cards:
                        if card.name.split()[0] in self.synergy:
                            damage += 1
                    for card in self.point.point2_cards:
                        if card.short_name == 'benkei' and not card.passive_is_used:
                            return damage - 2
                        if card.short_name == 'benkei' and card.passive_is_used:
                            return damage + 1
                        if card.short_name == 'hiruko' and card.himera_is_used:
                            if card.himera_card.short_name == 'benkei' and \
                                    not card.himera_card.passive_is_used:
                                return damage - 2
                            if card.himera_card.short_name == 'benkei' and card.himera_card.passive_is_used:
                                return damage + 1
        return damage  # возвращаем урон

    def get_heal_sound(self):
        if self.heal_sounds:
            my_sound = random.choice(self.heal_sounds)
            return my_sound
        return None

    def get_owl_sound(self):
        if self.owl_sound:
            my_sound = random.choice(self.owl_sound)
            return my_sound
        return None


class Ryu(PlayCard):
    """Класс игровой карты Рюу"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'ryu.wav')]

    def get_ability(self):  # способность доступна 1 раз за игру
        if not self.passive_is_used and self.chakra > 0:
            if self.fraction == self.groups()[0].main_fraction:
                if len(self.point.point2_cards) > 0:
                    return True
            else:
                if len(self.point.point1_cards) > 0:
                    return True
        return False

    def ability(self):
        "Активация пассивной способности, включение режима атаки"
        self.point.info_fragment.set_static_mode()
        self.passive_is_active = True
        self.point.info_fragment.set_attack_mode()

    def attack(self, enemy):
        """Атака"""
        self.damage = self.set_damage()  # передаём урон
        """Проверка на виды техник"""
        if self.technic[1] == 'Ниндзюцу' and enemy.technic[1] == 'Гендзюцу':
            self.damage += 1
        if self.technic[1] == 'Гендзюцу' and (enemy.technic[1] == 'Тайдзюцу' or
                                              enemy.technic[1] == 'Кендзюцу'):
            self.damage += 1
        if (self.technic[1] == 'Тайдзюцу' or self.technic[1] == 'Кендзюцу') and \
                enemy.technic[1] == 'Ниндзюцу':
            self.damage += 1
        enemy.get_damage(self.damage, self)  # наносим урон противнику
        if self.chakra > 0:
            self.chakra -= 1  # тратим чакру
        if self.passive_is_active:
            self.passive_is_used = True
            enemy.is_blocked = True

    def heal(self, friend):
        """Лечение"""
        if friend.current_health + int(self.technic[0]) > friend.health_capacity:
            friend.current_health = friend.health_capacity
        else:
            friend.current_health += int(self.technic[0])
        if friend.chakra < friend.default_chakra:
            friend.chakra += 1
        self.is_healed = True
        if self.chakra > 0:
            self.chakra -= 1

    def get_damage(self, damage, *enemy):
        """Получение урона"""
        if self.is_alive:  # если карта жива
            if self.passive_is_active:
                self.is_damaged = 0
                self.passive_is_active = False
                return
            if damage >= self.resist:
                self.is_damaged = damage - self.resist
            else:
                self.is_damaged = 0  # если урон меньше стойкости, то он не наносится
            if self.current_health <= self.is_damaged:  # если урон больше чем здоровье + стойкость
                self.current_health = 0
                self.is_alive = False  # карта погибает
                if self.fraction == self.groups()[0].main_fraction:  # отосвюду удаляется
                    self.point.point1_cards.remove(self)
                else:
                    self.point.point2_cards.remove(self)
                self.kill()
                self.death()  # а также срабатывает анимация уничтожения
            else:
                self.current_health -= self.is_damaged  # наносим урон карте


class Kitsu(PlayCard):
    """Класс игровой карты Кицу"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'kitsu.wav')]
        self.attack_sounds = [load_sound(C_VOICES, 'attack_kitsu.wav'),
                              load_sound(C_VOICES, 'attack_kitsu1.wav')]

    def get_damage(self, damage, *enemy):
        """Реализация пассивной способности: 90% шанс не получить
        урон от Бойца Ближнего боя"""
        if enemy[0].spec == 'Боец Ближнего боя':
            self.passive_is_used = random.randint(0, 9)
            if self.passive_is_used:
                self.is_damaged = 0
                self.passive_is_used = False
                return
        if damage >= self.resist:
            self.is_damaged = damage - self.resist
        else:
            self.is_damaged = 0
        if self.current_health <= self.is_damaged:  # если урон больше чем здоровье + стойкость
            self.current_health = 0
            self.is_alive = False  # карта погибает
            if self.fraction == self.groups()[0].main_fraction:  # отосвюду удаляется
                self.point.point1_cards.remove(self)
            else:
                self.point.point2_cards.remove(self)
            self.kill()
            self.death()  # а также срабатывает анимация уничтожения
        else:
            self.current_health -= self.is_damaged  # наносим урон карте


class Benkei(PlayCard):
    """Класс игровой карты Бенкей"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'benkei.wav')]
        self.attack_sounds = [load_sound(C_VOICES, 'attack_benkei.wav'),
                              load_sound(C_VOICES, 'attack_benkei1.wav')]
        self.death_sounds = [load_sound(C_VOICES, 'death_benkei.wav')]


class Teeru(PlayCard):
    """Класс игровой карты Тееру"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'teeru.wav')]
        self.attack_sounds = [load_sound(C_VOICES, 'attack_teeru.wav')]
        self.death_sounds = [load_sound(C_VOICES, 'death_teeru.wav')]

    def attack(self, enemy):
        """Реализация пассивной способонсти: сжигание вражеской карты-бонуса после уничтожения противника"""
        self.damage = self.set_damage()  # передаём урон
        if self.technic[1] == 'Ниндзюцу' and enemy.technic[1] == 'Гендзюцу':
            self.damage += 1
        if self.technic[1] == 'Гендзюцу' and (enemy.technic[1] == 'Тайдзюцу' or
                                              enemy.technic[1] == 'Кендзюцу'):
            self.damage += 1
        if (self.technic[1] == 'Тайдзюцу' or self.technic[1] == 'Кендзюцу') and \
                enemy.technic[1] == 'Ниндзюцу':
            self.damage += 1
        enemy.get_damage(self.damage, self)  # наносим урон противнику
        if not enemy.is_alive:
            if self.groups()[0].main_fraction == self.fraction:
                if self.point.info_fragment.main_activity.second_cards.bonus_deck.sprites():
                    bonus = random.choice(self.point.info_fragment.main_activity.
                                          second_cards.bonus_deck.sprites())
                    self.point.info_fragment.main_activity.second_cards.bonus_deck.remove(bonus)
            else:
                if self.point.info_fragment.main_activity.first_cards.bonus_deck.sprites():
                    bonus = random.choice(self.point.info_fragment.main_activity.
                                          first_cards.bonus_deck.sprites())
                    self.point.info_fragment.main_activity.first_cards.bonus_deck.remove(bonus)
        if self.chakra > 0:
            self.chakra -= 1  # тратим чакру


"""Классы бонусных карт Конохагакуре"""


class BarKonoha(BonusCard):
    """Класс бонусной карты Бар Конохи"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'bar.wav'), load_sound(C_VOICES, 'bar1.wav')]

    def bonus(self):
        """Активация эффекта"""
        for card in PLAYCARDS:  # связываем все доступные карты Конохи синергией
            if card.fraction == KONOHAGAKURE and card.groups():
                card.synergy = 'Все'
        for card in OTHER_PCARDS:
            if card.fraction == KONOHAGAKURE and card.groups():
                card.synergy = 'Все'


class Himera(BonusCard):
    """Класс бонусной карты Химера"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'himera.wav'), load_sound(C_VOICES, 'himera1.wav')]

    def bonus(self):
        """Активация эффекта"""
        for card in PLAYCARDS:  # активация Химеры
            if card.short_name == 'hiruko':
                card.himera_is_active = True


class Tsunami(BonusCard):
    """Класс бонусной карты Тсунами"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'tsunami.wav')]

    def bonus(self):
        """Активация эффекта"""
        for card in PLAYCARDS:
            if card.short_name == 'akemi' and card.groups():
                card.passive_is_used = True  # отмена пассивной способности Акеми
            if card.short_name == 'kentaru' and card.groups():
                for other_card in OTHER_PCARDS:
                    if other_card.short_name == 'iketani':  # появление Икетани в руке
                        other_card.fraction = card.fraction
                        card.groups()[0].add(other_card)
                        card.groups()[0].add_card([other_card])
                        card.groups()[0].update_hand()
                card.current_health = 0  # уничтожение игровой карты Кентару
                card.is_alive = False  # карта погибает
                if card.point != card.groups()[0]:
                    if card.fraction == card.groups()[0].main_fraction:  # отосвюду удаляется
                        card.point.point1_cards.remove(card)
                    else:
                        card.point.point2_cards.remove(card)
                else:
                    card.groups()[0].hand.remove(card)
                card.kill()


class KingOfMouse(BonusCard):
    """Класс бонусной карты Король мышей"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'king_of_mouse.wav')]

    def bonus(self):
        """Активация эффекта"""
        for card in OTHER_PCARDS:
            if card.short_name == 'jerry':  # создание Джерри и добавление в руку
                for other_card in PLAYCARDS:
                    if other_card.fraction == KONOHAGAKURE and other_card.groups():
                        other_card.groups()[0].add(card)
                        other_card.groups()[0].add_card([card])
                        other_card.groups()[0].update_hand()
                        return
                for other_card in OTHER_PCARDS:
                    if other_card.fraction == KONOHAGAKURE and other_card.groups():
                        other_card.groups()[0].add(card)
                        other_card.groups()[0].add_card([card])
                        other_card.groups()[0].update_hand()
                        return


class Ren(BonusCard):
    """Класс бонусной карты Рен"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'ren.wav')]

    def bonus(self):
        """Активация эффекта: переход всех союзных карт с вражеской точки к сопернику"""
        if self.main_activity.first_cards.fraction == KONOHAGAKURE:
            for battlepoint in self.main_activity.battlepoints[3:]:
                    for i in range(len(battlepoint.point1_cards)):
                        battlepoint.point1_cards[i].kill()
                        battlepoint.point1_cards[i].fraction = IVAGAKURE
                        self.main_activity.second_cards.add(battlepoint.point1_cards[i])
                    self.main_activity.second_cards.add_card(battlepoint.point1_cards)
                    self.main_activity.second_cards.update_hand()
                    battlepoint.point1_cards.clear()
        else:
            for battlepoint in self.main_activity.battlepoints[:6]:
                for i in range(len(battlepoint.point2_cards)):
                    battlepoint.point2_cards[i].kill()
                    battlepoint.point2_cards[i].fraction = IVAGAKURE
                    self.main_activity.first_cards.add(battlepoint.point2_cards[i])
                self.main_activity.first_cards.add_card(battlepoint.point2_cards)
                self.main_activity.first_cards.update_hand()
                battlepoint.point2_cards.clear()


class I_leave(BonusCard):
    """Класс бонусной карты Я ухожу"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'i_leave.wav')]

    def bonus(self):
        """Активация эффекта: сжигает случайную карту-бонус у противника"""
        if self.main_activity.first_cards.main_fraction == self.fraction:
            if len(self.main_activity.second_cards.bonus_deck.sprites()) > 1:
                bonuscard = self
                while bonuscard == self:
                    bonuscard = random.choice(self.main_activity.second_cards.bonus_deck.sprites())
                self.main_activity.second_cards.bonus_deck.remove(bonuscard)
        else:
            if len(self.main_activity.first_cards.bonus_deck.sprites()) > 1:
                bonuscard = self
                while bonuscard == self:
                    bonuscard = random.choice(self.main_activity.first_cards.bonus_deck.sprites())
                self.main_activity.first_cards.bonus_deck.remove(bonuscard)


"""Классы бонусных карт Ивагакуре"""


class HymnIva(BonusCard):
    """Класс бонусной карты Гимн Ивагакуре"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'hymn.wav')]

    def bonus(self):
        """Активация эффекта"""
        for card in PLAYCARDS:  # добавление стойкости всем доступным картам Ивагакуре
            if card.fraction == IVAGAKURE and card.groups():
                card.resist += 1
        for card in OTHER_PCARDS:
            if card.fraction == IVAGAKURE and card.groups():
                card.resist += 1


class Turtle(BonusCard):
    """Класс бонусной карты Построение: Черепаха"""

    def bonus(self):
        """Активация эффекта"""
        for card in OTHER_PCARDS:  # создание 4-х клонов Кеико Гисе
            if card.short_name == 'clone':
                if self.main_activity.first_cards.fraction == KONOHAGAKURE:
                    self.main_activity.second_cards.add(card)
                    self.main_activity.second_cards.add_card([card])
                    self.main_activity.second_cards.update_hand()
                else:
                    self.main_activity.first_cards.add(card)
                    self.main_activity.first_cards.add_card([card])
                    self.main_activity.first_cards.update_hand()


class Kin(BonusCard):
    """Класс бонусной карты Кин Ивата"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'kin.wav')]

    def bonus(self):
        """Активация эффекта: обновление пассивной способности Бенкея"""
        for card in PLAYCARDS:
            if card.short_name == 'benkei':
                card.passive_is_used = True
                P_SECOND_INFO[card.id - 1][0][1] = '«Признание» – все союзники, находящиеся на одной' \
                                                   ' точке с данной картой, получают +1 к урону. Сама карта ' \
                                                   'также получает бонус к урону (+1).'


class TrueMedic(BonusCard):
    """Класс бонусной карты Я медик, честно!"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'true_medic.wav')]

    def bonus(self):
        """Активация эффекта"""
        for card in PLAYCARDS:
            if card.short_name == 'akito':
                card.new_technic = [4, 'Ниндзюцу']  # добавление новой техники
                P_SECOND_INFO[card.id - 1][0][0] += '<br /><br />«Адамантовые Цепи» – наносит 4' \
                                                    ' единицы урона (Ниндзюцу).'


class Ambitions(BonusCard):
    """Класс бонусной карты Амбициозноасть"""

    def __init__(self, image, args, *group):
        super().__init__(image, args, group)
        self.sounds = [load_sound(C_VOICES, 'death_keiko.wav')]

    def bonus(self):
        """Активация эффекта: уничтожение Кеико и всех карт,
        находившихся с ним на одной точке."""
        if self.main_activity.first_cards.main_fraction == KONOHAGAKURE:
            for card in self.main_activity.second_cards:
                if card.short_name == 'keiko':
                    if card in self.main_activity.second_cards.hand:
                        self.main_activity.second_cards.hand.remove(card)
                        card.kill()
                        break
            for battlepoint in self.main_activity.battlepoints:
                if len(battlepoint.point2_cards) > 0:
                    for i in range(len(battlepoint.point2_cards)):
                        if battlepoint.point2_cards[i].short_name == 'keiko':
                            if i == 0:
                                for j in range(len(battlepoint.point2_cards)):
                                    battlepoint.point2_cards[j].kill()
                            elif i == 1:
                                battlepoint.point2_cards[i].kill()
                                battlepoint.point2_cards[i - 1].kill()
                                if len(battlepoint.point2_cards) == 3:
                                    battlepoint.point2_cards[i + 1].kill()
                            else:
                                for j in range(3):
                                    battlepoint.point2_cards[2 - j].kill()
                            battlepoint.point2_cards.clear()
                            break
        else:
            for card in self.main_activity.first_cards:
                if card.short_name == 'keiko':
                    if card in self.main_activity.first_cards.hand:
                        self.main_activity.first_cards.hand.remove(card)
                        card.kill()
                        break
            for battlepoint in self.main_activity.battlepoints:
                if len(battlepoint.point1_cards) > 0:
                    for i in range(len(battlepoint.point1_cards)):
                        if battlepoint.point1_cards[i].short_name == 'keiko':
                            if i == 0:
                                for j in range(len(battlepoint.point1_cards)):
                                    battlepoint.point1_cards[j].kill()
                            elif i == 1:
                                battlepoint.point1_cards[i].kill()
                                battlepoint.point1_cards[i - 1].kill()
                                if len(battlepoint.point1_cards) == 3:
                                    battlepoint.point1_cards[i + 1].kill()
                            else:
                                for j in range(3):
                                    battlepoint.point1_cards[2 - j].kill()
                            battlepoint.point1_cards.clear()
                            break
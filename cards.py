import pygame
import sqlite3
import os
import sys

database = os.path.join('data', 'card_db.db')
PLAYCARDS_DATA = sqlite3.connect(database).cursor().execute("""SELECT id, fraction, name, short_name, 
                        specialization, pace, chakra, resistance, health, technic, synergy FROM playcards""")
BONUSCARDS_DATA = sqlite3.connect(database).cursor().execute("""SELECT id, fraction, name, 
                                                                short_name FROM bonuscards""")
PLAYCARDS_DATA, BONUSCARDS_DATA = [list(i) for i in PLAYCARDS_DATA], [list(i) for i in BONUSCARDS_DATA]
p_images = ['shu.jpg', 'pashke.jpg', 'akemi.jpg', 'raik.jpg', 'kentaru.jpg', 'hiruko.jpg',
            'keiko.jpg', 'akito.jpg', 'ryu.jpg', 'kitsu.jpg', 'benkei.jpg', 'teeru.jpg']
b_images = ['bar.jpg', 'himera.jpg', 'tsunami.jpg', 'king_mouse.jpg', 'ren.jpg',
            'hymn.jpg', 'turtle.jpg', 'kin.jpg', 'true_medic.jpg', 'ambitions.jpg']
PLAYCARDS, BONUSCARDS, P_SECOND_INFO, B_SECOND_INFO = [], [], [], []

pygame.font.init()
b_font = pygame.font.Font('resources/fonts/rusmadeinchinav2.ttf', 26)
b_font1 = pygame.font.Font('resources/fonts/rusmadeinchinav2.ttf', 30)
font = pygame.font.Font('resources/fonts/HanZi.ttf', 14)
font1 = pygame.font.Font('resources/fonts/HanZi.ttf', 12)
font2 = pygame.font.Font('resources/fonts/HanZi.ttf', 10)
font3 = pygame.font.Font('resources/fonts/HanZi.ttf', 8)


def load_image(name, colorkey=None):
    fullname = os.path.join('resources', 'cards')
    fullname = os.path.join(fullname, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class PlayCard(pygame.sprite.Sprite):

    def __init__(self, image, id, fraction, name, short_name, spec, pace, chakra,
                 resist, health, technic, synergy):
        super().__init__()
        self.image = load_image(image)
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

    def passive_ability(self):
        pass

    def get_info(self, *args):
        screen2 = pygame.Surface(args[0].get_size())
        screen2.blit(args[1], (0, 0))

        pygame.draw.rect(screen2, pygame.Color('black'), args[2], 3)
        pygame.draw.line(screen2, pygame.Color('black'), (args[0].get_width() - 60, 25),
                         (args[0].get_width() - 30, 55), 5)
        pygame.draw.line(screen2, pygame.Color('black'), (args[1].get_width() - 30, 25),
                         (args[0].get_width() - 60, 55), 5)

        pygame.draw.rect(screen2, pygame.Color('black'), args[3], 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (45, 32, 45, 16))
        pygame.draw.polygon(screen2, pygame.Color('black'), ((30, 40), (55, 25), (55, 55)))

        pygame.draw.rect(screen2, pygame.Color('black'), (8, 160, 464, 246), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (8, 405, 464, 45), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (8, 449, 232, 44), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (238, 449, 233, 44), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (8, 492, 232, 45), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (238, 492, 233, 45), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (8, 536, 232, 44), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (238, 536, 233, 44), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (8, 405, 464, 444), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (8, 405, 464, 290), 3)

        img_coord = self.rect.copy()
        img_coord.center = pygame.Rect((8, 160, 465, 245)).center
        title = b_font.render(f'{self.name}, ({self.spec})', 1, pygame.Color('black'))
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
        technic = b_font.render('Техника:', 1, pygame.Color('black'))
        passive_ability = b_font.render('Пассивная способность:', 1, pygame.Color('black'))
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

        screen2.blit(self.image, img_coord)
        screen2.blit(title, title_coord)
        screen2.blit(pace, pace_coord)
        screen2.blit(chakra, chakra_coord)
        screen2.blit(resist, resist_coord)
        screen2.blit(health, health_coord)
        screen2.blit(damage, damage_coord)
        screen2.blit(synergy, synergy_coord)
        screen2.blit(technic, (16, 586))
        screen2.blit(passive_ability, (16, 700))
        for i in range(len(technic_info)):
            line = font2.render(technic_info[i], 1, pygame.Color('black'))
            y = 615 + 20 * i
            screen2.blit(line, (16, y))
        for i in range(len(passive_ability_info)):
            line = font2.render(passive_ability_info[i], 1, pygame.Color('black'))
            y = 729 + 20 * i
            screen2.blit(line, (16, y))

        args[4].empty()
        args[0].blit(screen2, (0, 0))

    def __str__(self):
        return self.short_name


class BonusCard(pygame.sprite.Sprite):

    def __init__(self, image, id, fraction, name, short_name):
        super().__init__()
        self.image = load_image(image)
        self.id = id
        self.fraction = fraction
        self.name = name
        self.short_name = short_name
        self.rect = self.image.get_rect()

    def ability(self):
        pass

    def get_info(self, *args):
        screen2 = pygame.Surface(args[0].get_size())
        screen2.blit(args[1], (0, 0))

        pygame.draw.rect(screen2, pygame.Color('black'), args[2], 3)
        pygame.draw.line(screen2, pygame.Color('black'), (args[0].get_width() - 60, 25),
                         (args[0].get_width() - 30, 55), 5)
        pygame.draw.line(screen2, pygame.Color('black'), (args[1].get_width() - 30, 25),
                         (args[0].get_width() - 60, 55), 5)

        pygame.draw.rect(screen2, pygame.Color('black'), args[3], 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (45, 32, 45, 16))
        pygame.draw.polygon(screen2, pygame.Color('black'), ((30, 40), (55, 25), (55, 55)))

        pygame.draw.rect(screen2, pygame.Color('black'), (8, 160, 464, 245), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (8, 404, 464, 50), 3)
        pygame.draw.rect(screen2, pygame.Color('black'), (8, 453, 464, 393), 3)

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


        screen2.blit(self.image, img_coord)
        screen2.blit(title, title_coord)
        screen2.blit(ability, (18, 462))
        for i in range(len(ability_info)):
            line = font.render(ability_info[i], 1, pygame.Color('black'))
            y = 500 + 22 * i
            screen2.blit(line, (16, y))

        args[4].empty()
        args[0].blit(screen2, (0, 0))

    def __str__(self):
        return self.short_name


for i in range(len(PLAYCARDS_DATA)):
    data = PLAYCARDS_DATA[i]
    PLAYCARDS.append(PlayCard(p_images[i], data[0], data[1], data[2], data[3], data[4],
                              data[5], data[6], data[7], data[8], data[9], data[10]))
for i in range(len(BONUSCARDS_DATA)):
    data = BONUSCARDS_DATA[i]
    BONUSCARDS.append(BonusCard(b_images[i], data[0], data[1], data[2], data[3]))
for card in PLAYCARDS:
    second_info = sqlite3.connect(database).cursor().execute(f"""SELECT technic_info, passive_ability_info 
                                                                    FROM playcards
                                                                    WHERE short_name = '{card.short_name}'""")
    second_info = [list(i) for i in second_info]
    P_SECOND_INFO.append(second_info)
for card in BONUSCARDS:
    second_info = sqlite3.connect(database).cursor().execute(f"""SELECT ability_info FROM bonuscards
                                                                 WHERE short_name = '{card.short_name}'""")
    second_info = [list(i) for i in second_info]
    B_SECOND_INFO.append(second_info)
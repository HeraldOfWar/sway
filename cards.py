import pygame
import sqlite3
import os

database = os.path.join('data', 'card_db.db')
PLAYCARDS_DATA = sqlite3.connect(database).cursor().execute("""SELECT fraction, name, specialization, 
                                        pace, chakra, resistance, health, technic, synergy FROM playcards""")
BONUSCARDS_DATA = sqlite3.connect(database).cursor().execute("""SELECT fraction, name FROM bonuscards""")
PLAYCARDS_DATA, BONUSCARDS_DATA = [list(i) for i in PLAYCARDS_DATA], [list(i) for i in BONUSCARDS_DATA]
p_images = ['shu.jpg', 'pashke.jpg', 'akemi.jpg', 'raik.jpg', 'kentaru.jpg', 'hiruko.jpg',
            'keiko.jpg', 'akito.jpg', 'ryu.jpg', 'kitsu.jpg', 'benkei.jpg', 'teeru.jpg']
b_images = ['bar.jpg', 'himera.jpg', 'tsunami.jpg', 'king_mouse.jpg', 'ren.jpg',
            'hymn.jpg', 'turtle.jpg', 'kin.jpg', 'true_medic.jpg', 'ambitions.jpg']
PLAYCARDS, BONUSCARDS = [], []


def load_image(name, colorkey=None):
    fullname = os.path.join('resources', 'cards')
    fullname = os.path.join(fullname, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class PlayCard(pygame.sprite.Sprite):

    def __init__(self, image, fraction, name, spec, pace, chakra,
                 resist, health, technic, synergy):
        super().__init__()
        self.image = load_image(image)
        self.fraction = fraction
        self.name = name
        self.spec = spec
        self.pace = pace
        self.chakra = chakra
        self.resist = resist
        self.health = health
        self.technic = technic.split()
        self.synergy = synergy.split()
        self.rect = self.image.get_rect()


    def update(self, *args):
        pass

    def passive_ability(self):
        pass

    def get_info(self):
        pass

    def __str__(self):
        return self.name


class BonusCard(pygame.sprite.Sprite):

    def __init__(self, image, fraction, name):
        super().__init__()
        self.image = load_image(image)
        self.fraction = fraction
        self.name = name
        self.rect = self.image.get_rect()

    def ability(self):
        pass

    def get_info(self):
        pass

    def __str__(self):
        return self.name


for i in range(len(PLAYCARDS_DATA)):
    data = PLAYCARDS_DATA[i]
    PLAYCARDS.append(PlayCard(p_images[i], data[0], data[1], data[2], data[3], data[4],
                              data[5], data[6], data[7], data[8]))
for i in range(len(BONUSCARDS_DATA)):
    data = BONUSCARDS_DATA[i]
    BONUSCARDS.append(BonusCard(b_images[i], data[0], data[1]))

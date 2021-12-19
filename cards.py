import pygame
import sqlite3
import os

database = os.path.join('data', 'card_db.db')
PLAYCARDS_DATA = sqlite3.connect(database).cursor().execute("""SELECT * FROM playcards""")
BONUSCARDS_DATA = sqlite3.connect(database).cursor().execute("""SELECT * FROM bonuscards""")
PLAYCARDS_DATA, BONUSCARDS_DATA = [list(i) for i in PLAYCARDS_DATA], [list(i) for i in BONUSCARDS_DATA]


class PlayCard(pygame.sprite.Sprite):

    def __init__(self, image, fraction, name, spec, pace, chakra,
                 resist, health, technic, technic_info, passive_ability_info, synergy):
        super().__init__()
        self.image = image
        self.fraction = fraction
        self.name = name
        self.spec = spec
        self.pace = pace
        self.chakra = chakra
        self.resist = resist
        self.health = health
        self.technic = technic.split()
        self.technic_info = technic_info
        self.passive_ability_info = passive_ability_info
        self.synergy = synergy.split()


    def update(self, *args):
        pass

    def passive_ability(self):
        pass

    def get_info(self):
        pass


class BonusCard(pygame.sprite.Sprite):

    def __init__(self, image, fraction, name, ability_info):
        super().__init__()

    def ability(self):
        pass

    def get_info(self):
        pass
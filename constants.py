import sys, os, sqlite3
import pygame
from system_func import load_image


FRACTION = None
KONOHAGAKURE = 'KONOHAGAKURE', 0
IVAGAKURE = 'IVAGAKURE', 1
FPS = 60
size = width, height = 480, 854
screen = pygame.display.set_mode(size)

"""Пути к ресурсам"""
DATABASE = os.path.join('data', 'card_db.db')
FONTS = os.path.join('resources', 'fonts')
TITLE_FONT = os.path.join(FONTS, 'rusmadeinchinav2.ttf')
MAIN_FONT = os.path.join(FONTS, 'HanZi.ttf')
CARDS = os.path.join('resources', 'cards')
BACKGROUND = os.path.join('resources', 'back_and_buttons')

"""Фоны и кнопки"""
start_back = load_image(BACKGROUND, 'start_background.jpg')
cf_back = load_image(BACKGROUND, 'cf_background.jpg')
basic_back = load_image(BACKGROUND, 'basic_background.jpg')
pc_img, bc_img = load_image(BACKGROUND, 'playcards.png'), load_image(BACKGROUND, 'bonuscards.png')

"""Группы спрайтов"""
cf_sprites = pygame.sprite.Group()
info_sprites = pygame.sprite.Group()

"""Кнопки-спрайты"""
konohagakure, ivagakure = pygame.sprite.Sprite(cf_sprites), pygame.sprite.Sprite(cf_sprites)
info_1, info_2 = pygame.sprite.Sprite(cf_sprites), pygame.sprite.Sprite(cf_sprites)
playcards, bonuscards = pygame.sprite.Sprite(info_sprites), pygame.sprite.Sprite(info_sprites)

"""Кнопки навигации"""
play_button = pygame.Rect((145, 580, 180, 180))
exit_button = pygame.Rect(width - 70, 15, 50, 50)
escape_button = pygame.Rect(20, 15, 80, 50)

"""Выгрузка данных из БД"""
PLAYCARDS_DATA = sqlite3.connect(DATABASE).cursor().execute("""SELECT id, fraction, name, short_name, 
                        specialization, pace, chakra, resistance, health, technic, synergy FROM playcards""")
BONUSCARDS_DATA = sqlite3.connect(DATABASE).cursor().execute("""SELECT id, fraction, name, 
                                                                short_name FROM bonuscards""")
PLAYCARDS_DATA, BONUSCARDS_DATA = [list(i) for i in PLAYCARDS_DATA], [list(i) for i in BONUSCARDS_DATA]
PLAYCARDS, BONUSCARDS, P_SECOND_INFO, B_SECOND_INFO = [], [], [], []

"""Инициализация шрифтов"""
pygame.font.init()
b_font = pygame.font.Font(TITLE_FONT, 40)
b_font1, b_font2 = pygame.font.Font(TITLE_FONT, 30), pygame.font.Font(TITLE_FONT, 26)
font, font1 = pygame.font.Font(MAIN_FONT, 14), pygame.font.Font(MAIN_FONT, 12)
font2, font3 = pygame.font.Font(MAIN_FONT, 10), pygame.font.Font(MAIN_FONT, 8)

import sys, os, sqlite3
import pygame
from system_func import load_image


"""Основные константы"""
FRACTION = None # выбранная фракция (Конохагакуре или Ивагакуре)
KONOHAGAKURE = 'KONOHAGAKURE', 0
IVAGAKURE = 'IVAGAKURE', 1
FPS = 60 # частота смены кадров в секунду
size = width, height = 480, 854 # размеры окна
screen = pygame.display.set_mode(size) # главное холст, на котором рисуются все окна

"""Пути к ресурсам"""
DATABASE = os.path.join('data', 'card_db.db') # база данных
FONTS = os.path.join('resources', 'fonts') # шрифты
TITLE_FONT = os.path.join(FONTS, 'rusmadeinchinav2.ttf') # заголовок
MAIN_FONT = os.path.join(FONTS, 'HanZi.ttf') # основной текст
CARDS = os.path.join('resources', 'cards') # изображения карт
BACK_N_BUT = os.path.join('resources', 'back_and_buttons') # фоны и кнопки

"""Фоны и кнопки"""
start_back = load_image(BACK_N_BUT, 'start_background.jpg') # стартовый фон
cf_back = load_image(BACK_N_BUT, 'cf_background.jpg') # фон для выбора фракции
basic_back = load_image(BACK_N_BUT, 'basic_background.jpg') # стандартный фон
pc_img, bc_img = load_image(BACK_N_BUT, 'playcards.png'), load_image(BACK_N_BUT, 'bonuscards.png') # кнопки
battlefield = load_image(BACK_N_BUT, 'main_battlefield.jpg') # игровое поле

"""Группы спрайтов"""
cf_sprites = pygame.sprite.Group() # группа спрайтов при выборе фракции
info_sprites = pygame.sprite.Group() # группа спрайтов для выдачи информации о картах

"""Кнопки-спрайты"""
konohagakure, ivagakure = pygame.sprite.Sprite(cf_sprites), pygame.sprite.Sprite(cf_sprites)
info_1, info_2 = pygame.sprite.Sprite(cf_sprites), pygame.sprite.Sprite(cf_sprites)
playcards, bonuscards = pygame.sprite.Sprite(info_sprites), pygame.sprite.Sprite(info_sprites)

"""Кнопки навигации"""
play_button = pygame.Rect((145, 580, 180, 180)) # кнопка "Играть" (->)
exit_button = pygame.Rect(width - 70, 15, 50, 50) # кнопка "Выйти" ([х])
escape_button = pygame.Rect(20, 15, 80, 50) # кнопка "Назад" (<-)
ok_button = pygame.Rect(165, height - 100, 150, 75); # кнопка "ОК"

"""Выгрузка данных из БД"""
PLAYCARDS_DATA = sqlite3.connect(DATABASE).cursor().execute("""SELECT id, fraction, name, short_name, 
                        specialization, pace, chakra, resistance, health, technic, synergy FROM playcards""") # данные об игровых картах
BONUSCARDS_DATA = sqlite3.connect(DATABASE).cursor().execute("""SELECT id, fraction, name, 
                                                                short_name FROM bonuscards""") # данные о бонусных картах
PLAYCARDS_DATA, BONUSCARDS_DATA = [list(i) for i in PLAYCARDS_DATA], [list(i) for i in BONUSCARDS_DATA]
PLAYCARDS, BONUSCARDS, P_SECOND_INFO, B_SECOND_INFO = [], [], [], []

"""Инициализация шрифтов"""
pygame.font.init()
b_font = pygame.font.Font(TITLE_FONT, 70)
b_font1, b_font2 = pygame.font.Font(TITLE_FONT, 30), pygame.font.Font(TITLE_FONT, 26)
font, font1 = pygame.font.Font(MAIN_FONT, 14), pygame.font.Font(MAIN_FONT, 12)
font2, font3 = pygame.font.Font(MAIN_FONT, 10), pygame.font.Font(MAIN_FONT, 8)

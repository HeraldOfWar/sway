import os, sqlite3
import pygame
from system_func import load_image

"""Основные константы"""
FRACTION = None  # выбранная фракция (Конохагакуре или Ивагакуре)
KONOHAGAKURE = 'KONOHAGAKURE'
IVAGAKURE = 'IVAGAKURE'
FPS = 60  # частота смены кадров в секунду
size = width, height = 480, 854  # размеры окна
screen = pygame.display.set_mode(size)  # главный холст, на котором рисуются все окна

"""Пути к ресурсам"""
DATABASE = os.path.join('data', 'card_db.db')  # база данных
FONTS = os.path.join('resources', 'fonts')  # шрифты
TITLE_FONT = os.path.join(FONTS, 'rusmadeinchinav2.ttf')  # заголовок
MAIN_FONT = os.path.join(FONTS, 'HanZi.ttf')  # основной текст
CARDS = os.path.join('resources', 'cards')  # изображения карт
BACK_N_BUT = os.path.join('resources', 'back_and_buttons')  # фоны и кнопки

"""Фоны и кнопки"""
start_back = load_image(BACK_N_BUT, 'start_background.jpg')  # стартовый фон
cf_back = load_image(BACK_N_BUT, 'cf_background.jpg')  # фон для выбора фракции
basic_back = load_image(BACK_N_BUT, 'basic_background.jpg')  # стандартный фон
pc_img, bc_img = load_image(BACK_N_BUT, 'playcards.jpg'), load_image(BACK_N_BUT, 'bonuscards.jpg')  # кнопки
rules_back = load_image(BACK_N_BUT, 'rules_background.jpg')  # фон для активности с правилами
k_battlefield = load_image(BACK_N_BUT, 'main_battlefield.jpg')  # игровое поле
i_battlefield = pygame.transform.rotate(k_battlefield, 180)
konoha_bonus = load_image(BACK_N_BUT, 'konoha_bonus.jpg')
iva_bonus = load_image(BACK_N_BUT, 'iva_bonus.jpg')

"""Группы спрайтов"""
cf_sprites = pygame.sprite.Group()  # группа спрайтов при выборе фракции
info_sprites = pygame.sprite.Group()  # группа спрайтов для выдачи информации о картах
konoha_bonusdeck = pygame.sprite.Group()  # группа бонусных карт-спрайтов Конохагакуре
iva_bonusdeck = pygame.sprite.Group()  # группа бонусных карт-спрайтов Ивагакуре

"""Кнопки-спрайты"""
konohagakure, ivagakure = pygame.sprite.Sprite(cf_sprites), pygame.sprite.Sprite(cf_sprites)
info_1, info_2 = pygame.sprite.Sprite(cf_sprites), pygame.sprite.Sprite(cf_sprites)
playcards, bonuscards = pygame.sprite.Sprite(info_sprites), pygame.sprite.Sprite(info_sprites)

"""Кнопки навигации"""
play_button = pygame.Rect((145, 580, 180, 180))  # кнопка "Играть" (->)
exit_button = pygame.Rect(width - 70, 15, 50, 50)  # кнопка "Выйти" ([х])
escape_button = pygame.Rect(20, 15, 80, 50)  # кнопка "Назад" (<-)
ok_button = pygame.Rect(165, height - 100, 150, 75)  # кнопка "ОК"

"""Игровые кнопки"""
endstep_button1 = pygame.Rect(width - 125, height - 140, 90, 55)  # кнопка "Закончить ход" для первого игрока
endstep_button2 = pygame.Rect(35, 85, 90, 55)  # кнопка "Закончить ход" для второго игрока
bonus_button1 = pygame.Rect(35, height - 140, 91, 135)  # кнопка для покупки карты-бонуса (1 игрок)
bonus_button2 = pygame.Rect(width - 126, 5, 90, 135)  # кнопка для покупки карты-бонуса (2 игрок)
leftslide1 = pygame.Rect(140, height - 103, 35, 60)  # прокрутить колоду влево (1 игрок)
rightslide1 = pygame.Rect(width - 174, height - 103, 35, 60) # прокрутить колоду вправо (1 игрок)
leftslide2 = pygame.Rect(140, 43, 35, 60)  # прокрутить колоду влево (2 игрок)
rightslide2 = pygame.Rect(width - 174, 43, 35, 60)  # прокрутить колоду вправо (2 игрок)

"""Кнопки для боевых точек"""
b_pass1, b_pass2 = pygame.Rect(30, height - 260, 120, 50), pygame.Rect(180, height - 260, 120, 50)
b_pass3, b_pass4 = pygame.Rect(330, height - 260, 120, 50), pygame.Rect(30, 210, 120, 50)
b_pass5, b_pass6 = pygame.Rect(180, 210, 120, 50), pygame.Rect(330, 210, 120, 50)
b_bridge1, b_bridge2 = pygame.Rect(42, height / 2 - 20, 96, 40), pygame.Rect(338, height / 2 - 20, 96, 40)
b_horanpass = pygame.Rect(width / 2 - 72, height / 2 - 30, 144, 60)

game_buttons = [endstep_button1, endstep_button2, bonus_button1, bonus_button2, leftslide1, leftslide2,
                rightslide1, rightslide2, b_pass4, b_pass5, b_pass6, b_bridge1, b_horanpass, b_bridge2,
                b_pass1, b_pass2, b_pass3] # список игровых кнопок
b_battlefields = game_buttons[8:]

"""Выгрузка данных из БД"""
PLAYCARDS_DATA = sqlite3.connect(DATABASE).cursor().execute("""SELECT id, fraction, name, short_name, 
                                                specialization, pace, chakra, resistance, health,
                                                technic, synergy FROM playcards""")  # данные об игровых картах
BONUSCARDS_DATA = sqlite3.connect(DATABASE).cursor().execute("""SELECT id, fraction, name, short_name 
                                                                FROM bonuscards""")  # данные о бонусных картах
PLAYCARDS_DATA, BONUSCARDS_DATA = [list(i) for i in PLAYCARDS_DATA], [list(i) for i in BONUSCARDS_DATA]
PLAYCARDS, BONUSCARDS, P_SECOND_INFO, B_SECOND_INFO = [], [], [], []

"""Инициализация шрифтов"""
pygame.font.init()
b_font, b_font1 = pygame.font.Font(TITLE_FONT, 70), pygame.font.Font(TITLE_FONT, 30)
b_font2, b_font3 = pygame.font.Font(TITLE_FONT, 26), pygame.font.Font(TITLE_FONT, 24)
font, font1 = pygame.font.Font(MAIN_FONT, 14), pygame.font.Font(MAIN_FONT, 12)
font2, font3 = pygame.font.Font(MAIN_FONT, 10), pygame.font.Font(MAIN_FONT, 8)

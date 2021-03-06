import os
import sqlite3
import pygame
import random
from system_func import load_image, load_music, load_sound, add_music
from gui_elements import Button, ImageButton

"""Основные константы"""
VERSION = '1.0.0'  # версия игры
FRACTION = None  # выбранная фракция (Конохагакуре или Ивагакуре)
KONOHAGAKURE = 'KONOHAGAKURE'
IVAGAKURE = 'IVAGAKURE'
FPS = 30  # частота смены кадров в секунду
MAIN_VOLUME = 0.5  # громкость фоновой музыки
CARD_VOLUME = 0.7  # громкость звуковых эффектов
size = width, height = 480, 854  # размеры окна
screen = pygame.display.set_mode(size)  # главный холст, на котором рисуются все окна
clock = pygame.time.Clock()  # объект часов для управления временем

"""Пути к ресурсам"""
DATABASE = os.path.join('data', 'card_db.db')  # база данных
FONTS = os.path.join('resources', 'fonts')  # шрифты
TITLE_FONT = os.path.join(FONTS, 'Gang of Three.ttf')  # заголовок
GAME_FONT = os.path.join(FONTS, 'rusmadeinchinav2.ttf')
MAIN_FONT = os.path.join(FONTS, 'HanZi.ttf')  # основной текст
CARDS = os.path.join('resources', 'cards')  # изображения карт
BACK_N_BUT = os.path.join('resources', 'back_and_buttons')  # фоны и кнопки
THEMES = os.path.join('resources', 'themes')  # темы
MUSIC = os.path.join('resources', 'music')  # музыка
C_VOICES = os.path.join(MUSIC, 'card_voices')  # озвучка карт
GAME_EVENTS = os.path.join(MUSIC, 'game_events')  # звуковые эффекты в игре
BACK_MUSIC = os.path.join(MUSIC, 'soundtracks')  # фоновая музыка

icon = load_image(BACK_N_BUT, 'icon.jpg')  # иконка

"""Фоны и кнопки"""
start_back = load_image(BACK_N_BUT, 'start_background.jpg')  # стартовый фон
cf_back = load_image(BACK_N_BUT, 'cf_background.jpg')  # фон для выбора фракции
basic_back = load_image(BACK_N_BUT, 'basic_background.jpg')  # стандартный фон
pc_img, bc_img = load_image(BACK_N_BUT, 'playcards.jpg'), load_image(BACK_N_BUT, 'bonuscards.jpg')  # кнопки
rules_back = load_image(BACK_N_BUT, 'rules_background.jpg')  # фон для активности с правилами
k_battlefield = load_image(BACK_N_BUT, 'main_battlefield.jpg')  # игровое поле при выборе Конохагакуре
i_battlefield = pygame.transform.rotate(k_battlefield, 180)  # игровое поле при выборе Ивагакуре
konoha_bonus = load_image(BACK_N_BUT, 'konoha_bonus.jpg')  # рубашка карт Конохагакуре
iva_bonus = load_image(BACK_N_BUT, 'iva_bonus.jpg')  # рубашка карт Ивагакуре

"""Изображения для вывода результата игры"""
# победа одной из фракций
konoha_win, iva_win = load_image(BACK_N_BUT, 'konoha_win.png'), load_image(BACK_N_BUT, 'iva_win.png')
draw_back = load_image(BACK_N_BUT, 'draw.jpg')  # ничья

"""Фоны для боевых точек"""
img_konoha_pass1 = load_image(BACK_N_BUT, 'konoha_pass1.jpg')  # перевал 1 (Коноха)
img_konoha_pass2 = load_image(BACK_N_BUT, 'konoha_pass2.jpg')  # перевал 2 (Коноха)
img_konoha_pass3 = load_image(BACK_N_BUT, 'konoha_pass3.jpg')  # перевал 3 (Коноха)
img_iva_pass1 = load_image(BACK_N_BUT, 'iva_pass1.jpg')  # перевал 1 (Ива)
img_iva_pass2 = load_image(BACK_N_BUT, 'iva_pass2.jpg')  # перевал 2 (Ива)
img_iva_pass3 = load_image(BACK_N_BUT, 'iva_pass3.jpg')  # перевал 3 (Ива)
img_bridge1 = load_image(BACK_N_BUT, 'bridge1.jpg')  # мост 1
img_bridge2 = load_image(BACK_N_BUT, 'bridge2.jpg')  # мост 2
img_horanpass = load_image(BACK_N_BUT, 'horanpass.jpg')  # перевал Хорана

"""Группы спрайтов"""
cf_sprites = pygame.sprite.Group()  # группа спрайтов при выборе фракции
info_sprites = pygame.sprite.Group()  # группа спрайтов для выдачи информации о картах
konoha_bonusdeck = pygame.sprite.Group()  # группа бонусных карт-спрайтов Конохагакуре
iva_bonusdeck = pygame.sprite.Group()  # группа бонусных карт-спрайтов Ивагакуре

"""Кнопки-спрайты"""
konohagakure, ivagakure = ImageButton(cf_sprites), ImageButton(cf_sprites)  # выбор фракции
info_1, info_2 = ImageButton(cf_sprites), ImageButton(cf_sprites)  # информация о фракциях
playcards, bonuscards = ImageButton(info_sprites), ImageButton(info_sprites)  # выбор типа карт

"""Кнопки навигации"""
play_button = Button((145, 630, 180, 100))  # кнопка "Играть" (->)
exit_button = Button(width - 65, 15, 50, 50)  # кнопка "Выйти" ([х])
escape_button = Button(15, 15, 80, 50)  # кнопка "Назад" (<-)
ok_button = Button(165, height - 100, 150, 75)  # кнопка "ОК"
rules_button = Button(width // 2 - 150, height // 2 - 20, 300, 100)  # кнопка "Правила"
help_button = Button(width // 2 - 150, height // 2 + 100, 300, 100)  # кнопка "Помощь"
terminate_button = Button(width // 2 - 150, height // 2 + 220, 300, 100)  # кнопка "Выйти"
menu_buttons = [escape_button, help_button, rules_button, terminate_button]  # список кнопок для главного меню

"""Игровые кнопки"""
endstep_button1 = Button(width - 125, height - 140, 90, 55)  # кнопка "Закончить ход" для первого игрока
endstep_button2 = Button(35, 85, 90, 55)  # кнопка "Закончить ход" для второго игрока
bonus_button1 = Button(35, height - 140, 91, 135)  # кнопка для покупки карты-бонуса (1 игрок)
bonus_button2 = Button(width - 126, 5, 90, 135)  # кнопка для покупки карты-бонуса (2 игрок)
leftslide1 = Button(135, height - 103, 45, 60)  # прокрутить колоду влево (1 игрок)
rightslide1 = Button(width - 179, height - 103, 45, 60)  # прокрутить колоду вправо (1 игрок)
leftslide2 = Button(135, 43, 45, 60)  # прокрутить колоду влево (2 игрок)
rightslide2 = Button(width - 179, 43, 45, 60)  # прокрутить колоду вправо (2 игрок)
battle_ok = Button(width // 2 - 50, height // 2 + 35, 100, 50)  # кнопка "ОК" для поединка

"""Кнопки для боевых точек"""
b_pass1, b_pass2 = Button(30, height - 260, 120, 50), Button(180, height - 260, 120, 50)  # перевалы (1 и 2)
b_pass3, b_pass4 = Button(330, height - 260, 120, 50), Button(30, 210, 120, 50)  # перевалы (3 и 4)
b_pass5, b_pass6 = Button(180, 210, 120, 50), Button(330, 210, 120, 50)  # перевалы (5 и 6)
b_bridge1, b_bridge2 = Button(42, height / 2 - 20, 96, 40), Button(338, height / 2 - 20, 96, 40)  # мосты
b_horanpass = Button(width / 2 - 72, height / 2 - 30, 144, 60)  # перевал Хорана

play_board = [[b_pass4, b_pass5, b_pass6],
              [b_bridge1, b_horanpass, b_bridge2],
              [b_pass1, b_pass2, b_pass3]]  # игровое поле
game_buttons = [endstep_button1, endstep_button2, bonus_button1, bonus_button2, leftslide1, leftslide2,
                rightslide1, rightslide2, b_pass1, b_pass2, b_pass3, b_bridge1, b_horanpass, b_bridge2,
                b_pass4, b_pass5, b_pass6]  # список игровых кнопок
b_battlepoints = game_buttons[8:]  # cписок кнопок боевых точек

"""Позиции на боевых точках"""
point1, point2, point3 = Button(58, 562, 120, 175), Button(180, 562, 120, 175), Button(302, 562, 120, 175)
point4, point5, point6 = Button(58, 150, 120, 175), Button(180, 150, 120, 175), Button(302, 150, 120, 175)
b_points = [exit_button, point1, point2, point3, point4, point5, point6]  # список позиций на боевой точке

"""Выгрузка данных из БД"""
connect = sqlite3.connect(DATABASE)  # открытие БД
cursor = connect.cursor()
PLAYCARDS_DATA = cursor.execute("""SELECT id, fraction, name, short_name, specialization, pace, chakra, 
                        resistance, health, technic, synergy FROM playcards""")  # данные об игровых картах
PLAYCARDS_DATA = [list(i) for i in PLAYCARDS_DATA]
BONUSCARDS_DATA = cursor.execute("""SELECT id, fraction, name, short_name 
                                    FROM bonuscards""")  # данные о бонусных картах
BONUSCARDS_DATA = [list(i) for i in BONUSCARDS_DATA]
connect.close()  # закрытие БД
PLAYCARDS, BONUSCARDS, OTHER_PCARDS, OTHER_BCARDS, P_SECOND_INFO, B_SECOND_INFO = [], [], [], [], [], []

"""Инициализация шрифтов"""
pygame.font.init()  # инициализация шрифтов
b_font, b_font1 = pygame.font.Font(TITLE_FONT, 60), pygame.font.Font(TITLE_FONT, 50)
b_font2, b_font3 = pygame.font.Font(TITLE_FONT, 30), pygame.font.Font(TITLE_FONT, 22)
g_font, g_font1 = pygame.font.Font(GAME_FONT, 60), pygame.font.Font(GAME_FONT, 30)
g_font2, g_font3 = pygame.font.Font(GAME_FONT, 26), pygame.font.Font(GAME_FONT, 24)
font, font1 = pygame.font.Font(MAIN_FONT, 14), pygame.font.Font(MAIN_FONT, 12)
font2, font3 = pygame.font.Font(MAIN_FONT, 10), pygame.font.Font(MAIN_FONT, 8)

"""Инициализация тем"""
sway_theme = os.path.join(THEMES, 'sway_theme.json')  # стандартная тема

"""Инициализация текстов"""
rules_txt = ''  # правила
with open(os.path.join('data', 'rules.txt'), encoding='utf8') as rules:
    rules_txt = rules.read().split('\n')
rules_txt = ' '.join(rules_txt)
help_txt = ''  # справка
with open(os.path.join('data', 'help.txt'), encoding='utf8') as helps:
    help_txt = helps.read().split('\n')
help_txt = ' '.join(help_txt)

"""Инициализация аудио"""
pygame.mixer.init()  # инициализация микшера
basic_music = ['basic.mp3', 'basic1.mp3', 'basic2.mp3', 'basic3.mp3']  # фоновая музыка в меню
game_music = ['game.mp3', 'game1.mp3', 'game2.mp3']  # фоновая музыка в игре
battle_music = ['battle.mp3', 'battle1.mp3']  # фоновая музыка на боевых точках
"""Аудио-события"""
# выбор Конохагакуре
choose_konoha_sounds = [load_sound(GAME_EVENTS, 'konoha.wav'), load_sound(GAME_EVENTS, 'konoha1.wav')]
# выбор Ивагакуре
choose_iva_sounds = [load_sound(GAME_EVENTS, 'iva.wav'), load_sound(GAME_EVENTS, 'iva1.wav')]
konoha_lead = load_sound(GAME_EVENTS, 'konoha_lead.wav')  # Конохагакуре лидирует
iva_lead = load_sound(GAME_EVENTS, 'iva_lead.wav')  # Ивагакуре лидирует
konoha_win_sound = load_sound(GAME_EVENTS, 'konoha_win.wav')  # победа Конохагакуре
iva_win_sound = load_sound(GAME_EVENTS, 'iva_win.wav')  # победа Ивагакуре
draw_sound = load_sound(GAME_EVENTS, 'draw.wav')  # ничья

# пользовательское событие, которое срабатывает, когда заканчивается музыка
MUSIC_END = pygame.USEREVENT + 1

import pygame
import cards
from activities import BasicActivity, GameActivity, Fragment
from board import BattlePoint, Deck
from constants import *


def game_init():
    """Предварительная инициализация игры"""

    """Создание колод игровых карт для каждой деревни"""
    konoha_deck = Deck(KONOHAGAKURE)  # группа игровых карт-спрайтов Конохагакуре
    iva_deck = Deck(IVAGAKURE)  # группа игровых карт-спрайтов Ивагакуре

    """Создание боевых точек"""
    pass1, pass2, pass3 = BattlePoint(b_pass1, 1), BattlePoint(b_pass2, 1), \
                          BattlePoint(b_pass3, 1)  # союзные перевалы
    pass4, pass5, pass6 = BattlePoint(b_pass4, 1), BattlePoint(b_pass5, 1), \
                          BattlePoint(b_pass6, 1)  # вражеские перевалы
    bridge1, bridge2 = BattlePoint(b_bridge1, 2), BattlePoint(b_bridge2, 2)  # мосты
    horanpass = BattlePoint(b_horanpass, 3)  # перевал Хорана
    battlefields = [pass1, pass2, pass3, bridge1, horanpass, bridge2, pass4, pass5, pass6]  # список точек

    """Инициализация боевых точек"""
    for i in range(len(battlefields)):
        if i < 3:
            battlefields[i].title = f'Перевал {i + 1}'  # название
            battlefields[i].type = 'Перевал'  # тип
            for j in range(3):  # союзные позиции
                battlefields[i].points.append(pygame.Rect(30 + 40 * j + 150 * (i % 3), 644, 40, 35))
            for j in range(3):  # вражеские позиции
                battlefields[i].points.append(pygame.Rect(30 + 40 * j + 150 * (i % 3), 559, 40, 35))
            battlefields[i].update_points()
        elif i > 5:
            battlefields[i].title = f'Перевал {i - 2}'
            battlefields[i].type = 'Перевал'
            for j in range(3):
                battlefields[i].points.append(pygame.Rect(30 + 40 * j + 150 * (i % 3), 260, 40, 35))
            for j in range(3):
                battlefields[i].points.append(pygame.Rect(30 + 40 * j + 150 * (i % 3), 175, 40, 35))
            battlefields[i].update_points()
        elif i == 4:
            battlefields[i].title = 'Первал Хорана'
            battlefields[i].type = 'Перевал Хорана'
            for j in range(3):
                battlefields[i].points.append(pygame.Rect(168 + 48 * j, 457, 48, 35))
            for j in range(3):
                battlefields[i].points.append(pygame.Rect(168 + 48 * j, 362, 48, 35))
            battlefields[i].update_points()
        else:
            battlefields[i].title = f'Мост {i % 3 // 2 + 1}'
            battlefields[i].type = 'Мост'
            for j in range(3):
                battlefields[i].points.append(pygame.Rect(42 + 32 * j + 148 * (i % 3), 447, 32, 35))
            for j in range(3):
                battlefields[i].points.append(pygame.Rect(42 + 32 * j + 148 * (i % 3), 372, 32, 35))
            battlefields[i].update_points()

    """Создание всех карт"""
    """Игровые карты Конохагакуре"""
    shu = cards.Shu(f'{PLAYCARDS_DATA[0][3]}.jpg', PLAYCARDS_DATA[0], konoha_deck)
    pashke = cards.Pashke(f'{PLAYCARDS_DATA[1][3]}.jpg', PLAYCARDS_DATA[1], konoha_deck)
    akemi = cards.Akemi(f'{PLAYCARDS_DATA[2][3]}.jpg', PLAYCARDS_DATA[2], konoha_deck)
    raik = cards.Raik(f'{PLAYCARDS_DATA[3][3]}.jpg', PLAYCARDS_DATA[3], konoha_deck)
    kentaru = cards.Kentaru(f'{PLAYCARDS_DATA[4][3]}.jpg', PLAYCARDS_DATA[4], konoha_deck)
    hiruko = cards.Hiruko(f'{PLAYCARDS_DATA[5][3]}.jpg', PLAYCARDS_DATA[5], konoha_deck)

    """Игровые карты Ивагакуре"""
    keiko = cards.Keiko(f'{PLAYCARDS_DATA[6][3]}.jpg', PLAYCARDS_DATA[6], iva_deck)
    akito = cards.Akito(f'{PLAYCARDS_DATA[7][3]}.jpg', PLAYCARDS_DATA[7], iva_deck)
    ryu = cards.Ryu(f'{PLAYCARDS_DATA[8][3]}.jpg', PLAYCARDS_DATA[8], iva_deck)
    kitsu = cards.Kitsu(f'{PLAYCARDS_DATA[9][3]}.jpg', PLAYCARDS_DATA[9], iva_deck)
    benkei = cards.Benkei(f'{PLAYCARDS_DATA[10][3]}.jpg', PLAYCARDS_DATA[10], iva_deck)
    teeru = cards.Teeru(f'{PLAYCARDS_DATA[11][3]}.jpg', PLAYCARDS_DATA[11], iva_deck)

    """Бонусные карты Конохагакуре"""
    bar = cards.BarKonoha(f'{BONUSCARDS_DATA[0][3]}.jpg', BONUSCARDS_DATA[0], konoha_bonusdeck)
    himera = cards.Himera(f'{BONUSCARDS_DATA[1][3]}.jpg', BONUSCARDS_DATA[1], konoha_bonusdeck)
    tsunami = cards.Tsunami(f'{BONUSCARDS_DATA[2][3]}.jpg', BONUSCARDS_DATA[2], konoha_bonusdeck)
    king_of_mouse = cards.KingOfMouse(f'{BONUSCARDS_DATA[3][3]}.jpg', BONUSCARDS_DATA[3], konoha_bonusdeck)
    ren = cards.Ren(f'{BONUSCARDS_DATA[4][3]}.jpg', BONUSCARDS_DATA[4], konoha_bonusdeck)

    """Бонусные карты Ивагакуре"""
    hymn = cards.HymnIva(f'{BONUSCARDS_DATA[5][3]}.jpg', BONUSCARDS_DATA[5], iva_bonusdeck)
    turtle = cards.Turtle(f'{BONUSCARDS_DATA[6][3]}.jpg', BONUSCARDS_DATA[6], iva_bonusdeck)
    kin = cards.Kin(f'{BONUSCARDS_DATA[7][3]}.jpg', BONUSCARDS_DATA[7], iva_bonusdeck)
    true_medic = cards.TrueMedic(f'{BONUSCARDS_DATA[8][3]}.jpg', BONUSCARDS_DATA[8], iva_bonusdeck)
    ambitions = cards.Ambitions(f'{BONUSCARDS_DATA[9][3]}.jpg', BONUSCARDS_DATA[9], iva_bonusdeck)

    """Создание всех окон (активностей и фрагментов)"""
    cf_activity = BasicActivity(cf_back, sprites=cf_sprites, old_activity=start_activity)
    info_activity = BasicActivity(basic_back, buttons=[exit_button], sprites=info_sprites,
                                  old_activity=cf_activity)
    card_info_activity = BasicActivity(basic_back, buttons=[escape_button, exit_button],
                                       old_activity=cf_activity)
    rules = Fragment('rules', rules_back, buttons=[ok_button])
    card_info_fragment = Fragment('card_info', basic_back, buttons=[exit_button])
    game_activity = GameActivity(k_battlefield, buttons=game_buttons,
                                 decks=[konoha_deck, iva_deck],
                                 battlepoints=battlefields,
                                 fragments=[rules, card_info_fragment])  # главная игровая активность
    """Настройка навигации"""
    start_activity.next_activity = cf_activity
    cf_activity.next_activity = info_activity
    cf_activity.start_game_activity = game_activity
    info_activity.next_activity = card_info_activity
    card_info_activity.previous_activity = info_activity

    """Инициализация спрайтов в окне выбора фракции"""
    konohagakure.image, ivagakure.image = load_image(BACK_N_BUT, 'konoha_background.jpg'), \
                                          load_image(BACK_N_BUT, 'iva_background.jpg')
    info_1.image, info_2.image = load_image(BACK_N_BUT, 'info_1.png'), load_image(BACK_N_BUT, 'info_2.png')
    konohagakure.rect, ivagakure.rect = konohagakure.image.get_rect(), ivagakure.image.get_rect()
    info_1.rect, info_2.rect = info_1.image.get_rect(), info_2.image.get_rect()
    konohagakure.rect.x, konohagakure.rect.y = width - 390, 0
    ivagakure.rect.x, ivagakure.rect.y = 0, height - 285
    info_1.rect.x, info_1.rect.y = 0, 0
    info_2.rect.x, info_2.rect.y = width - 80, height - 285

    """Инициализация кнопок для выдачи списка игровых и бонусных карт"""
    playcards.image, bonuscards.image = pygame.transform.scale(pc_img, (183, 95)), \
                                        pygame.transform.scale(bc_img, (183, 95))
    playcards.rect, bonuscards.rect = playcards.image.get_rect(), bonuscards.image.get_rect()
    playcards.rect.x, playcards.rect.y = 49, height - 110
    bonuscards.rect.x, bonuscards.rect.y = 248, height - 110

    """Очистка списков карт"""
    PLAYCARDS.clear()
    BONUSCARDS.clear()

    """Заполнение списка игровых карт"""
    for card in konoha_deck:
        PLAYCARDS.append(card)
    for card in iva_deck:
        PLAYCARDS.append(card)

    """Заполнение списка бонусных карт"""
    for card in konoha_bonusdeck:
        BONUSCARDS.append(card)
    for card in iva_bonusdeck:
        BONUSCARDS.append(card)

    """Заполнение списка описаний техник и способностей игровых карт"""
    for card in PLAYCARDS:
        second_info = sqlite3.connect(DATABASE).cursor().execute(f"""SELECT technic_info, passive_ability_info 
                                                                    FROM playcards
                                                                    WHERE id = '{card.id}'""")
        second_info = [list(i) for i in second_info]
        P_SECOND_INFO.append(second_info)
    """Заполнение списка эффектов бонусных карт"""
    for card in BONUSCARDS:
        second_info = sqlite3.connect(DATABASE).cursor().execute(f"""SELECT ability_info FROM bonuscards
                                                                     WHERE id = '{card.id}'""")
        second_info = [list(i) for i in second_info]
        B_SECOND_INFO.append(second_info)


def main():
    """Начинаем!"""
    game_init()  # инициализация всех объектов
    start_activity.run()  # отрисовка стартового окна
    return main()  # надо сыграть ещё раз...


if __name__ == '__main__':
    pygame.init()  # инициализация pygame
    pygame.display.set_caption('SWAY')  # установка названия

    start_activity = BasicActivity(start_back, buttons=[play_button])  # стартовое окно

    main()  # запуск игры

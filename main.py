import pygame
from activities import sprites_init, BasicActivity, GameActivity
from constants import *


def main():
    """Начинаем!"""
    start_activity.run() # отрисовка стартового окна
    return main() # надо сыграть ещё раз...


if __name__ == '__main__':
    pygame.init() # инициализация pygame
    pygame.display.set_caption('SWAY') # установка названия
    sprites_init() # инициализация спрайтов

    """Создание всех окон (активностей)"""
    start_activity = BasicActivity(start_back, buttons=[play_button])
    cf_activity = BasicActivity(cf_back, sprites=cf_sprites, old_activity=start_activity)
    info_activity = BasicActivity(basic_back, buttons=[exit_button], sprites=info_sprites,
                                  old_activity=cf_activity)
    card_info_activity = BasicActivity(basic_back, buttons=[escape_button, exit_button],
                                       old_activity=cf_activity)
    rules_activity = BasicActivity(basic_back, buttons=[ok_button])
    game_activity = GameActivity(battlefield)
    """Настройка навигации"""
    start_activity.next_activity = cf_activity
    cf_activity.next_activity = info_activity
    cf_activity.start_game_activity = rules_activity
    info_activity.next_activity = card_info_activity
    card_info_activity.previous_activity = info_activity
    rules_activity.next_activity = game_activity

    main() # запуск игры
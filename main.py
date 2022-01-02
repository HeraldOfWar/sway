import pygame
from view import sprites_init, BasicActivity
from constants import *


def main():
    start_activity.run()
    return main()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('SWAY')
    sprites_init()

    start_activity = BasicActivity(start_back, buttons=[play_button])
    cf_activity = BasicActivity(cf_back, sprites=cf_sprites, old_activity=start_activity)
    info_activity = BasicActivity(basic_back, buttons=[exit_button], sprites=info_sprites,
                                  old_activity=cf_activity)
    card_info_activity = BasicActivity(basic_back, buttons=[escape_button, exit_button],
                                       old_activity=cf_activity)
    start_activity.next_activity = cf_activity
    cf_activity.next_activity = info_activity
    info_activity.next_activity = card_info_activity
    card_info_activity.previous_activity = info_activity

    main()
(os.path.join(font_path, 'rusmadeinchinav2.ttf'), 'resources/fonts'),
                    (os.path.join(font_path, 'HanZi.ttf'), 'resources/fonts'),
                    (os.path.join(path_theme, 'sway_theme.json'), 'resources/themes'),
                    (pygame_data_loc, os.path.join('pygame_gui', 'data'))


import os, pygame_gui
pygame_data_loc = os.path.join(os.path.dirname(pygame_gui.__file__), 'data')
path_theme = os.path.join('resources', 'themes')
font_path = os.path.join('resources', 'fonts')
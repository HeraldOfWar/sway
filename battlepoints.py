import pygame
from constants import *
from activities import Fragment


class BattlePoint(pygame.sprite.Group):
    """Класс боевой точки, наследуемый от sprite.Group"""

    def __init__(self, view, number, points):
        """Инициализация боевой точки"""
        super().__init__()
        self.view = view
        self.number = number  # номер точки
        self.points = points  # количество ОЗ, которое генерируется точкой

    def output(self):
        """Отрисовка боевой точки"""
        if self.number < 3 or self.number > 5:
            pygame.draw.rect(screen, pygame.Color('white'), (30 + 150 * (self.number % 3),
                                                             175 + 192 * (self.number // 3), 40, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (70 + 150 * (self.number % 3),
                                                             175 + 192 * (self.number // 3), 40, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (110 + 150 * (self.number % 3),
                                                             175 + 192 * (self.number // 3), 40, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (30 + 150 * (self.number % 3),
                                                             260 + 192 * (self.number // 3), 40, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (70 + 150 * (self.number % 3),
                                                             260 + 192 * (self.number // 3), 40, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (110 + 150 * (self.number % 3),
                                                             260 + 192 * (self.number // 3), 40, 35), 3)
            if self.number < 3:
                name = b_font4.render(f'Перевал {self.number + 4}', 1, pygame.Color('white'))
            else:
                name = b_font4.render(f'Перевал {self.number - 5}', 1, pygame.Color('white'))
            name_coord = name.get_rect()
            name_coord.center = b_battlefields[self.number].center
            screen.blit(name, name_coord)  # вывод названия точки
        elif self.number == 4:
            pygame.draw.rect(screen, pygame.Color('white'), (168, 362, 48, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (216, 362, 48, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (264, 362, 48, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (168, 457, 48, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (216, 457, 48, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (264, 457, 48, 35), 3)
            for i in range(2):
                name = b_font2.render(f'Перевал Хорана'.split()[i], 1, pygame.Color('white'))
                name_coord = name.get_rect()
                name_coord.center = b_battlefields[self.number].center
                name_coord.y = height // 2 - 25
                name_coord.y += 22 * i
                screen.blit(name, name_coord)
        else:
            pygame.draw.rect(screen, pygame.Color('white'), (42 + 148 * (self.number % 3), 372, 32, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (74 + 148 * (self.number % 3), 372, 32, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (106 + 148 * (self.number % 3), 372, 32, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (42 + 148 * (self.number % 3), 447, 32, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (74 + 148 * (self.number % 3), 447, 32, 35), 3)
            pygame.draw.rect(screen, pygame.Color('white'), (106 + 148 * (self.number % 3), 447, 32, 35), 3)
            name = b_font4.render(f'Мост {self.number % 3 // 2 + 1}', 1, pygame.Color('white'))
            name_coord = name.get_rect()
            name_coord.center = b_battlefields[self.number].center
            screen.blit(name, name_coord)

    def get_info(self):
        """Выдача информации о боевой точке"""

        """Создание и запуск фрагмента"""
        battlepoint_info = Fragment('battlepoint', battlepoint_back, buttons=b_battlepoint, sprites=[self])
        battlepoint_info.run()
import pygame


class Button(pygame.Rect):
    """Класс стандартной кнопки, наследуемый от pygame.Rect (прямоугольник)"""

    def __init__(self, *args):
        """Инициализация кнопки"""
        super().__init__(args)
        self.is_hovered = False  # проверка кнопки на пересечение с мышкой

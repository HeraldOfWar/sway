import sys, os
import pygame


def load_image(directory, name, colorkey=None):
    """Загрузка изображений"""
    fullname = os.path.join(directory, name)  # путь к изображению
    if not os.path.isfile(fullname):  # если указанный путь неверный, осуществляется выход из игры
        print(f"Файл с изображением '{fullname}' не найден")  # и выводится соответсвующий текст в консоль
        sys.exit()
    image = pygame.image.load(fullname)  # если всё правильно, то загружается изображение
    return image


def terminate():
    pygame.quit()
    sys.exit()

import sys, os
import pygame


"""Загрузка изображений"""
def load_image(directory, name, colorkey=None):
    fullname = os.path.join(directory, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


"""Выход из игры"""
def terminate():
    pygame.quit()
    sys.exit()

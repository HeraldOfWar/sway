import sys
import os
import pygame


def load_image(directory, name, colorkey=None):
    """Загрузка изображений"""
    fullname = os.path.join(directory, name)  # путь к изображению
    if not os.path.isfile(fullname):  # если указанный путь неверный, осуществляется выход из игры
        print(f"Файл с изображением '{fullname}' не найден")  # и выводится соответсвующий текст в консоль
        sys.exit()
    image = pygame.image.load(fullname)  # если всё правильно, то загружается изображение
    return image


def load_music(directory, name):
    """Загрузка аудиофайлов"""
    fullname = os.path.join(directory, name)  # путь к аудиофайлу
    if not os.path.isfile(fullname):  # если указанный путь неверный, осуществляется выход из игры
        print(f"Файл с аудиофайлом '{fullname}' не найден")  # и выводится соответсвующий текст в консоль
        sys.exit()
    pygame.mixer.music.load(fullname)  # если всё правильно, то загружается аудиофайл


def add_music(directory, name):
    """Добавление аудиофайлов"""
    fullname = os.path.join(directory, name)  # путь к аудиофайлу
    if not os.path.isfile(fullname):  # если указанный путь неверный, осуществляется выход из игры
        print(f"Файл с аудиофайлом '{fullname}' не найден")  # и выводится соответсвующий текст в консоль
        sys.exit()
    pygame.mixer.music.queue(fullname)  # если всё правильно, то загружается аудиофайл


def load_sound(directory, name):
    """Загрузка звукового эффекта или озвучки"""
    fullname = os.path.join(directory, name)  # путь к аудиофайлу
    if not os.path.isfile(fullname):  # если указанный путь неверный, осуществляется выход из игры
        print(f"Файл с аудиофайлом '{fullname}' не найден")  # и выводится соответсвующий текст в консоль
        sys.exit()
    audio = pygame.mixer.Sound(fullname)  # если всё правильно, то загружается аудиофайл
    return audio


def terminate():
    """Выход из игры"""
    pygame.quit()
    sys.exit()

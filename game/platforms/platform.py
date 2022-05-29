from pygame import *
from os import path

# папка с платформой
DIR = path.dirname(__file__)

# класс платформы
class Platform(sprite.Sprite):
    # константы для платформы
    PLATFORM_SIZE = 32
    PLATFORM_COLOR = "#FF6262"

    def __init__(self, x, y, breakable=False):
        sprite.Sprite.__init__(self)
        # изображение для платформы
        self.image = Surface((self.PLATFORM_SIZE, self.PLATFORM_SIZE))
        self.image.fill(Color(self.PLATFORM_COLOR))
        self.breakable = breakable # задание разрушаемости
        if breakable: # если разрушаема
            # загрузка изображения
            self.image = image.load(
                f"{DIR}/platform_breakable.png")
        else: # иначе
            # загрузка другого изображения
            self.image = image.load(f"{DIR}/platform.png")
        # прямоугольник, представляющий платформу
        self.rect = Rect(x, y, self.PLATFORM_SIZE, self.PLATFORM_SIZE)
        # загрузка звука
        self.sound = mixer.Sound(f"{DIR}/sound.wav")
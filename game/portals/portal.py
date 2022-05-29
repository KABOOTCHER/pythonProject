from pygame import *
from pyganim import *
from players.player import Player
from os import path

DIR = path.dirname(__file__)

ANIMATION_DELAY = 150
ANIMATION_IDLE = [
    (f"{DIR}\\imgs\\tile000.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile001.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile002.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile003.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile004.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile005.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile006.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile007.png", ANIMATION_DELAY),
]

class Portal(sprite.Sprite):
    PORTAL_SIZE = 32
    PORTAL_COLOR = "#33FF33"

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        # изображение для портала
        self.image = Surface((self.PORTAL_SIZE, self.PORTAL_SIZE))
        self.image.fill(self.PORTAL_COLOR)
        self.image.set_colorkey(self.PORTAL_COLOR)
        # прямоугольник, представляющий портал
        self.rect = Rect(x, y, self.PORTAL_SIZE, self.PORTAL_SIZE)
        # включение анимации
        self.boltAnimIdle = PygAnimation(ANIMATION_IDLE)
        self.boltAnimIdle.play()
        self.boltAnimIdle.blit(self.image, (0, 0))
        # загрузка звука
        self.sound = mixer.Sound(f"{DIR}\\sound.wav")

    # функция обновления
    def update(self, hero):
        # обновить анимацию
        self.image.fill(self.PORTAL_COLOR)
        self.boltAnimIdle.blit(self.image, (0, 0))
        # проверить на столкновение
        self.collide(hero)

    # функция проверки столкновения с игроком
    def collide(self, hero: Player):
        # если столкновение с игроком
        if sprite.collide_rect(self, hero):
            # включить звук
            self.sound.play()
            # включить флаг финиша
            hero.finish = True
from pygame import *
from pyganim import *
from players.player import Player
from os import path

# папка с монеткой
DIR = path.dirname(__file__)

# создание анимаций монетки
ANIMATION_DELAY = 150
ANIMATION_IDLE = [
    (f"{DIR}\\imgs\\tile000.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile001.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile002.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile003.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile004.png", ANIMATION_DELAY),
]

# класс монетки
class Coin(sprite.Sprite):
    # константы для монетки
    COIN_SIZE = 16
    COIN_COLOR = "#FFCC00"
    COIN_VALUE = 10

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        # изображение для монетки
        self.image = Surface((self.COIN_SIZE, self.COIN_SIZE))
        self.image.fill(self.COIN_COLOR)
        self.image.set_colorkey(self.COIN_COLOR)
        # прямоугольник, представляющий монетку
        self.rect = Rect(x + self.COIN_SIZE / 2,
                         y + self.COIN_SIZE / 2,
                         self.COIN_SIZE,
                         self.COIN_SIZE)
        # включение анимации
        self.boltAnimIdle = PygAnimation(ANIMATION_IDLE)
        self.boltAnimIdle.play()
        self.boltAnimIdle.blit(self.image, (0, 0))
        # загрузка звука
        self.sound = mixer.Sound(f"{DIR}\\sound.wav")

    # функция обновления
    def update(self, hero):
        # обновить анимацию
        self.image.fill(self.COIN_COLOR)
        self.boltAnimIdle.blit(self.image, (0, 0))
        # проверить на столкновение
        self.collide(hero)

    # функция проверки столкновения с игроком
    def collide(self, hero: Player):
        # если столкновение с игроком
        if sprite.collide_rect(self, hero):
            # если монетка существует
            if self.alive():
                # добавить очки
                hero.score += self.COIN_VALUE
                # включить звук
                self.sound.play()
                # убрать монетку
                self.kill()

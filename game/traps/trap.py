from pygame import *
from pyganim import *
from players.player import Player
from os import path

# папка с ловушкой
DIR = path.dirname(__file__)

# создание анимаций ловушки
ANIMATION_DELAY = 150
ANIMATION_IDLE = [
    (f"{DIR}\\imgs\\tile000.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile001.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile002.png", ANIMATION_DELAY),
    (f"{DIR}\\imgs\\tile003.png", ANIMATION_DELAY),
]

# класс ловушки
class Trap(sprite.Sprite):
    # константы для ловушки
    TRAP_SIZE = 32
    TRAP_COLOR = "#FFCC00"

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        # изображение для ловушки
        self.image = Surface((self.TRAP_SIZE, self.TRAP_SIZE))
        self.image.fill(self.TRAP_COLOR)
        self.image.set_colorkey(self.TRAP_COLOR)
        # прямоугольник, представляющий ловушку
        self.rect = Rect(x, y,
                         self.TRAP_SIZE - 5,
                         self.TRAP_SIZE - 5)
        # включение анимации
        self.trapAnimIdle = PygAnimation(ANIMATION_IDLE)
        self.trapAnimIdle.play()
        self.trapAnimIdle.blit(self.image, (0, 0))
        # загрузка звука
        self.sound = mixer.Sound(f"{DIR}\\sound.wav")

    # функция обновления
    def update(self, hero):
        # обновить анимацию
        self.image.fill(self.TRAP_COLOR)
        self.trapAnimIdle.blit(self.image, (0, 0))
        # проверить на столкновение
        self.collide(hero)

    # функция проверки столкновения с игроком
    def collide(self, hero: Player):
        # если столкновение с игроком
        if sprite.collide_rect(self, hero):
            # убить игрока
            hero.kill()
            # включить звук
            self.sound.play()

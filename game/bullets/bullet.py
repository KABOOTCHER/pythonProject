from pygame import *
from os import path

# папка с пулей
DIR = path.dirname(__file__)

# класс пули
class Bullet(sprite.Sprite):
    # константы для пули
    BULLET_COLOR = "#322300"

    def __init__(self, x, y, direction):
        sprite.Sprite.__init__(self)
        # изображение для пули
        self.image = Surface((5, 3))
        self.image.fill(self.BULLET_COLOR)
        # прямоугольник, представляющий пулю
        self.rect = Rect(x, y + 26, 5, 3)
        self.speed = 6 * direction # скорость пули
        # загрузка звука
        self.sound = mixer.Sound(f"{DIR}/sound.wav")

    # функция обновления
    def update(self, platforms):
        if self.alive(): # если существует
            # обновление положения
            self.rect.x += self.speed
            # если вышла за пределы экрана
            if self.rect.left > 0 and self.rect.right < 0:
                self.kill() # удалить
            # проверка на столкновение
            self.collide(platforms)

    # функция проверки столкновения с платформой
    def collide(self, platforms):
        # цикл по всем платформам
        for p in platforms: 
            # если столкновение с игроком
            if sprite.collide_rect(self, p) and p.alive():
                # удалить пулю
                self.kill()
                # если платформа разрушаема
                if p.breakable:
                    # удалить платформу
                    p.kill()
                    # включить звук платформы
                    p.sound.play()

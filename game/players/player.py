from pygame import *
from pyganim import *
from bullets.bullet import Bullet
from typing import List
from os import path

# задание констант
MOVE_SPEED = 3
WIDTH = 32
HEIGHT = 48
COLOR = (255, 255, 0)
JUMP_POWER = 5
GRAVITY = 0.25
ANIMATION_DELAY = 150
PLAYER_DIR = path.dirname(__file__)
COIN_POINTS = 10

# создание анимаций игрока
ANIMATION_IDLE = [
    (f"{PLAYER_DIR}\\imgs\\idle\\tile000.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\idle\\tile001.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\idle\\tile002.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\idle\\tile003.png", ANIMATION_DELAY),
]
ANIMATION_WALK = [
    (f"{PLAYER_DIR}\\imgs\\walk\\tile000.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\walk\\tile001.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\walk\\tile002.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\walk\\tile003.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\walk\\tile004.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\walk\\tile005.png", ANIMATION_DELAY),
]
ANIMATION_JUMP = [
    (f"{PLAYER_DIR}\\imgs\\jump\\tile000.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\jump\\tile001.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\jump\\tile002.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\jump\\tile003.png", ANIMATION_DELAY),
]
ANIMATION_ATTACK = [
    (f"{PLAYER_DIR}\\imgs\\attack\\tile000.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\attack\\tile001.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\attack\\tile002.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\attack\\tile003.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\attack\\tile004.png", ANIMATION_DELAY),
    (f"{PLAYER_DIR}\\imgs\\attack\\tile005.png", ANIMATION_DELAY),
]

# константы для шрифта
font.init()
FONT = font.Font(font.match_font("Tahoma"), 18)
FONT_COLOR = "#333333"

# класс игрока
class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0 # скорость по x
        self.yvel = 0 # скорость по y
        self.up = False # движение вверх
        self.attack = False # атака
        self.left = False # движение влево
        self.right = False # движение вправо
        self.direction = 1 # направление игрока
        self.finish = False # конец уровня
        self.onGround = False # стоит на земле
        # прямоугольник, представляющий игрока
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        # изображение игрока
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(COLOR)
        self.image.set_colorkey(COLOR)

        self.score = 0 # текущие очки

        # загрузка анимаций
        
        self.boltAnimIdleRight = PygAnimation(ANIMATION_IDLE)
        self.boltAnimIdleRight.play()
        # анимация по умолчанию
        self.boltAnimIdleRight.blit(self.image, (0, 0))

        self.boltAnimIdleLeft = PygAnimation(ANIMATION_IDLE)
        self.boltAnimIdleLeft.flip(True, False)
        self.boltAnimIdleLeft.play()

        self.boltAnimWalkRight = PygAnimation(ANIMATION_WALK)
        self.boltAnimWalkRight.play()

        self.boltAnimWalkLeft = PygAnimation(ANIMATION_WALK)
        self.boltAnimWalkLeft.flip(True, False)
        self.boltAnimWalkLeft.play()

        self.boltAnimJumpRight = PygAnimation(ANIMATION_JUMP)
        self.boltAnimJumpRight.play()

        self.boltAnimJumpLeft = PygAnimation(ANIMATION_JUMP)
        self.boltAnimJumpLeft.flip(True, False)
        self.boltAnimJumpLeft.play()

        self.boltAnimAttackRight = PygAnimation(ANIMATION_ATTACK)
        self.boltAnimAttackRight.play()

        self.boltAnimAttackLeft = PygAnimation(ANIMATION_ATTACK)
        self.boltAnimAttackLeft.flip(True, False)
        self.boltAnimAttackLeft.play()

    # обработка кнопок для игрока
    def process_key(self, e: List[event.Event], entities):
        if e.type == KEYDOWN and e.key == K_UP:
            self.up = True
        if e.type == KEYDOWN and e.key == K_LEFT:
            self.left = True
        if e.type == KEYDOWN and e.key == K_RIGHT:
            self.right = True

        if e.type == KEYDOWN and e.key == K_SPACE:
            self.attack = True
            bullet = Bullet(self.rect.centerx, self.rect.top, self.direction)
            bullet.sound.play()
            entities.add(bullet)
        if e.type == KEYUP and e.key == K_SPACE:
            self.attack = False

        if e.type == KEYUP and e.key == K_UP:
            self.up = False
        if e.type == KEYUP and e.key == K_RIGHT:
            self.right = False
        if e.type == KEYUP and e.key == K_LEFT:
            self.left = False

    # обновление игрока
    def update(self, win, platforms=[]):
        if self.up: # если нажата стрелка вверх
            if self.onGround: # если игрок на земле
                self.yvel = -JUMP_POWER # прыгнуть
            self.image.fill(COLOR) # закрасить
            if self.left: # если нажата стрелка влево
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else: # если нажата стрелка вправо
                self.boltAnimJumpRight.blit(self.image, (0, 0))


        if self.left: # если нажата стрелка влево
            self.direction = -1 # изменить направление
            self.xvel = -MOVE_SPEED # отнять скорость по x
            if not self.up: # если не нажата стрелка вверх
                # включить анимацию
                self.image.fill(COLOR)
                self.boltAnimWalkLeft.blit(self.image, (0, 0))

        if self.right: # если нажата стрелка вправо
            self.direction = 1 # изменить направление
            self.xvel = MOVE_SPEED # добавить скорость по x
            if not self.up: # если не нажата стрелка вверх
                # включить анимацию
                self.image.fill(COLOR)
                self.boltAnimWalkRight.blit(self.image, (0, 0))

        if not (self.left or self.right): # если стрелки не нажаты
            self.xvel = 0 # убрать скорость по x
            if not self.up: # если не нажата стрелка вверх
                # включить анимацию в зависимости от направления
                self.image.fill(COLOR)
                if self.direction == 1:
                    self.boltAnimIdleRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimIdleLeft.blit(self.image, (0, 0))

        if self.attack: # если нажат пробел
            # включить анимацию
            self.image.fill(COLOR)
            if self.direction == 1:
                self.boltAnimAttackRight.blit(self.image, (0, 0))
            else:
                self.boltAnimAttackLeft.blit(self.image, (0, 0))

        if not self.onGround: # если не на земле
            self.yvel += GRAVITY # добавить гравитацию

        # переместить игрока
        self.onGround = False
        self.rect.y += self.yvel
        # проверить на столкновения
        self.collide(0, self.yvel, platforms)

        # переместить игрока
        self.rect.x += self.xvel
        # проверить на столкновения
        self.collide(self.xvel, 0, platforms)

        # отрисовать очки над игроком
        self.draw_score(win)

    # функция проверки на столкновение с платформами
    def collide(self, xvel, yvel, platforms):
        # цикл по каждой платформе
        for p in platforms:
            # если столкновение с платформой и платформа существует
            if sprite.collide_rect(self, p) and p.alive():
                # обновление перемещения игрока
                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

    # функция отрисовки очков над игроком
    def draw_score(self, win):
        text_surface = FONT.render(str(self.score), True, FONT_COLOR)
        rect = text_surface.get_rect()
        rect.topleft = (self.rect.centerx - rect.width / 2, self.rect.y - 15)
        win.blit(text_surface, rect)
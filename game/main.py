from pygame import *
from coins.coin import Coin
from portals.portal import Portal
from platforms.platform import Platform
from players.player import Player
from bullets.bullet import Bullet
from traps.trap import Trap
from os import path

# размеры окна
WIDTH = 640
HEIGHT = 192
SIZE = (WIDTH, HEIGHT)

# папка с файлом
DIR = path.dirname(__file__)

# цвета
BG_COLOR = "#8fbaff"
FONT_COLOR = "#333333"
FONT_SHADOW_COLOR = "#cccccc"

levels = [] # список уровней
# функция чтения уровней из файла
def load_levels():
    # открытие файла
    with open("levels.txt", "r") as f:
        level = []
        for line in f: # чтение строки
            if "level" in line:
                # добавление уровня в список
                levels.append(level)
                level = []
            else:
                level.append(line)

# функция рисования текста
font_name = font.match_font('Tahoma')
shadow_offset = 1
def draw_text(win: Surface, text, size, x, y):
    f = font.Font(font_name, size)
    text_shadow = f.render(text, True, FONT_SHADOW_COLOR)
    text_shadow_rect = text_shadow.get_rect()
    text_shadow_rect.topleft = (
        x - shadow_offset - text_shadow_rect.width / 2,
        y - shadow_offset - text_shadow_rect.height / 2
    )
    text = f.render(text, True, FONT_COLOR)
    text_rect = text.get_rect()
    text_rect.topleft = (x - text_rect.width / 2, y - text_rect.height / 2)
    win.blit(text_shadow, text_shadow_rect)
    win.blit(text, text_rect)

# функция создания игры
def create_game(current_level, scores):
    hero = Player(0, 100) # создание игрока
    hero.score = scores # сохранение очков предыдущего уровня
    entities = sprite.Group() # список объектов
    entities.add(hero) # добавление игрока в список объектов
    platforms = [] # список платформ
    if current_level >= len(levels): # если уровни кончились
        return None, platforms, entities
    else:
        # чтение уровня
        x = -Platform.PLATFORM_SIZE
        y = 0
        for row in levels[current_level]:
            for sym in row:
                if sym == "-": # создание платформы
                    pf = Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)
                elif sym == "#": # создание разрушаемой платформы
                    pf = Platform(x, y, True)
                    entities.add(pf)
                    platforms.append(pf)
                elif sym == "*": # создание монетки
                    coin = Coin(x, y)
                    entities.add(coin)
                elif sym == "&": # создание огня
                    trap = Trap(x, y)
                    entities.add(trap)
                elif sym == "0": # создание портала
                    portal = Portal(x, y)
                    entities.add(portal)
                x += Platform.PLATFORM_SIZE
            y += Platform.PLATFORM_SIZE
            x = -Platform.PLATFORM_SIZE
        return hero, platforms, entities

# основная функция
def main():
    init() # инициализация pygame
    # создание окна
    win = display.set_mode(SIZE)
    win.fill(BG_COLOR)
    display.set_caption("Приключение бродяги")

    load_levels() # загрузка уровней из файла

    #инициализация переменных
    current_level = 0
    best_score = 0
    last_score = 0

    bg = image.load(f"{DIR}/bg.png")

    # загрузка и включение музыки
    mixer.music.load(f"{DIR}/sounds/music.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play(-1)

    timer = time.Clock()

    # создание уровня
    hero, platforms, entities = create_game(current_level, 0)

    while True:
        timer.tick(60)

        # обработка нажатий на кнопки
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
            if hero != None and hero.alive():
                hero.process_key(e, entities)
            elif e.type == KEYDOWN and e.key == K_RETURN:
                hero, platforms, entities = create_game(0, 0)

        win.blit(bg, (0, 0)) # закрашивание окна
        if hero != None and hero.alive(): # если игрок существует
            hero.update(win, platforms) # обновление игрока
            last_score = hero.score # запоминание очков игрока
            if best_score < last_score: # проверка на новый рекорд
                best_score = last_score

            # цикл по игровым объектам
            for e in entities:
                # отрисовка объектов
                win.blit(e.image, e.rect.topleft)
                # обновление объектов
                if isinstance(e, Bullet):
                    e.update(platforms)
                elif isinstance(e, Coin) or isinstance(e, Portal) or isinstance(e, Trap):
                    e.update(hero)
                    # проверка на конец уровня
                    if hero.finish:
                        # создание следующего уровня
                        current_level += 1
                        hero, platforms, entities = create_game(current_level, hero.score)
        else: # иначе, игрок не существует
            # вывод результатов
            current_level = 0
            draw_text(win, f"Конец игры!", 20, WIDTH / 2, HEIGHT / 2 - 24)
            draw_text(win, f"Лучший результат: {best_score}", 20, WIDTH / 2, HEIGHT / 2)
            draw_text(win, f"Ваш результат: {last_score}", 20, WIDTH / 2, HEIGHT / 2 + 24)
            draw_text(win, f"Для начала новой игры нажмите Enter", 20, WIDTH / 2, HEIGHT - 24)

        # обновление экрана

        display.update()

main()
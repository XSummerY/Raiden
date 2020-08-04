import random

import numpy as np
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

# 刷新帧率
FRAME_PER_SECOND = 60

# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT


def rand_pick(seq, probabilities):
    x = random.uniform(0, 1)
    cumprob = 0.0
    for item, item_pro in zip(seq, probabilities):
        cumprob += item_pro
        if x < cumprob:
            break
    return item


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    __is_alt = False

    def __init__(self, image_name="./images/background.png", speed=1):
        super().__init__(image_name)
        if Background.__is_alt:
            self.rect.y = -self.rect.height
        Background.__is_alt = True

    def update(self):

        # 1. 调用父类方法实现
        super().update()
        # 2 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        self.enemy1_hit_surface = list()
        self.enemy1_hit_surface.append(pygame.image.load("./images/enemy1_down1.png"))
        self.enemy1_hit_surface.append(pygame.image.load("./images/enemy1_down2.png"))
        self.enemy1_hit_surface.append(pygame.image.load("./images/enemy1_down3.png"))
        self.enemy1_hit_surface.append(pygame.image.load("./images/enemy1_down4.png"))
        self.enemy2_hit_surface = list()
        self.enemy2_hit_surface.append(pygame.image.load("./images/enemy2_down1.png"))
        self.enemy2_hit_surface.append(pygame.image.load("./images/enemy2_down2.png"))
        self.enemy2_hit_surface.append(pygame.image.load("./images/enemy2_down3.png"))
        self.enemy2_hit_surface.append(pygame.image.load("./images/enemy2_down4.png"))

        self.enemy_list = [0, 1]
        self.random_list = [0.7, 0.3]
        self.index = rand_pick(self.enemy_list, self.random_list)
        if self.index == 0:
            image = "./images/enemy1.png"
        else:
            image = "./images/enemy2.png"
        # 1. 调用父类方法，创建敌机精灵，同时指定图片
        super().__init__(image)
        # 2. 指定敌机的初始随机速度
        self.speed = random.randint(1, 5)
        # 3. 指定敌机的初始随机位置
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = 0
        # 4. 爆炸指示
        self.explode_index1 = 0
        self.explode_index2 = 0

    def update(self):
        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()
        # 2. 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()

    def __del__(self):
        pass


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):
        # 1.调用父类方法，设置image&speed
        super().__init__("./images/me1.png", 0)
        self.speed_x = 0
        self.speed_y = 0
        # 2. 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # 3. 设置子弹的精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        if SCREEN_RECT.width - self.rect.width >= self.rect.x + self.speed_x >= 0:
            self.rect.x += self.speed_x
        if SCREEN_RECT.height - self.rect.height >= self.rect.y + self.speed_y >= 0:
            self.rect.y += self.speed_y

    def fire(self):
        bullet = Bullet()
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.bottom = self.rect.top
        self.bullet_group.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet2.png", -2)

    def update(self):
        super().update()

        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        pass


class PressButton(GameSprite):
    def __init__(self, image_name):
        super().__init__(image_name, 0)

    def update(self):
        super().update()


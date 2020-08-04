from itertools import cycle

import time
import pygame
from plane_sprites import *
from cover_sprites import *

# 定义动画周期（帧数）
ANIMATE_CYCLE = 100
ticks = 0

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
blue = (0, 0, 255)

pygame.init()


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):

        # 1. 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_RECT.size))
        # 2. 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3. 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 4. 设定定时器事件 - 创建敌机 1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # 5.初始化mixer
        pygame.mixer.init()

    def wait(self):
        pygame.mixer.music.load("./music/background1.wav")
        pygame.mixer.music.play(-1, 0.0)
        event_wait = pygame.event.get()
        font = pygame.font.Font("./fonts/KH-Dot-Hibiya-32/KH-Dot-Hibiya-32.ttf", 20)
        on_text_surface = font.render('Press Any Key To Start', True, pygame.Color('white'))
        blink_rect = on_text_surface.get_rect()
        blink_rect.centerx = SCREEN_RECT.centerx
        blink_rect.centery = SCREEN_RECT.centery + 200
        off_text_surface = pygame.Surface(blink_rect.size)
        off_text_surface.set_alpha(0)
        blink_surfaces = cycle([on_text_surface, off_text_surface])
        blink_surface = next(blink_surfaces)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        while True:
            self.clock.tick(FRAME_PER_SECOND)
            self.cover_background_group.update()
            self.cover_background_group.draw(self.screen)
            self.title_group.update()
            self.title_group.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("./music/start.wav")
                    pygame.mixer.music.play()
                    time.sleep(2)
                    pygame.mixer.music.stop()
                    return
                if event.type == pygame.USEREVENT:
                    blink_surface = next(blink_surfaces)
                if event.type == pygame.QUIT:
                    PlaneGame.__game_over()
            self.screen.blit(blink_surface, blink_rect)
            pygame.display.update()

    def __paused(self):

        while True:
            self.clock.tick(FRAME_PER_SECOND)
            mouse_x1, mouse_y1 = pygame.mouse.get_pos()
            if (self.pause_button.rect.x <= mouse_x1 <= self.pause_button.rect.x + self.pause_button.rect.width
                    and 0 <= mouse_y1 <= self.pause_button.rect.x + self.pause_button.rect.height):
                self.pause_group.remove(self.pause_button)
                self.pause_button = next(self.pause_buttons)
                self.pause_group.add(self.pause_button)
                self.pause_group.update()
                self.pause_group.draw(self.screen)
                pygame.display.update()
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_array1 = pygame.mouse.get_pressed()
                    for index in range(len(pressed_array1)):
                        if pressed_array1[index]:
                            if index == 0:
                                return
            keys_pressed1 = pygame.key.get_pressed()
            # 判断元组中对应的按键索引值
            if keys_pressed1[pygame.K_ESCAPE]:
                return

    def __create_sprites(self):

        # 1.创建背景
        bg1 = Background()
        bg2 = Background()
        self.background_group = pygame.sprite.Group(bg1, bg2)

        # 2. 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 3. 创建英雄以及其精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        # 4. 创建封面和菜单类
        title = Title()
        self.title_group = pygame.sprite.Group(title)
        bg3 = CoverBackground()
        bg4 = CoverBackground()
        self.cover_background_group = pygame.sprite.Group(bg3, bg4)
        # press_any_button = PressAnyButton()
        # self.press_group = pygame.sprite.Group(press_any_button)

        # 5. 创建分数
        self.score = 0
        self.font_score = pygame.font.Font("./fonts/KH-Dot-Hibiya-32/KH-Dot-Hibiya-32.ttf", 30)
        self.score_str = "score:" + str(self.score)
        self.score_surface = self.font_score.render(self.score_str, True, pygame.Color('white'))
        self.score_rect = self.score_surface.get_rect()
        self.score_rect.x = 0
        self.score_rect.y = 0

        # 6.创建暂停按钮
        pause_button1 = PressButton("./images/pause_nor.png")
        pause_button1.rect.x = SCREEN_RECT.width - pause_button1.rect.width
        pause_button1.rect.y = 0
        pause_button2 = PressButton("./images/pause_pressed.png")
        pause_button2.rect.x = SCREEN_RECT.width - pause_button2.rect.width
        pause_button2.rect.y = 0
        resume_button1 = PressButton("./images/resume_nor.png")
        resume_button1.rect.centerx = SCREEN_RECT.centerx
        resume_button1.rect.y = SCREEN_RECT.centery
        resume_button2 = PressButton("./images/resume_pressed.png")
        resume_button2.rect.centerx = SCREEN_RECT.centerx
        resume_button2.rect.y = SCREEN_RECT.centery
        self.pause_buttons = cycle([pause_button1, pause_button2])
        self.resume_buttons = cycle([resume_button1, resume_button2])
        self.pause_button = next(self.pause_buttons)
        self.resume_button = next(self.resume_buttons)
        # print("pause_button: %d %d" % (self.pause_button.rect.x, self.pause_button.rect.y))
        # print(type(self.pause_button))
        self.pause_group = pygame.sprite.Group(self.pause_button)
        self.resume_group = pygame.sprite.Group(self.resume_button)

    def start_game(self):

        while True:
            # 1.设置刷新帧率
            self.clock.tick(FRAME_PER_SECOND)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新/绘制精灵组
            self.__update_sprites()
            # 5.更新屏幕显示
            pygame.display.update()
            pass

    def __event_handler(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # print("敌机出场")
                # 1. 创建敌机精灵
                enemy = Enemy()
                # 2. 将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            self.__paused()

        # 使用键盘提供的方法获取键盘按键
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed_x = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed_x = -2
        else:
            self.hero.speed_x = 0
        if keys_pressed[pygame.K_UP]:
            self.hero.speed_y = -2
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speed_y = 2
        else:
            self.hero.speed_y = 0
        if keys_pressed[pygame.K_SPACE]:
            self.hero.fire()
        if keys_pressed[pygame.K_ESCAPE]:
            self.__paused()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.pause_button.rect.x <= mouse_x <= self.pause_button.rect.x + self.pause_button.rect.width
                and 0 <= mouse_y <= self.pause_button.rect.x + self.pause_button.rect.height):
            self.pause_group.remove(self.pause_button)
            self.pause_button = next(self.pause_buttons)
            self.pause_group.add(self.pause_button)

    def __check_collide(self):

        # 创建被击中的敌方飞机组
        self.enemy_hit_group = pygame.sprite.Group()
        # 1. 子弹摧毁敌机
        self.enemy_hit_group.add(pygame.sprite.groupcollide(self.enemy_group, self.hero.bullet_group, True, True))

        # 2. 英雄飞机与敌机碰撞
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 3. 判断列表是否有内容
        if len(enemies) > 0:
            # 让英雄牺牲
            self.hero.kill()
            # 结束游戏
            PlaneGame.__game_over()

    def __update_sprites(self):
        self.background_group.update()
        self.background_group.draw(self.screen)

        for enemy_hit in self.enemy_hit_group:
            if enemy_hit.index == 0:
                self.score += 1000
                self.score_str = "score:" + str(self.score)
                self.score_surface = self.font_score.render(self.score_str, True, pygame.Color('white'))
                self.score_rect = self.score_surface.get_rect()
                self.screen.blit(enemy_hit.enemy1_hit_surface[enemy_hit.explode_index1], enemy_hit.rect)
                pygame.mixer.music.load("./music/enemy1_down.wav")
                pygame.mixer.music.play()
                if ANIMATE_CYCLE % 3 == 0:
                    if enemy_hit.explode_index1 < 3:
                        enemy_hit.explode_index1 += 1
                    else:
                        self.enemy_hit_group.remove(enemy_hit)

            else:
                self.score += 2000
                self.score_str = "score:" + str(self.score)
                self.score_surface = self.font_score.render(self.score_str, True, pygame.Color('white'))
                self.score_rect = self.score_surface.get_rect()
                self.screen.blit(enemy_hit.enemy2_hit_surface[enemy_hit.explode_index2], enemy_hit.rect)
                pygame.mixer.music.load("./music/enemy1_down.wav")
                pygame.mixer.music.play()
                if ANIMATE_CYCLE % 3 == 0:
                    if enemy_hit.explode_index2 < 3:
                        enemy_hit.explode_index2 += 1
                    else:
                        self.enemy_hit_group.remove(enemy_hit)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

        self.screen.blit(self.score_surface, self.score_rect)

        self.pause_group.update()
        self.pause_group.draw(self.screen)

        pygame.display.update()

    @staticmethod
    def __game_over():
        print("游戏结束")

        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()

    # 显示开始画面
    game.wait()

    # 开始游戏
    game.start_game()

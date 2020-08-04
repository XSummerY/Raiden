import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

# 刷新帧率
FRAME_PER_SECOND = 60


class MenuSprite(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=0):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class CoverBackground(MenuSprite):
    """背景精灵"""

    __is_alt = False

    def __init__(self, image_name="./images/background.png", speed=1):
        super().__init__(image_name, speed)
        if CoverBackground.__is_alt:
            self.rect.y = -self.rect.height
        CoverBackground.__is_alt = True

    def update(self):

        # 1. 调用父类方法实现
        super().update()
        # 2 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Title(MenuSprite):

    def __init__(self, image_name="./images/title.png"):
        super().__init__(image_name)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.top + 200
        self.flag = 0

    def update(self):
        super().update()


# class PressAnyButton(MenuSprite):
#
#     def __init__(self, image_name="./images/press_any_button.png"):
#         super().__init__(image_name)
#         self.rect.centerx = SCREEN_RECT.centerx
#         self.rect.bottom = SCREEN_RECT.bottom - 200
#         self.flag = 0
#
#     def update(self):
#         super().update()




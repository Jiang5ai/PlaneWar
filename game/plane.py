# -*- coding: utf-8 -*-
# @Time    : 2020/3/28 14:49
# @Author  : JS
# @File    : plane.py
# @Software: PyCharm
import pygame
import constants
import random
from game.bullet import Bullet


class Plane(pygame.sprite.Sprite):
    """飞机的基类"""
    # 飞机的图片
    plane_images = []
    # 飞机爆炸的图片
    destroy_images = []
    # 坠毁的音乐地址
    down_sound_src = None
    # 飞机的状态 True:活的 Flase:死的
    active = True
    # 飞机发射的子弹精灵组
    bullets = pygame.sprite.Group()

    def __init__(self, screen, speed=None):
        super().__init__()
        self.screen = screen
        # 加载静态资源
        self.img_list = []
        self._destroy_images_list = []
        self.down_sound = None
        self.load_src()
        # 飞机飞行的速度
        self.speed = speed or 100
        # 获取飞机的位置
        self.rect = self.img_list[0].get_rect()
        # print(self.rect)
        # 获取飞机的宽度和高度
        self.plane_w, self.plane_h = self.img_list[0].get_size()
        # print(self.plane_w, self.plane_h)
        # 获取屏幕的大小
        self.width, self.height = self.screen.get_size()
        # 改变飞机的初始化位置，放在屏幕的下方
        self.rect.left = int((self.width - self.plane_w) / 2)
        self.rect.top = int(self.height / 2)

    def load_src(self):
        """加载静态资源"""
        # 加载飞机图片
        for img in self.plane_images:
            self.img_list.append(pygame.image.load(img))
        # 加载飞机坠毁图片
        for img in self.destroy_images:
            self._destroy_images_list.append(pygame.image.load(img))
        # 加载坠毁音乐
        if self.down_sound_src:
            self.down_sound = pygame.mixer.Sound(self.down_sound_src)

    @property
    def image(self):
        return self.img_list[0]

    def blit_me(self):
        self.screen.blit(self.image, self.rect)

    def move_up(self):
        """飞机向上移动"""
        self.rect.top -= self.speed

    def move_down(self):
        """飞机向下移动"""
        self.rect.top += self.speed

    def move_left(self):
        """飞机向左移动"""
        self.rect.left -= self.speed

    def move_right(self):
        """飞机向右移动"""
        self.rect.right += self.speed

    def broken_down(self):
        """飞机坠毁效果"""
        # 播放坠毁音乐
        if self.down_sound:
            self.down_sound.play()
        # 展示坠毁动画
        for img in self._destroy_images_list:
            self.screen.blit(img, self.rect)
        # 其他操作
        self.active = False


class OurPlane(Plane):
    """我方的飞机"""
    # 飞机的图片
    plane_images = constants.OUR_PLANE_IMG
    # 飞机爆炸的图片
    destroy_images = constants.OUR_DESTROY_IMG_LIST
    # 坠毁的音乐地址
    down_sound_src = None

    def update(self, war):
        """更新飞机的动画效果"""
        # 切换飞机的动画效果，喷气式效果
        if war.frame % 5 == 0:
            self.screen.blit(self.img_list[0], self.rect)
        else:
            self.screen.blit(self.img_list[1], self.rect)
        # 飞机撞击检测
        rest = pygame.sprite.spritecollide(self, war.enemies, False)
        if rest:
            # 游戏结束
            war.status = war.OVER
            # 敌方飞机清除
            war.enemies.empty()
            war.small_enemies.empty()
            # 我方飞机坠毁
            self.broken_down()
            # 统计分数

    def move_up(self):
        """向上移动，超出范围后，重置"""
        super().move_up()
        if self.rect.top <= 0:
            self.rect.top = 0

    def move_down(self):
        """飞机向下移动,超出范围后，重置"""
        super().move_down()
        # print(self.rect.bottom, self.height)
        # 如果飞机当前位置的y >= 飞机在屏幕最低端时y的值，重置
        if self.rect.top >= self.height - self.plane_h:
            self.rect.top = self.height - self.plane_h
        # if self.rect.bottom >= self.height:
        #     self.rect.bottom = self.height

    def move_left(self):
        """飞机向左移动,超出范围后，重置"""
        super().move_left()
        if self.rect.left <= 0:
            self.rect.left = 0

    def move_right(self):
        """飞机向右移动,超出范围后，重置"""
        super().move_right()
        # print(self.rect.right, self.screen.get_rect().right, self.width)
        if self.rect.left >= self.width - self.plane_w:
            self.rect.left = self.width - self.plane_w
        # if self.rect.right >= self.width:
        #     self.rect.right = self.width

    def shoot(self):
        """发射子弹"""
        bullet = Bullet(self.screen, self, 15)
        self.bullets.add(bullet)


class SmallEnemyPlane(Plane):
    """敌方的小型飞机"""
    # 飞机的图片
    plane_images = constants.SMALL_ENEMY_PLANE_IMG_LIST
    # 飞机爆炸的图片
    destroy_images = constants.SMALL_ENEMY_DESTROY_IMG_LIST
    # 坠毁的音乐地址
    down_sound_src = constants.SMALL_ENEMY_PLANE_DOWN_SOUND
    # 飞机的状态 True:活的 Flase:死的
    active = True

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        self.init_pos()

    def init_pos(self):
        """改变飞机的随机位置"""
        # 每次生成一架新的小型飞机的时候，随机的位置出现在屏幕中
        # 屏幕的宽度-飞机的宽度
        self.rect.left = random.randint(0, self.width - self.plane_w)
        # 屏幕之外随机高度
        self.rect.top = random.randint(-5 * self.plane_h, -self.plane_h)

    def update(self, *args):
        """更新飞机的移动"""
        super().move_down()
        # 画在屏幕上
        self.blit_me()
        # 超出范围后如何处理： 1.重用 2.多线程
        if self.rect.top >= self.height:
            self.active = False
            self.reset()

    def reset(self):
        """重置飞机得状态，达到复用的效果"""
        self.active = True
        self.init_pos()

    def break_down(self):
        """飞机爆炸"""
        super().broken_down()
        # 重复利用飞机对象
        self.reset()

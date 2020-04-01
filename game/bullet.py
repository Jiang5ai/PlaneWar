# -*- coding: utf-8 -*-
# @Time    : 2020/3/28 14:49
# @Author  : JS
# @File    : bullet.py
# @Software: PyCharm
import pygame
import constants


class Bullet(pygame.sprite.Sprite):
    """子弹类"""

    # 子弹状态
    active = True

    def __init__(self, screen, plane, speed=None):
        super().__init__()
        self.speed = speed or 10
        self.plane = plane
        # 加载子弹的图片
        self.image = pygame.image.load(constants.BULLET_IMG)
        self.screen = screen
        # 改变子弹的位置
        self.rect = self.image.get_rect()
        # 让子弹的中心位置与飞机的中心位置一致，让子弹x方向的中心与飞机x方向的中心一致
        self.rect.centerx = plane.rect.centerx
        self.rect.top = plane.rect.top
        # 发射的音乐效果
        self.shoot_sound = pygame.mixer.Sound(constants.BULLET_SHOOT_SOUND)
        self.shoot_sound.set_volume(0.2)
        self.shoot_sound.play()

    def update(self, war):
        """更新子弹的位置"""
        self.rect.top -= self.speed
        # 超出屏幕范围 将子弹从精灵组中移除
        if self.rect.top < 0:
            self.remove(self.plane.bullets)
        # 绘制子弹
        self.screen.blit(self.image, self.rect)
        # 碰撞检测，检测子弹是否已经碰撞到敌机
        rest = pygame.sprite.spritecollide(self, war.enemies, False)
        for r in rest:
            # 子弹消失
            self.kill()
            # 飞机爆炸坠毁
            r.break_down()
            # 统计游戏成绩
            war.rest.score += constants.SCORE_SHOOT_SMALL

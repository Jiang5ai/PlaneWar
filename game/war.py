# -*- coding: utf-8 -*-
# @Time    : 2020/3/28 14:50
# @Author  : JS
# @File    : war.py
# @Software: PyCharm
import pygame
import sys
import constants
from game.plane import OurPlane, SmallEnemyPlane
from store.result import PlayRest


class PlaneWar(object):
    """飞机大战"""

    READY = 0  # 游戏准备中
    PLAYING = 1  # 游戏中
    OVER = 2  # 游戏结束
    status = READY
    # 实例化我方飞机
    our_plane = None
    # 播放帧数
    frame = 0
    # 一架飞机可以属于多个精灵组
    small_enemies = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    clock = pygame.time.Clock()
    # 实例化游戏结果
    rest = PlayRest()

    def __init__(self):
        # 初始化
        pygame.init()
        # 设置宽度高度
        self.width, self.height = 480, 852
        # 屏幕对象
        self.screen = pygame.display.set_mode((self.width, self.height))
        # 加载背景图片
        self.bg = pygame.image.load(constants.BG_IMG)
        self.bg_over = pygame.image.load(constants.BG_IMG_OVER)
        # 游戏标题
        self.img_game_title = pygame.image.load(constants.IMG_GAME_TITLE)
        self.img_game_title_rect = self.img_game_title.get_rect()
        # 获取游戏标题的宽度高度
        t_width, t_height = self.img_game_title.get_size()
        self.img_game_title_rect.topleft = (int((self.width - t_width) / 2),
                                            int((self.height - t_height) / 2))

        # 开始按钮
        self.btn_start = pygame.image.load(constants.IMG_GAME_START_BTN)
        self.btn_start_rect = self.btn_start.get_rect()
        # 获取开始按钮的宽度高度
        self.btn_width, self.btn_height = self.btn_start.get_size()
        self.btn_start_rect.topleft = (int((self.width - self.btn_width) / 2),
                                       int(self.height / 2 + self.btn_height + 20))

        # 游戏文字对象
        self.score_font = pygame.font.SysFont('kaiti', 50)

        # 加载背景音乐
        # pygame.mixer.music.load(constants.BG_MUSIC)
        # pygame.mixer.music.play(-1)  # 设置循环播放
        # pygame.mixer.music.set_volume(0.2)  # 音量设置
        # 设置窗口标题
        pygame.display.set_caption('飞机大战')
        # 我方飞机对象
        self.our_plane = OurPlane(self.screen, speed=20)

        self.clock = pygame.time.Clock()

    def bind_event(self):
        """绑定事件"""

        # 监听事件
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标点击进入游戏
                # 游戏正在准备中，点击才能进入游戏
                if self.status == self.READY:
                    self.status = self.PLAYING
            elif event.type == pygame.KEYDOWN:
                # 键盘事件
                # 游戏正在进行中，才需要控制键盘
                if self.status == self.PLAYING:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.our_plane.move_up()
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.our_plane.move_down()
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.our_plane.move_left()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.our_plane.move_right()
                    elif event.key == pygame.K_SPACE:
                        # 发射子弹
                        self.our_plane.shoot()

    def add_small_enemies(self, num):
        """随机添加N架小型飞机"""
        for i in range(num):
            plane = SmallEnemyPlane(self.screen, speed=8)
            plane.add(self.small_enemies, self.enemies)

    def run_game(self):
        """游戏主循环部分"""
        while True:
            # 1.设置帧速率
            self.clock.tick(60)
            self.frame += 1
            if self.frame >= 60:
                self.frame = 0
            # 2.绑定事件
            self.bind_event()
            # 3.更新游戏的状态
            if self.status == self.READY:
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 标题
                self.screen.blit(self.img_game_title, self.img_game_title_rect)
                # 开始按钮
                self.screen.blit(self.btn_start, self.btn_start_rect)
            elif self.status == self.PLAYING:
                # 游戏进行中
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 绘制飞机
                self.our_plane.update(self)
                # 绘制子弹
                self.our_plane.bullets.update(self)
                # 绘制敌方飞机
                self.small_enemies.update()
                # 绘制游戏分数
                score_text = self.score_font.render("得分:{}".format(self.rest.score), False, constants.TEXT_SOCRE_COLOR)
                self.screen.blit(score_text, score_text.get_rect())
            elif self.status == self.OVER:
                # 游戏结束
                # 游戏背景
                self.screen.blit(self.bg_over, self.bg_over.get_rect())
                # 分数统计
                # 绘制本次总分数
                score_text = self.score_font.render("{}".format(self.rest.score), False, constants.TEXT_SOCRE_COLOR)
                score_text_rect = score_text.get_rect()
                text_w, text_h = score_text.get_size()
                score_text_rect.topleft = (int((self.width - text_w) / 2), int(self.height / 2))
                self.screen.blit(score_text, score_text_rect)
            pygame.display.flip()

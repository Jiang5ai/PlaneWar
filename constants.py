# -*- coding: utf-8 -*-
# @Time    : 2020/3/28 14:53
# @Author  : JS
# @File    : constants.py
# @Software: PyCharm
import os

# 获取项目的根目录 F:\chapter12
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 静态本间的目录
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# 背景图片
BG_IMG = os.path.join(ASSETS_DIR, 'images\\background.png')
BG_IMG_READY = os.path.join(ASSETS_DIR, 'images\\background.png')
BG_IMG_OVER= os.path.join(ASSETS_DIR, 'images\\game_over.png')
# 标题图片
IMG_GAME_TITLE = os.path.join(ASSETS_DIR, 'images\\game_title.png')
# 开始按钮
IMG_GAME_START_BTN = os.path.join(ASSETS_DIR, 'images\\game_start.png')
# 背景音乐
BG_MUSIC = os.path.join(ASSETS_DIR, 'sounds\\game_bg_music.mp3')

# 我方飞机的静态资源
OUR_PLANE_IMG = [os.path.join(ASSETS_DIR, 'images\\hero1.png'), os.path.join(ASSETS_DIR, 'images\\hero2.png')]
OUR_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images\\hero_broken_n1.png'),
    os.path.join(ASSETS_DIR, 'images\\hero_broken_n2.png'),
    os.path.join(ASSETS_DIR, 'images\\hero_broken_n3.png'),
    os.path.join(ASSETS_DIR, 'images\\hero_broken_n3.png')]
# 子弹的图片
BULLET_IMG = os.path.join(ASSETS_DIR, 'images\\bullet1.png')
# 射击的声音
BULLET_SHOOT_SOUND = os.path.join(ASSETS_DIR, 'sounds\\bullet.wav')

# 敌方小型飞机图片及音效
SMALL_ENEMY_PLANE_IMG_LIST = [os.path.join(ASSETS_DIR, 'images\\enemy1.png')]
SMALL_ENEMY_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images\\enemy1_down1.png'),
    os.path.join(ASSETS_DIR, 'images\\enemy1_down1.png'),
    os.path.join(ASSETS_DIR, 'images\\enemy1_down1.png'),
    os.path.join(ASSETS_DIR, 'images\\enemy1_down1.png')]
SMALL_ENEMY_PLANE_DOWN_SOUND = os.path.join(ASSETS_DIR, 'sounds\\enemy1_down.wav')

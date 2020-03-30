# -*- coding: utf-8 -*-
# @Time    : 2020/3/28 14:52
# @Author  : JS
# @File    : main.py
# @Software: PyCharm
import pygame
import sys
import constants
from game.plane import OurPlane,SmallEnemyPlane
from game.war import PlaneWar

def main():
    """游戏入口，main方法"""
    war = PlaneWar()
    # 添加小型敌方飞机
    war.add_small_enemies(6)
    war.run_game()

if __name__ == '__main__':
    main()

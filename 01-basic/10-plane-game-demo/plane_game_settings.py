import pygame

# 此文件用来保存飞机大战中的一些设置参数

# 屏幕大小
SCREEN_SIZE = (480, 720)

# 刷新的帧率
FRAME_PER_SEC = 60

# 自定义敌机刷新事件
CREATE_ENEMY_EVENT = pygame.USEREVENT

# hero开火事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1

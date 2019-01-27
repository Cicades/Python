import pygame
from plane_sprite import *
# 加载pygame中的模块
pygame.init()

# 绘制游戏窗口
screen = pygame.display.set_mode((480, 700))

# 加载图片
bg = pygame.image.load('./images/background.png')
# 将图片绘制到窗口
screen.blit(bg, (0, 0))
hero = pygame.image.load('./images/me1.png')
screen.blit(hero, (150, 300))
# 刷新窗口
pygame.display.update()
# 定义rect记录游戏对象的位置
hero_rect = pygame.Rect(150, 300, 102, 126)
# 创建敌机精灵
enemy = GameSprite('./images/enemy1.png')
enemy1 = GameSprite('./images/enemy1.png', 2)
# 创建敌机精灵组
enemy_group = pygame.sprite.Group(enemy, enemy1)
# 创建时钟对象
clock = pygame.time.Clock()
while True:
    # 指定游戏循环中的刷新率,1秒60帧
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            print('游戏结束！')
    if hero_rect.y <= -hero_rect.height:
        hero_rect.y = 700
    hero_rect.y -= 1
    screen.blit(bg, (0, 0))
    screen.blit(hero, hero_rect)
    # 调用精灵组的update方法 =》 调用精灵组中所有精灵的update方法
    enemy_group.update()
    # 同精灵组的update方法,需将窗口作为参数传入
    enemy_group.draw(screen)
    pygame.display.update()
# 卸载pygame中模块

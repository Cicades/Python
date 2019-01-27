import pygame
import plane_game_settings as settings
from plane_game_bg import *
from plane_sprite import *


class PlaneGame(object):
    """飞机大战主游戏"""
    def __init__(self):
        """初始化游戏"""
        # 1. 创建游戏窗口
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        # 2. 创建精灵
        self.__create_sprites()
        # 3. 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 4. 设置创建敌机事件定时器
        pygame.time.set_timer(settings.CREATE_ENEMY_EVENT, 1000)
        # 5. hero开火定时器
        pygame.time.set_timer(settings.HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        """创建游戏精灵"""
        bg1 = SpriteBackground('./images/background.png', False)
        bg2 = SpriteBackground('./images/background.png', True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # 敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 英雄精灵
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def __event_process(self):
        """事件处理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.end_game()
            elif event.type == settings.CREATE_ENEMY_EVENT:
                self.enemy_group.add(EnemySprite())
            elif event.type == settings.HERO_FIRE_EVENT:
                self.hero.fire()

        # 获取按键元组(此方式可持续触发按键事件)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            # 向右移动
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        """碰撞检测"""
        # 子弹消灭敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # hero牺牲
        collided_enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(collided_enemies) > 0:
            PlaneGame.end_game()

    def __update_sprites(self):
        """重绘精灵"""
        # 背景刷新
        self.back_group.update()
        self.back_group.draw(self.screen)
        # 敌机刷新
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        # 英雄刷新
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        # 子弹刷新
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    def start_game(self):
        print('游戏开始！')
        # 创建游戏循环
        while True:
            # 1. 设置刷新率
            self.clock.tick(settings.FRAME_PER_SEC)
            # 2. 事件处理
            self.__event_process()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新/绘制精灵
            self.__update_sprites()
            # 5. 刷新窗口
            pygame.display.update()

    @staticmethod
    def end_game():
        print('游戏结束！')
        pygame.quit()
        exit()


if __name__ == '__main__':
    """方便此模块被其他模块调用"""
    plane_game = PlaneGame()
    plane_game.start_game()

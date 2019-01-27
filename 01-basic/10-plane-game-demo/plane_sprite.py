import random
import pygame
import plane_game_settings as settings


class GameSprite(pygame.sprite.Sprite):
    """飞机精灵"""
    def __init__(self, image_name, speed=1):
        """如果一个类不是继承自object类,且重写__init__，那么必须在初始化方法
        中调用父类的初始化方法，以享用父类中一些封装好的方法"""
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.speed = speed
        self.rect = self.image.get_rect()  # 通过image对象可以快创建rect对象，并且其下x，y为0，0，宽高为图片的宽高

    def update(self):
        """重写父类的update方法"""
        self.rect.y += self.speed


class EnemySprite(GameSprite):
    """敌机精灵"""
    def __init__(self):
        super().__init__('./images/enemy1.png')
        self.rect.bottom = 0
        # 1. 速度随机
        self.speed = random.randint(1, 3)
        # 2. 位置随机
        self.rect.x = random.randint(0, settings.SCREEN_SIZE[0] - self.rect.width)

    def update(self):
        super().update()
        # 1. 若果飞机飞出屏幕外就销毁敌机
        if self.rect.y >= settings.SCREEN_SIZE[1]:
            # 将精灵从所有组中删除
            self.kill()


class Hero(GameSprite):
    def __init__(self):
        super().__init__('./images/me1.png', 0)
        self.rect.centerx = settings.SCREEN_SIZE[0] / 2
        self.rect.bottom = settings.SCREEN_SIZE[1] - 120
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.right >= settings.SCREEN_SIZE[0]:
            self.rect.right = settings.SCREEN_SIZE[0]

    def fire(self):
        for i in range(3):
            bullet = Bullet()
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.bottom = self.rect.y - i * 20
            self.bullets.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__('./images/bullet1.png', -2)

    def update(self):
        super().update()
        if self.rect.bottom <= 0:
            self.kill()

    # def __del__(self):
    #     print('子弹销毁')

import plane_sprite
import plane_game_settings as settings


class SpriteBackground(plane_sprite.GameSprite):

    def __init__(self, image_name, alt):
        super().__init__(image_name)
        if alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= settings.SCREEN_SIZE[1]:
            self.rect.y = -self.rect.height

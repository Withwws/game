import pygame

vec = pygame.math.Vector2


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, itemtype, name):
        super().__init__()

        self.ID = itemtype
        self.image = pygame.image.load(name).convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = vec(x, y-17) 
        self.rect.topleft = self.pos

    def update(self,shift):
        self.rect.x += shift

    def render(self, display):
        display.blit(self.image, self.pos)



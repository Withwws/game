import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        #direction = player.status
        # self.image = pygame.Surface((1,1))
        # self.rect = self.image.get_rect(center = player.rect.center)
        
        self.image = pygame.image.load('graphic/magic/slash.png').convert_alpha()
        
        if 'down'in player.status_2:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0,-5))
        elif 'up'in player.status_2:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,5))
        elif 'r'in player.status:
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-10,0))
        else: #'l'in player.status:
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(10,0))
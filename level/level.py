import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice,randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from drop import *

itemGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
class Level():
    def __init__(self):
        #get the display surface
        self.game_paused = False
        self.display_surface = pygame.display.get_surface()
        
        #spirte group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstracle_sprites = pygame.sprite.Group()
     
        #attack sprite
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
     
        #sprite setup
        self.create_map()
        
        #ui
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        
        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        self.endgame_text = 'game over'
        self.gamestatus = True
        self.leader = 0
        
    def create_map(self):
        layouts = { 
            'boundary': import_csv_layout('graphic/tilecsv/map_floor block.csv'),
            'tree': import_csv_layout('graphic/tilecsv/map_tree.csv'),
            'bush': import_csv_layout('graphic/tilecsv/map_bush.csv'),
            'object': import_csv_layout('graphic/tilecsv/map_object.csv'),
            'entities': import_csv_layout('graphic/tilecsv/map_enemy.csv')
        }
        graphics = {
            'bush' : import_folder('graphic/bush'),
            'tree' : import_folder('graphic/tree'),
            'objects' : import_folder('graphic/objects'),
            
        }
        # print(graphics)
        
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstracle_sprites],'invisible')
                        if style == 'bush':
                            #create a bush tile
                            random_bush_image = choice(graphics['bush'])
                            Tile((x,y),[self.visible_sprites,self.attackable_sprites],'bush',random_bush_image)
                        if style == 'tree':
                            #create a tree tile
                            random_tree_image = choice(graphics['tree'])
                            Tile((x,y),[self.visible_sprites],'tree',random_tree_image)
                        if style == 'object':
                            #create a object tile
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstracle_sprites],'object',surf)
                        
                        if style == 'entities':
                            if col == '100':
                                self.player = Player((x,y),[self.visible_sprites],self.obstracle_sprites,self.create_attack,self.destroy_attack,self.create_magic)  
                            else:
                                if col == '299': monster_name = 'bamboo'
                                elif col == '5': monster_name = 'slime'
                                elif col == '0': monster_name = 'bamboobig'
                                elif col == '4': monster_name = 'raccoon'
                                elif col == '2': monster_name = 'spirit'
                                elif col == '3': monster_name = 'squid'
                                enemy = Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],self.obstracle_sprites,self.damage_player,self.trigger_death_particles,self.add_exp,self.add_score)
                                enemyGroup.add(enemy)
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
    
    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
        
        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])
    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprites in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprites,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'bush':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_bush_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprites.sprite_type)
                        
    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])
        if self.player.health <=0: 
            self.endgame_text = 'game over'
            self.gamestatus  = False
        if self.player.score == 7220:
            self.endgame_text = 'congrat!!'
            self.gamestatus  = False
    
    def trigger_death_particles(self,pos,particle_type):
            self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
            
    def add_exp(self,amount):
        self.player.exp += amount
        
    def add_score(self,amount):
        self.player.score += amount
        print(self.player.score)
        self.leader = self.player.score
        
    def export_score(self):
        return self.leader
    
    def toggle_menu(self):
        self.game_paused = not self.game_paused         
            
    def run(self):
        #update and draw the game
         i = 0
         self.visible_sprites.custom_draw(self.player)
         self.ui.display(self.player)
        #  for enemy in enemyGroup:
        #     if enemy.check_death():
        #         self.drop_item(enemy)
        #         i = 1
        #  if i == 1:   
        #     itemGroup.update()
        #     itemGroup.draw(self.display_surface)
         if self.game_paused:
             self.upgrade.display()
         else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            
    # def drop_item(self, enemy):
    #     # rand = randint(1,5)
    #     rand = 1
    #     if rand ==1 :
    #         item = Item(enemy.rect.x, enemy.rect.y, 0, "graphic/test/mana.png")
    #         itemGroup.add(item)
         
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        #creating floor
        self. floor_surf = pygame.image.load('graphic/test/map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        
    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #drawing floor\
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
        enemy_sprites= [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
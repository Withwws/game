import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstracle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('graphic/test/r1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-10,-10)
        
        #graphic setup
        self.import_player_assets()
        self.status_2= ''
        self.status = 'r'
        self.frame_index = 0
        self.animation_speed = 0.15
        
        #movement
        self.speed = 3
        self.attacking = False
        self.attack_cooldown = 500
        self.attack_time = None
        self.obstracle_sprites = obstracle_sprites
        
        #attack
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        
        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.switch_duration_cooldown = 200
        
        #stat
        self.stats = {'health' : 100,'energy' : 60,'attack' : 30,'magic':4,'speed' : 3}
        self.max_stats = {'health': 400, 'energy': 140, 'attack': 150, 'magic' : 10, 'speed': 7}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']
        self.score = 0
        
        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
        
        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)
        
    def import_player_assets(self):
        characters_path = 'graphic/characters/'
        self.animations = {'lstand': [],'rstand': [],'l': [],'r': [],'lattack': [],'rattack': [],'ldied': [],'rdied': []}
        
        for animation in self.animations.keys():
            full_path = characters_path + animation
            self.animations[animation] = import_folder(full_path)
        
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
        
        #movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status_2 = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status_2 = 'down'
            else:
                self.direction.y = 0
        
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'l'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'r'
            else:
                self.direction.x = 0
            
        #attack input
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play() 
            
        #magic input
            if keys[pygame.K_g]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style,strength,cost)
            
            if keys [pygame.K_f] and self.can_switch_magic:
                self.can_switch_magic = False
                self. magic_switch_time = pygame.time.get_ticks()
                
                if self. magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index +=1
                else:
                    self.magic_index = 0
                    
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        
        #set stand status
        if self.direction.x==0 and self.direction.y==0:
            if not 'stand' in self.status and not 'attack' in self.status:
                self.status = self.status + 'stand'
            
                
        if self.direction.x==0 and self.direction.y!=0:
            if 'stand' in self.status and not 'attack' in self.status:
                self.status = self.status.replace('stand', '')
            
        if self.direction.x!=0 and self.direction.y==0:
            if 'up' in self.status_2:
                self.status_2 = self.status_2.replace('up','')
            if 'down' in self.status_2:
                self.status_2 = self.status_2.replace('down','')
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'stand' in self.status:
                    self.status = self.status.replace('stand','attack')
                else:
                    self.status = self.status + 'attack'
            if not 'attack' in self.status_2:
                self.status_2 = self.status_2 + 'attack'
                    
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('attack','')
                 
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
            if current_time - self.attack_time >= 200:
                self.destroy_attack()
                
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
               
    def animate(self):
        animation = self.animations[self.status]
        
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        #flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        return base_damage
        
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]
    
    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.005 * self.stats['magic']
        else:
            self.energy = self.stats['energy']
        
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
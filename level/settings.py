#game set up
WIDTH    = 800
HEIGHT   = 600
FPS      = 60
TILESIZE = 32

#ui
BAR_HEIGHT =20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphic/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'


#weapon
weapon_data = {
    'sword': {'cooldown': 100, 'damage' :15}
}

#magic
magic_data = {
    'flame' : {'strength': 5, 'cost' : 20, 'graphic' : 'graphic/magic/flame/fire.png'},
    'heal'  : {'strength': 20, 'cost' : 10, 'graphic' : 'graphic/magic/heal/heal.png'}
}

#enemies
monster_data = {
    'squid': {'health': 1000,'exp':1000,'damage':50,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 40, 'notice_radius': 180, 'score' :350},
	'raccoon': {'health': 800,'exp':500,'damage':100,'attack_type': 'claw',  'attack_sound':'audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 200, 'score':500},
	'spirit': {'health': 300,'exp':200,'damage':30,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 30, 'notice_radius': 175, 'score':320},	
    'bamboo': {'health': 70,'exp':150,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 25, 'notice_radius': 150, 'score':150},
    'slime': {'health': 50,'exp': 100,'damage':4,'attack_type': 'slash','attack_sound':'audio/attack/slash.wav', 'speed': 2, 'resistance': 3, 'attack_radius':25,'notice_radius':100,'score':100},
    'bamboobig': {'health': 250,'exp':250,'damage':25,'attack_type': 'bigleaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 25, 'notice_radius': 150, 'score':300}
    }

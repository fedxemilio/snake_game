from colors import *

WIDTH, HEIGHT = 600, 400 #make bigger

NORMAL_SPEED = 100
FAST_SPEED = 70

BONUS_PROB = 0.05
BOMB_PROB = 0.25

block_size = 20

direction_map = {
    'UP': (0, -block_size),
    'DOWN': (0, block_size),
    'LEFT': (-block_size, 0),
    'RIGHT': (block_size, 0)
    }

left_turn = {
    'UP': 'LEFT',
    'DOWN': 'RIGHT',
    'LEFT': 'DOWN',
    'RIGHT': 'UP'
    }

right_turn = {
    'UP': 'RIGHT',
    'DOWN': 'LEFT',
    'LEFT': 'UP',
    'RIGHT': 'DOWN'
    }

NEGG_TYPES = [
    {"color": YELLOW, "points": 1, "weight": 80},
    {"color": GREEN, "points": 5, "weight": 12},
    {"color": BLUE_NEGG, "points": 10, "weight": 5},
    {"color": PURPLE, "points": 25, "weight": 2},
    {"color": GREY, "points": 100, "weight": 1},
]

BONUS_NEGGS = [
    {"color": ORANGE, "ability": "clear_bombs"},
    {"color": PINK, "ability": "cut_tail"},
    {"color": CYAN, "ability": "speed_up"},
    {"color": BROWN, "ability": "eat_bombs"}
]  

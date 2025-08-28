from colors import *
from game import Game
from constants import *

game = Game()
while True:
    if game.state == 'playing':
        game.play()
    elif game.state == 'menu':
        game.main_menu()
    elif game.state == 'settings':
        game.settings()
    elif game.state == 'game over':
        game.game_over()
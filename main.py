from colors import *
from game import Game, screen, font, game_over_font, game_over_font2, death_text
from constants import *

game = Game()
while True:
    if game.state == 'playing':
        game.play()
    elif game.state == 'game over':
        game.game_over()

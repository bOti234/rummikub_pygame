import screeninfo
from typing import List, Dict, Tuple, Union, Type
from classes.game import Game
from classes.player import Player


if __name__ == "__main__":
    players: List[Player] = [
        Player("player 1", False),
        Player("player 2", True),
        Player("player 3", True),
        Player("player 4", True),
    ]
    g = Game(
        players, 
        "normal",
        screen_width = screeninfo.get_monitors()[0].width,
        screen_height = screeninfo.get_monitors()[0].height
    )
    g.start()
import screeninfo
from typing import List, Dict, Tuple, Union, Type
from classes.game import Game
from classes.cpu import CPU
from classes.player import Player


if __name__ == "__main__":
    players: List[Union[Player, CPU]] = [
        Player("player 1", False),
        CPU(),
        CPU(),
        CPU(),
    ]
    g = Game(
        players, 
        "normal",
        screen_width = screeninfo.get_monitors()[0].width,
        screen_height = screeninfo.get_monitors()[0].height
    )
    g.start()
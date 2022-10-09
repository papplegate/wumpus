from cmd import Cmd
from dataclasses import dataclass
import readline
from types import MappingProxyType
from typing import (
    Mapping,
    Tuple,
)

# https://en.wikipedia.org/wiki/Hunt_the_Wumpus#/media/File:Hunt_the_Wumpus_map.svg
MAP: Mapping[int, Tuple[int, int, int]] = MappingProxyType(
    {
        1: (2, 5, 8),
        2: (1, 3, 10),
        3: (2, 4, 12),
        4: (3, 5, 14),
        5: (4, 1, 6),
        6: (5, 7, 15),
        7: (6, 8, 17),
        8: (1, 7, 9),
        9: (8, 10, 18),
        10: (2, 9, 11),
        11: (10, 12, 19),
        12: (3, 11, 13),
        13: (12, 14, 20),
        14: (4, 13, 15),
        15: (6, 14, 16),
        16: (15, 17, 20),
        17: (7, 16, 18),
        18: (9, 17, 19),
        19: (11, 18, 20),
        20: (13, 16, 19),
    }
)


@dataclass
class GameState:

    player_location: int = 1


class GameLoop(Cmd):
    def do_move(self, destination: str):

        invalid = f"Invalid destination!  Remaining at {str(state.player_location)}."
        try:
            dest = int(destination)
        except ValueError:
            print(invalid)

        if int(destination) in MAP[state.player_location]:
            print(f"Moving to {str(destination)}.")
            state.player_location = dest
        else:
            print(invalid)

    def do_shoot(self, targets)


if __name__ == "__main__":
    state = GameState()
    GameLoop().cmdloop()

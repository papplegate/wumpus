from collections.abc import Mapping
from cmd import Cmd
from dataclasses import dataclass
import readline
from types import MappingProxyType
from typing import (
    Literal,
    Sequence,
    Union,
)


class CaveMap:
    graph: Mapping[int, tuple[int, int, int]]

    def __init__(self):
        # https://en.wikipedia.org/wiki/Hunt_the_Wumpus#/media/File:Hunt_the_Wumpus_map.svg
        self.graph = MappingProxyType(
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

    def adjacent_caves(self, cave: int) -> tuple[int, int, int]:
        return self.graph[cave]

    def is_adjacent(self, cave1: int, cave2: int) -> bool:
        return cave1 in self.adjacent_caves(cave2)


@dataclass
class GameState:
    status: Literal["PLAY", "WIN", "LOSE"]
    player_cave: int
    arrows: int
    wumpus_cave: int
    pit_caves: list[int]
    bat_caves: list[int]


class GameLoop(Cmd):
    cave_map: CaveMap
    game_state: GameState

    def __init__(self):
        super().__init__()
        self.prompt = ""
        self.cave_map = CaveMap()
        self.game_state = GameState(
            status="PLAYING",
            player_cave=1,
            arrows=5,
            wumpus_cave=20,
            pit_caves=[10, 15],
            bat_caves=[9, 18],
        )
        self.intro = self.status_line()

    def do_quit(self, line) -> bool:
        print("Thanks for playing!")
        return True

    def do_move(self, destination: str):

        invalid = f"You can't reach that cave from here!"
        try:
            safeDestination = int(destination)
        except ValueError:
            print(invalid)

        if safeDestination in self.cave_map.adjacent_caves(self.game_state.player_cave):
            self.game_state.player_cave = safeDestination
            print(self.hazards_in_adjacent_caves())
            self.prompt = self.status_line() + "\n"
        else:
            print(invalid)

    def do_shoot(self, targets): ...
    
    def hazards_in_adjacent_caves(self) -> dict[str, bool]:
        return {
            "wumpus": self.cave_map.is_adjacent(self.game_state.player_cave, self.game_state.wumpus_cave),
            "pit": any(
                self.cave_map.is_adjacent(self.game_state.player_cave, pit_cave)
                for pit_cave in self.game_state.pit_caves
            ),
            "bat": any(
                self.cave_map.is_adjacent(self.game_state.player_cave, bat_cave)
                for bat_cave in self.game_state.bat_caves
            ),
        }

    def status_line(self) -> str:
        messages = [
            f"You are in cave {self.game_state.player_cave}.",
            f"Caves {', '.join([str(cave) for cave in self.cave_map.adjacent_caves(self.game_state.player_cave)])} are nearby.",
        ]
        hazards = self.hazards_in_adjacent_caves()
        if hazards["wumpus"]:
            messages.append("There is a terrible smell here.")
        if hazards["pit"]:
            messages.append("You feel a draft of air.")
        if hazards["bat"]:
            messages.append("There is a faint chittering sound.")
        return "\n".join(messages)

    def result(self, arrow_path: list[int]):
        if self.game_state.player_cave == self.game_state.wumpus_cave:
            self.game_state.status = "LOSE"
            print("You stumble on the Wumpus in the darkness, and it devours you!")


if __name__ == "__main__":
    GameLoop().cmdloop()

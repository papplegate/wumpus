from collections.abc import Mapping
from cmd import Cmd
from dataclasses import dataclass
from random import choice, sample
from textwrap import dedent
from types import MappingProxyType
from typing import (
    Sequence,
    Union,
)

Network = Mapping[int, tuple[int, int, int]]

class CaveMap:
    _network: Network 

    def __init__(self):
        self._network = MappingProxyType(
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

    @property
    def network(self) -> Network:
        return self._network

    def adjacent_caves(self, cave: int) -> tuple[int, int, int]:
        return self.network[cave]

    def is_adjacent(self, caves: tuple[int, Union[int, Sequence[int]]]) -> bool:
        if isinstance(caves[1], int):
            return caves[1] in self.adjacent_caves(caves[0])

        # recursion
        return any(self.is_adjacent((caves[0], cave)) for cave in caves[1])


@dataclass
class GameState:
    player_cave: int
    wumpus_cave: int
    pit_caves: list[int]
    bat_caves: list[int]
    playing: bool = True
    arrows: int = 5


class GameLoop(Cmd):
    cave_map: CaveMap
    game_state: GameState

    def __init__(self):
        super().__init__()
        self.prompt = ""
        self.cave_map = CaveMap()
        self.game_state = GameState(**self.occupied_caves())
        self.intro = (
            "\n".join(
                [
                    "Welcome to the Wumpus Caves!",
                    "Type help for help.\n",
                ]
            )
            + self.status_line()
        )

    def occupied_caves(self) -> dict[str, Union[int, list[int]]]:
        unoccupied_caves = list(self.cave_map.network.keys())

        player_cave = choice(unoccupied_caves)
        unoccupied_caves.remove(player_cave)

        for cave in self.cave_map.adjacent_caves(player_cave):
            unoccupied_caves.remove(cave)

        wumpus_cave = choice(unoccupied_caves)
        unoccupied_caves.remove(wumpus_cave)

        pit_caves = sample(unoccupied_caves, 2)
        for cave in pit_caves:
            unoccupied_caves.remove(cave)

        bat_caves = sample(unoccupied_caves, 2)

        return {
            "player_cave": player_cave,
            "wumpus_cave": wumpus_cave,
            "pit_caves": pit_caves,
            "bat_caves": bat_caves,
        }

    def hazards_in_adjacent_caves(self) -> dict[str, bool]:
        return {
            "wumpus": self.cave_map.is_adjacent(
                (self.game_state.player_cave, self.game_state.wumpus_cave)
            ),
            "pit": self.cave_map.is_adjacent(
                (self.game_state.player_cave, self.game_state.pit_caves)
            ),
            "bat": self.cave_map.is_adjacent(
                (self.game_state.player_cave, self.game_state.bat_caves)
            ),
        }

    def status_line(self) -> str:
        messages = [
            f"You are in cave {self.game_state.player_cave}.",
            f"Caves {', '.join([str(cave) for cave in self.cave_map.adjacent_caves(self.game_state.player_cave)])} are nearby.",
        ]
        hazards = self.hazards_in_adjacent_caves()
        if hazards["wumpus"]:
            messages.append("You smell the Wumpus.")
        if hazards["pit"]:
            messages.append("You feel a draft of air from a nearby pit.")
        if hazards["bat"]:
            messages.append("You hear the faint chittering sound of a bat.")
        messages.extend(
            [
                f"You have {self.game_state.arrows} arrows.",
                "Your move?",
            ]
        )
        return "\n".join(messages)

    def do_help(self, arg):
        if not arg:
            print(
                dedent(
                    """
                Somewhere out there, in the darkness, is the Wumpus --
                a creature no one has ever seen.  Will your crooked arrows
                find the Wumpus before it catches you?

                Move from cave to cave, looking for the Wumpus' hiding place
                and avoiding bats and pits.

                When you've found the Wumpus' cave, shoot a crooked arrow
                toward that cave.  Aim carefully!

                Win by hitting the Wumpus with a crooked arrow.
                Lose by falling into a pit, hitting yourself with an arrow,
                or running out of arrows (you start with five).
            """
                )
            )
        super().do_help(arg)

    def help_move(self):
        print(
            dedent(
                """
            Move to an adjacent cave.  For example, "move 2" moves to cave
            2 if it is adjacent to the current cave. 
        """
            )
        )

    def help_shoot(self):
        print(
            dedent(
                """
            Shoot a crooked arrow through up to five connected caves,
            starting at any cave adjacent to your current position.  For
            example, "shoot 1 2 3 4 5" shoots an arrow through caves 1-5,
            assuming that those caves connect to each other and that cave 1
            is adjacent to your current position.

            Pay attention to how the caves are arranged -- if you try to
            shoot into a cave that doesn't connect, your arrow will go
            wild, and it could even hit you!
        """
            )
        )

    def help_quit(self):
        print("Quits the game.")

    def do_quit(self, line):
        self.game_state.playing = False

    def do_move(self, destination: str):
        try:
            safe_destination = int(destination)
        except ValueError:
            print("Please enter a valid cave.")
            return

        if safe_destination not in self.cave_map.adjacent_caves(
            self.game_state.player_cave
        ):
            print(f"You can't reach cave {destination} from here!")
            return

        self.game_state.player_cave = safe_destination

    def player_turn_result(self):
        if self.game_state.player_cave in self.game_state.bat_caves:
            new_player_cave = choice(self.cave_map.network)
            self.game_state.bat_caves.remove(self.game_state.player_cave)
            self.game_state.bat_caves.append(
                choice(self.cave_map.adjacent_caves(new_player_cave))
            )
            self.game_state.player_cave = new_player_cave
            print(f"A bat picks you up and drops you in cave {new_player_cave}!")
            # recursion
            self.player_turn_result()
        if self.game_state.player_cave in self.game_state.pit_caves:
            print("You fall into a pit!")
            self.game_state.playing = False
            return
        if self.game_state.player_cave == self.game_state.wumpus_cave:
            self.game_state.playing = False
            print("You stumble on the Wumpus in the darkness, and it devours you!")
        if self.game_state.arrows < 1:
            self.game_state.playing = False
            print("You have no more arrows and no defense against the Wumpus.")

    def do_shoot(self, target_caves: str):
        arrow_path = [self.game_state.player_cave]
        for target_cave in target_caves.replace(",", "").split()[:5]:
            try:
                safe_target_cave = int(target_cave)
            except ValueError:
                print("Please enter valid, space-separated target caves.")
                return

            possible_target_caves = list(self.cave_map.adjacent_caves(arrow_path[-1]))
            if len(arrow_path) > 1:
                # arrow shouldn't go back the way it came
                possible_target_caves.remove(arrow_path[-2])
            if safe_target_cave in possible_target_caves:
                arrow_path.append(safe_target_cave)
                continue

            print(f"Cave {safe_target_cave} does not connect to cave {arrow_path[-1]}.")
            arrow_path.append(choice(possible_target_caves))

        print(
            f"The arrow flies through cave{'s' if len(arrow_path[1:]) > 1 else ''} {', '.join([str(cave) for cave in arrow_path[1:]])}!"
        )

        if self.game_state.wumpus_cave in arrow_path[1:]:
            print("The Wumpus is struck by an arrow!")
            self.game_state.playing = False
            return
        if self.game_state.player_cave == arrow_path[1:]:
            print("You are struck by your own arrow!")
            self.game_state.playing = False
            return

        print("The Wumpus roars as it moves to another cave!")
        self.game_state.wumpus_cave = choice(
            self.cave_map.adjacent_caves(self.game_state.wumpus_cave)
        )

        self.game_state.arrows -= 1

    def postcmd(self, stop, line):
        self.player_turn_result()
        if not self.game_state.playing:
            print("Thanks for playing!")
            return True
        self.prompt = self.status_line() + "\n"


if __name__ == "__main__":
    GameLoop().cmdloop()

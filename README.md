# Hunt the Wumpus

## Introduction

This project reimplements the classic Hunt the Wumpus game in Python.  Hunt the Wumpus comes to us from the era when computer games were typed in by hand from books or sent in the mail on cassettes.

In Hunt the Wumpus, you play a hunter who seeks to kill a creature called the Wumpus with your arrows.  You move from room to room within a cave system, looking for traces of the Wumpus and avoiding hazards.  The rooms are arranged like the vertices on a dodecahedron (a 20-sided solid) and connected by the dodecahedron's edges.  Thus, each room connects to three others.  Besides the Wumpus, the hazards include pits and bats, which will pick you up and drop you in a different cave.  You win if you shoot an arrow through the caves such that it strikes the Wumpus; you lose if you stumble across the Wumpus, fall down a pit, shoot yourself with your own arrow, or run out of arrows. 

## Dependencies

Only a reasonably recent copy of Python 3 is needed to play.  The code was written using Python 3.11.2, but most copies of Python 3.x should also work.  Python 2 is not supported.

## Running the code

Navigate to the directory where the `wumpus.py` file is located and run `python -m wumpus`.

## How to play

On each turn, the game displays
* what cave you are located in,
* the caves to which you can move,
* whether there are hazards in adjacent caves, and
* how many arrows you have.

You then enter a command to interact with the game world.  Commands include `help`, `move`, and `shoot`.  `help` displays a list of commands or, if entered with the name of another command, gives help on that command.  `move` lets you move to an adjacent cave, and `shoot` fires an arrow through up to five connected caves.

## Strategy

Move from cave to cave, avoiding the pits and bats.  When you smell the Wumpus, note the two caves that you haven't visited that adjoin your current cave.  Back up and search further until you smell the Wumpus in another cave that connects to one of the two candidate Wumpus nests.  Fire an arrow into that cave and enjoy your victory.  To my knowledge, this strategy always works, unless the hazards are very unfavorably arranged.

Alternatively, fire your arrows and hope to hit the Wumpus.  This strategy works best if you map out which caves are connected to each other over several playthroughs.  The hunter's starting position varies between games, but the arrangement of the caves does not. 

## Differences from the original game

* No hazards are placed in caves adjacent to the hunter's starting position.
* Arrows can't turn around and go back to the cave they came from.
* Bats roost in a cave adjacent to the hunter's new position after moving the hunter, rather than returning to their original cave. 
* The Wumpus always kills the hunter when the hunter enters its cave.

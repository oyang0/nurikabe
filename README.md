# Nurarihyon

This is Nurarihyon, a Battlesnake implemented in Python. It's deployed with [Replit](https://repl.it).

## Technologies Used

* [Python3](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)


## Profile

* [Daedalean](https://play.battlesnake.com/u/daedalean/)

---

## Customizations

Nurarihyon presently uses these settings for personalizing its appearance:

```python
return {
    "apiversion": "1",
    "author": "daedalean",
    "color": "#3E338F",
    "head": "pixel",
    "tail": "pixel",
    "version": "0.0.1-beta",
}

```

## Behavior

On every turn of each game, Nurarihyon first removes moves that move Nurarihyon back on its own neck, hit walls, hit itself, and collide with others from possibility. If all moves are removed from possibility, then Nurarihyon moves up. Otherwise, Nurarihyon uses flood fill to assign each move not removed from possibility a score. The score is calculated by first calculating the enclosed space a move moves towards, then assigning all squares in the enclosed space points: empty squares are assigned 1 point, hazard squares are assigned 1/16 points, and food squares are assigned 1 more than the amount of health Nurarihyon would restore if it consumed food now. The score is the sum of all points. Nurarihyon then selects the move with the greatest score.

# Nurikabe

This is Nurikabe, a Battlesnake implemented in Python. It's deployed with [Replit](https://repl.it).

## Technologies Used

* [Python3](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)


## Profile

* [Daedalean](https://play.battlesnake.com/u/daedalean/)

---

## Customizations

Nurikabe presently uses these settings for personalizing its appearance:

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

On every turn of each game, Nurikabe first removes moves that move Nurikabe back on its own neck, hit walls, hit itself, and collide with others from possibility. If all moves are removed from possibility, then Nurikabe moves up. Otherwise, Nurikabe selects a random move.

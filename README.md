# LIDL MINESWEEPER

This is a very scuffed, very bad implementation of minesweeper. However, this project's intention is not to make the best minesweeper there is, but to try the so called `functional core imperative shell` "architecture" that I learned from Gary Bernhardt's talks. This project tries to mimic as close as possible to the concept. 

The functional core part is just data of states and pure functions that take a state and return a new state. You can find it in `states.py` and `cell.py`. The imperative shell is in the `main` program. The plan was to make the shell as small as possible, but apparently due to time constraints and tinkering with tkinter, it ended up being really messy. Definitely need some rework.

### Instructions to run it

Just run `main.py` lol
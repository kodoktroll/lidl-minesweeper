from dataclasses import dataclass
from typing import List
import cell as c
import random

@dataclass
class GameState:
    board: List[List[c.Cell]]
    is_over: bool

    def open_at(self, x, y): 
        # mutate ga bisa pake [x][y] soalnya ternyata ngubah 
        # value sebelumnya. jadi terpaksa dibikin gini
        if(x >= 0 and x < len(self.board)):
            if(y >= 0 and y < len(self.board[0])):
                curr_cell = self.board[x][y]
                if(curr_cell.is_open or curr_cell.is_flagged):
                    # don't change anything if already open
                    return self.do_nothing()
                else:
                    if(isinstance(curr_cell, c.NotBomb)):
                        if(curr_cell.bomb_count != 0):
                            return self.just_open(x, y)
                        else:
                            return self.when_zero(x, y)
                    else:
                        return self.when_bomb(x, y)
        return self.do_nothing()
    
    def open_around(self, x, y):
        this_cell = self.get_cell_at(x, y)
        if(isinstance(this_cell, c.NotBomb)):
            neighbor_cells = [self.get_cell_at(x+i, y+j) for i in range(-1,2) for j in range(-1,2) \
                                if (i,j) != (0,0) and (x+i) >= 0 and (x+i) < len(self.board) and \
                                (y+j) >= 0 and (y+j) < len(self.board[i])] 
            flags_cells = map(lambda grid: grid.is_flagged, neighbor_cells)
            only_flags = list(filter(lambda x: x == True, flags_cells))
            if(this_cell.bomb_count == len(only_flags)):
                new_state = self
                # print(neighbor_cells)
                for i in neighbor_cells:
                    (x_,y_) = i.coord
                    new_state = new_state.open_at(x_, y_)
                return new_state
            return self.do_nothing()
        return self.do_nothing()

    def when_zero(self, x, y):
        open_zero = self.just_open(x, y)

        open_top_left = open_zero.open_at(x-1, y-1)
        open_top = open_top_left.open_at(x-1,y)
        open_top_right = open_top.open_at(x-1,y+1)

        open_mid_left = open_top_right.open_at(x, y-1)
        open_mid_right = open_mid_left.open_at(x,y+1)

        open_bot_left = open_mid_right.open_at(x+1, y-1)
        open_bot = open_bot_left.open_at(x+1,y)
        open_bot_right = open_bot.open_at(x+1,y+1)

        res = open_bot_right
        return res

    def just_open(self, x, y):
        #saat bukan 0, maka cuma buka aja.
        newboard = list(self.board)
        cell = newboard[x][y]
        newcell = cell.toggle_cell_open()
        newboard[x] = newboard[x][:y] + [newcell] + newboard[x][y+1:]
        return self.update_board(newboard)
        # return GameState(self.board, self.is_over)

    def flag_at(self, x, y):
        #saat bukan 0, maka cuma buka aja.
        newboard = list(self.board)
        cell = newboard[x][y]
        newcell = cell.toggle_cell_flag()
        newboard[x] = newboard[x][:y] + [newcell] + newboard[x][y+1:]
        return self.update_board(newboard)
        # return GameState(self.board, self.is_over)

    def get_cell_at(self, x, y):
        return self.board[x][y]

    def update_cell(self, x, y, f):
        if(x >= 0 and x < len(self.board)):
            if(y >= 0 and y < len(self.board[0])):
                #saat bukan 0, maka cuma buka aja.
                newboard = list(self.board)
                cell = newboard[x][y]
                newcell = f(cell)
                newboard[x] = newboard[x][:y] + [newcell] + newboard[x][y+1:]
                return self.update_board(newboard)
                # return GameState(self.board, self.is_over)
        return self.do_nothing()
    
    def swap_bomb_at(self, x, y):
        return self.update_cell(x, y, lambda cell: c.swap_to_bomb(cell))

    def increment_bomb_count_at(self, x, y):
        return self.update_cell(x, y, lambda cell: c.increment_bomb_count(cell))

    def increment_bomb_count_around(self, x, y):
        update_top = self.increment_bomb_count_at(x-1, y-1) \
                         .increment_bomb_count_at(x-1, y) \
                         .increment_bomb_count_at(x-1, y+1)

        update_mid = update_top.increment_bomb_count_at(x, y-1) \
                               .increment_bomb_count_at(x, y+1) 

        update_bot = update_mid.increment_bomb_count_at(x+1, y-1) \
                               .increment_bomb_count_at(x+1, y) \
                               .increment_bomb_count_at(x+1, y+1) 
        return update_bot

    def update_board(self, newboard):
        return GameState(newboard, self.is_over)

    def do_nothing(self):
        return GameState(self.board, self.is_over)

    def when_bomb(self, x, y): 
        #saat bomb, maka ubah jadi game over.
        newgame = self.just_open(x, y)
        newgame_ = newgame.toggle_is_over()
        return newgame_

    def toggle_is_over(self):
        return GameState(self.board, not self.is_over)
    
    def toggle_over_if_win(self):
        non_bombs = [j for i in range(len(self.board)) for j in self.board[i] if isinstance(j, c.NotBomb)]
        has_been_opened = [j for i in range(len(self.board)) for j in self.board[i] if isinstance(j, c.NotBomb) and j.is_open]
        if(len(non_bombs) == len(has_been_opened)):
            win_state = self.toggle_is_over()
            return win_state
        return self.do_nothing()

    def is_won(self):
        non_bombs = [j for i in range(len(self.board)) for j in self.board[i] if isinstance(j, c.NotBomb)]
        has_been_opened = [j for i in range(len(self.board)) for j in self.board[i] if isinstance(j, c.NotBomb) and j.is_open]
        return self.is_over and len(non_bombs) == len(has_been_opened)

def generate_initial_game_state(height, width):
    board = [[c.NotBomb((x, y), False, False, 0) for y in range(width)] for x in range(height)]
    return GameState(board, False)

def generate_bomb_after_first_move(game_state, first_coord, total_bombs, height, width):
    bomb_coords = [first_coord]
    curr_game = game_state
    while len(bomb_coords) < total_bombs+1:
        coord = (random.randrange(height), random.randrange(width))
        if(coord not in bomb_coords):
            (x, y) = coord
            bomb_coords.append(coord)
            newgame = curr_game.swap_bomb_at(x,y)
            newgame_ = newgame.increment_bomb_count_around(x, y)
            curr_game = newgame_
    (x,y) = first_coord
    return curr_game.open_at(x,y)
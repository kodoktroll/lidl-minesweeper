from dataclasses import dataclass

@dataclass(frozen=True)
class Cell:
    coord: (int, int)
    is_flagged: bool
    is_open: bool
    def toggle_cell_flag(self):
        pass
    def toggle_cell_open(self):
        pass
    def open_at(self, x, y):
        pass
    

@dataclass(frozen=True)
class Bomb(Cell):
    def toggle_cell_flag(self):
        return Bomb(self.coord, not self.is_flagged, self.is_open)
    def toggle_cell_open(self):
        return Bomb(self.coord, self.is_flagged, not self.is_open)
    def open_at(self, x, y):
        selfX, selfY = self.coord
        if(selfX == x and selfY == y):
            return self.toggle_cell_open()
        return self

@dataclass(frozen=True)
class NotBomb(Cell):
    bomb_count: int
    def toggle_cell_flag(self):
        return NotBomb(self.coord, not self.is_flagged, self.is_open, self.bomb_count)
    
    def toggle_cell_open(self):
        return NotBomb(self.coord, self.is_flagged, not self.is_open, self.bomb_count)

    def open_at(self, x, y):
        selfX, selfY = self.coord
        if(selfX == x and selfY == y):
            return self.toggle_cell_open()
        return self

    def increment_bomb_count(self):
        return NotBomb(self.coord, self.is_flagged, self.is_open, self.bomb_count + 1)

def swap_to_bomb(cell):
    if(isinstance(cell, NotBomb)):
        return Bomb(cell.coord, False, False)
    else:
        return cell

def increment_bomb_count(cell):
    if(isinstance(cell, NotBomb)):
        return cell.increment_bomb_count()
    else:
        return cell

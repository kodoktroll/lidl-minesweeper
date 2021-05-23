from dataclasses import dataclass
import state
import tkinter as tk
from tkinter import messagebox as mb
import cell as c
import random

# @dataclass
class Game:
    height: int
    width: int
    game_state: state.GameState
    canvas: tk.Canvas
    frame: tk.Frame
    main_window: tk.Tk
    first_move: bool
    def __init__(self, height, width, game_state, canvas, main_window, first_move):
        self.height = height
        self.width = width
        self.game_state = game_state
        self.main_window = main_window
        self.frame = tk.Frame(main_window)
        self.canvas = tk.Canvas(self.frame)
        self.canvas.grid(row=1, column=0)
        self.frame.grid()
        # lf.frame.pack()
        self.first_move = first_move
        self.render_board()

    def generate_canvas_from_board(self):
        blank_image = tk.PhotoImage()
        board = self.game_state.board
        new_canvas = tk.Canvas(self.frame)
        for i in range(self.height):
            for j in range(self.width):
                if(not board[i][j].is_open):
                    #TODO: attach command to button (buat flag and stuff)
                    button = tk.Button(master=new_canvas, image=blank_image, height=12, width=12)
                    button.grid(row=i, column=j)
                    button['command'] = lambda x=i, y=j: self.handle_open_grid(x, y)
                else:
                    opened = tk.Canvas(master=new_canvas, height=12, width=12)
                    opened.grid(row=i, column=j)
        # new_canvas.grid(row=1,column=0)
        return new_canvas

    def render_board(self):
        blank_image = tk.PhotoImage()
        flag_image = tk.PhotoImage(file="flag.png")
        board = self.game_state.board
        new_canvas = tk.Canvas(self.frame)

        for i in range(self.height):
            for j in range(self.width):
                if(not board[i][j].is_open):
                    #TODO: attach command to button (buat flag and stuff)
                    if(not board[i][j].is_flagged):
                        button = tk.Button(master=new_canvas, image=blank_image, height=12, width=12)
                        button['command'] = lambda x=i, y=j: self.handle_open_grid(x, y)
                    else:
                        button = tk.Button(master=new_canvas, image=flag_image, height=12, width=12)
                    button.grid(row=i, column=j)
                    # button['command'] = lambda x=i, y=j: self.handle_open_grid(x, y)
                    button.bind("<Button-2>", lambda event, x=i, y=j: self.handle_flag(x,y))
                    button.bind("<Button-3>", lambda event, x=i, y=j: self.handle_flag(x,y))
                else:
                    curr_grid = self.game_state.board[i][j]
                    if(isinstance(curr_grid, c.NotBomb) and curr_grid.bomb_count > 0):
                        opened = tk.Label(master=new_canvas, bg="#DDDDDD", image=blank_image,height=12, width=12, text=str(curr_grid.bomb_count), compound="center")
                        opened.config(font=('Times new Roman', 8))
                    else:
                        opened = tk.Label(master=new_canvas, bg="#DDDDDD", image=blank_image,height=12, width=12)
                    # opened.create_line(0,0,15,0,15,15,0,15,0,0)
                    # opened.create_rectangle(0, 0, 18, 18)
                    opened.grid(row=i, column=j)
                    # opened.create_text(100, 10, fill="blue", font="Times 12", text=str(self.game_state.board[i][j].bomb_count))
        old_canvas = self.canvas
        old_canvas.destroy()
        # new_canvas = self.generate_canvas_from_board()
        self.canvas = new_canvas
        new_canvas.grid()
        if(self.game_state.is_over):
            if(not self.game_state.is_won()):
                if mb.askyesno(title="Game is over", message="You lost, Try again?"):
                    self.main_window.destroy()
                    main()
                else:
                    self.main_window.destroy()
            else:
                if mb.askyesno(title="Game is over", message="You won, Try again?"):
                    self.main_window.destroy()
                    main()
                else:
                    self.main_window.destroy()
        # self.canvas.pack()
        self.run()
    
    def handle_open_grid(self, x, y):
        new_state = self.game_state
        if(self.first_move):
            new_state = state.generate_bomb_after_first_move(self.game_state, (x,y), 4, self.height, self.width)
            self.first_move = False
        else:
            open_at = self.game_state.open_at(x,y)
            new_state = open_at.toggle_over_if_win()
        self.game_state = new_state
        self.render_board()
    
    def handle_flag(self, x, y):
        if(not self.first_move):
            curr_state = self.game_state
            new_state = curr_state.flag_at(x, y)
            self.game_state = new_state
            self.render_board()

    
    def run(self):
        self.main_window.mainloop()

class MainApp(tk.Frame):
    height: int
    width: int
    game_state: state.GameState
    def __init__(self, parent, height, width, total_bombs, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.game_state = state.generate_initial_game_state(height, width)
        self.height = height
        self.width = width
        self.total_bombs = total_bombs
        self.remaining_bombs = total_bombs
        self.current_time = 0

        self.mine_sweeper_label = tk.Label(self, text="0")
        self.remaining_bombs_label = tk.Label(self, text="Sisa bom: {}".format(self.remaining_bombs))
        self.first_move = True

        self.frame_board = tk.Frame(self)
        self.frame_indicator = tk.Frame(self)

        self.mine_sweeper_label = tk.Label(self.frame_indicator, text=self.current_time)
        self.remaining_bombs_label = tk.Label(self.frame_indicator, text="Sisa bom: {}".format(self.remaining_bombs))

        self.dummyImage = tk.PhotoImage()
        self.flagImage = tk.PhotoImage(file="flag.png")
        self.grid_widget = [[None for j in range(self.width)] for i in range(self.height)]
        print(len(self.grid_widget), self.height)
        print(len(self.grid_widget[0]), self.width)
        self.init_grids()
        # self.button = tk.Button(self, image=self.dummyImage, height=5, width=5, command=self.ubah_label)

        self.time_identifier = self.mine_sweeper_label.after(1000, self.increment_time(self.current_time))

        self.mine_sweeper_label.pack(side=tk.RIGHT)
        self.remaining_bombs_label.pack(side=tk.LEFT)
        self.frame_indicator.pack(fill=tk.BOTH)

        self.frame_board.pack()
        # self.button.pack()
        self.pack()

    def init_grids(self):
        if(len(self.grid_widget) > 0):
            [widget.destroy() for i in range(len(self.grid_widget)) for widget in self.grid_widget[i]  if widget is not None]
        for i in range(self.height):
            for j in range(self.width):
                button = tk.Button(self.frame_board, image=self.dummyImage, height=16, width=16)
                button.grid(row=i, column=j)
                button['command'] = lambda x=i, y=j: self.handle_grid(x, y)
                button.bind("<Button-2>", lambda event, x=i, y=j: self.handle_flag(x,y))
                button.bind("<Button-3>", lambda event, x=i, y=j: self.handle_flag(x,y))
                self.grid_widget[i][j] = button


    def handle_grid(self, x, y):
        old_state = self.game_state
        new_state = self.game_state
        if(self.first_move):
            first_move_state = state.generate_bomb_after_first_move(self.game_state, (x,y), self.total_bombs, self.height, self.width)
            new_state = first_move_state.toggle_over_if_win()
            self.first_move = False
        else:
            open_at = self.game_state.open_at(x, y)
            toggle_win = open_at.toggle_over_if_win()
            new_state = toggle_win
        diffs = [j for i in range(len(new_state.board)) for j in new_state.board[i] if j not in old_state.board[i]]
        get_coords = map(lambda cell: cell.coord, diffs)
        self.game_state = new_state
        for i in get_coords:
            (x, y) = i
            print(i)
            self.render_cells_on_board(x, y)
        if(self.game_state.is_over):
            self.handle_over()
        
    def handle_open_around(self, x, y):
        old_state = self.game_state
        new_state = self.game_state
        open_at = self.game_state.open_around(x, y)
        toggle_win = open_at.toggle_over_if_win()
        new_state = toggle_win
        diffs = [j for i in range(len(new_state.board)) for j in new_state.board[i] if j not in old_state.board[i]]
        get_coords = map(lambda cell: cell.coord, diffs)
        self.game_state = new_state
        for i in get_coords:
            (x, y) = i
            self.render_cells_on_board(x, y)
        if(self.game_state.is_over):
            self.handle_over()


    def handle_flag(self, x, y):
        old_state = self.game_state
        new_state = self.game_state
        if(not self.first_move):
            curr = self.game_state.board[x][y]
            if(curr.is_flagged):
                self.remaining_bombs += 1
                flag_at = self.game_state.flag_at(x,y)
                new_state = flag_at
            elif(self.remaining_bombs <= 0):
                new_state = self.game_state.do_nothing()
            else:
                self.remaining_bombs -= 1
                flag_at = self.game_state.flag_at(x,y)
                new_state = flag_at
            self.remaining_bombs_label["text"] = "Sisa bom: {}".format(self.remaining_bombs)
        diffs = [j for i in range(len(new_state.board)) for j in new_state.board[i] if j not in old_state.board[i]]
        get_coords = map(lambda cell: cell.coord, diffs)
        self.game_state = new_state
        for i in get_coords:
            (x, y) = i
            self.render_cells_on_board(x, y)
    
    def render_cells_on_board(self, x, y):
        curr_grid = self.game_state.board[x][y]
        old_widget = self.grid_widget[x][y]
        # new_widget = None
        if(curr_grid.is_open):
            if(isinstance(curr_grid, c.NotBomb) and curr_grid.bomb_count > 0):
                opened = tk.Label(master=self.frame_board, bg="#DDDDDD", image=self.dummyImage,height=16, width=16, text=str(curr_grid.bomb_count), compound="center")
                opened.config(font=('Times new Roman', 8))
                opened.grid(row=x, column=y)
                opened.bind('<Double-Button-1>', lambda event, x=x, y=y: self.handle_open_around(x, y))
            else:
                opened = tk.Label(master=self.frame_board, bg="#DDDDDD", image=self.dummyImage,height=16, width=16, text="", compound="center", relief="flat")
                opened.grid(row=x, column=y)
            new_widget = opened
        else:
            if(curr_grid.is_flagged):
                button = tk.Button(master=self.frame_board, image=self.flagImage, height=16, width=16)
            else:
                button = tk.Button(master=self.frame_board, image=self.dummyImage, height=16, width=16)
                button['command'] = lambda x=x, y=y: self.handle_grid(x, y)
            button.grid(row=x, column=y)
            button.bind("<Button-2>", lambda event, x=x, y=y: self.handle_flag(x,y))
            button.bind("<Button-3>", lambda event, x=x, y=y: self.handle_flag(x,y))
            new_widget = button
        self.grid_widget[x][y] = new_widget
        old_widget.destroy()
    
    def handle_over(self):
        self.mine_sweeper_label.after_cancel(self.time_identifier)
        if(self.game_state.is_won()):
            if(mb.askyesno(title="You Won!", 
                           message="Congratulations, you finished the game in {} seconds! Try again?"\
                               .format(self.current_time))):
                self.reset()
            else:
                self.parent.destroy()
        else:
            if(mb.askyesno(title="You Lost!", message="You lost! Try again?")):
                self.reset()
            else:
                self.parent.destroy()

    def reset(self):
        self.game_state = state.generate_initial_game_state(self.height, self.width)
        self.current_time = 0
        self.remaining_bombs = self.total_bombs
        self.update_remaining_bomb_label()
        self.first_move = True
        self.time_identifier = self.mine_sweeper_label.after(1000, self.increment_time(self.current_time))
        self.init_grids()

    def update_remaining_bomb_label(self):
        self.remaining_bombs_label['text'] = "Sisa bom: {}".format(self.remaining_bombs)

    
    def ubah_label(self, x, y):
        self.mine_sweeper_label["text"] = "aku row ke {} column ke {}".format(x, y)

    def increment_time(self, curr):
        self.current_time += 1
        self.mine_sweeper_label["text"] = str(self.current_time)
        self.time_identifier = self.mine_sweeper_label.after(1000, lambda curr=self.current_time: self.increment_time(curr))


def prompt_mode():

    window = tk.Tk()
    var = tk.StringVar(value="Easy")

    difficulty_placeholder = tk.Frame(window)

    easy = tk.Radiobutton(difficulty_placeholder, text="EZ", variable=var, value="Easy", anchor='w')
    medium = tk.Radiobutton(difficulty_placeholder, text="Medium", variable=var, value="Medium", anchor="w")
    hard = tk.Radiobutton(difficulty_placeholder, text="Hard", variable=var, value="Hard", anchor="w")

    custom_placeholder = tk.Frame(window)

    entries_placeholder = tk.Frame(custom_placeholder)

    height_placeholder = tk.Frame(entries_placeholder)
    height_label = tk.Label(height_placeholder, text="Height")
    height = tk.Entry(height_placeholder, width="10")

    width_placeholder=tk.Frame(entries_placeholder)
    width_label = tk.Label(width_placeholder, text="Width")
    width = tk.Entry(width_placeholder, width="10")

    bombs_placeholder=tk.Frame(entries_placeholder)
    bombs_label = tk.Label(bombs_placeholder, text="Bombs")
    bombs = tk.Entry(bombs_placeholder, width="10")

    custom = tk.Radiobutton(custom_placeholder, text="Custom", variable=var, value="Custom")

    submit_button = tk.Button(window, text="Submit")
    submit_button['command'] = lambda master=window, val=var, height=height, width=width, bombs=bombs: handle_prompt(master, val, height, width, bombs)

    easy.pack(side=tk.LEFT)
    medium.pack(side=tk.LEFT)
    hard.pack(side=tk.LEFT)

    height_label.pack(side=tk.LEFT)
    width_label.pack(side=tk.LEFT)
    bombs_label.pack(side=tk.LEFT)

    height.pack(side=tk.RIGHT)
    width.pack(side=tk.RIGHT)
    bombs.pack(side=tk.RIGHT)

    height_placeholder.pack(fill=tk.BOTH)
    width_placeholder.pack(fill=tk.BOTH)
    bombs_placeholder.pack(fill=tk.BOTH)

    entries_placeholder.pack(side=tk.RIGHT)
    custom.pack(side=tk.LEFT)

    difficulty_placeholder.pack(fill=tk.BOTH, pady=10)
    custom_placeholder.pack(fill=tk.BOTH, pady=10)
    submit_button.pack(pady=10)

    window.mainloop()

def handle_prompt(master, var, height, width, bombs):
    if(var.get() in diff_config):
        master.destroy()
        config = diff_config[var.get()]
        (h, w, b) = config["height"], config["width"], config["total_bombs"]
        run_game(h, w, b)
    else:
        try:
            int_height = int(height.get())
            int_width = int(width.get())
            int_bombs = int(bombs.get())
            if(int_bombs < int_height * int_width and int_height <= 40 and int_height > 0\
                and int_width <= 40 and int_width > 0):
                master.destroy()
                run_game(int_height, int_width, int_bombs)
            else:
                raise Exception("Too many bombs")
        except Exception as e:
            mb.showerror(title="Error!", message="Error found: {}".format(str(e)))
    
diff_config = {"Easy": {"height": 8, "width":10, "total_bombs":10}
             , "Medium": {"height": 14, "width": 18, "total_bombs": 40}
             , "Hard": {"height": 20, "width": 24, "total_bombs": 80}
             }

def run_game(height, width, bombs):
    window = tk.Tk()
    window.title("minesweeper")
    MainApp(window, height, width, bombs).pack(side="top", fill="both", expand=True)
    window.mainloop()

def main():
    # height = 32
    # width = 32
    prompt_mode()
    # height = 10 
    # width = 10 
    # total_bombs = 15
    # window = tk.Tk()
    # window.title("minesweeper")
    # MainApp(window, height, width, total_bombs).pack(side="top", fill="both", expand=True)
    # canvas = tk.Canvas(window)
    # game = Game(10, 10, new_game_state, canvas, window, True)
    # game.render_board()
    # window.mainloop()
    # game.run()
    # window.mainloop()
    # blank_image = tk.PhotoImage()
    # for i in range(10):
    #     for j in range(10):
    #         button = tk.Button(master=canvas, image=blank_image, height=12, width=12)
    #         button.grid(row=i, column=j)
    #         button['command'] = lambda master=canvas, i=i, j=j : tk.Canvas(master=master, height=12, width=12).grid(row=i, column=j)
    # canvas.pack()
    # window.mainloop()

if __name__ == "__main__":
    main()
import BreachForce
import tkinter as tk


class CodeBox(tk.OptionMenu):
    SEGS = ['  ', 'BD', '55', '1C', '7A', 'E9']

    def __init__(self, master, *args, **kwargs):
        var = tk.StringVar()
        var.set(CodeBox.SEGS[0])
        super().__init__(master, var, *CodeBox.SEGS, command=self.next)
        # print(self.__dict__)
        self['borderwidth'] = 0
        self['width'] = 1
        self.var = var
        self.next_box = None
        self.bind("<KeyPress>", self.key_press)

    def key_press(self, event):
        c = event.char.upper()
        for val in CodeBox.SEGS:
            if val.startswith(c):
                self.var.set(val)
                self.next(None)
                break

    def get_code(self):
        return self.var.get()

    def set_next(self, next_focus):
        self.next_box = next_focus

    def next(self, event):
        if self.next_box is not None:
            self.next_box.focus()


class BufferSelect(tk.OptionMenu):
    SEGS = ['4', '5', '6', '7', '8']

    def __init__(self, master, *args, **kwargs):
        var = tk.StringVar()
        super().__init__(master, var, *BufferSelect.SEGS, command=self.next)
        var.set(BufferSelect.SEGS[0])
        # print(self.__dict__)
        self['borderwidth'] = 0
        self['width'] = 1
        self.var = var
        self.next_box = None
        self.bind("<KeyPress>", self.key_press)

    def key_press(self, event):
        c = event.char.upper()
        for val in BufferSelect.SEGS:
            if val.startswith(c):
                self.var.set(val)
                self.next(None)
                break

    def get_value(self):
        return int(self.var.get())

    def set_next(self, next_focus):
        self.next_box = next_focus

    def next(self, event):
        if self.next_box is not None:
            self.next_box.focus()


class MatrixFrame(tk.LabelFrame):
    def __init__(self, master, grid_size=5, *args, **kwargs):
        super().__init__(master, relief="ridge", text="Code Matrix", *args, **kwargs)
        self.entry_grid = []
        self.path_labels = []
        last = None
        for i in range(grid_size):
            row = []
            p_row = []
            for j in range(grid_size):
                e = CodeBox(self)
                if last is not None:
                    last.set_next(e)
                last = e
                e.grid(row=i, column=j*2)
                p = tk.Label(self, text=" ", fg="red")
                p.grid(row=i, column=(j*2)+1)
                row.append(e)
                p_row.append(p)
            self.entry_grid.append(row)
            self.path_labels.append(p_row)
        self.entry_grid[0][0].focus()

    def get_first(self):
        return self.entry_grid[0][0]

    def clear_path(self):
        for row in self.path_labels:
            for label in row:
                label['text'] = '  '

    def show_path(self, path):
        """Takes a sequence and displays it in the MatrixFrame"""
        self.clear_path()
        for i, pos in enumerate(path.get_coords()):
            row, col = pos
            self.path_labels[row][col]['text'] = str(i+1)

    def get_matrix(self):
        """Returns a BreachForce.CodeMatrix for the entered matrix"""
        matrix = []
        for m_row in self.entry_grid:
            row = []
            for e in m_row:
                v = e.get_code()
                row.append(v)
            matrix.append(row)

        return BreachForce.CodeMatrix(matrix)

    def set_next(self, next_focus):
        """Useful for transitioning from the code matrix into the sequences"""
        self.entry_grid[-1][-1].set_next(next_focus)


class SequenceBox(tk.Frame):
    """Represents a sequence to be uploaded"""
    def __init__(self, master, size=4, checked=False):
        super().__init__(master)
        self.size = size
        self.checked_var = tk.IntVar()
        self.checked_var.set(1 if checked else 0)
        self.codes = []
        last = None
        i = 0
        while i < size:
            e = CodeBox(self)
            if last is not None:
                last.set_next(e)
            last = e
            e.grid(row=0, column=i)
            self.codes.append(e)
            i += 1
        self.checkMark = tk.Checkbutton(self, variable=self.checked_var)
        self.checkMark.grid(row=0, column=i)

    def get_first(self):
        return self.codes[0]

    def checked(self):
        return self.checked_var.get() == 1

    def set_next(self, next_focus):
        self.codes[-1].set_next(next_focus)

    def get_path(self):
        """Returns a path for this sequence"""
        return BreachForce.Sequence([e.get_code() for e in self.codes if e.get_code() != "  "])


class SequenceSelect(tk.LabelFrame):
    """Provides a number of sequence entry boxes, and can return a list of sequences that are currently checked"""
    def __init__(self, master, seq_count=5):
        super().__init__(master, relief="ridge", text="Sequences to upload")
        self.sequences = []
        last = None
        for i in range(seq_count):
            seq = SequenceBox(self)
            self.sequences.append(seq)
            seq.grid(row=i, column=0)
            if last is not None:
                last.set_next(seq.get_first())
            last = seq

    def get_first(self):
        return self.sequences[0].get_first()

    def get_paths(self):
        """Returns a list of paths for each sequenceselect that is checked"""
        out = []
        for seq in self.sequences:
            if seq.checked():
                out.append(seq.get_path())
        return out

    def set_next(self, next_focus):
        self.sequences[-1].set_next(next_focus)


class MatrixWindow(tk.Toplevel):
    def __init__(self, grid_size=6, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = grid_size
        self.code_grid = MatrixFrame(master=self, grid_size=grid_size)
        self.code_grid.grid(row=0, column=0, columnspan=2)

        self.seq_grid = SequenceSelect(self)
        self.seq_grid.grid(row=0, column=2)
        self.code_grid.set_next(self.seq_grid.get_first())

        self.b_label = tk.Label(self, text="Buffers")
        self.b_label.grid(row=1, column=0, sticky="e")

        self.buffers = BufferSelect(self)
        self.buffers.grid(row=1, column=1, sticky="w")
        self.seq_grid.set_next(self.buffers)

        self.solve_button = tk.Button(self, text="Solve", command=self.solve)
        self.solve_button.grid(row=1, column=2)
        self.buffers.set_next(self.solve_button)

        # self.code_grid.show_path(BreachForce.Sequence(['55', '55', '55', '55'],[(0,0), (1,0), (1,5),(0,5)]))

    def solve(self):
        matrix = self.code_grid.get_matrix()
        paths = self.seq_grid.get_paths()
        if len(paths) > 0:
            result = BreachForce.solve(matrix, self.buffers.get_value(), *paths)
            if result is not None:
                self.code_grid.show_path(result)


class CodeApp(tk.Tk):
    def __init__(self):
        super().__init__(screenName="CodeBreaker")
        self.title("CodeBreaker")
        tk.Label(self, text="CodeMatrix size").grid(row=0, column=0)
        self.c_size = tk.IntVar()
        self.code_size = tk.OptionMenu(self, self.c_size, 5, 6)
        self.c_size.set(6)
        self.code_size.grid(row=0, column=1)
        self.go_button=tk.Button(self, text="Jack in", command=self.show_window)
        self.go_button.grid(row=0, column=2)
        self.mainloop()

    def show_window(self):
        MatrixWindow(grid_size=self.c_size.get())



if __name__ == "__main__":
    s = CodeApp()

import BreachForce
import tkinter as tk


class CodeBox(tk.OptionMenu):
    SEGS = ['  ', 'BD', '55', '1C', '7A', 'E9']

    def __init__(self, master, *args, **kwargs):
        var = tk.StringVar()
        var.set(CodeBox.SEGS[0])
        super().__init__(master, var, *CodeBox.SEGS, command=self.next)
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

    def set_next(self, box):
        self.next_box = box

    def next(self, event):
        if self.next_box is not None:
            self.next_box.focus()


class MatrixFrame(tk.Frame):
    def __init__(self,master, grid_size=5, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.entry_grid = []
        last = None
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                e = CodeBox(self)
                if last is not None:
                    last.set_next(e)
                last = e
                e.grid(row=i, column=j)
                row.append(e)
            self.entry_grid.append(row)
        self.entry_grid[0][0].focus()

    def get_list(self):
        out = []
        for i in self.entry_grid:
            row = []
            for e in row:
                v = e['text']
                row.append(v)
            out.append(row)
        return out

    def set_next(self, next):
        """Useful for transitioning from the code matrix into the sequences"""
        self.entry_grid[-1][-1].set_next(next)


class SequenceBox(tk.Frame):
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
            i += 1
        self.checkMark = tk.Checkbutton(self, variable=self.checked_var)
        self.checkMark.grid(row=0, column=i)

    def checked(self):
        return self.checked_var.get() == 1

    def set_next(self, next):
        self.codes[-1].set_next(next)

    def get_path(self):
        """Returns a path for this sequence"""
        return []


class SequenceSelect(tk.Frame):
    """Provides a number of sequence entry boxes, and can return a list of sequences that are currently checked"""
    def __init__(self, master, seq_count=5):
        super().__init__(master)
        self.sequences = []
        for i in range(seq_count):
            seq = SequenceBox(self)
            self.sequences.append(seq)
            seq.grid(row=i, column=0)

    def get_paths(self):
        """Returns a list of paths for each sequenceselect that is checked"""
        out = []
        for seq in self.sequences:
            if seq.checked():
                out.append(seq.get_path())
        return out

    def set_next(self, next):
        self.sequences[-1].set_next(next)


class MatrixWindow(tk.Toplevel):
    def __init__(self, grid_size=6, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = grid_size
        self.code_grid = MatrixFrame(master=self, grid_size=grid_size)
        self.code_grid.grid(row=0, column=0)
        self.seq_grid = SequenceSelect(self)
        self.seq_grid.grid(row=0, column=1)
        # Prepare the grid


class CodeApp(tk.Tk):
    def __init__(self):
        super().__init__(screenName="CodeBreaker")
        MatrixWindow()
        self.mainloop()


if __name__ == "__main__":
    s = CodeApp()

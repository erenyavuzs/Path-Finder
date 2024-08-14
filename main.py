import tkinter as tk
from tkinter import messagebox
import queue

maze = [
    ["#", " ", "#", "O", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")

        self.cell_size = 40  
        self.rows = len(maze)
        self.cols = len(maze[0])


        self.canvas_width = self.cols * self.cell_size
        self.canvas_height = self.rows * self.cell_size

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white', bd=0, highlightthickness=0)
        self.canvas.pack()

        self.solve_button = tk.Button(root, text="Solve Path", command=self.solve_maze)
        self.solve_button.pack()

        self.draw_maze()


    def draw_maze(self):
        for i, row in enumerate(maze):
            for j, value in enumerate(row):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = 'black' if value == '#' else 'white'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                if value == 'O':
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill='green')
                elif value == 'X':
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill='red')


    def solve_maze(self):
        start = 'O'
        end = 'X'
        start_pos = self.find_start(start)
        if not start_pos:
            messagebox.showerror("Error", "Start position not found")
            return

        self.path = self.find_path(start_pos, end)
        if self.path:
            self.path_index = 0
            self.show_path_step()
        else:
            messagebox.showinfo("Result", "No path found")


    def show_path_step(self):
        if self.path_index < len(self.path):
            (row, col) = self.path[self.path_index]
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='deep sky blue', outline='black')
            self.path_index += 1
            self.root.after(500, self.show_path_step)  


    def find_start(self, start):
        for i, row in enumerate(maze):
            for j, value in enumerate(row):
                if value == start:
                    return (i, j)
        return None


    def find_path(self, start_pos, end):
        q = queue.Queue()
        q.put((start_pos, [start_pos]))

        visited = set()
        visited.add(start_pos)

        while not q.empty():
            current_pos, path = q.get()
            row, col = current_pos

            if maze[row][col] == end:
                return path

            neighbors = self.find_neighbors(row, col)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                if maze[neighbor[0]][neighbor[1]] == "#":
                    continue

                new_path = path + [neighbor]
                q.put((neighbor, new_path))
                visited.add(neighbor)
        return []


    def find_neighbors(self, row, col):
        neighbors = []
        if row > 0:  # up
            neighbors.append((row - 1, col))
        if row + 1 < len(maze):  # down
            neighbors.append((row + 1, col))
        if col > 0:  # left
            neighbors.append((row, col - 1))
        if col + 1 < len(maze[0]):  # right
            neighbors.append((row, col + 1))
        return neighbors


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
import tkinter as tk
import random
from heapq import heappush, heappop

class Puzzle:
    def __init__(self, size):
        self.size = size
        self.goal = list(range(1, size * size)) + [0]
        self.board = self.goal[:]
        random.shuffle(self.board)
        while not self.is_solvable() or self.board == self.goal:
            random.shuffle(self.board)

    def is_solvable(self):
        inversions = 0
        for i in range(len(self.board)):
            for j in range(i + 1, len(self.board)):
                if self.board[i] > self.board[j] != 0:
                    inversions += 1
        return inversions % 2 == 0

    def is_solved(self):
        return self.board == self.goal

    def move(self, pos):
        zero_pos = self.board.index(0)
        if pos in [zero_pos - 1, zero_pos + 1, zero_pos - self.size, zero_pos + self.size]:
            self.board[zero_pos], self.board[pos] = self.board[pos], self.board[zero_pos]
            return True
        return False

class PuzzleGUI:
    def __init__(self, root, puzzle, size):
        self.root = root
        self.puzzle = puzzle
        self.size = size
        self.buttons = []
        self.create_buttons()
        self.update_buttons()

    def create_buttons(self):
        colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1', '#955251', '#B565A7']
        for i in range(self.puzzle.size * self.puzzle.size):
            color = random.choice(colors)
            button = tk.Button(self.root, font=('Arial', 20), width=6, height=3, bg=color, fg='white',
                               command=lambda i=i: self.on_click(i))
            button.grid(row=i // self.puzzle.size, column=i % self.puzzle.size)
            self.buttons.append(button)

    def update_buttons(self):
        for i, num in enumerate(self.puzzle.board):
            self.buttons[i].config(text=str(num) if num != 0 else "")
        if self.puzzle.is_solved():
            self.show_victory_message()

    def on_click(self, index):
        if self.puzzle.move(index):
            self.update_buttons()

    def show_victory_message(self):
        victory_label = tk.Label(self.root, text="You Win!", font=('Arial', 40), fg='green', bg='white')
        victory_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def solve(self):
        solution = self.solve_puzzle()
        if solution:
            self.animate_solution(solution)

    def solve_puzzle(self):
        def heuristic(board):
            distance = 0
            for i, num in enumerate(board):
                if num != 0:
                    target_pos = self.puzzle.goal.index(num)
                    distance += abs(i // self.puzzle.size - target_pos // self.puzzle.size) + \
                                abs(i % self.puzzle.size - target_pos % self.puzzle.size)
            return distance

        def a_star_search():
            start = tuple(self.puzzle.board)
            frontier = []
            heappush(frontier, (0, start, []))
            explored = set()

            while frontier:
                _, current, path = heappop(frontier)
                if list(current) == self.puzzle.goal:
                    return path
                explored.add(current)
                zero_pos = current.index(0)
                neighbors = []
                if zero_pos % self.puzzle.size > 0:  # Can move left
                    neighbors.append(zero_pos - 1)
                if zero_pos % self.puzzle.size < self.puzzle.size - 1:  # Can move right
                    neighbors.append(zero_pos + 1)
                if zero_pos >= self.puzzle.size:  # Can move up
                    neighbors.append(zero_pos - self.puzzle.size)
                if zero_pos < self.puzzle.size * (self.puzzle.size - 1):  # Can move down
                    neighbors.append(zero_pos + self.puzzle.size)

                for neighbor in neighbors:
                    new_board = list(current)
                    new_board[zero_pos], new_board[neighbor] = new_board[neighbor], new_board[zero_pos]
                    new_board_tuple = tuple(new_board)
                    if new_board_tuple not in explored:
                        new_path = path + [neighbor]
                        heappush(frontier, (heuristic(new_board) + len(new_path), new_board_tuple, new_path))

            return None  # No solution found

        return a_star_search()

    def animate_solution(self, solution):
        def animate(step=0):
            if step < len(solution):
                self.puzzle.move(solution[step])
                self.update_buttons()
                self.root.after(200, animate, step + 1)

        animate()

def start_game(root, size):
    puzzle = Puzzle(size)
    gui = PuzzleGUI(root, puzzle, size)
    
    solve_button = tk.Button(root, text="Solve", font=('Arial', 16), command=gui.solve, bg='blue', fg='white')
    solve_button.grid(row=size, column=0, columnspan=size)
    
    root.mainloop()

def choose_grid_size():
    def set_size_and_start(size):
        window.destroy()
        root = tk.Tk()
        root.title(f"{size*size - 1} Puzzle")
        root.geometry("1080x720")
        root.configure(bg='white')
        start_game(root, size)

    window = tk.Tk()
    window.title("Choose Puzzle Size")
    window.geometry("1080x720")
    window.configure(bg='white')

    label = tk.Label(window, text="Choose Puzzle Size", font=('Arial', 40), bg='white')
    label.pack(pady=50)

    sizes = [3, 4, 5]
    for size in sizes:
        button = tk.Button(window, text=f"{size}x{size}", font=('Arial', 30), width=10, height=2,
                           command=lambda size=size: set_size_and_start(size), bg='#FF6F61', fg='white')
        button.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    choose_grid_size()

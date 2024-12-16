import tkinter as tk
from tkinter import messagebox
import random

class LightsOutGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lights Out")
        self.difficulty = tk.IntVar()
        self.board_size = tk.IntVar()
        self.start_frame = None
        self.board_frame = None
        self.buttons = []
        self.create_start_screen()

    def create_start_screen(self):
        self.start_frame = tk.Frame(self.master)
        self.start_frame.pack()

        tk.Label(self.start_frame, text="Zorluk Seviyesini Seçin:").pack()
        difficulty_frame = tk.Frame(self.start_frame)
        difficulty_frame.pack()

        for i in range(3):
            difficulty_button = tk.Radiobutton(difficulty_frame, text=str(i+1), variable=self.difficulty, value=i)
            difficulty_button.pack(side=tk.LEFT)

        tk.Label(self.start_frame, text="Tahta Büyüklüğünü Seçin:").pack()
        size_frame = tk.Frame(self.start_frame)
        size_frame.pack()

        for i in range(3, 7):
            size_button = tk.Radiobutton(size_frame, text=str(i), variable=self.board_size, value=i)
            size_button.pack(side=tk.LEFT)

        start_button = tk.Button(self.start_frame, text="Başlat", command=self.start_game)
        start_button.pack()

    def start_game(self):
        if self.start_frame:
            self.start_frame.pack_forget()

        if self.board_frame:
            self.board_frame.destroy()

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()
        self.buttons = []
        self.initialize_board()
        self.initialize_buttons()
        self.create_reset_button()
        self.create_solve_button()
        self.create_back_button()

    def initialize_board(self):
        self.board = [[random.randint(0, 1) for _ in range(self.board_size.get())] for _ in range(self.board_size.get())]

    def initialize_buttons(self):
        for i in range(self.board_size.get()):
            row_buttons = []
            for j in range(self.board_size.get()):
                button = tk.Button(self.board_frame, text="", width=4, height=2, command=lambda row=i, col=j: self.toggle(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def toggle(self, row, col):
        self.flip_square(row, col)
        self.flip_square(row-1, col)
        self.flip_square(row+1, col)
        self.flip_square(row, col-1)
        self.flip_square(row, col+1)
        self.check_win()

    def flip_square(self, row, col):
        if 0 <= row < self.board_size.get() and 0 <= col < self.board_size.get():
            if self.board[row][col] == 0:
                self.buttons[row][col].config(bg="yellow")
                self.board[row][col] = 1
            else:
                self.buttons[row][col].config(bg="white")
                self.board[row][col] = 0

    def create_reset_button(self):
        if not hasattr(self, 'reset_button'):
            self.reset_button = tk.Button(self.master, text="Yeniden Başla", command=self.start_game)
            self.reset_button.pack()

    def create_solve_button(self):
        if not hasattr(self, 'solve_button'):
            self.solve_button = tk.Button(self.master, text="İpucu Al", command=self.show_solution)
            self.solve_button.pack()

    def create_back_button(self):
        if not hasattr(self, 'back_button'):
            self.back_button = tk.Button(self.master, text="Geri", command=self.back_to_start)
            self.back_button.pack()

    def show_solution(self):
        current_board = [row[:] for row in self.board]
        solution_steps = self.generate_solution(current_board)
        if solution_steps:
            for row, col in solution_steps:
                self.flip_square(row, col)

    def generate_solution(self, board):
        solution_steps = []
        for row in range(self.board_size.get()):
            for col in range(self.board_size.get()):
                if board[row][col] == 1:
                    solution_steps.append((row, col))
                    self.flip_square(row, col)
                    self.flip_square(row-1, col)
                    self.flip_square(row+1, col)
                    self.flip_square(row, col-1)
                    self.flip_square(row, col+1)
        return solution_steps

    def check_win(self):
        for row in self.board:
            for cell in row:
                if cell != 0:
                    return
        self.show_win_message()

    def show_win_message(self):
        win_message = tk.messagebox.showinfo("Oyun Bitti", "Tebrikler! Oyunu Kazandınız!")

    def back_to_start(self):
        if self.board_frame:
            self.board_frame.destroy()
        self.create_start_screen()

def main():
    root = tk.Tk()
    root.geometry("300x250")
    app = LightsOutGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import threading
import time
import customtkinter as ctk

from generator import generate_puzzle
from validator import find_conflicts, is_solved

ctk.set_appearance_mode("light")

CELL = 76
MARGIN = 20
BOARD = CELL * 9
SIZE = BOARD + 2 * MARGIN

BG_MAIN = "#EAE4F7"
CARD_BG = "#FFFFFF"
PURPLE_ACCENT = "#7C5CBF"
PURPLE_HOVER = "#6A4CA8"
SELECTED_COLOR = "#D8C7F8"
CONFLICT_COLOR = "#FFBABA"

COLORS = [
    "#FFFFFF", "#F7F2FE", "#EFF7F6", "#FFF5EB", "#F8EFF8",
    "#F0F7EE", "#FAF9EB", "#FCF0F2", "#EBF3FB"
]

DIFFICULTY = {"Легкий": 35, "Середній": 45, "Складний": 52}


class VictoryDialog(ctk.CTkToplevel):
    def __init__(self, parent, time_str, on_new_game):
        super().__init__(parent)

        self.title("Перемога!")
        self.configure(fg_color=BG_MAIN)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        width, height = 350, 200
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=20)
        card.pack(fill="both", expand=True, padx=12, pady=12)

        title_label = ctk.CTkLabel(
            card,
            text="🎉 Вітаємо!",
            font=("Segoe UI", 20, "bold"),
            text_color="#3A2E4C"
        )
        title_label.pack(pady=(14, 4))

        msg_label = ctk.CTkLabel(
            card,
            text=f"Ви успішно розв'язали судоку за\n{time_str}",
            font=("Segoe UI", 13),
            text_color="#6C5C82",
            justify="center"
        )
        msg_label.pack(pady=(0, 12))

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=(0, 10))

        new_game_btn = ctk.CTkButton(
            btn_frame,
            text="Нова гра",
            font=("Segoe UI", 13, "bold"),
            fg_color=PURPLE_ACCENT,
            hover_color=PURPLE_HOVER,
            text_color="#FFFFFF",
            corner_radius=12,
            height=36,
            width=110,
            command=lambda: [self.destroy(), on_new_game()]
        )
        new_game_btn.pack(side="left", padx=6)

        close_btn = ctk.CTkButton(
            btn_frame,
            text="Закрити",
            font=("Segoe UI", 13, "bold"),
            fg_color="#FFFFFF",
            hover_color="#D8CBF8",
            text_color="#3A2E4C",
            corner_radius=12,
            height=36,
            width=90,
            command=self.destroy
        )
        close_btn.pack(side="left", padx=6)


class SudokuApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Судоку-фігури")
        self.configure(fg_color=BG_MAIN)
        self.resizable(False, False)

        self.regions = None
        self.puzzle = None
        self.solution = None
        self.matrix = None
        self.selected = None
        self.conflicts = set()
        self.busy = False
        self._result = None

        self.start_time = None
        self.timer_running = False
        self.elapsed_seconds = 0

        self._create_widgets()
        self.new_game()

    def _create_widgets(self):
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(pady=(22, 14), padx=28, fill="x")

        self.diff_segmented = ctk.CTkSegmentedButton(
            top_bar,
            values=list(DIFFICULTY.keys()),
            font=("Segoe UI", 13, "bold"),
            selected_color=PURPLE_ACCENT,
            selected_hover_color=PURPLE_HOVER,
            unselected_color="#FFFFFF",
            unselected_hover_color="#D8CBF8",
            text_color="#3A2E4C",
            corner_radius=14,
            height=42,
            command=self.on_difficulty_change
        )
        self.diff_segmented.set("Середній")
        self.diff_segmented.pack(side="left")

        self.timer_label = ctk.CTkLabel(
            top_bar, text="00:00", font=("Segoe UI", 19, "bold"), text_color="#3A2E4C"
        )
        self.timer_label.pack(side="left", expand=True, padx=12)

        self.new_btn = ctk.CTkButton(
            top_bar,
            text="Нова гра",
            font=("Segoe UI", 14, "bold"),
            fg_color=PURPLE_ACCENT,
            hover_color=PURPLE_HOVER,
            text_color="#FFFFFF",
            corner_radius=16,
            height=42,
            width=125,
            command=self.new_game
        )
        self.new_btn.pack(side="right")

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=22)
        card.pack(pady=8, padx=28)

        self.canvas = ctk.CTkCanvas(
            card, width=SIZE, height=SIZE, bg=CARD_BG, highlightthickness=0, bd=0
        )
        self.canvas.pack(padx=14, pady=14)
        self.canvas.bind("<Button-1>", self.on_click)
        self.bind("<Key>", self.on_key)

        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(pady=(18, 8))

        self.check_btn = ctk.CTkButton(
            actions_frame,
            text="Перевірити",
            font=("Segoe UI", 14, "bold"),
            fg_color="#FFFFFF",
            hover_color="#D8CBF8",
            text_color="#3A2E4C",
            corner_radius=20,
            height=48,
            width=150,
            command=self.check
        )
        self.check_btn.pack(side="left", padx=10)

        self.sol_btn = ctk.CTkButton(
            actions_frame,
            text="Показати розв'язок",
            font=("Segoe UI", 14, "bold"),
            fg_color="#FFFFFF",
            hover_color="#D8CBF8",
            text_color="#3A2E4C",
            corner_radius=20,
            height=48,
            width=200,
            command=self.show_solution
        )
        self.sol_btn.pack(side="left", padx=10)

        self.status = ctk.CTkLabel(
            self, text="", font=("Segoe UI", 13), text_color="#6C5C82"
        )
        self.status.pack(pady=(4, 18))

    def on_difficulty_change(self, value):
        self.new_game()

    def update_timer(self):
        if self.timer_running:
            self.elapsed_seconds = int(time.time() - self.start_time)
            mins = self.elapsed_seconds // 60
            secs = self.elapsed_seconds % 60
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
            self.after(1000, self.update_timer)

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def new_game(self):
        if self.busy:
            return
        self.busy = True
        self.stop_timer()
        self.timer_label.configure(text="00:00")
        self.status.configure(text="Генерація судоку...")
        target = DIFFICULTY[self.diff_segmented.get()]

        def worker():
            self._result = generate_puzzle(target)

        threading.Thread(target=worker, daemon=True).start()
        self.after(100, self.wait_for_result)

    def wait_for_result(self):
        if self._result is None:
            self.after(100, self.wait_for_result)
            return
        self.puzzle, self.solution, self.regions = self._result
        self._result = None
        self.matrix = [row[:] for row in self.puzzle]
        self.selected = None
        self.conflicts = set()
        self.busy = False
        self.status.configure(text="Оберіть клітинку та введіть число 1-9")
        self.draw()
        self.start_timer()

    def is_given(self, r, c):
        return self.puzzle[r][c] != 0

    def on_click(self, event):
        if self.matrix is None or self.busy:
            return
        c = (event.x - MARGIN) // CELL
        r = (event.y - MARGIN) // CELL
        if 0 <= r < 9 and 0 <= c < 9:
            self.selected = (r, c)
        else:
            self.selected = None
        self.draw()

    def on_key(self, event):
        if self.matrix is None or self.selected is None or self.busy:
            return
        r, c = self.selected

        moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        if event.keysym in moves:
            dr, dc = moves[event.keysym]
            self.selected = (min(8, max(0, r + dr)), min(8, max(0, c + dc)))
            self.draw()
            return

        if self.is_given(r, c):
            return

        if event.char in "123456789" and event.char != "":
            self.matrix[r][c] = int(event.char)
        elif event.keysym in ("BackSpace", "Delete", "0"):
            self.matrix[r][c] = 0
        else:
            return

        self.conflicts = set()
        self.draw()

    def check(self):
        if self.matrix is None or self.busy:
            return
        if is_solved(self.matrix, self.regions):
            self.stop_timer()
            self.conflicts = set()
            self.draw()
            VictoryDialog(
                parent=self,
                time_str=self.timer_label.cget("text"),
                on_new_game=self.new_game
            )
            return

        self.conflicts = find_conflicts(self.matrix, self.regions)
        if self.conflicts:
            self.status.configure(text="Знайдено помилки у заповненні")
        else:
            self.status.configure(text="Поки що все правильно!")
        self.draw()

    def show_solution(self):
        if self.matrix is None or self.busy:
            return
        self.matrix = [row[:] for row in self.solution]
        self.conflicts = set()
        self.stop_timer()
        self.draw()

    def draw(self):
        cv = self.canvas
        cv.delete("all")
        if self.matrix is None:
            return

        for r in range(9):
            for c in range(9):
                x0 = MARGIN + c * CELL
                y0 = MARGIN + r * CELL
                x1 = x0 + CELL
                y1 = y0 + CELL

                color = COLORS[self.regions[r][c]]

                if (r, c) in self.conflicts:
                    color = CONFLICT_COLOR
                elif self.selected == (r, c):
                    color = SELECTED_COLOR

                cv.create_rectangle(
                    x0, y0, x1, y1,
                    fill=color, outline="#EAE4F7", width=1
                )

                val = self.matrix[r][c]
                if val != 0:
                    fg = "#1C1427" if self.is_given(r, c) else PURPLE_ACCENT
                    font_style = ("Segoe UI", 28, "bold") if self.is_given(r, c) else ("Segoe UI", 28)
                    cv.create_text(x0 + CELL / 2, y0 + CELL / 2, text=str(val), font=font_style, fill=fg)

        for r in range(9):
            for c in range(9):
                x0 = MARGIN + c * CELL
                y0 = MARGIN + r * CELL
                x1 = x0 + CELL
                y1 = y0 + CELL
                k = self.regions[r][c]
                line_color = "#3A2E4C"

                if r == 0 or self.regions[r - 1][c] != k:
                    cv.create_line(x0, y0, x1, y0, width=3, fill=line_color)
                if c == 0 or self.regions[r][c - 1] != k:
                    cv.create_line(x0, y0, x0, y1, width=3, fill=line_color)
                if r == 8:
                    cv.create_line(x0, y1, x1, y1, width=3, fill=line_color)
                if c == 8:
                    cv.create_line(x1, y0, x1, y1, width=3, fill=line_color)
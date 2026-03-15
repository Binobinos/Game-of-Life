import copy
import random
import tkinter.messagebox
from collections import deque
from tkinter import (
    Tk,
    Canvas,
    Event,
    ttk,
    Entry,
    Label,
)
from typing import Self

type Board = list[list[bool]]
type Coord = tuple[int, int]
type Cell = set[Coord]


def color_to_str(color: bool) -> str:
    """Преобразует значение цвета в HEX-формат"""
    color = 0 if color else 255
    return f"#{hex(color)[2:].zfill(2) * 3}"


class GuiNetworkProgram:
    def __init__(self: Self, width: int = 64, height: int = 32, size: int = 16) -> None:
        self.root: Tk = Tk()
        self.root.title("Игра жизнь")
        self.root.geometry("1200x700")
        self.width: int = width
        self.height: int = height
        self.x = 0
        self.y = 0
        self.size: int = size
        self.rectangles = []
        self.drawing: bool = False
        self.breaking: bool = False
        self.brush_radius: int = 0
        self.cursor_radius_indicator = None
        self.canvas: Canvas | None = None
        self.cell: Cell = set()
        self._is_running: bool = False
        self.time: int | float = 1
        self.delta_time: float = 1.1
        self.coof_random: float = 0.02
        self.last_move: Cell | None = None
        self.status_label = None
        self.entry: Entry | None = None
        self.speed_label: Label | None = None
        self.move_label: Label | None = None
        self.save_cell: Cell | None = None
        self.maxlen: int = None
        self.moves: deque[Cell] = deque(maxlen=self.maxlen)
        self._move: int = 0
        self.setup_ui()

    @property
    def is_running(self):
        return self._is_running

    @is_running.setter
    def is_running(self, value):
        self._is_running = value
        self.update_status_label()

    @property
    def move(self) -> int:
        return self._move

    @move.setter
    def move(self, value: int) -> None:
        self._move = value
        self.update_move_label()

    def test_line(self):
        """Асинхронное тестирование линий 1-30"""
        n_Max = 129  # до 30 включительно
        y = self.height // 2
        start_x = self.width // 3  # начинаем от центра
        self.current_test_length = 0
        self.max_test_length = n_Max - 1
        print("\n" + "=" * 80)
        print(f"ТЕСТИРОВАНИЕ ЛИНИЙ ДЛИНОЙ {self.current_test_length}-{self.max_test_length}")
        print("=" * 80)
        print(f"{'Длина':<6} {'Тип':<20} {'Поколений':<10} {'Период':<8} {'Клеток':<8} {'Останавливается?'}")
        print("-" * 80)

        # Запускаем первый тест
        self.current_test_length = 0
        self.max_test_length = n_Max - 1
        self.test_y = y
        self.test_start_x = start_x

        self.start_single_test()

    def start_single_test(self):
        """Запускает тест одной конкретной длины"""
        if self.current_test_length > self.max_test_length:
            print("=" * 80)
            print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
            return

        length = self.current_test_length

        # Очищаем всё
        self.cell.clear()
        self.moves.clear()
        self.last_move = None
        self.move = 0
        self.is_running = False

        # Рисуем линию
        for x in range(self.test_start_x, self.test_start_x + length):
            self.cell.add((x, self.test_y))

        self.clear_board()
        self.print_board()

        print(f"Запуск теста для длины {length}...", end=" ")

        # Запускаем симуляцию
        self.is_running = True
        self.game_with_callback()

    def game_with_callback(self):
        """Запускает игру с колбэком по завершении"""
        if self.is_running:
            self.next_board()
            if self.move > 4000:
                print("Бесконечные не повторяющиеся глайдеры/корабли или очень долгая сходимость")
                self.current_test_length += 1
                self.start_single_test()
                return
            if self.is_running:
                self.root.after(self.time, self.game_with_callback)
            else:
                self.current_test_length += 1
                self.start_single_test()
        else:
            self.current_test_length += 1
            self.start_single_test()

    def setup_ui(self: Self) -> None:
        """Настройка пользовательского интерфейса"""
        button_frame = ttk.Frame(self.root)
        button_frame.place(relx=0.05, rely=0.925, width=1500, height=60)

        text_frame = ttk.Frame(self.root)
        text_frame.place(relx=0.1, rely=0.04, width=1500, height=60)

        ttk.Button(button_frame, text="Запустить/Остановить", command=self.toggle_game).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Следующий ход", command=self.next_board).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Очистить", command=self.clear_canvas).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Ускорить", command=self.speed_up).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Замедлить", command=self.slow_down).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Сохранить", command=self.save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Загрузить", command=self.load).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Тестирование", command=self.test_line).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Рандомное заполнение", command=self.random_fill).pack(side="left", padx=5)
        self.entry = ttk.Entry(button_frame, justify="center")
        self.entry.pack(side="left", padx=5)
        self.speed_label = ttk.Label(text_frame, text=f"Скорость: {1000 / self.time:.1f} FPS")
        self.speed_label.pack(side="left", padx=20)

        self.status_label = ttk.Label(text_frame, text="Не запущена")
        self.status_label.pack(side="left", padx=20)
        self.move_label = ttk.Label(text_frame, text="Начало")
        self.move_label.pack(side="left", padx=20)
        self.canvas: Canvas = Canvas(
            self.root, bg="white", width=self.width * self.size, height=self.height * self.size
        )
        self.canvas.place(relx=0.1, rely=0.1)

        self.root.bind("<Left>", self.left_move)
        self.root.bind("<Right>", self.right_move)
        self.root.bind("<Up>", self.up_move)
        self.root.bind("<Down>", self.down_move)
        self.setup_canvas()
        # self.test_line()

    def save(self) -> None:
        self.is_running = False
        self.save_cell = copy.deepcopy(self.cell)

    def left_move(self, _):
        self.x -= 1
        self.clear_board()
        self.print_board()

    def right_move(self, _):
        self.x += 1
        self.clear_board()
        self.print_board()

    def up_move(self, _):
        self.y -= 1
        self.print_board()

    def down_move(self, _):
        self.y += 1
        self.print_board()

    def load(self) -> None:
        self.is_running = False
        self.move = 0
        self.moves.clear()
        if self.save_cell is not None:
            self.cell = copy.deepcopy(self.save_cell)
            self.print_board()

    def update_speed_label(self: Self) -> None:
        """Обновляет label со скоростью"""
        fps = 1000 / self.time if self.time > 0 else 0
        self.speed_label.config(text=f"Скорость: {fps:.1f} FPS")

    def update_status_label(self: Self) -> None:
        """Обновляет label со скоростью"""
        self.status_label.config(text="Запущена" if self.is_running else "Не запущена")

    def update_move_label(self: Self) -> None:
        """Обновляет label со скоростью"""
        self.move_label.config(text=f"Ход {self._move}")

    def speed_up(self: Self) -> None:
        self.time = round(max(10, self.time / self.delta_time))
        self.update_speed_label()

    def slow_down(self: Self) -> None:
        self.time = round(max(10, self.time * self.delta_time))
        self.update_speed_label()

    def random_fill(self: Self) -> None:
        try:
            self.cell = set()
            self.coof_random = int(self.entry.get()) / 100
            for y in range(self.height):
                for x in range(self.width):
                    if random.random() <= self.coof_random:
                        self.cell.add((x + self.x, y + self.y))
            self.print_board()
        except ValueError as error:
            tkinter.messagebox.showerror("Синтаксическая ошибка", "Не удалось преобразовать в число")

    def setup_canvas(self: Self) -> None:
        """Настройка холста для рисования"""
        for y in range(self.height):
            self.rectangles.append([])
            for x in range(self.width):
                rect = self.canvas.create_rectangle(
                    x * self.size,
                    y * self.size,
                    (x + 1) * self.size,
                    (y + 1) * self.size,
                    fill="#ffffff",
                    outline="#e0e0e0",
                    width=1,
                    tags=[f"{x}{y}"],
                )
                self.rectangles[y].append(rect)

        # Привязка событий мыши
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", lambda e: setattr(self, "drawing", True))
        self.canvas.bind("<ButtonRelease-1>", lambda e: setattr(self, "drawing", False))
        self.canvas.bind("<Button-3>", lambda e: setattr(self, "breaking", True))
        self.canvas.bind("<ButtonRelease-3>", lambda e: setattr(self, "breaking", False))
        # self.canvas.bind("<MouseWheel>", self.change_brush_radius)

    def draw_with_radius(self: Self, x: int, y: int, is_drawing: bool) -> None:
        """Обрабатывает рисование с учетом радиуса кисти"""
        w_x = x - self.x
        w_y = y - self.y
        if 0 <= x < self.width and 0 <= y < self.height:
            self.canvas.itemconfig(self.rectangles[y][x], fill=color_to_str((w_x, w_y) in self.cell))
        coord = (w_x, w_y)
        if is_drawing:
            self.cell.add(coord)
        else:
            self.cell.discard(coord)

    def update_cursor_indicator(self: Self, x: int, y: int) -> None:
        """Обновляет индикатор радиуса кисти"""
        if self.cursor_radius_indicator:
            self.canvas.delete(self.cursor_radius_indicator)

        if 0 <= x < self.width and 0 <= y < self.height:
            self.cursor_radius_indicator = self.canvas.create_oval(
                (x - self.brush_radius) * self.size,
                (y - self.brush_radius) * self.size,
                (x + self.brush_radius + 1) * self.size,
                (y + self.brush_radius + 1) * self.size,
                outline="red",
                dash=(2, 2),
                width=1,
            )

    def change_brush_radius(self: Self, event: Event) -> None:
        """Изменяет радиус кисти колесиком мыши"""
        if event.delta > 0:
            self.brush_radius = min(5, self.brush_radius + 1)
        else:
            self.brush_radius = max(0, self.brush_radius - 1)
        self.update_cursor_indicator(event.x // self.size, event.y // self.size)

    def on_mouse_move(self: Self, event: Event) -> None:
        """Обработчик движения мыши"""
        x, y = event.x // self.size, event.y // self.size
        self.update_cursor_indicator(x, y)
        if self.drawing or self.breaking:
            self.draw_with_radius(x, y, self.drawing)

    def clear_canvas(self: Self) -> None:
        """Очищает холст"""
        self.is_running = False
        self.clear_board()
        self.cell.clear()
        self.canvas.update()
        self.moves.clear()
        self.move = 0
        self.last_move = None
        self.x = 0
        self.y = 0

    def clear_board(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.itemconfig(self.rectangles[y][x], fill="#ffffff")

    def print_board(self: Self) -> None:
        if self.last_move is not None:
            changed = self.cell.symmetric_difference(self.last_move)
            for x, y in changed:
                w_x = x + self.x
                w_y = y + self.y
                if 0 <= w_x < self.width and 0 <= w_y < self.height:
                    self.canvas.itemconfig(self.rectangles[w_y][w_x], fill=color_to_str((x, y) in self.cell))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    w_x = x + self.x
                    w_y = y + self.y
                    if 0 <= w_x < self.width and 0 <= w_y < self.height:
                        self.canvas.itemconfig(self.rectangles[w_y][w_x], fill=color_to_str((x, y) in self.cell))

    def neighbors(self: Self, coord: Coord, is_alive: bool = False) -> Cell:
        cell = set()
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                x_ = coord[0] + x
                y_ = coord[1] + y
                c = (x_, y_)
                if is_alive:
                    if (x_, y_) in self.cell:
                        cell.add(c)
                else:
                    cell.add(c)
        return cell

    def next_board(self: Self) -> None:
        self.move += 1

        copy_cell = set()
        for coord in self.cell:
            copy_cell.add(coord)
            copy_cell |= self.neighbors(coord)

        U = set()
        for coord in copy_cell:
            alive = coord in self.cell
            n = len(self.neighbors(coord, is_alive=True))
            if alive and 2 <= n <= 3:
                U.add(coord)
            elif not alive and n == 3:
                U.add(coord)
        self.cell = U

        self.print_board()

        if not self.cell:
            self.is_running = False
            message = f"Пустое поле {self.move} ходе!"
            # tkinter.messagebox.showinfo("Уведомление", message)
            print(message)
        elif self.last_move is not None and self.last_move == self.cell:
            self.is_running: bool = False
            message = (
                f"Остановка(Стабилизация) {self.move} ходе!" if self.move > 1 else "Стабильная расстановка с начала"
            )
            # tkinter.messagebox.showinfo("Уведомление", message)
            print(message)
            self.move -= 1
        elif self.cell in self.moves:
            self.is_running = False
            index = self.moves.index(self.cell, 0, len(self.moves)) + 1
            message = f"Цикл {index} - {self.move - 1}, Период - {self.move - index}"

            # tkinter.messagebox.showinfo(
            #     "Уведомление",
            #     f"Цикл на {self.move - 1} ходе!\nЦикл {index} - {self.move - 1}\nПериод - {self.move - index}",
            # )
            print(message)
        self.moves.append(self.cell)
        self.last_move = self.cell

    def game(self: Self) -> None:
        if self.is_running:
            self.next_board()
            if self.is_running:
                self.root.after(self.time, self.game)

    def toggle_game(self: Self) -> None:
        self.is_running: bool = not self.is_running
        if self.is_running:
            self.game()

    def main(self: Self) -> None:
        """Запускает приложение"""
        self.root.mainloop()

import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, StringVar
from PIL import Image, ImageDraw


class DrawingApp:
    """Класс, представляющий приложение для рисования."""

    def __init__(self, root):
        """Инициализирует приложение для рисования."""
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Создание изображения и объекта для рисования
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Создание холста
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        # Инициализация переменных для рисования
        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = 1
        self.eraser_size = 1
        self.is_eraser_active = False
        self.is_pipette_active = False

        # Привязка событий мыши
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)

        # Привязка горячих клавиш с аргументом события
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    def setup_ui(self):
        """Настраивает пользовательский интерфейс."""
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        buttons = [
            ("Очистить", self.clear_canvas),
            ("Выбрать цвет", self.choose_color),
            ("Сохранить", self.save_image),
            ("Ластик", self.toggle_eraser),
            ("Пипетка", self.toggle_pipette),
        ]

        for text, command in buttons:
            tk.Button(control_frame, text=text, command=command).pack(side=tk.LEFT)

        # Размер кисти
        brush_frame = tk.Frame(control_frame)
        brush_frame.pack(side=tk.LEFT, padx=5)

        tk.Label(brush_frame, text="Размер кисти:").pack()

        self.brush_size_var = StringVar(value='1')
        tk.OptionMenu(brush_frame, self.brush_size_var, *[1, 2, 5, 10], command=self.update_brush_size).pack()

    def paint(self, event):
        """Обрабатывает событие рисования."""
        if not (self.is_pipette_active or not (self.last_x and self.last_y)):
            current_size = self.eraser_size if self.is_eraser_active else self.brush_size
            line = [self.last_x, self.last_y, event.x, event.y]
            self.canvas.create_line(line, width=current_size, fill=self.pen_color,
                                    capstyle=tk.ROUND)
            if not self.is_eraser_active:
                self.draw.line(line, fill=self.pen_color, width=current_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """Сбрасывает координаты последней точки рисования."""
        self.last_x = None
        self.last_y = None

    def clear_canvas(self):
        """Очищает холст и сбрасывает изображение."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        """Открывает диалоговое окно выбора цвета."""
        color = colorchooser.askcolor(color=self.pen_color)[1]
        if color:
            self.pen_color = color

    def save_image(self, event=None):
        """Сохраняет текущее изображение в файл."""
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path and not file_path.endswith('.png'):
            file_path += '.png'
            try:
                self.image.save(file_path)
                messagebox.showinfo("Информация", "Изображение успешно сохранено!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")

    def update_brush_size(self, size):
        """Обновляет размер кисти."""
        self.brush_size = int(size)

    def toggle_eraser(self):
        """Переключает режим ластика."""
        if not (self.is_pipette_active or (self.pen_color == "white")):
            print("Eraser activated.")
            print(f"Current pen color: {self.pen_color}")
            print(f"Eraser active: {self.is_eraser_active}")
            print("You can now use the eraser tool.")
            print("Press the eraser button again to deactivate it.")
            print()

            # Установка режима ластика
            if not self.is_eraser_active:
                print("Switched to eraser mode.")
                print()

    def toggle_pipette(self):
        """Переключает режим пипетки."""
        if not (self.is_eraser_active or (self.pen_color == "white")):
            print("Pipette activated.")
            print(f"Current pen color: {self.pen_color}")
            print(f"Pipette active: {self.is_pipette_active}")
            print("You can now use the pipette to pick colors from the canvas.")
            print("Press the left mouse button on the canvas to pick a color.")
            print()

            # Установка режима пипетки
            if not self.is_pipette_active:
                print("Switched to pipette mode.")
                print()

    def pick_color(self, event):
        """Выбирает цвет с холста (инструмент пипетка)."""
        x = event.x
        y = event.y
        color = tuple(self.image.getpixel((x, y)))
        if color:
            hex_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
            messagebox.showinfo("Цвет выбран", f"Выбранный цвет: {hex_color}")
            self.pen_color = hex_color


def main():
    """Основная функция для запуска приложения."""
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

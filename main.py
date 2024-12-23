import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, StringVar
from PIL import Image, ImageDraw

class DrawingApp:
    """
    Класс, представляющий приложение для рисования.
    """

    def __init__(self, root):
        """
        Инициализирует приложение для рисования.

        Args:
            root (tk.Tk): Корневое окно приложения.
        """
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

        # Привязка событий мыши
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        """Настраивает пользовательский интерфейс."""
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Кнопка очистки холста
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Кнопка выбора цвета
        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Кнопка сохранения изображения
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Выпадающий список для выбора размера кисти
        self.brush_sizes = [1, 2, 5, 10]
        self.brush_size_var = StringVar(self.root)
        self.brush_size_var.set(self.brush_sizes[0])  # Установка начального значения
        brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *self.brush_sizes, command=self.update_brush_size)
        brush_size_menu.pack(side=tk.LEFT)

    def paint(self, event):
        """
        Обрабатывает событие рисования.

        Args:
            event (tk.Event): Событие движения мыши.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Сбрасывает координаты последней точки рисования.

        Args:
            event (tk.Event): Событие отпускания кнопки мыши.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """Очищает холст и сбрасывает изображение."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """Открывает диалоговое окно выбора цвета."""
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        """Сохраняет текущее изображение в файл."""
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_brush_size(self, size):
        """
        Обновляет размер кисти.

        Args:
            size (str): Новый размер кисти.
        """
        self.brush_size = int(size)

def main():
    """Основная функция для запуска приложения."""
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

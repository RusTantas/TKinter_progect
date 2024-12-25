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
        self.previous_color = 'black'  # Для сохранения цвета при использовании ластика
        self.brush_size = 1
        self.eraser_size = 1
        self.is_eraser_active = False

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

        # Кнопка ластика
        eraser_button = tk.Button(control_frame, text="Ластик", command=self.toggle_eraser)
        eraser_button.pack(side=tk.LEFT)

        # Фрейм для размера кисти
        brush_frame = tk.Frame(control_frame)
        brush_frame.pack(side=tk.LEFT, padx=5)

        brush_label = tk.Label(brush_frame, text="Размер кисти:")
        brush_label.pack()

        # Выпадающий список для выбора размера кисти
        self.brush_sizes = [1, 2, 5, 10]
        self.brush_size_var = StringVar(self.root)
        self.brush_size_var.set(self.brush_sizes[0])  # Установка начального значения
        brush_size_menu = tk.OptionMenu(brush_frame, self.brush_size_var, *self.brush_sizes, command=self.update_brush_size)
        brush_size_menu.pack()

        # Фрейм для размера ластика
        eraser_frame = tk.Frame(control_frame)
        eraser_frame.pack(side=tk.LEFT, padx=5)

        eraser_label = tk.Label(eraser_frame, text="Размер ластика:")
        eraser_label.pack()

        # Выпадающий список для выбора размера ластика
        self.eraser_size_var = StringVar(self.root)
        self.eraser_size_var.set(self.brush_sizes[0])  # Установка начального значения
        eraser_size_menu = tk.OptionMenu(eraser_frame, self.eraser_size_var, *self.brush_sizes, command=self.update_eraser_size)
        eraser_size_menu.pack()

    def paint(self, event):
        """
        Обрабатывает событие рисования.

        Args:
            event (tk.Event): Событие движения мыши.
        """
        if self.last_x and self.last_y:
            current_size = self.eraser_size if self.is_eraser_active else self.brush_size
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=current_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=current_size)

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
        color = colorchooser.askcolor(color=self.pen_color)[1]
        if color:
            self.pen_color = color
            self.previous_color = color
            self.is_eraser_active = False

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

    def update_eraser_size(self, size):
        """
        Обновляет размер ластика.

        Args:
            size (str): Новый размер ластика.
        """
        self.eraser_size = int(size)

    def toggle_eraser(self):
        """Переключает режим ластика."""
        if self.is_eraser_active:
            self.pen_color = self.previous_color
            self.is_eraser_active = False
        else:
            self.previous_color = self.pen_color
            self.pen_color = "white"
            self.is_eraser_active = True

def main():
    """Основная функция для запуска приложения."""
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

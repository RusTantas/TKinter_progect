import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk
from settings import *
from utilities import image_to_icon


class DrawingApp:
    """Класс для GUI-приложения."""

    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")
        self.root.minsize(610, 450)
        self.set_icon()

        self.bg_color = 'white'
        self.pen_color = 'black'
        self.width = 600
        self.height = 400
        self.text = ''
        self.font = 'Times 20'
        self.image = Image.new("RGB", (self.width, self.height), color=self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

        self.icons = {
            'save': image_to_icon(ICON_SAVE),
            'insert': image_to_icon(ICON_INSERT),
            'new': image_to_icon(ICON_NEW),
            'brush': image_to_icon(ICON_BRASH),
            'pipette': image_to_icon(ICON_PIPETTE),
            'palette': image_to_icon(ICON_PALETTE),
            'eraser': image_to_icon(ICON_ERASER),
            'resize': image_to_icon(ICON_RESIZE),
            'text': image_to_icon(ICON_TEXT),
            'fon': image_to_icon(ICON_FON)
        }

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=self.bg_color)
        self.canvas.pack(expand=True)

        self.last_x, self.last_y = None, None
        self.pen_color_save = self.pen_color

        self.setup_ui()
        self.bind_events()

    def set_icon(self):
        """Устанавливает иконку приложения."""
        try:
            self.root.iconbitmap(default="./icon/favicon.ico")
            # Для компиляции с помощью auto-py-to-exe заменить строку выше на:
            # self.root.iconbitmap(default=path.join(sys._MEIPASS, "./icon/favicon.ico"))
        except Exception:
            pass

    def setup_ui(self):
        """Создает интерфейс управления."""
        control_frame = tk.Frame(self.root, relief=tk.RAISED, border=2)
        control_frame.pack(fill=tk.BOTH)

        buttons = [
            ("Сохранить", self.icons['save'], self.save_image),
            ("Вставить", self.icons['insert'], self.image_insert),
            ("Очистить", self.icons['new'], self.clear_canvas),
            ("Изменить размер", self.icons['resize'], self.image_resize),
            ("Палитра", self.icons['palette'], self.choose_color),
            ("Фон", self.icons['fon'], self.choose_fon),
            ("Кисть", self.icons['brush'], self.pen_image),
            ("Ластик", self.icons['eraser'], self.eraser_image),
            ("Текст", self.icons['text'], self.insert_text)
        ]

        for text, icon, command in buttons:
            tk.Button(control_frame, image=icon, text=text, command=command).pack(side=tk.LEFT)

        self.canvas_color = tk.Canvas(control_frame, width=20, height=20, bg=self.pen_color)
        self.canvas_color.pack(side=tk.RIGHT, padx=8)

        self.brush_size_scale = tk.Scale(control_frame, from_=5, to=20, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        sizes = [1, 2, 5, 10, 20]
        variable = tk.StringVar()
        variable.set(str(sizes[2]))
        tk.OptionMenu(control_frame, variable, *sizes, command=self.set_brush).pack(side=tk.LEFT)

    def bind_events(self):
        """Привязывает события к методам."""
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    def set_brush(self, choice):
        """Устанавливает размер кисти."""
        self.brush_size_scale.set(int(choice))

    def paint(self, event):
        """Рисует линии на холсте."""
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """Сбрасывает последние координаты."""
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """Очищает холст."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.width, self.height), color=self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

    def image_resize(self):
        """Изменяет размер холста."""
        try:
            x, y = map(int, simpledialog.askstring(
                'Изменение размера изображения',
                'Введите ширину и высоту изображения (разделитель - пробел):',
                parent=self.root).split())
        except (ValueError, AttributeError):
            messagebox.showerror(title='Ошибка', message='Вы ввели неверные значения')
            return

        self.width, self.height = x, y
        self.image = self.image.resize((x, y))
        self.photo = ImageTk.PhotoImage(self.image)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.config(width=self.width, height=self.height)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def choose_color(self, event=None):
        """Выбирает цвет кисти."""
        pen_color = colorchooser.askcolor(color=self.pen_color, title='Цвет кисти')[1]
        if pen_color:
            self.pen_color = pen_color
            self.pen_color_save = self.pen_color
            self.canvas_color['bg'] = self.pen_color

    def choose_fon(self, event=None):
        """Выбирает цвет фона."""
        bg_color = colorchooser.askcolor(color=self.bg_color, title='Цвет фона')[1]
        if bg_color:
            self.bg_color = bg_color
            self.canvas.config(background=self.bg_color)

    def pick_color(self, event):
        """Выбирает цвет с изображения."""
        self.pen_color = "#{:02X}{:02X}{:02X}".format(*self.image.getpixel((event.x, event.y)))
        self.pen_color_save = self.pen_color
        self.canvas_color['bg'] = self.pen_color

    def pen_image(self):
        """Устанавливает инструмент кисть."""
        self.pen_color = self.pen_color_save

    def eraser_image(self):
        """Устанавливает инструмент ластик."""
        self.pen_color = self.bg_color

    def insert_text(self):
        """Вставляет текст на изображение."""
        self.text = simpledialog.askstring('Добавить текст', 'Введите текст для вставки:',
                                           initialvalue=self.text, parent=self.root)
        if self.text:
            self.root.tk.call("tk", "fontchooser", "configure", "-font", self.font,
                              "-command", self.root.register(self.font_changed))
            self.root.tk.call("tk", "fontchooser", "show")
            self.canvas.bind('<Button-1>', self.put_text)

    def font_changed(self, font):
        """Сохраняет выбранный шрифт."""
        self.font = font

    def put_text(self, event):
        """Вставляет текст на холст."""
        x, y = event.x, event.y
        self.draw.text((x, y), text=self.text, fill=self.pen_color)
        self.canvas.create_text(x, y, text=self.text, fill=self.pen_color, font=self.font)
        self.canvas.unbind('<Button-1>')

    def save_image(self, event=None):
        """Сохраняет изображение."""
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def image_insert(self):
        """Вставляет изображение из файла."""
        file_path = filedialog.askopenfilename(filetypes=[("JPG files", ".jpg"), ("PNG files", ".png")])
        if file_path:
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.draw = ImageDraw.Draw(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
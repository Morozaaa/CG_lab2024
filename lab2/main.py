import cv2
import numpy as np
from tkinter import Tk, Label, Button, Scale, HORIZONTAL, filedialog, Frame, Canvas, Scrollbar
from PIL import Image, ImageTk

# Инициализация глобальных переменных для хранения изображений
img = None
img_otsu = None
img_adaptive = None
img_sharpen = None
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 450

# Функция для открытия и загрузки изображения
def open_image():
    global img, img_otsu, img_adaptive, img_sharpen

    # Открытие диалогового окна для выбора изображения
    filepath = filedialog.askopenfilename()
    if filepath:
        # Чтение изображения через OpenCV
        img = cv2.imread(filepath)

        # Создаем копии для каждого метода
        img_otsu = img.copy()
        img_adaptive = img.copy()
        img_sharpen = img.copy()

        # Преобразование для отображения через Tkinter (OpenCV использует BGR, а Tkinter — RGB)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Масштабирование изображения для большого разрешения
        img_resized = cv2.resize(img_rgb, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Преобразование изображения в формат PIL
        img_pil = Image.fromarray(img_resized)

        # Преобразование изображения PIL в формат, который может отображать Tkinter
        img_display = ImageTk.PhotoImage(image=img_pil)

        # Отображение изображения в интерфейсе (в каждом методе обновляется своя метка)
        img_label_otsu.config(image=img_display)
        img_label_otsu.image = img_display
        img_label_adaptive.config(image=img_display)
        img_label_adaptive.image = img_display
        img_label_sharpen.config(image=img_display)
        img_label_sharpen.image = img_display

# Функция для применения пороговой обработки (метод Оцу)
def apply_threshold_otsu():
    global img_otsu, img_display

    if img_otsu is not None:
        # Преобразование изображения в градации серого
        gray = cv2.cvtColor(img_otsu, cv2.COLOR_BGR2GRAY)

        # Применение метода Оцу
        _, img_processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Масштабирование изображения
        img_resized = cv2.resize(img_processed, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Преобразование изображения в формат PIL для отображения в Tkinter
        img_pil = Image.fromarray(img_resized)
        img_display = ImageTk.PhotoImage(image=img_pil)

        # Обновление изображения в метке для метода Оцу
        img_label_otsu.config(image=img_display)
        img_label_otsu.image = img_display

# Функция для применения адаптивной пороговой обработки
def apply_adaptive_threshold(val):
    global img_adaptive, img_display

    if img_adaptive is not None:
        # Преобразование изображения в градации серого
        gray = cv2.cvtColor(img_adaptive, cv2.COLOR_BGR2GRAY)

        # Получаем параметры из ползунков
        block_size = adaptive_block_size_slider.get()
        c_value = adaptive_c_slider.get()

        # Блок размера должен быть нечетным и больше 1
        if block_size % 2 == 0:
            block_size += 1
        if block_size < 3:
            block_size = 3

        # Применение адаптивной пороговой обработки
        img_processed = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c_value)

        # Масштабирование изображения
        img_resized = cv2.resize(img_processed, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Преобразование изображения в формат PIL для отображения в Tkinter
        img_pil = Image.fromarray(img_resized)
        img_display = ImageTk.PhotoImage(image=img_pil)

        # Обновление изображения в метке для адаптивного метода
        img_label_adaptive.config(image=img_display)
        img_label_adaptive.image = img_display

# Функция для применения фильтра резкости
def apply_sharpening(val):
    global img_sharpen, img_display

    if img_sharpen is not None:
        # Получаем коэффициент усиления резкости из ползунка
        sharpen_value = sharpen_slider.get() / 10.0

        # Ядро фильтра для резкости (можно регулировать степень резкости)
        kernel = np.array([[0, -1, 0],
                           [-1, 5 + sharpen_value, -1],
                           [0, -1, 0]])

        # Применение фильтра резкости
        img_processed = cv2.filter2D(img_sharpen, -1, kernel)

        # Преобразование для отображения через Tkinter
        img_rgb = cv2.cvtColor(img_processed, cv2.COLOR_BGR2RGB)

        # Масштабирование изображения
        img_resized = cv2.resize(img_rgb, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Преобразование изображения в формат PIL для отображения в Tkinter
        img_pil = Image.fromarray(img_resized)
        img_display = ImageTk.PhotoImage(image=img_pil)

        # Обновление изображения в метке для метода резкости
        img_label_sharpen.config(image=img_display)
        img_label_sharpen.image = img_display

# Инициализация главного окна Tkinter
root = Tk()
root.title("Image Processing App")
root.geometry("1500x1000")  # Увеличиваем размер главного окна для размещения всех элементов

# Добавляем область прокрутки (Canvas)
canvas = Canvas(root)
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Создаем фреймы для каждой секции: Оцу, адаптивный метод и резкость
otsu_frame = Frame(scrollable_frame)
otsu_frame.pack(pady=10)

adaptive_frame = Frame(scrollable_frame)
adaptive_frame.pack(pady=10)

sharpen_frame = Frame(scrollable_frame)
sharpen_frame.pack(pady=10)

# ОТСЕК МЕТОДА ОЦУ
# Кнопка для применения метода Оцу
btn_threshold_otsu = Button(otsu_frame, text="Apply Otsu Threshold", command=apply_threshold_otsu)
btn_threshold_otsu.pack()

# Виджет для отображения изображения метода Оцу
img_label_otsu = Label(otsu_frame, text="Otsu Threshold Result")
img_label_otsu.pack()

# ОТСЕК АДАПТИВНОЙ ПОРОГОВОЙ ОБРАБОТКИ
# Ползунок для адаптивной пороговой обработки (размер блока)
adaptive_block_size_slider = Scale(adaptive_frame, from_=3, to=51, orient=HORIZONTAL, label="Adaptive Block Size")
adaptive_block_size_slider.set(11)
adaptive_block_size_slider.pack()

# Ползунок для адаптивной пороговой обработки (значение C)
adaptive_c_slider = Scale(adaptive_frame, from_=-20, to=20, orient=HORIZONTAL, label="Adaptive C Value")
adaptive_c_slider.set(2)
adaptive_c_slider.pack()

# Кнопка для применения адаптивной пороговой обработки
btn_adaptive_threshold = Button(adaptive_frame, text="Apply Adaptive Threshold", command=lambda: apply_adaptive_threshold(0))
btn_adaptive_threshold.pack()

# Виджет для отображения изображения адаптивного метода
img_label_adaptive = Label(adaptive_frame, text="Adaptive Threshold Result")
img_label_adaptive.pack()

# ОТСЕК РЕЗКОСТИ
# Ползунок для настройки резкости
sharpen_slider = Scale(sharpen_frame, from_=0, to=30, orient=HORIZONTAL, label="Sharpening Strength")
sharpen_slider.set(10)
sharpen_slider.pack()

# Кнопка для применения фильтра резкости
btn_sharpen = Button(sharpen_frame, text="Sharpen Image", command=lambda: apply_sharpening(0))
btn_sharpen.pack()

# Виджет для отображения изображения метода резкости
img_label_sharpen = Label(sharpen_frame, text="Sharpening Result")
img_label_sharpen.pack()

# Кнопка для открытия изображения (можно добавить в начало окна)
btn_open = Button(scrollable_frame, text="Open Image", command=open_image)
btn_open.pack(pady=20)

# Упаковка Canvas и Scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Запуск интерфейса
root.mainloop()

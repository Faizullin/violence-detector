import json
import queue
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from dotenv import load_dotenv

from libs.detection_app import DetectionApp
from libs.model import Model
from libs.requester import ApiRequester

API_DEVICE_ID = None
API_KEY = None
API_URL = None


# Загрузка переменных окружения из файла .env
load_dotenv()


def load_data():
    global API_DEVICE_ID, API_KEY, API_URL
    with open("data.json", "r") as f:
        data = json.load(f)
        API_DEVICE_ID = data.get("API_DEVICE_ID")
        API_KEY = data.get("API_KEY")
        API_URL = data.get("API_URL")


load_data()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Программа Детекции")
        self.root.geometry("600x700")
        self.root.config(bg="#F5F5F5")

        # Инициализация APIRequester, Model и DetectionApp с очередью для общения между процессами
        self.queue = queue.Queue()  # Очередь для межпроцессного общения
        self.api_requester = ApiRequester(self.queue, api_device_id=API_DEVICE_ID, api_key=API_KEY,
                                          api_url=API_URL)
        self.api_requester.start()

        self.model = Model()  # Предполагается, что Model — это обработчик модели
        self.detection_app = DetectionApp(
            self.queue, self.model, self.api_requester)

        # Инициализация кнопок и компонентов интерфейса
        self.api_key_entry = None
        self.device_id_entry = None
        self.submit_button = None
        self.upload_button = None
        self.save_checkbox1 = None
        self.save_checkbox2 = None
        self.result_label = None
        self.file_path = None
        self.camera_running = False  # Для отслеживания состояния камеры

        # Пропустить первую страницу, если .env уже содержит значения
        if API_KEY and API_DEVICE_ID:
            self.show_main_page()
        else:
            self.show_first_page(intialize=True)

    def show_first_page(self, intialize=False):
        """Первая страница для ввода API ключа и ID устройства"""
        self.clear_window()

        self.title_label = tk.Label(self.root, text="Введите данные API", font=(
            "Arial", 16, "bold"), bg="#F5F5F5")
        self.title_label.pack(pady=20)

        self.api_key_label = tk.Label(self.root, text="API ключ", bg="#F5F5F5")
        self.api_key_label.pack()
        self.api_key_entry = tk.Entry(self.root, relief="solid", width=30)
        self.api_key_entry.pack(pady=5)

        self.device_id_label = tk.Label(
            self.root, text="ID устройства", bg="#F5F5F5")
        self.device_id_label.pack()
        self.device_id_entry = tk.Entry(self.root, relief="solid", width=30)
        self.device_id_entry.pack(pady=5)

        self.submit_button = tk.Button(
            self.root, text="Отправить", command=self.save_api_details, bg="#4CAF50", fg="white")
        self.submit_button.pack(pady=10)

        if not intialize:
            self.back_button = tk.Button(
                self.root, text="Назад", command=self.show_main_page, bg="#FF5722", fg="white")
            self.back_button.pack(pady=10)

    def save_api_details(self):
        """Сохранить данные API в json файл"""
        global API_URL, API_KEY, API_DEVICE_ID
        API_KEY = self.api_key_entry.get()
        API_DEVICE_ID = self.device_id_entry.get()

        with open('data.json', 'w') as f:
            json.dump({
                "API_KEY": API_KEY,
                "API_URL": API_URL,
                "API_DEVICE_ID": API_DEVICE_ID,
            }, f)

        self.api_requester.api_key = API_KEY
        self.api_requester.api_device_id = API_DEVICE_ID
        self.api_requester.api_url = API_URL

        messagebox.showinfo("Успех", "Данные API успешно сохранены!")
        self.show_main_page()

    def show_main_page(self):
        """Главная страница с переходом к другим страницам"""
        self.clear_window()

        self.main_label = tk.Label(self.root, text="Главная страница", font=(
            "Arial", 18, "bold"), bg="#F5F5F5")
        self.main_label.pack(pady=20)

        self.process_button = tk.Button(
            self.root, text="Обработать изображение", command=self.show_second_page, bg="#2196F3", fg="white")
        self.process_button.pack(pady=10)

        self.camera_button = tk.Button(
            self.root, text="Открыть камеру", command=self.show_third_page, bg="#FF5722", fg="white")
        self.camera_button.pack(pady=10)

        self.env_button = tk.Button(
            self.root, text="Настройки", command=self.show_first_page, bg="#FFC107", fg="white")
        self.env_button.pack(pady=10)

    def show_second_page(self):
        """Вторая страница для загрузки и обработки изображения"""
        self.clear_window()

        self.file_path = None

        self.image_label = tk.Label(
            self.root, text="Загрузите изображение для обработки", font=("Arial", 14), bg="#F5F5F5")
        self.image_label.pack(pady=20)

        self.upload_button = tk.Button(
            self.root, text="Загрузить изображение", command=self.upload_image, bg="#4CAF50", fg="white")
        self.upload_button.pack(pady=10)

        self.file_label = tk.Label(
            self.root, text="Файл не выбран", bg="#F5F5F5")
        self.file_label.pack()

        self.save_checkbox1_val = tk.BooleanVar()
        self.save_checkbox1 = tk.Checkbutton(
            self.root, text="Сохранить изображение", variable=self.save_checkbox1_val, bg="#F5F5F5")
        self.save_checkbox1.pack(pady=10)

        self.submit_button = tk.Button(
            self.root, text="Обработать изображение", command=self.process_image, bg="#2196F3", fg="white")
        self.submit_button.pack(pady=10)

        # Добавить кнопку "Назад"
        self.back_button = tk.Button(
            self.root, text="Назад", command=self.show_main_page, bg="#FF5722", fg="white")
        self.back_button.pack(pady=10)

    def upload_image(self):
        """Загрузить изображение"""
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        self.file_label.config(text=self.file_path)

    def process_image(self):
        """Обработать изображение с помощью модели и отправить запрос на сервер"""
        self.submit_button.config(
            state="disabled", text="Обработка...")  # Отключить кнопку во время обработки

        if not self.file_path:
            messagebox.showerror("Ошибка", "Изображение не выбрано!")
            self.submit_button.config(
                state="normal", text="Обработать изображение")
            return

        # Обработка изображения с помощью модели (Clip)
        image = cv2.imread(self.file_path)
        result1 = self.detection_app.detect_from_image(image)
        print("результат", result1)

        # Отображение результата на второй странице
        self.result_label = tk.Label(
            self.root, text=f"Результат предсказания: {result1}", font=("Arial", 12), bg="#F5F5F5")
        self.result_label.pack(pady=10)

        # Проверка состояния флажка
        # Получить состояние флажка (True или False)
        save_to_server = self.save_checkbox1_val.get()

        data = {
            "prediction1": json.dumps({
                "prediction": result1,
            }),
            "device_id": API_DEVICE_ID,
            "save_to_server": save_to_server,
        }

        # Отправить запрос в зависимости от значения флажка (сохранить на сервере или нет)
        result2 = self.api_requester.send_request_api(data, image)

        # Обработка ответа от сервера (опционально: показать дополнительную информацию, если успешно)
        if result2 and result2.status_code == 200:
            result2_text = "Ответ сервера: \n"

            result2_json = result2.json()
            pred_data = result2_json['data']['pred']
            result2_text += "Обнаружено: " + pred_data['prediction1']['prediction']['label'] + " с уверенностью: " + str(
                round(pred_data['prediction1']['prediction']['confidence'], 4)) + "\n"
            result2_text += "Обнаружено: " + pred_data['prediction2'][0]['message'] + " с уверенностью: " + str(
                round(pred_data['prediction2'][0]['prediction'], 4)) + "\n"
            result2_text += "Предсказания сохранены: " + \
                ("сохранено" if result2_json['data']
                 ['saved'] else "не сохранено") + "\n"
            result2_text += "Новости сохранены: " + \
                ("сохранено" if result2_json['data']
                 ['news_saved'] else "не сохранено") + "\n"
            self.result_label.config(text=result2_text)

        self.submit_button.config(
            state="normal", text="Обработать изображение")  # Включить кнопку

    def show_third_page(self):
        """Третья страница для камеры"""
        self.clear_window()

        self.title_label = tk.Label(
            self.root, text="Открыть камеру для обработки", font=("Arial", 14, "bold"), bg="#F5F5F5")
        self.title_label.pack(pady=20)

        self.start_button = tk.Button(
            self.root, text="Начать съемку", command=self.start_camera, bg="#4CAF50", fg="white")
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            self.root, text="Остановить съемку", command=self.stop_camera, bg="#FF5722", fg="white")
        self.stop_button.pack(pady=10)

        self.back_button = tk.Button(
            self.root, text="Назад", command=self.show_main_page, bg="#FFC107", fg="white")
        self.back_button.pack(pady=10)

    def start_camera(self):
        """Запуск камеры"""
        if self.camera_running:
            return

        self.camera_running = True
        self.detection_app.start_camera()

    def stop_camera(self):
        """Остановка камеры"""
        if not self.camera_running:
            return

        self.camera_running = False
        self.detection_app.stop_camera()

    def clear_window(self):
        """Очистить окно"""
        for widget in self.root.winfo_children():
            widget.destroy()


# Создание и запуск главного окна
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

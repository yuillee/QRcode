import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from pyzbar.pyzbar import decode
import cv2

def load_valid_ids(filename="valid_ids.txt"):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл базы {filename} не найден!")
        return []

valid_ids = load_valid_ids()

def scan_from_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    image = Image.open(file_path)
    decoded_objects = decode(image)
    if not decoded_objects:
        messagebox.showinfo("Результат", "QR-код не найден.")
        return

    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        if data in valid_ids:
            messagebox.showinfo("Результат", f"Пропуск действителен.\nID: {data}")
        else:
            messagebox.showwarning("Результат", f"Доступ запрещён.\nНеизвестный ID: {data}")

def scan_from_camera():
    cap = cv2.VideoCapture(0)
    found = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objects = decode(frame)
        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            cv2.rectangle(frame, (obj.rect.left, obj.rect.top),
                          (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height),
                          (0, 255, 0), 2)
            cv2.putText(frame, data, (obj.rect.left, obj.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            if data in valid_ids:
                messagebox.showinfo("Результат", f"Пропуск действителен.\nID: {data}")
            else:
                messagebox.showwarning("Результат", f"Доступ запрещён.\nНеизвестный ID: {data}")
            found = True
            break

        cv2.imshow("Сканер пропусков (Нажмите Q для выхода)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or found:
            break

    cap.release()
    cv2.destroyAllWindows()

root = tk.Tk()
root.title("Пропускная система")

label = tk.Label(root, text="Пожалуйста, предъявите QR-пропуск", font=("Arial", 14))
label.pack(pady=10)

btn_camera = tk.Button(root, text="Сканировать с камеры", font=("Arial", 12), command=scan_from_camera)
btn_camera.pack(pady=5)

btn_file = tk.Button(root, text="Загрузить пропуск (фото)", font=("Arial", 12), command=scan_from_image)
btn_file.pack(pady=5)

root.mainloop()
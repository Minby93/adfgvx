import tkinter as tk
from tkinter import messagebox

# Создание квадрата Полибия
def generate_polybius_square():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Алфавит [A-Z, 0-9]
    square = {}
    adfgvx = "ADFGVX"
    index = 0
    for row in adfgvx:
        for col in adfgvx:
            square[row + col] = alphabet[index]
            index += 1
    return square

# Шифрование с помощью квадрата Полибия
def encrypte(message, key):
    encrypted_message = ""
    square = generate_polybius_square()
    for char in message.upper():  # Делаю все буквы сообщения заглавными
        for k, value in square.items():
            if value == char:
                encrypted_message += k
                break
    encrypted_message = final_encrypte(encrypted_message, key)  
    return encrypted_message

# Окончательное шифрование с помощью ключевого слова
def final_encrypte(message, key):
    while(len(message) % len(key) != 0):  # Выравнивание длины сообщения в зависимости от длины ключа
        message += "X"

    encrypted_message = ""
    columns = {k: [] for k in key}

    for i, char in enumerate(message):  # Запись сообщения в колонки относительно ключа
        columns[key[i % len(key)]].append(char)
        
    sorted_columns = dict(sorted(columns.items()))  # Перестановка столбцов при сортировки ключа по алфавиту

    for k in sorted_columns:
        encrypted_message += "".join(sorted_columns[k])  # Запись зашифрованного сообщения
    
    return encrypted_message

# Окончательная дешифровка по квадрату Полибия
def decrypte_square(message, square):
    decrypted_message = ""
    for i in range(0, len(message), 2):
        for key, value in square.items():
            if len(message[i:]) >= 2:  # Чтобы не было выхода за границы массива
                if (message[i] + message[i + 1]) == key:  # Беру по 2 символа из зашифрованного сообщения и ищу их значение в квадрате Полибия
                    decrypted_message += value
    return decrypted_message

# Дешифровка сообщения в состояния для расшифровки квадратом Полибия
def decrypte(message, key):
    decrypted_message = ""
    col_size = len(message) // len(key)  # Нахожу длину колонки

    columns = {k: [] for k in sorted(key)}
    temp_message = message
    for k in columns:  # Привожу к виду колонок отсортированных по ключу
        for i in range(col_size):
            columns[k].append(temp_message[i])       
        temp_message = temp_message[col_size:]

    unsorted_key_columns = {k: [] for k in key}
    for k in columns:  # Возвращаю колонки с изначальному положению (ключ без сортировик по алфавиту)
        for i in unsorted_key_columns:
            if k == i:
                unsorted_key_columns[k] = columns[i]
                break
    
    for i in range(col_size):  # Приведение к строке для дальнейшей дешифровки по квадрату Полибия
        for k in unsorted_key_columns:
            decrypted_message += unsorted_key_columns[k][i]

    return decrypte_square(decrypted_message, generate_polybius_square())

# Интерфейс приложения
def encrypt_text():
    try:
        message = input_text.get("1.0", tk.END).strip()
        key = key_entry.get().strip()
        if not message or not key:
            messagebox.showerror("Ошибка", "Введите текст и ключ.")
            return
        encrypted_message = encrypte(message, key)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, encrypted_message)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def decrypt_text():
    try:
        message = input_text.get("1.0", tk.END).strip()
        key = key_entry.get().strip()
        if not message or not key:
            messagebox.showerror("Ошибка", "Введите текст и ключ.")
            return
        decrypted_message = decrypte(message, key)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decrypted_message)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# Создаем главное окно
window = tk.Tk()
window.title("Шифр ADFGVX")

# Метка для ввода текста
input_label = tk.Label(window, text="Введите текст:")
input_label.pack()

# Поле ввода текста
input_text = tk.Text(window, height=5, width=40)
input_text.pack()

# Метка для ввода ключа
key_label = tk.Label(window, text="Введите ключ:")
key_label.pack()

# Поле ввода ключа
key_entry = tk.Entry(window)
key_entry.pack()

# Кнопка для шифрования
encrypt_button = tk.Button(window, text="Зашифровать", command=encrypt_text)
encrypt_button.pack()

# Кнопка для дешифровки
decrypt_button = tk.Button(window, text="Расшифровать", command=decrypt_text)
decrypt_button.pack()

# Поле вывода результата
output_label = tk.Label(window, text="Результат:")
output_label.pack()

# Поле вывода текста
output_text = tk.Text(window, height=10, width=40)
output_text.pack()

# Запуск главного цикла
window.mainloop()



    




    
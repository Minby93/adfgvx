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
    padding_len = 0
    if len(message) % len(key) != 0:  # Проверка на необходимость добавления символов выравнивания
        padding_len = len(key) - len(message) % len(key)  # Сколько символов нужно добавить
        message += "X" * padding_len  # Добавляю символы выравнивания

    encrypted_message = ""
    key_indices = list(range(len(key)))  # Индексы символов ключа
    columns = {i: [] for i in key_indices}

    for i, char in enumerate(message):  # Запись сообщения в колонки относительно индексов ключа
        columns[i % len(key)].append(char)
        
    sorted_key_indices = sorted(key_indices, key=lambda x: key[x])  # Сортировка индексов ключа по алфавиту символов ключа

    for k in sorted_key_indices:
        encrypted_message += "".join(columns[k])  # Запись зашифрованного сообщения
    
    return encrypted_message + str(padding_len)  # Добавляем количество добавленных символов в конец строки

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
    # Извлекаем количество добавленных символов
    padding_len = int(message[-1])  # Последний символ — это количество добавленных символов
    message = message[:-1]  # Удаляем этот символ

    decrypted_message = ""
    col_size = len(message) // len(key)  # Нахожу длину колонки

    key_indices = list(range(len(key)))  # Индексы символов ключа
    sorted_key_indices = sorted(key_indices, key=lambda x: key[x])  # Сортировка индексов ключа по алфавиту символов ключа

    columns = {i: [] for i in sorted_key_indices}
    temp_message = message
    for i in sorted_key_indices:  # Привожу к виду колонок отсортированных по ключу
        for j in range(col_size):
            columns[i].append(temp_message[j])       
        temp_message = temp_message[col_size:]

    unsorted_key_columns = {i: [] for i in key_indices}
    for i in sorted_key_indices:  # Возвращаю колонки к изначальному положению
        unsorted_key_columns[i] = columns[i]

    for i in range(col_size):  # Приведение к строке для дальнейшей дешифровки по квадрату Полибия
        for j in key_indices:
            decrypted_message += unsorted_key_columns[j][i]
    if padding_len > 0:
        decrypted_message = decrypted_message[:-padding_len]  # Удаление лишних символов
    # Удаление добавленных символов выравнивания
    decrypted_message = decrypte_square(decrypted_message, generate_polybius_square())

    return decrypted_message

# Тестирование
# encrypted_message = encrypte("password", "kky")
# print(encrypted_message)
# print(decrypte(encrypted_message, "kky"))

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
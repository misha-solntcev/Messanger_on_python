from flask import Flask, request, render_template
from datetime import datetime
import json

application = Flask(__name__)  # Создаем Flask-приложение
# Начинаем писать мессенджер
DB_FILE = "./data/db.json"


# Функция чтения сообщений из файла
def load_messages():
    json_file = open(DB_FILE, "r")
    data = json.load(json_file)
    return data["messages"]


all_messages = load_messages()  # Список всех сообщений


# Функция сохранения сообщений в файл
def save_messages():
    data = {
        "messages": all_messages
    }
    json_file = open(DB_FILE, "w")  # Открываем файл для записи
    json.dump(data, json_file)
    return


@application.route("/chat")
def display_chat():
    return render_template("form.html")  # Показываем файл из папки templates


@application.route("/")
def index_page():
    return "Hello, welcome to Skillbox chat"


@application.route("/get_messages")
def get_messages():
    return {"messages": all_messages}


@application.route("/send_message")
def send_message():
    # Получаем информацию от пользователя
    sender = request.args["name"]
    text = request.args["text"]
    # Добавляем сообщение в список
    add_message(sender, text)
    save_messages()
    return "Ok"


def add_message(sender, text):
    # 1. Подготовить словарь с данными сообщения.
    new_message = {
        "sender": sender,
        "text": text,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    # 2. Добавить получившийся словарь в список сообщений.
    all_messages.append(new_message)


def print_message(mess):
    print(f"[{mess['sender']}]:  {mess['text']} / {mess['time']}")


# add_message("Миша", "Всем привет")
# add_message("Вася", "Здорово!")
#
# for message in all_messages:
#     print_message(message)

application.run(host='0.0.0.0', port=80)  # Запускаем Flask-приложение

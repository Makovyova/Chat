import telebot
from telebot import types
import database  # Импорт функций работы с базой данных
import messages  # Импорт текстов сообщений
import tasks  # Импорт функций для работы с заданиями

TOKEN = "7837829015:AAHatd5nNchwGV0WpB8BxLP5evVuJw6R7LM"  # Замените на ваш токен бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if not database.user_exists(user_id):
        database.add_user(user_id, user_name)  # добавление нового пользователя
    bot.send_message(message.chat.id, messages.welcome_message(user_name))  # Приветствие
    main_menu(message)

@bot.message_handler(commands=['menu'])
def main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("Лексика"),
        types.KeyboardButton("Грамматика"),
        types.KeyboardButton("Личный кабинет")
    ]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, messages.choose_section_message, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Лексика")
def handle_lexic(message):
    user_id = message.from_user.id
    task, task_type = tasks.get_lexic_task()
    if task is None:
        bot.send_message(message.chat.id, "Нет доступных заданий")
        return
    current_tasks[user_id] = (task, task_type)  # Запоминаем текущее задание
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(option) for option in task['options']]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, f"{task['question']}", reply_markup=keyboard)  # Отправляем вопрос с вариантами

# Обработчик всех текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    user_answer = message.text
    if user_id in current_tasks:
        task, task_type = current_tasks[user_id]
        if task_type == "lexic":
            if tasks.check_answer(user_answer, task['answer']):
                bot.send_message(message.chat.id, "Правильно!")
                database.save_progress(user_id, task['task_id'], 1)  # сохранение прогресса
            else:
                bot.send_message(message.chat.id, f"Неправильно. Правильный ответ: {task['answer']}")
                database.save_progress(user_id, task['task_id'], 0)  # сохранение прогресса
            del current_tasks[user_id]  # удаляем текущее задание
            main_menu(message)  # возврат в основное меню
        else:
            bot.send_message(message.chat.id, messages.default_message)  # Если тип задания не определен
    elif message.text == "Личный кабинет":
        personal_cabinet(message)
    else:
        bot.send_message(message.chat.id, messages.default_message)  # Если не было запроса задания

# Личный кабинет
@bot.message_handler(func=lambda message: message.text == "Личный кабинет")
def personal_cabinet(message):
    user_id = message.from_user.id
    user_data = database.get_user_data(user_id)
    progress = database.get_user_progress(user_id)
    bot.send_message(message.chat.id, messages.personal_cabinet_message(user_data, progress))

# Добавление задания
@bot.message_handler(func=lambda message: message.text == "Добавить задание")
def add_task_handler(message):
    bot.send_message(message.chat.id, "Введите тип задания (lexic, grammar):")
    bot.register_next_step_handler(message, process_task_type)

def process_task_type(message):
    task_type = message.text.strip()
    bot.send_message(message.chat.id, "Введите текст задания:")
    bot.register_next_step_handler(message, process_question, task_type)

def process_question(message, task_type):
    question = message.text.strip()
    bot.send_message(message.chat.id, "Введите варианты ответа через запятую (если есть):")
    bot.register_next_step_handler(message, process_options, task_type, question)

def process_options(message, task_type, question):
    options = [opt.strip() for opt in message.text.split(',')]
    bot.send_message(message.chat.id, "Введите правильный ответ:")
    bot.register_next_step_handler(message, process_answer, task_type, question, options)

def process_answer (message, task_type, question, options):
    answer = message.text.strip()
    database.add_task(task_type, question, options, answer)
    bot.send_message(message.chat.id, "Задание добавлено!")
    main_menu(message)  # возврат в основное меню

if __name__ == '__main__':
    database.init_db()
    bot.polling(none_stop=True)







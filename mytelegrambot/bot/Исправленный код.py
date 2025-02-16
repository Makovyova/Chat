
import telebot
from telebot import types
import database  # Импорт функций работы с базой данных
import messages  # Импорт текстов сообщений
import tasks  # Импорт функций для работы с заданиями

TOKEN = "7837829015:AAHatd5nNchwGV0WpB8BxLP5evVuJw6R7LM" # Замените на ваш токен бота
bot = telebot.TeleBot(TOKEN)

current_tasks = {}  # Словарь для хранения текущих заданий у пользователя
current_section = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if not database.user_exists(user_id):
        database.add_user(user_id, user_name)  # Добавление нового пользователя
    bot.send_message(message.chat.id, messages.welcome_message(user_name))  # Приветствие
    main_menu(message)

@bot.message_handler(commands=['menu'])
def main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("Лексика"),
        types.KeyboardButton("Грамматика"),
        types.KeyboardButton("Аудирование"),
        types.KeyboardButton("Личный кабинет"),
        types.KeyboardButton("Перезагрузка")
    ]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, messages.choose_section_message, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Личный кабинет")
def personal_cabinet(message):
    user_id = message.from_user.id
    user_data = database.get_user_data(user_id)
    progress = None  # Замените на логику получения прогресса
    bot.send_message(message.chat.id, messages.personal_cabinet_message(user_data, progress))

@bot.message_handler(func=lambda message: message.text == "Лексика")
def vocabulary_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    topics = ["Авиационный алфавит", "Часто используемые фразы", "Терминология при ЧС", "Навигация", "Аббревиатуры", "Шарады", "Назад"]
    buttons = [types.KeyboardButton(topic) for topic in topics]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, "Выберите подраздел лексики:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Авиационный алфавит")
def show_aviation_alphabet(message):
    alphabet = tasks.get_aviation_alphabet()
    alphabet_text = "\n".join([f"{letter}: {code}" for letter, code in alphabet.items()])
    bot.send_message(message.chat.id, f"Авиационный алфавит:\n{alphabet_text}")

@bot.message_handler(func=lambda message: message.text == "Часто используемые фразы")
def show_common_phrases(message):
    phrases = tasks.get_common_phrases()
    phrases_text = "\n".join(phrases)
    bot.send_message(message.chat.id, f"Наиболее часто используемые фразы:\n{phrases_text}")
 

@bot.message_handler(func=lambda message: message.text == "Терминология при ЧС")
def show_emergency_terms(message):
    terms = tasks.get_emergency_terms()
    terms_text = "\n".join(terms)
    bot.send_message(message.chat.id, f"Терминология при чрезвычайных ситуациях:\n{terms_text}")

@bot.message_handler(func=lambda message: message.text == "Навигация")
def show_navigation_terms(message):
    terms = tasks.get_navigation_terms()
    terms_text = "\n".join(terms)
    bot.send_message(message.chat.id, f"Навигационные термины:\n{terms_text}")

@bot.message_handler(func=lambda message: message.text == "Аббревиатуры")
def show_abbreviations(message):
    abbreviations = tasks.get_abbreviations()
    abbreviations_text = "\n".join(abbreviations)
    bot.send_message(message.chat.id, f"Аббревиатуры:\n{abbreviations_text}")

@bot.message_handler(func=lambda message: message.text == "Шарады")
def show_charade(message):
    user_id = message.from_user.id  # Получаем user_id из message
    current_section[user_id] = "Шарады"  # Fix: Added user_id
    charade_data = tasks.get_random_charade()
    current_tasks[user_id] = charade_data # Сохраняем шараду для проверки ответа

    keyboard = types.InlineKeyboardMarkup()
    show_answer_button = types.InlineKeyboardButton(text="Показать ответ", callback_data="show_answer")
    keyboard.add(show_answer_button)

    bot.send_message(message.chat.id, f"Шарада:\n{charade_data['charade']}", reply_markup=keyboard)

# Обработчик callback-запросов (для InlineKeyboardButton)
@bot.callback_query_handler(func=lambda call: call.data == "show_answer")
def show_correct_answer(call):
    user_id = call.from_user.id
    if user_id in current_tasks:
        correct_answer = current_tasks[user_id]['answer']
        bot.send_message(call.message.chat.id, f"Правильный ответ: {correct_answer}")
        del current_tasks[user_id]
        main_menu(call.message) #Возвращаемся в главное меню
    else:
        bot.send_message(call.message.chat.id, "Шарада не найдена.")

@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_main_menu(message):
    main_menu(message)

# Обработчик ответов на шарады (если пользователь вводит ответ текстом)
@bot.message_handler(func=lambda message: message.from_user.id in current_tasks and current_section.get(message.from_user.id) == "Шарады")
def check_charade_answer(message):
    user_id = message.from_user.id
    user_answer = message.text.lower()
    correct_answer = current_tasks[user_id]['answer'].lower()
    if user_answer == correct_answer:
        bot.send_message(message.chat.id, "Правильно!")
    else:
        bot.send_message(message.chat.id, f"Неправильно. Правильный ответ: {correct_answer}")
    del current_tasks[user_id]
    del current_section[user_id]
    main_menu(message)
    

@bot.message_handler(func=lambda message: message.text == "Грамматика")
def handle_grammar(message):
    user_id = message.from_user.id
    current_section[user_id] = "Грамматика"  # Set current section to 'grammar'
    task, task_type = tasks.get_task("grammar")

    if task is None:
        bot.send_message(message.chat.id, "Нет доступных заданий.")
        return

    current_tasks[user_id] = task  # Сохраняем текущее задание

    # Проверяем, есть ли опции в задании
    if 'options' in task and task['options']:
        options = task['options']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True) # Added one_time_keyboard
        
        # Создаем кнопки только если опции есть
        buttons = [types.KeyboardButton(option) for option in options]
        keyboard.add(*buttons)
        
        bot.send_message(message.chat.id, task['question'], reply_markup=keyboard)
    else:
        # Если нет опций, просто отправляем вопрос без клавиатуры
        bot.send_message(message.chat.id, task['question'])

@bot.message_handler(content_types=['text'])
def handle_answer(message):
    user_id = message.from_user.id

    if user_id in current_tasks and current_section.get(user_id) in ["Грамматика", "Шарады"]:
        task = current_tasks[user_id]
        
        if current_section[user_id] == "Грамматика":
            # Check if the task has options
            if 'options' in task and task['options']:
                if message.text in task['options']:
                    if tasks.check_answer(message.text, task['answer']):
                        bot.send_message(message.chat.id, "Правильно! Следующее задание:")
                    else:
                        bot.send_message(message.chat.id, f"Неправильно. Правильный ответ: {task['answer']}")
                    # Remove the current task and section after answering
                    del current_tasks[user_id]
                    del current_section[user_id]
                    handle_grammar(message)
                else:
                    bot.send_message(message.chat.id, "Пожалуйста, выберите один из предложенных вариантов.")
            else:
                # Handle tasks without options
                if tasks.check_answer(message.text, task['answer']):
                    bot.send_message(message.chat.id, "Правильно! Следующее задание:")
                else:
                    bot.send_message(message.chat.id, f"Неправильно. Правильный ответ: {task['answer']}")
                # Remove the current task and section after answering
                del current_tasks[user_id]
                del current_section[user_id]
                handle_grammar(message)

        elif current_section[user_id] == "Шарады":
           # This is handled by check_charade_answer function.  No need to duplicate the logic.
           pass # Let check_charade_answer handle it.

    else:
        bot.send_message(message.chat.id, "Сначала выберите раздел.")
    
    


@bot.message_handler(func=lambda message: message.text == "Перезагрузка")
def reset_dialog(message):
    #  Этот код просто отправляет сообщение, говорящее пользователю, что он может очистить историю вручную.
    bot.send_message(message.chat.id, "История диалога не может быть очищена автоматически. Вы можете очистить ее вручную в настройках Telegram.  Сейчас я верну вас в главное меню.")
    main_menu(message)






# Функция для добавления задания
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
    options = [opt.strip() for opt in message.text.split(',')] if message.text else []
    bot.send_message(message.chat.id, "Введите правильный ответ:")
    bot.register_next_step_handler(message, process_answer, task_type, question, options)

def process_answer(message, task_type, question, options):
    answer = message.text.strip()
    database.add_task(task_type, question, options, answer)
    bot.send_message(message.chat.id, "Задание добавлено!")
    main_menu(message)  # возврат в основное меню


if __name__ == '__main__':
    database.init_db()
    tasks.add_grammar_tasks()  # Правильный вызов функции
    bot.polling(none_stop=True)

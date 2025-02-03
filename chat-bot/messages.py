def welcome_message(user_name):
    return f"Привет, {user_name}! Я бот для изучения английского."

choose_section_message = "Выберите раздел:"

def personal_cabinet_message(user_data, progress):
    user_name, level = user_data
    message = f"Ваше имя: {user_name}, Ваш уровень: {level}\n\nСтатистика:\n"
    if progress:
      for question, correct in progress:
        message += f"- Вопрос: {question}, Ответ: {'верно' if correct else 'неверно'}\n"
    else:
      message += "Еще нет статистики"

    return message
default_message = "Я не понимаю вас."

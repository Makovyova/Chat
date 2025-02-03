import random
import sqlite3
import json

def get_lexic_task():
    conn = sqlite3.connect("english_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, question, options, answer FROM tasks WHERE type = 'lexic'")
    tasks = cursor.fetchall()
    conn.close()
    if not tasks:
        return None, None
    task = random.choice(tasks)
    task_id, question, options, answer = task
    options_list = json.loads(options)
    return {
        'task_id': task_id,
        'question': question,
        'options': options_list,
        'answer': answer
    }, 'lexic'


def get_grammar_task():
    conn = sqlite3.connect("english_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, question, options, answer FROM tasks WHERE type = 'grammar'")
    tasks = cursor.fetchall()
    conn.close()
    if not tasks:
        return None, None
    task = random.choice(tasks)
    task_id, question, options, answer = task
    return {
        'task_id': task_id,
        'question': question,
        'options': options,
        'answer': answer
    }, 'grammar'

def check_answer(user_answer, correct_answer):
    return user_answer.lower().strip() == correct_answer.lower().strip()

# Функция для добавления заданий на грамматику (можно убрать после заполнения базы)
def add_grammar_tasks():
    conn = sqlite3.connect("english_bot.db")
    cursor = conn.cursor()

    grammar_tasks = [
        # Present Simple
        ("grammar", "Я читаю книгу каждый день.", None, "I read a book every day."),
        ("grammar", "Она работает в офисе.", None, "She works in an office."),
        ("grammar", "Они играют в футбол по субботам.", None, "They play football on Saturdays."),

        # Present Continuous
        ("grammar", "Я сейчас готовлю ужин.", None, "I am cooking dinner now."),
        ("grammar", "Он сейчас смотрит телевизор.", None, "He is watching TV now."),
        ("grammar", "Они сейчас учатся в университете.", None, "They are studying at the university now."),

        # Past Simple
        ("grammar", "Я вчера посмотрел фильм.", None, "I watched a movie yesterday."),
        ("grammar", "Она приготовила пирог на день рождения.", None, "She baked a cake for the birthday."),
        ("grammar", "Они посетили музей на прошлой неделе.", None, "They visited the museum last week."),

        # Past Continuous
        ("grammar", "Я читал книгу, когда она позвонила.", None, "I was reading a book when she called."),
        ("grammar", "Он играл в компьютерные игры весь вечер.", None, "He was playing computer games all evening."),
        ("grammar", "Они работали над проектом вчера в 5 часов.", None, "They were working on the project yesterday at 5 o'clock."),

        # Present Perfect
        ("grammar", "Я уже прочитал эту книгу.", None, "I have already read this book."),
        ("grammar", "Она только что закончила работу.", None, "She has just finished work."),
        ("grammar", "Они никогда не были в Париже.", None, "They have never been to Paris."),

        # Past Perfect
        ("grammar", "Я уже пообедал, когда пришел друг.", None, "I had already had lunch when my friend arrived."),
        ("grammar", "Она закончила работать до того, как начался дождь.", None, "She had finished working before it started raining."),
        ("grammar", "Они уже сдали экзамены к тому моменту, когда начались каникулы.", None, "They had already passed the exams by the time the holidays started."),

        # Future Simple
        ("grammar", "Я пойду в кино завтра.", None, "I will go to the cinema tomorrow."),
        ("grammar", "Она позвонит тебе вечером.", None, "She will call you in the evening."),
        ("grammar", "Они будут играть в теннис на выходных.", None, "They will play tennis at the weekend."),

        # Future Continuous
        ("grammar", "Я буду спать в это время завтра.", None, "I will be sleeping at this time tomorrow."),
        ("grammar", "Он будет работать допоздна завтра вечером.", None, "He will be working late tomorrow evening."),
        ("grammar", "Они будут смотреть фильм в 8 часов.", None, "They will be watching a movie at 8 o'clock.")
    ]


    for task_type, question, options, answer in grammar_tasks:
      cursor.execute(
          "INSERT INTO tasks (type, question, options, answer) VALUES (?, ?, ?, ?)",
          (task_type, question, json.dumps(options), answer)
      )
    conn.commit()
    conn.close()


if __name__ == '__main__':
  add_grammar_tasks()  # Вызов функции для заполнения базы данных (запускать только один раз)

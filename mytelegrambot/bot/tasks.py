import random
import sqlite3
import json

def get_task(task_type):
    conn = sqlite3.connect("english_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, question, options, answer FROM tasks WHERE type = ?", (task_type,))
    tasks = cursor.fetchall()
    conn.close()
    if not tasks:
        return None, None  # Если заданий нет, возвращаем None
    task = random.choice(tasks)
    task_id, question, options, answer = task
    return {
        'task_id': task_id,
        'question': question,
        'options': json.loads(options) if options else [],  # Преобразуем JSON-строку в список
        'answer': answer
    }, task_type

def check_answer(user_answer, correct_answer):
    return user_answer.lower().strip() == correct_answer.lower().strip()

def add_grammar_tasks():
    conn = sqlite3.connect("english_bot.db")
    cursor = conn.cursor()

    grammar_tasks = [
        # Present Simple
        ("grammar", "Pr.Sim. Я читаю книгу каждый день.", None, "I read a book every day."),
        ("grammar", "Pr.Sim. Она работает в офисе.", None, "She works in an office."),
        ("grammar", "Pr.Sim. Они играют в футбол по субботам.", None, "They play football on Saturdays."),
	("grammar", "Pr.Sim. Она не работает в отеле.", None, "She does not work in a hotel."),
        ("grammar", "Pr.Sim. Они завтракают каждый день в 8 утра.", None, "They have a breafast at 8 o'clock every day."),
        ("grammar", "Pr.Sim. Джон любит яблоки", None, "John likes apples."),
	("grammar", "Pr.Sim. Самолет прилетает в 5:40.", None, "The aircraft arrives at 5:40 am."),
	("grammar", "Pr.Sim. Почему ты всегда приходишь вовремя?", None, "Why do you always come in time?."),


        # Present Continuous
        ("grammar", "Pr. Cont. Я сейчас готовлю ужин.", None, "I am cooking dinner now."),
        ("grammar", "Pr. Cont. Он сейчас смотрит телевизор.", None, "He is watching TV now."),
        ("grammar", "Pr. Cont. Они сейчас учатся в университете.", None, "They are studying at the university now."),
	("grammar", "Pr. Cont. Сейчас идет дождь?.", None, "Is it raining now?."),
        ("grammar", "Pr. Cont. Катя усердно работает в эти дни.", None, "Kate is working hard thees days."),
	("grammar", "Pr. Cont. Он отдыхает в данный момент.", None, "He is resting at the moment."),
	("grammar", "Pr. Cont. Селена выходит замуж сегодня в 13:00.", None, "Selena is getting married at 13:00 pm."),
	("grammar", "Pr. Cont. Что она сейчас делает? Она не работает сейчас.", None, "What is she doing now? She is not working now."),
	


        # Past Simple
        ("grammar", "Pst. Sim. Я вчера посмотрел фильм.", None, "I watched a movie yesterday."),
        ("grammar", "Pst. Sim. Она приготовила пирог на день рождения.", None, "She baked a cake for the birthday."),
        ("grammar", "Pst. Sim. Они посетили музей на прошлой неделе.", None, "They visited the museum last week."),
	("grammar", "Pst. Sim. Он позвонил его начальнику, затем прочитал газету.", None, "He called his boss, then he read the newspaper."),
	("grammar", "Pst. Sim. Кто ходил в университет вчера? Никто.", None, "Who went to the university yesterday? Nobody did."),
	("grammar", "Pst. Sim. Вчера шел дождь?.", None, "Did it rain yesteday?."),
	("grammar", "Pst. Sim. Они провели их выходные в Москве.", None, "They spent their holidays in Moscow."),
	("grammar", "Pst. Sim. Когда ты поступил в гугу?. В 2022 году", None, "When did you enter the GUGA?. In 2022."),
	("grammar", "Pst. Sim. Что ты делал 2 дня назад?.", None, "What did you do 2 days ago?."),
	("grammar", "Pst. Sim. Том не играл в доту позавчера.", None, "Tom did not play Dota the day before yesterday."),


        # Past Continuous
        ("grammar", "Pst. Cont. Я читал книгу, когда она позвонила.", None, "I was reading a book when she called."),
        ("grammar", "Pst. Cont. Он играл в компьютерные игры весь вечер.", None, "He was playing computer games all evening."),
        ("grammar", "Pst. Cont. Они работали над проектом вчера в 5 часов.", None, "They were working on the project yesterday at 5 o'clock."),
	("grammar", "Pst. Cont. Что ты делала, когда я пришел? .", None, "What were you doing when i came?."),
	("grammar", "Pst. Cont. Она разговаривала по телефону, в то время как он готовил ужин.", None, "She was calling the phone while he was cooling a dinner."),
	("grammar", "Pst. Cont. Вчера в 7 вечера они смотрели романтический фильм.", None, "They were watching a romantic movie at 7 p.m. yesterday."),
	("grammar", "Pst. Cont. Дженни рассказывала историю про своего бывшего, когда он написал ей .", None, "Jenny was telling a story about her ex-boyfriend when he texted her."),
	("grammar", "Pst. Cont. Вчера шел дожждь, когда ты шел домой? .", None, "Was it raining when you were going home yesterday?."),
	("grammar", "Pst. Cont. Она не работала вчера весь день.", None, "She was not working all day yesterday.."),
	("grammar", "Pst. Cont. Ты ужинал вчера здесь в это же время?.", None, "Were you having a dinner at this time here yesterday?."),
	


	# Present Perfect 
        ("grammar", "Pr. Perf. Я уже прочитал эту книгу.", None, "I have already read this book."),
        ("grammar", "Pr. Perf. Она только что закончила работу.", None, "She has just finished work."),
        ("grammar", "Pr. Perf. Они никогда не были в Париже.", None, "They have never been to Paris."),
	("grammar", "Pr. Perf. Он прочитал все книги этой серии.", None, "He has read all the books in this series."),
	("grammar", "Pr. Perf. Они дружат уже 10 лет.", None, "theu have been friends for 10 years."),
	("grammar", "Pr. Perf. Я выпил кофе.", None, "I have drunk coffee."),
	("grammar", "Pr. Perf. Ты уже купил новую машину?.", None, "Have you already bought a new car?."),
	("grammar", "Pr. Perf. Она еще не приехала.", None, "She hasn't come yet."),
	("grammar", "Pr. Perf. Мы не видели этот спектакль.", None, "We haven't seen this performance."),
	("grammar", "Pr. Perf. Этот пилот уже сдал экзамен ИКАО?. Да.", None, "Has this pilot already passed the ICAO exam? Yes, he has."),
	("grammar", "Pr. Perf. Ты в последнее время видел его?. Нет.", None, "Have you seen him lately? No, i haven't."),
	("grammar", "Pr. Perf. Кто-нибудь недавно ходил на пары?", None, "Has anyone attended classes recently?"),


        # Present Perfect Continuous
        ("grammar", "Pr. Perf. Cont. Я работаю над этим проектом уже два часа.", None, " I have been working on this project for two hours."),
        ("grammar", "Pr. Perf. Cont. Она ждет его уже полчаса.", None, " She has been waiting for him for half an hour."),
        ("grammar", "Pr. Perf. Cont. Снег идет уже 3 дня.", None, "It has been snowing for 3 days"),
	("grammar", "Pr. Perf. Cont. Они живут в этом городе уже десять лет?", None, "Have they been living in this city for 10 years?."),
	("grammar", "Pr. Perf. Cont. Он сдает курсовую уже пол часа.", None, "He's been defending his term paper for half an hour now."),
	("grammar", "Pr. Perf. Cont. Она собирает персики все утро.", None, "She's been picking peaches all morning."),
	("grammar", "Pr. Perf. Cont. Они обсуждают этот вопрос уже целый день.", None, "They have been discussing this issue all day."),
	("grammar", "Pr. Perf. Cont. Они спорят с утра.", None, "They have been arguing since morning."),
	("grammar", "Pr. Perf. Cont. Кто учится в универе уже 4 года?.", None, "Who has been studying at the university for 4 years?"),
	("grammar", "Pr. Perf. Cont. Он не готовится к экзамену с сентября.", None, "He hasn't been preparing for the exam since September."),
	("grammar", "Pr. Perf. Cont. Она работает на эту компанию уже 7 лет.", None, "She has been working for this company for 7 years now."),

	
        # Past Perfect
        ("grammar", "Pst. Perf. Я уже пообедал, когда пришел друг.", None, "I had already had lunch when my friend arrived."),
        ("grammar", "Pst. Perf. Она закончила работать до того, как начался дождь.", None, "She had finished working before it started raining."),
        ("grammar", "Pst. Perf. Они уже сдали экзамены к тому моменту, когда начались каникулы.", None, "They had already passed the exams by the time the holidays started."),
	("grammar", "Pst. Perf. Они уже забронировали стол до того как пришли в ресторан.", None, "They had already booked a table before they came to the restaurant."),
	("grammar", "Pst. Perf. Он прочитал книгу к тому моменту, как вернулся домой.", None, "He had read the book by the time he got home."),
	("grammar", "Pst. Perf. Они уже уехали, когда мы пришли.", None, "They had already left when we arrived."),
	("grammar", "Pst. Perf. Степан переехал в этот город к 2020 году.", None, "Stepan had moved to this city by 2020."),
	("grammar", "Pst. Perf. Настя сдала все экзамены до начала лета.", None, "Nastya had passed all the exams before the beginning of summer"),
	("grammar", "Pst. Perf. Кто закончил проект к октябрю?.", None, "Who had finished the project by October?."),
	("grammar", "Pst. Perf. Он приехал раньше гостей?.", None, "Had he arrived before the guests came?"),
	("grammar", "Pst. Perf. Она не выучила это правило к 5 часам.", None, "She hadn't learned this rule by 5 o'clock."),

	# Past Perfect Continuous
        ("grammar", "Pst. Perf. Cont. Я работал над этим проектом уже два часа, когда ты позвонил.", None, " I had been working on this project for two hours when you called."),
        ("grammar", "Pst. Perf. Cont. Она ждала его уже полчаса, когда он наконец пришел.", None, "She had been waiting for him for half an hour when he finally arrived."),
        ("grammar", "Pst. Perf. Cont. Я искал ключи уже 20 минут, когда вспомнил где они.", None, " I had been looking for my keys for 20 minutes when I remembered where they were."),
	("grammar", "Pst. Perf. Cont. Мы ждали автобус уже полчаса, когда он наконец приехал.", None, " We had been waiting for the bus for half an hour when it finally arrived."),
	("grammar", "Pst. Perf. Cont. Они катались на коньках уже 5 лет до того, как выиграли соревнование.", None, "They had been skating together for five years before they won the competition."),
	("grammar", "Pst. Perf. Cont. Как долго ты работал, когда начался дождь?", None, "How long had you been working when it rained?"),
	("grammar", "Pst. Perf. Cont. Он учил английский 5 лет перед тем, как поступил в университет.", None, "He had been studying English for 5 years before he entered to the university."),
	("grammar", "Pst. Perf. Cont. Они смотрели фильм уже 2 часа к вечеру.", None, "They had already been watching the movie for 2 hours by the evening."),
	("grammar", "Pst. Perf. Cont. Эмили не готовила ужины уже месяц к концу весны.", None, "Emily hadn't been cooking dinner for a month by the end of spring."),
	("grammar", "Pst. Perf. Cont. К твоему приезду дождь шел уже 2 дня.", None, "It had been raining for 2 days by the time you arrived."),
	

        # Future Simple
        ("grammar", "Fut. Sim. Я пойду в кино завтра.", None, "I will go to the cinema tomorrow."),
        ("grammar", "Fut. Sim. Она позвонит тебе вечером.", None, "She will call you in the evening."),
        ("grammar", "Fut. Sim. Они будут играть в теннис на выходных.", None, "They will play tennis at the weekend."),
	("grammar", "Fut. Sim. Его родители думают, что он однажды станет художником.", None, "His parents think he will become an artist one day."),
	("grammar", "Fut. Sim. Его друзья уверены, что он не будет пилотом.", None, "His friends are sure that he will not be a pilot."),
	("grammar", "Fut. Sim. Она надеется, что сдаст сессию.", None, "She hopes she will pass the session."),
	("grammar", "Fut. Sim. Он не купит новый компьютер в следующем месяце.", None, "He won't buy a new computer next month."),
	("grammar", "Fut. Sim. Я помогу тебе с твоим заданием.", None, "I'll help you with your task."),
	("grammar", "Fut. Sim. Что ты будешь делать завтра?", None, "What will you do tomorrow?"),
	("grammar", "Fut. Sim. Тому исполнится 8 лет на следующей неделе.", None, "Tom will be 8 years old next week."),
	("grammar", "Fut. Sim. Он сегодня приедет пораньше.", None, "He will come early today."),
	("grammar", "Fut. Sim. Вероника боится, что он расскажет ее секрет.", None, "Veronica is afraid that he will tell her secret."),
	("grammar", "Fut. Sim. Она не приедет завтра.", None, "She will not come tomorrow."),
	("grammar", "Fut. Sim. Они думают, что начнут ходить в зал с понедельника.", None, "They think they'll start going to the gym on Monday."),

        # Future Continuous
        ("grammar", "Fut. Cont. Я буду спать в это время завтра.", None, "I will be sleeping at this time tomorrow."),
        ("grammar", "Fut. Cont. Он будет работать допоздна завтра вечером.", None, "He will be working late tomorrow evening."),
        ("grammar", "Fut. Cont. Они будут смотреть фильм в 8 часов.", None, "They will be watching a movie at 8 o'clock."),
    	("grammar", "Fut. Cont. Чем ты будешь заниматься завтра в 10 утра?", None, "What will you doing tomorrow at 10 a.m.?"),
	("grammar", "Fut. Cont. В это же время через месяц я буду загорать на пляже.", None, "This time next month, I'll be sunbathing on the beach."),
	("grammar", "Fut. Cont. Они будут обсуждать проект на собрании.", None, "They will be discussing the project at the meeting."),
	("grammar", "Fut. Cont. Я буду спать в это время завтра.", None, "I will be sleeping at this time tomorrow."),
	("grammar", "Fut. Cont. Она не будет делать домашнее задание в эти выходные.", None, "She won't be doing her homework this weekend."),
	("grammar", "Fut. Cont. Завтра в 5 часов она будет танцевать.", None, "Tomorrow at 5 o'clock she will be dancing."),
	("grammar", "Fut. Cont. Послезватра в 2 часа будет идти снег.", None, "It will be snowing the day after tomorrow at 2 o'clock."),
	("grammar", "Fut. Cont. Они будут гулять по городу во время занятий в универе", None, "They will be walking around the city during classes at the university."),

	# Future Perfect 
        ("grammar", "Fut. Perf. Я закончу эту работу к завтрашнему вечеру.", None, " I will have finished this work by tomorrow evening."),
        ("grammar", "Fut. Perf. Они не закончат их встречу к 4 часам", None, "They won't have finished their meeting by 4 o'clock."),
        ("grammar", "Fut. Perf. Мы завершим проект к следующей неделе?", None, "Will we have finished the project by next week?"),
	("grammar", "Fut. Perf. Они уже переедут к следующему месяцу.", None, "They will have already moved by next month."),
	("grammar", "Fut. Perf. Я выучу все новые слова до завтра.", None, " I will have learned all the new words by tomorrow."),
	("grammar", "Fut. Perf. Он починит самолет к следующей пятнице.", None, "He will have repaired the aircraft by next Friday."),
	("grammar", "Fut. Perf. Она позвонит ему сегодня к вечеру.", None, "She will have called him by tonight"),
	("grammar", "Fut. Perf. Он пригласит ее на свидание до того, как она посмотрит фильм.", None, "He'll have asked her out before she watches the movie."),
	("grammar", "Fut. Perf. Снег начнется к 8 вечера.", None, "It will have snowed by 8 p.m.."),
	("grammar", "Fut. Perf. Она не приготовит ужин к его приходу.", None, "She will not have cooked dinner for him by his arrival."),
	("grammar", "Fut. Perf. Он вернется домой до начала этого фильма?.", None, "Will he have come home before this movie starts?"),


	# Future Perfect Continuous
        ("grammar", "Fut. Perf. Cont. К тому времени, как ты придешь, я буду работать над проектом уже два часа.", None, "By the time you come, I will have been working on the project for two hours."),
        ("grammar", "Fut. Perf. Cont. К тому моменту, как мы приедем, они будут жить в этом городе уже десять лет.", None, " By the time we arrive, they will have been living in this city for ten years."),
        ("grammar", "Fut. Perf. Cont. К тому времени, как начнется собрание, они будут обсуждать этот вопрос уже целый день.", None, "By the time the meeting starts, they will have been discussing this issue all day."),
	("grammar", "Fut. Perf. Cont. К тому времени, как Рик уйдет в отстаку он будет работать на эту компанию уже 30 лет.", None, "By the time Rick retires, he will have been working for this company for 30 years."),
	("grammar", "Fut. Perf. Cont. К 2026 году он будет изучать английский уже 5 лет.", None, "By 2026, he will have been studying English for 5 years."),
	("grammar", "Fut. Perf. Cont. Она будет готовить торт уже 5 часов к 7 вечера.", None, "She will have been cooking the cake for 5 hours by 7 p.m."),
	("grammar", "Fut. Perf. Cont. Таня будет разговаривать по телефону уже 2 часа с подругой, когда ей позвонит ее муж.", None, "Tanya will have been talking phone for 2 hours with a friend when her husband calls her."),
	("grammar", "Fut. Perf. Cont. К тому времени, как поезд приедет, мы будем ждать автобус уже полчаса.", None, "By the time the train arrives, we will have been waiting for the bus for half an hour."),
	("grammar", "Fut. Perf. Cont. К тому времени, как мы закончим пить чай, я буду слушать музыку уже 20 минут.", None, "By the time we finish drinking tea, I'll have been listening to music for 20 minutes."),
	("grammar", "Fut. Perf. Cont. К концу дня он будет писать статью уже 9 часов.", None, "By the end of the day, he will have been writing the article for 9 hours."),

    ]

    for task_type, question, options, answer in grammar_tasks:
        cursor.execute(
            "INSERT INTO tasks (type, question, options, answer) VALUES (?, ?, ?, ?)",
            (task_type, question, options, answer)
        )
        print(f"Added task: {question}")  # Дебаг вывод

    conn.commit()
    conn.close()

def add_lexis_tasks():
    conn = sqlite3.connect("english_bot.db")
    cursor = conn.cursor()

    
aviation_alphabet = {
    "A": "Alfa", "B": "Bravo", "C": "Charlie", "D": "Delta", "E": "Echo",
    "F": "Foxtrot", "G": "Golf", "H": "Hotel", "I": "India", "J": "Juliet",
    "K": "Kilo", "L": "Lima", "M": "Mike", "N": "November", "O": "Oscar",
    "P": "Papa", "Q": "Quebec", "R": "Romeo", "S": "Sierra", "T": "Tango",
    "U": "Uniform", "V": "Victor", "W": "Whiskey", "X": "X-ray", "Y": "Yankee", "Z": "Zulu"
}

common_phrases = [
    "Roger: Indicates that a message has been received and understood.",
    "Wilco: Short for - will comply, meaning the instructions will be followed.",
    "Standby: A request to wait for further instructions.",
    "Affirm: Yes.",
    "Negative: No.",
    "Say again: A request to repeat the last message.",
    "Cleared for Takeoff: Permission granted for the aircraft to take off.",
    "Cleared to Land: Permission granted for the aircraft to land.",
    "Hold Short: An instruction to stop before reaching a specific point (e.g., a runway).",
    "Line Up and Wait: An instruction to enter the runway and wait for takeoff clearance."
    
]

emergency_terms = [
    "Mayday: A radio call indicating a life-threatening emergency",
    "Pan-pan: A radio call indicating an urgent situation that is not life-threatening.",
    "Emergency descent: A rapid descent to a lower altitude due to cabin pressure loss or other issues.",
    "Ditching: An emergency landing on water.",
    "Evacuation: The immediate exit of passengers and crew from the aircraft.",
    "Fire on Board: Indicates a fire inside the aircraft."
]

navigation_terms = [
    "Fix: A geographical position determined by visual or electronic means.",
    "Altitude: Vertical distance from sea level to aircraft",
    "GPS (Global Positioning System): Satellite-based navigation system.",
    "Waypoint: A specific location used in Area navigation.",
    "VOR(VHF Omnidirectional Range): A ground-based navigation aid."
]

abbreviations = [
    "ATC: Air Traffic Control",
    "ETA: Estimated Time of Arrival",
    "ICAO: International Civil Aviation Organization",
    "IATA: International Air Transport Association.",
    "FAA: Federal Aviation Administration (U.S.).",
    "TAF: Terminal Aerodrome Forecast.",
    "NOTAM: Notice to Airmen"
]

charades = [
    {"charade": "I am a large metal bird, but I have no feathers. I soar through the sky, but I have no wings of my own.", "answer": "Airplane"},
    {"charade": "I am a place where airplanes take off and land. I have runways and terminals.", "answer": "Airdrome"},
    {"charade": "I'm a long strip of pavement where planes take off and land, but I'm not a road. What am I?", "answer": "Runway"},
    {"charade": "I'm a building at an airport where passengers wait, but I'm not a hotel. What am I?", "answer": "Terminal"},
    {"charade": "I'm the part of the plane that makes it go, but I'm not the wings. What am I?", "answer": "Engine"},
    {"charade": "I tell the pilot where to go, but I'm not a map and FMS. What am I?", "answer": "ATC"},
    {"charade": "I’m a bag you carry onto a plane, but not if it is too large. What am I?", "answer": "Carry-on"},
    {"charade": "I’m aa situation where a flight does not depart or arrive at its scheduled time. What am I?", "answer": "Delay"}

]          
            
# функции

def get_aviation_alphabet():
    """Возвращает авиационный алфавит."""
    return aviation_alphabet

def get_common_phrases():
    """Возвращает список наиболее часто используемых фраз."""
    return common_phrases

def get_emergency_terms():
    """Возвращает список терминов при чрезвычайных ситуациях."""
    return emergency_terms

def get_navigation_terms():
    """Возвращает список навигационных терминов."""
    return navigation_terms

def get_abbreviations():
    """Возвращает список аббревиатур."""
    return abbreviations

def get_random_charade():
    """Возвращает случайную шараду."""
    return random.choice(charades)

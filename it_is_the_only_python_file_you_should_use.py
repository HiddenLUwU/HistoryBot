# отсюда надо брать этот файл, participant.jpg, winner.jpg, test_bd и все


import telebot
from telebot import types
import sqlite3
import random
import datetime

correct_answers_quiz = []
correct_answers_quiz_1 = []
one_answers_quiz = []
answers_quiz = []
questions_quiz = []
correct_answers_quiz_2 = ''
in_guide = False


def make_quiz(message):
    global correct_answers_quiz, correct_answers_quiz_1, one_answers_quiz, answers_quiz, questions_quiz, \
        correct_answers_quiz_2
    correct_answers_quiz = []
    correct_answers_quiz_1 = []
    one_answers_quiz = []
    answers_quiz = []
    questions_quiz = []
    correct_answers_quiz_2 = ''
    connect = sqlite3.connect('test_bd')
    cur = connect.cursor()
    questions = cur.execute(f"SELECT * FROM questions").fetchall()
    connect.close()
    tasks_quiz = random.sample(questions, 15)
    print(tasks_quiz)
    for el in tasks_quiz:
        questions_quiz.append(el[1])
        for x in range(2, 6):
            one_answers_quiz.append(el[x])
        correct_answers_quiz.append(el[6])
        correct_answers_quiz_1.append(el[6])
        answers_quiz.append(one_answers_quiz)
        one_answers_quiz = []
    for sus in range(len(correct_answers_quiz_1)):
        correct_answers_quiz_2 += f'{sus + 1}. {correct_answers_quiz_1[sus]}\n'
    d[message.from_user.id][0] = correct_answers_quiz
    d[message.from_user.id][1] = correct_answers_quiz_1
    d[message.from_user.id][2] = one_answers_quiz
    d[message.from_user.id][3] = answers_quiz
    d[message.from_user.id][4] = questions_quiz
    d[message.from_user.id][5] = correct_answers_quiz_2


# кусок кода ниже лучше не трогать
BOT_TOKEN = '7430083940:AAHGv3qpzyrpUF9UZzHifKTUJ-TWZmZVhto'
bot = telebot.TeleBot(BOT_TOKEN)
send_question = False
topic = ''
question_number = 0
answers_user = 0
quiz_started = False
keyboardsusss = types.ReplyKeyboardMarkup(row_width=3)
d = dict()


# кусок кода выше лучше не трогать


def quiz(message):
    keyboard_ans = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton(d[message.from_user.id][3][d[message.from_user.id][6]][0])
    button2 = types.KeyboardButton(d[message.from_user.id][3][d[message.from_user.id][6]][1])
    button3 = types.KeyboardButton(d[message.from_user.id][3][d[message.from_user.id][6]][2])
    button4 = types.KeyboardButton(d[message.from_user.id][3][d[message.from_user.id][6]][3])
    keyboard_ans.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, str(d[message.from_user.id][6] + 1) + '. ' +
                     questions_quiz[d[message.from_user.id][6]], reply_markup=keyboard_ans)
    d[message.from_user.id][6] += 1
    d[message.from_user.id][8] = True


def quiz_end(message):
    keyboardsuss = types.ReplyKeyboardMarkup(row_width=2)
    button2 = types.KeyboardButton("Вернуться в главное меню")
    button3 = types.KeyboardButton("Пройти заново")
    keyboardsuss.add(button3, button2)
    bot.send_message(message.chat.id, "Теперь Вы можете пройти викторину ещё раз, выбрав «Пройти заново» или вернуться "
                                      "к выбору раздела, нажав кнопку «Вернуться в главное меню».",
                     reply_markup=keyboardsuss)
    d[message.from_user.id][6] += 1
    d[message.from_user.id][8] = True


def add_q_buttons(message):
    keyboardsus = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton("Викторина")
    button2 = types.KeyboardButton("Справочник")
    button3 = types.KeyboardButton("Интересные факты")
    button4 = types.KeyboardButton("Техническая поддержка")
    keyboardsus.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id,
                     "А теперь выберите одну из четырёх кнопок. Вы можете поиграть в увлекательную викторину, нажав "
                     "кнопку «Викторина». Кнопка «Справочник» предоставит Вам доступ к справочным материалам — датам и "
                     "событиям ВОВ. Выбрав кнопку «Интересные факты», Вы сможете узнать кое-что интересное... Если у Вас"
                     " возникли какие-то проблемы, вопросы или пожелания во время пользования нашим ботом, вы можете "
                     "выбрать кнопку «Техническая поддержка», чтобы отправить сообщение разработчикам."
                     , reply_markup=keyboardsus)
    d[message.from_user.id][8] = True


def tp(message):
    keyboardus = types.ReplyKeyboardMarkup(row_width=1)
    button1 = types.KeyboardButton("Вернуться в главное меню")
    keyboardus.add(button1)
    bot.send_message(message.chat.id, "Итак, Вы находитесь в разделе «Техническая поддержка». Это значит, что у Вас,"
                                      " скорее всего, возникли вопросы, проблемы или пожелания. Напишите о них, и мы"
                                      " постараемся на вопросы ответить, проблемы решить, а пожелания — учесть."
                                      " С уважением, команда разработчиков.", reply_markup=keyboardus)
    d[message.from_user.id][9] = 'Техническая поддержка'


@bot.message_handler(commands=['start'])
def start(message):
    global questions_quiz
    bot.send_message(message.chat.id,
                     "Добро пожаловать в чат-бот Памяти и Победы! Здесь Вы можете:\n"
                     "• Пройти викторину по Великой Отечественной войне (далее — ВОВ);\n"
                     "• Узнать интересные факты по этой теме;\n"
                     "• Спросить об интересующих Вас датах этого исторического периода.")
    d[message.from_user.id] = [correct_answers_quiz, correct_answers_quiz_1, one_answers_quiz, answers_quiz,
                               questions_quiz, correct_answers_quiz_2, question_number, answers_user, send_question,
                               topic, quiz_started, in_guide]
    add_q_buttons(message)


@bot.message_handler(func=lambda message: True)
def hendler_message(message):
    if message.text == 'Вернуться в главное меню':
        start(message)
    if message.text == 'Техническая поддержка':
        tp(message)
    if not d[message.from_user.id][10] and not d[message.from_user.id][11]:
        if message.text == 'Викторина' or message.text == 'Пройти заново':
            d[message.from_user.id][9] = 'Викторина'
            print(d[message.from_user.id][9])
            d[message.from_user.id][10] = True
            bot.send_message(message.chat.id, "Добро пожаловать в викторину! \n"
                                              "Викторина состоит из 15 вопросов. Чтобы ответить на вопрос, Вам нужно"
                                              " будет выбрать один из предложенных вариантов. Вы можете сделать свой "
                                              "выбор, нажав на одну из четырёх кнопок. Поехали!!!")
            make_quiz(message)
            quiz(message)
        elif d[message.from_user.id][9] == 'Техническая поддержка' and message.text != 'Техническая поддержка':
            connect = sqlite3.connect('test_bd')
            cur = connect.cursor()
            result = cur.execute(
                f"INSERT INTO reqsss(compl) VALUES(\"{message.text}\")")
            connect.commit()
            connect.close()
            bot.send_message(message.chat.id, 'Здравствуйте!\n'
                                              'Благодарим Вас за предоставленную информацию.\n'
                                              'Мы примем необходимые меры в отношении данной ошибки.\n'
                                              'Спасибо за Ваше обращение и неравнодушие! Постараемся в'
                                              ' ближайшее время всё исправить, если вы уже отправляли данный'
                                              ' запрос, то просим прощения за долгое ожидание, мы постараемся'
                                              ' как можно скорее это отладить.\n'
                                              'Служба техподдержки пользователей «Чат-бот Памяти и Победы»')
        elif message.text == 'Справочник':
            d[message.from_user.id][9] = 'Справочник'
            keyboarddsuss = types.ReplyKeyboardMarkup(row_width=1)
            button1 = types.KeyboardButton("Вернуться в главное меню")
            keyboarddsuss.add(button1)
            bot.send_message(message.chat.id, 'Мы рады Вас видеть в разделе «Справочник»! Воспользуйтесь им, чтобы '
                                              'узнать, что происходило в различные дни ВОВ. Всё, что Вам нужно — ввести'
                                              ' дату в формате ДД.ММ.ГГГГ, принадлежащую периоду с 22.06.1941 по '
                                              '09.05.1945. Удачи!!!',
                             reply_markup=keyboarddsuss)
            d[message.from_user.id][11] = True
            d[message.from_user.id][7] = 0
            d[message.from_user.id][10] = False
            d[message.from_user.id][9] = ''
        elif message.text == 'Интересные факты':
            d[message.from_user.id][9] = 'Интересные факты'
            keyboarddsus = types.ReplyKeyboardMarkup(row_width=2)
            button1 = types.KeyboardButton("Получить интересный факт")
            button2 = types.KeyboardButton("Вернуться в главное меню")
            keyboarddsus.add(button1, button2)
            bot.send_message(message.chat.id, 'Приветствуем Вас в разделе «Интересные факты»! Здесь Вы можете открыть '
                                              'для себя много интересного о ВОВ, нажимая на кнопку «Получить интересный '
                                              'факт»... или вернуться назад, чтобы попробовать другие разделы.',
                             reply_markup=keyboarddsus)
            d[message.from_user.id][7] = 0
            d[message.from_user.id][10] = False
            d[message.from_user.id][9] = ''
        elif message.text == 'Получить интересный факт':
            connect = sqlite3.connect('test_bd')
            cur = connect.cursor()
            facts = cur.execute(f"SELECT * FROM facts").fetchall()
            connect.close()
            r = random.randint(0, 14)
            eh = facts[r][2].split('$')
            bot.send_message(message.chat.id, facts[r][1] + '\n' + '\n'.join(eh))
        elif message.text == 'Техническая поддержка' or message.text == 'Вернуться в главное меню':
            pass
        else:
            print(d[message.from_user.id][9])
            bot.send_message(message.chat.id, 'Нажмите на одну из кнопок для выбора раздела.')
    if d[message.from_user.id][11] and message.text != 'Вернуться в главное меню':
        datee = str(message.text)
        if '.' in datee and len(datee) == 10:
            f = datee.split('.')
            if 1 <= int(f[0]) <= 31 and 1 <= int(f[1]) <= 12 and 1941 <= int(f[2]) <= 1945:
                day_n = int(format(datetime.datetime(int(f[2]), int(f[1]), int(f[0])), '%j'))
                needed_date = f'{day_n}&{int(f[2][2:])}'
                connect = sqlite3.connect('test_bd')
                cur = connect.cursor()
                print(needed_date)
                facts1 = cur.execute(f"SELECT infa FROM guide WHERE dates LIKE \"%{needed_date}%\" "
                                     f"AND typee = \"1\"").fetchall()
                facts2 = cur.execute(f"SELECT dates, infa FROM guide WHERE dates LIKE \"%{int(f[2][2:])}%\" "
                                     f"AND typee = \"2\"").fetchall()
                facts3 = cur.execute(f"SELECT dates, infa FROM guide WHERE typee = \"3\"").fetchall()
                print(facts1, facts2, facts3)
                connect.close()
                if facts1 != '':
                    for fact in facts1:
                        bot.send_message(message.chat.id, fact[0])
                if facts2 != '':
                    for one in facts2:
                        e = one[0].split("$")
                        sus1 = e[0].split("&")[0]
                        sus2 = e[1].split("&")[0]
                        if int(sus1) <= day_n <= int(sus2):
                            bot.send_message(message.chat.id, one[1])
                if facts3 != '':
                    for two in facts3:            # day_n = цифра запрошенного дня
                        emm = two[0].split("$")   # f[2][2:] = две последние цифры года
                        sus3 = emm[0].split("&")  # sus3 это [день, год] начала
                        sus4 = emm[1].split("&")  # sus4 это [день, год] конца
                        if int(sus3[1]) <= int(f[2][2:]) <= int(sus4[1]):  # yes
                            if int(sus3[1]) == int(f[2][2:]):
                                if int(sus3[0]) <= day_n:
                                    bot.send_message(message.chat.id, two[1])
                            elif int(f[2][2:]) != int(sus3[1]) and int(f[2][2:]) != int(sus4[1]):
                                bot.send_message(message.chat.id, two[1])
                            elif int(sus4[1]) == int(f[2][2:]):
                                if int(sus4[0]) >= day_n:
                                    bot.send_message(message.chat.id, two[1])
            else:
                bot.send_message(message.chat.id, "Дата введена некорректно или эта дата не входит в ВОВ")
    if d[message.from_user.id][9] == 'Викторина':
        if d[message.from_user.id][6] >= len(d[message.from_user.id][4]):
            ans = message.text
            if ans == d[message.from_user.id][0][d[message.from_user.id][6] - 1]:
                d[message.from_user.id][7] += 1
            bot.send_message(message.chat.id, f"Правильных ответов {str(d[message.from_user.id][7])} из 15.")
            bot.send_message(message.chat.id, "Правильные ответы:\n" + str(d[message.from_user.id][5]))
            if d[message.from_user.id][7] >= 14:
                photo = open('winner.jpg', 'rb')
                bot.send_photo(message.chat.id, photo, 'Поздравляем! Здесь Вы можете получить диплом победителя!')
            elif 7 <= d[message.from_user.id][7] < 14:
                photo = open('participant.jpg', 'rb')
                bot.send_photo(message.chat.id, photo, 'Поздравляем! Здесь Вы можете получить '
                                                       'грамоту за участие в викторине.')
            quiz_end(message)
            d[message.from_user.id][7] = 0
            d[message.from_user.id][10] = False
            d[message.from_user.id][9] = ''
            d[message.from_user.id][6] = 0
        elif not d[message.from_user.id][8]:
            quiz(message)
        elif message.text not in d[message.from_user.id][3][d[message.from_user.id][6] - 1] and message.text != \
                'Викторина' and message.text != 'Пройти заново':
            bot.send_message(message.chat.id, f"Варианты ответа: "
                                              f"{', '.join(d[message.from_user.id][3][d[message.from_user.id][6] - 1])}")
        elif message.text == 'Викторина' or message.text == 'Пройти заново':
            pass
        else:
            ans = message.text
            if ans == d[message.from_user.id][0][d[message.from_user.id][6] - 1]:
                d[message.from_user.id][7] += 1
                d[message.from_user.id][8] = False
                quiz(message)
            else:
                d[message.from_user.id][8] = False
                quiz(message)


bot.polling()

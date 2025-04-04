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
    keyboardsuss = types.ReplyKeyboardMarkup(row_width=3)
    button1 = types.KeyboardButton("/info")
    button2 = types.KeyboardButton("/start")
    button3 = types.KeyboardButton("Пройти заново")
    keyboardsuss.add(button3, button2, button1)
    bot.send_message(message.chat.id, "Чтобы начать снова, нажмите на кнопку \"Пройти заново\"",
                     reply_markup=keyboardsuss)
    d[message.from_user.id][6] += 1
    d[message.from_user.id][8] = True


def add_q_buttons(message):
    keyboardsus = types.ReplyKeyboardMarkup(row_width=3)
    button1 = types.KeyboardButton("Викторина")
    button2 = types.KeyboardButton("Справочник")
    button3 = types.KeyboardButton("Интересные факты")
    keyboardsus.add(button1, button2, button3)
    bot.send_message(message.chat.id,
                     "А теперь выберите одну из трех кнопок ниже. Кнопка \"Викторина\" начнет викторину, "
                     "\"Справочник\" расскажет вам о любом событии или дате ВОВ, а \"Интересные факты\" "
                     "- интересные факты к 80-летию победы", reply_markup=keyboardsus)
    d[message.from_user.id][8] = True


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id,
                     "возможно тут потом появится какая то инфа про проект")


@bot.message_handler(commands=['start'])
def start(message):
    global questions_quiz
    bot.send_message(message.chat.id,
                     "Добро пожаловать в игру «Все про ВОВ»! Тут Вы можете:\n"
                     "✅ Пройти викторину по ВОВ\n"
                     "✅ Узнать интересные факты к 80-летию Победы\n"
                     "✅ Спросить бота про интересующие Вас даты и личности, связвнные с ВОВ!\n")
    d[message.from_user.id] = [correct_answers_quiz, correct_answers_quiz_1, one_answers_quiz, answers_quiz,
                               questions_quiz, correct_answers_quiz_2, question_number, answers_user, send_question,
                               topic, quiz_started, in_guide]
    add_q_buttons(message)


@bot.message_handler(func=lambda message: True)
def hendler_message(message):
    if message.text == 'Вернуться на главное меню':
        start(message)
    if not d[message.from_user.id][10] and not d[message.from_user.id][11]:
        if message.text == 'Викторина' or message.text == 'Пройти заново':
            d[message.from_user.id][9] = 'Викторина'
            print(d[message.from_user.id][9])
            d[message.from_user.id][10] = True
            bot.send_message(message.chat.id, 'Добро пожаловать в Викторину! \n'
                                              'Викторина состоит из 15 вопросов. На каждый вопрос будет дано четыре '
                                              'варианта ответа. Вам нужно выбрать один из них, нажав на одну из '
                                              'четырёх кнопок. Поехали!!\n- - - - - - - - - - - - - -')
            make_quiz(message)
            quiz(message)
        elif message.text == 'Справочник':
            d[message.from_user.id][9] = 'Справочник'
            keyboarddsuss = types.ReplyKeyboardMarkup(row_width=1)
            button1 = types.KeyboardButton("Вернуться на главное меню")
            keyboarddsuss.add(button1)
            bot.send_message(message.chat.id, 'Так тут крч справочник. вводить дату в формате "DD.MM.YYYY". если чет не'
                                              ' так напишете - ваша проблема. кнопка выхода в меню есть, дату печатать'
                                              ' самому надо. Антон напиши тут норм текст пж, настроения ваще нет.',
                             reply_markup=keyboarddsuss)
            d[message.from_user.id][11] = True
            d[message.from_user.id][7] = 0
            d[message.from_user.id][10] = False
            d[message.from_user.id][9] = ''
        elif message.text == 'Интересные факты':
            d[message.from_user.id][9] = 'Интересные факты'
            keyboarddsus = types.ReplyKeyboardMarkup(row_width=2)
            button1 = types.KeyboardButton("Получить интересный факт")
            button2 = types.KeyboardButton("Вернуться на главное меню")
            keyboarddsus.add(button1, button2)
            bot.send_message(message.chat.id, 'Приветствуем Вас в рубрике "Интересные Факты!". Здесь вы можете получить '
                                              'случайный интересный факт о ВОВ или вернуться в главное меню, '
                                              'воспользовавшись одной из двух кнопок ниже', reply_markup=keyboarddsus)
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
        else:
            print(d[message.from_user.id][9])
            bot.send_message(message.chat.id, 'Нажмите на одну из кнопок ниже')
    if d[message.from_user.id][11]:
        datee = str(message.text)
        if '.' in datee and len(datee) == 10:
            f = datee.split('.')
            if 1 <= int(f[0]) <= 31 and 1 <= int(f[1]) <= 12 and 1941 < int(f[2]) < 1945:
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
                connect.close()
                for fact in facts1:
                    bot.send_message(message.chat.id, fact[0])
                for one in facts2:
                    e = one[0].split("$")
                    sus1 = e[0].split("&")[0]
                    sus2 = e[1].split("&")[0]
                    if int(sus1) <= day_n <= int(sus2):
                        bot.send_message(message.chat.id, one[1])
                for two in facts2:
                    emm = two[0].split("$")
                    sus3 = emm[0].split("&")
                    sus4 = emm[1].split("&")
                    if sus3[1] <= int(f[2][2:]) <= sus4[1]:
                        if sus3[0] <= day_n:
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
            quiz_end(message)
            d[message.from_user.id][7] = 0
            d[message.from_user.id][10] = False
            d[message.from_user.id][9] = ''
            d[message.from_user.id][6] = 0
        elif not d[message.from_user.id][8]:
            quiz(message)
        elif message.text not in d[message.from_user.id][3][d[message.from_user.id][6] - 1] and message.text != \
                'Викторина':
            bot.send_message(message.chat.id, f"Варианты ответа: "
                                              f"{', '.join(d[message.from_user.id][3][d[message.from_user.id][6] - 1])}")
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

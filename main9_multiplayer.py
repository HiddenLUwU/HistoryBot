import telebot
from telebot import types
import random


correct_answers_quiz = []
correct_answers_quiz_1 = []
one_answers_quiz = []
answers_quiz = []
questions_quiz = []
correct_answers_quiz_2 = ''


def make_quiz(message):
    global correct_answers_quiz, correct_answers_quiz_1, one_answers_quiz, answers_quiz, questions_quiz, \
        correct_answers_quiz_2
    correct_answers_quiz = []
    correct_answers_quiz_1 = []
    one_answers_quiz = []
    answers_quiz = []
    questions_quiz = []
    correct_answers_quiz_2 = ''
    with open('questions.txt', encoding='utf-8') as f:
        questions = f.readlines()
        tasks_quiz = random.sample(questions, 10)
    print(tasks_quiz)
    for el in tasks_quiz:
        g = el.split("$")
        questions_quiz.append(g[0])
        del g[0]
        for elem in g:
            if "&" in elem and "\n" in elem:
                correct_answers_quiz.append(elem[:-2])
                correct_answers_quiz_1.append(elem[:-2])
                one_answers_quiz.append(elem[:-2])
            elif "&" in elem:
                correct_answers_quiz.append(elem[:-1])
                correct_answers_quiz_1.append(elem[:-1])
                one_answers_quiz.append(elem[:-1])
            elif "\n" in elem:
                one_answers_quiz.append(elem[:-1])
            else:
                one_answers_quiz.append(elem)
        answers_quiz.append(one_answers_quiz)
        one_answers_quiz = []
    correct_answers_quiz_2 = ', '.join(correct_answers_quiz_1)
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
keyboard = types.ReplyKeyboardMarkup(row_width=3)
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
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    button1 = types.KeyboardButton("/info")
    button2 = types.KeyboardButton("/start")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Чтобы начать снова введите /start", reply_markup=keyboard)
    d[message.from_user.id][6] += 1
    d[message.from_user.id][8] = True


def add_q_buttons(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    button1 = types.KeyboardButton("Викторина")
    button2 = types.KeyboardButton("Справочник")
    button3 = types.KeyboardButton("Интересные факты")
    keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id,
                     "А теперь выберите одну из трех кнопок ниже. Кнопка \"Викторина\" начнет викторину, "
                     "\"Справочник\" расскажет вам о любом событии или дате ВОВ, а \"Интересные факты\" "
                     "- интересные факты к 80-летию победы",
                     reply_markup=keyboard)
    d[message.from_user.id][8] = True


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id,
                     "возможно тут потом появится какая то инфа про проект", reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    global questions_quiz
    bot.send_message(message.chat.id,
                     "Добро пожаловать в игру «Все про ВОВ»! Тут Вы можете:\n"
                     "✅ Пройти викторину по ВОВ\n"
                     "✅ Узнать интересные факты к 80-летию Победы\n"
                     "✅ Спросить бота про интересующие Вас даты и личности, связвнные с ВОВ!\n",
                     reply_markup=keyboard)
    d[message.from_user.id] = [correct_answers_quiz, correct_answers_quiz_1, one_answers_quiz, answers_quiz,
                               questions_quiz, correct_answers_quiz_2, question_number, answers_user, send_question,
                               topic, quiz_started]
    add_q_buttons(message)


@bot.message_handler(func=lambda message: True)
def hendler_message(message):
    if not d[message.from_user.id][10]:
        if message.text == 'Викторина':
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
            bot.send_message(message.chat.id,
                             'Whoops! That part of our bot is still in development. Please check later :D')
            d[message.from_user.id][7] = 0
            d[message.from_user.id][10] = False
            d[message.from_user.id][9] = ''
            quiz_end(message)
        elif message.text == 'Интересные факты':
            d[message.from_user.id][9] = 'Интересные факты'
            bot.send_message(message.chat.id,
                             'Whoops! That part of our bot is still in development. Please check later :D')
            d[message.from_user.id][7] = 0
            d[message.from_user.id][10] = False
            d[message.from_user.id][9] = ''
            quiz_end(message)
        else:
            print(d[message.from_user.id][9])
            bot.send_message(message.chat.id, 'Выберите одну из предложенных викторин')
    if d[message.from_user.id][9] == 'Викторина':
        if d[message.from_user.id][6] >= len(d[message.from_user.id][4]):
            ans = message.text
            if ans == d[message.from_user.id][0][d[message.from_user.id][6] - 1]:
                d[message.from_user.id][7] += 1
            bot.send_message(message.chat.id, "Количество правильных ответов: " + str(d[message.from_user.id][7]))
            bot.send_message(message.chat.id, "Правильные ответы: " + str(d[message.from_user.id][5]))
            quiz_end(message)
            d[message.from_user.id][7] = 0
            d[message.from_user.id][10] = False
            d[message.from_user.id][9] = ''
            d[message.from_user.id][6] = 0
        elif not d[message.from_user.id][8]:
            quiz(message)
        elif message.text not in d[message.from_user.id][3][d[message.from_user.id][6] - 1]:
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

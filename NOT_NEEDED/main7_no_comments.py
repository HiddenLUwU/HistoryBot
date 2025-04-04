import telebot
from telebot import types
import random

with open('questions.txt', encoding='utf-8') as f:
    questions = f.readlines()
    tasks_quiz = [random.choice(questions) for x in range(10)]
print(tasks_quiz)


correct_answers_quiz = ['b', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
correct_answers_quiz_1 = 'b, a, a, a, a, a, a, a, a, a, a'
answers_quiz = [['b', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'],
                ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'],
                ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a']]

right_answers_quiz = []
right_answers_quiz_1 = []
one_answers_quiz = []
two_answers_quiz = []
questions_quiz = []
for el in tasks_quiz:
    g = el.split("$")
    questions_quiz.append(g[0])
    del g[0]
    for elem in g:
        if "&" in elem and "\n" in elem:
            right_answers_quiz.append(elem[:-1])
            right_answers_quiz_1.append(elem[:-1])
            one_answers_quiz.append(elem[:-3])
        elif "&" in elem:
            right_answers_quiz.append(elem[:-1])
            right_answers_quiz_1.append(elem[:-1])
            one_answers_quiz.append(elem[:-1])
        elif "\n" in elem:
            one_answers_quiz.append(elem[:-1])
        else:
            one_answers_quiz.append(elem)
    two_answers_quiz.append(one_answers_quiz)
    one_answers_quiz = []

right_answers_quiz_2 = ', '.join(right_answers_quiz_1)
print(right_answers_quiz)
print(right_answers_quiz_2)
print(two_answers_quiz)


# кусок кода ниже лучше не трогать
BOT_TOKEN = '7430083940:AAHGv3qpzyrpUF9UZzHifKTUJ-TWZmZVhto'
bot = telebot.TeleBot(BOT_TOKEN)
send_question = False
topic = ''
question_number = 0
answers_user = 0
quiz_started = False
keyboard = types.ReplyKeyboardMarkup(row_width=3)


# кусок кода выше лучше не трогать


def quiz(message):
    global topic, send_question, question_number, answers_user
    keyboard_ans = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton(answers_quiz[question_number][0])
    button2 = types.KeyboardButton(answers_quiz[question_number][1])
    button3 = types.KeyboardButton(answers_quiz[question_number][2])
    button4 = types.KeyboardButton(answers_quiz[question_number][3])  # тут кнопкам с ответами присваивается текст
    keyboard_ans.add(button1, button2, button3, button4)  # тут спавнятся кнопки
    bot.send_message(message.chat.id, str(question_number + 1) + '. ' + questions_quiz[question_number],
                     reply_markup=keyboard_ans)  # бот отправляет сообщение
    question_number += 1  # номер задания меняется на следующий
    send_question = True


def quiz_end(message):
    global topic, send_question, question_number, answers_user
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    button1 = types.KeyboardButton("/info")
    button2 = types.KeyboardButton("/start")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Чтобы начать снова введите /start", reply_markup=keyboard)
    question_number += 1
    send_question = True


def add_q_buttons(message):
    global topic, send_question, question_number, answers_user
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
    send_question = True


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id,
                     "возможно тут потом появится какая то инфа про проект", reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    global questions, questions_quiz
    bot.send_message(message.chat.id,
                     "Добро пожаловать в игру «Все про ВОВ»! Тут Вы можете:\n"
                     "* Пройти викторину по ВОВ\n"
                     "* Узнать интересные факты к 80-летию Победы\n"
                     "* Спросить бота про интересующие Вас даты и личности, связвнные с ВОВ!\n",
                     reply_markup=keyboard)

    with open('questions.txt', encoding='utf-8') as f:
        questions = f.readlines()
        questions_quiz = [random.choice(questions) for x in range(10)]
    print(questions_quiz)
    add_q_buttons(message)


@bot.message_handler(func=lambda message: True)
def hendler_message(message):
    global topic, send_question, question_number, answers_user, quiz_started
    global n
    n = 0  # BUTTONS
    if not quiz_started:
        if message.text == 'Викторина':
            topic = 'Викторина'
            quiz_started = True
            bot.send_message(message.chat.id, 'Добро пожаловать в Викторину! \n'
                                              'Викторина состоит из 15 вопросов. На каждый вопрос будет дано четыре '
                                              'варианта ответа. Вам нужно выбрать один из них, нажав на одну из '
                                              'четырёх кнопок. Поехали!!\n- - - - - - - - - - - - - -')
            quiz(message)
        elif message.text == 'Справочник':
            topic = 'Справочник'
            bot.send_message(message.chat.id,
                             'Whoops! That part of our bot is still in development. Please check later :D')
            answers_user = 0
            quiz_started = False
            topic = ''
            quiz_end(message)
        elif message.text == 'Интересные факты':
            topic = 'Интересные факты'
            bot.send_message(message.chat.id,
                             'Whoops! That part of our bot is still in development. Please check later :D')
            answers_user = 0
            quiz_started = False
            topic = ''
            quiz_end(message)
        else:
            bot.send_message(message.chat.id, 'Выберите одну из предложенных викторин')
    if topic == 'Викторина':
        if question_number >= len(questions_quiz):
            ans = message.text
            if ans == correct_answers_quiz[question_number - 1]:
                answers_user += 1
            print(answers_user)
            bot.send_message(message.chat.id, "Количество правильных ответов: " + str(answers_user))
            bot.send_message(message.chat.id, "Правильные ответы: " + str(correct_answers_quiz_1))
            quiz_end(message)
            answers_user = 0
            quiz_started = False
            topic = ''
            question_number = 0
        elif not send_question:
            quiz(message)
        elif message.text not in answers_quiz[question_number - 1]:
            pass
        else:
            ans = message.text
            if ans == correct_answers_quiz[question_number - 1]:
                answers_user += 1
                send_question = False
                quiz(message)
            else:
                send_question = False
                quiz(message)


bot.polling()

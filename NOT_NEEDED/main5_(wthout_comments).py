import telebot
from telebot import types
import random
f = open('sussy.txt', 'r')
QUESTIONS = f.readlines()
QUESTIONS_LUKOIL = [random.choice(QUESTIONS) for x in range(10)]
f.close()
print(QUESTIONS_LUKOIL)

CORRECT_ANSWERS_LUKOIL = ['b', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
CORRECT_ANSWERS_LUKOIL1 = 'b, a, a, a, a, a, a, a, a, a, a'
ANSWERS_LUKOIL = [['b', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'],
                  ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a'],
                  ['a', 'a', 'a', 'a'], ['a', 'a', 'a', 'a']]

# кусок кода ниже лучше не трогать
BOT_TOKEN = '7430083940:AAHGv3qpzyrpUF9UZzHifKTUJ-TWZmZVhto'
bot = telebot.TeleBot(BOT_TOKEN)
SEND_QUESTION = False
TOPIC = ''
NUM_QUESTION = 0
ANSWERS_USER = 0
QUIZE_STARTED = False
keyboard = types.ReplyKeyboardMarkup(row_width=3)
# кусок кода выше лучше не трогать


def quize_lukoil(message):
    global TOPIC, SEND_QUESTION, NUM_QUESTION, ANSWERS_USER
    keyboard_ans = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton(ANSWERS_LUKOIL[NUM_QUESTION][0])
    button2 = types.KeyboardButton(ANSWERS_LUKOIL[NUM_QUESTION][1])
    button3 = types.KeyboardButton(ANSWERS_LUKOIL[NUM_QUESTION][2])
    button4 = types.KeyboardButton(ANSWERS_LUKOIL[NUM_QUESTION][3]) 
    keyboard_ans.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, str(NUM_QUESTION + 1) + '. ' + QUESTIONS_LUKOIL[NUM_QUESTION], reply_markup=keyboard_ans)
    NUM_QUESTION += 1
    SEND_QUESTION = True


def quiz_end(message):
    global TOPIC, SEND_QUESTION, NUM_QUESTION, ANSWERS_USER
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    button1 = types.KeyboardButton("/info")
    button2 = types.KeyboardButton("/start")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Чтобы начать снова введите /start", reply_markup=keyboard)
    NUM_QUESTION += 1
    SEND_QUESTION = True



def add_q_butt(message):
    global TOPIC, SEND_QUESTION, NUM_QUESTION, ANSWERS_USER
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    button1 = types.KeyboardButton("Викторина")
    button2 = types.KeyboardButton("Справочник")
    button3 = types.KeyboardButton("Интересные факты")
    keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id, "А теперь вам необходимо выбрать викторину, нажав на одну из трёх кнопок у вас в чате", reply_markup=keyboard)
    SEND_QUESTION = True


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id,
                     "возможно тут потом появится какая то инфа про проект", reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    global QUESTIONS, QUESTIONS_LUKOIL
    bot.send_message(message.chat.id,
                     "Добро пожаловать в игру «Викторина по ВОВ»! Вы можете пройти различные викторины по трём "
                           "разным темам:\n"
                           "1. Федеральная территория Сириус\n"
                           "2. Общая викторина (на эрудированность)\n"
                           "3. ПАО «Лукойл»\n"
                           "############################\n"
                           "Каждая из викторин состоит из 10 вопросов. На каждый вопрос будет дано четыре варианта "
                           "ответа. Вам нужно выбрать один из них, нажав на одну из четырёх кнопок",
                     reply_markup=keyboard)

    f = open('sussy.txt', 'r')
    QUESTIONS = f.readlines()
    QUESTIONS_LUKOIL = random.sample(QUESTIONS, 10)
    f.close()
    print(QUESTIONS_LUKOIL)
    add_q_butt(message)


@bot.message_handler(func=lambda message: True)
def hendler_message(message):
    global TOPIC, SEND_QUESTION, NUM_QUESTION, ANSWERS_USER, QUIZE_STARTED
    global n
    n = 0  # BUTTONS
    if not QUIZE_STARTED:
        if message.text == 'Викторина':
            TOPIC = 'Викторина'
            QUIZE_STARTED = True
            bot.send_message(message.chat.id, 'Добро пожаловать в викторину ' + message.text)
            quize_lukoil(message)
        elif message.text == 'Справочник':
            TOPIC = 'Справочник'
            bot.send_message(message.chat.id, 'Whoops! That part of our bot is still in development. Please check later :D')
            ANSWERS_USER = 0
            QUIZE_STARTED = False
            TOPIC = ''
            quiz_end(message)
        elif message.text == 'Интересные факты':
            TOPIC = 'Интересные факты'
            bot.send_message(message.chat.id, 'Whoops! That part of our bot is still in development. Please check later :D')
            ANSWERS_USER = 0
            QUIZE_STARTED = False
            TOPIC = ''
            quiz_end(message)
        else:
            bot.send_message(message.chat.id, 'Выберите одну из предложенных викторин')
    if TOPIC == 'Викторина':
        if NUM_QUESTION >= len(QUESTIONS_LUKOIL):
            ans = message.text
            if ans == CORRECT_ANSWERS_LUKOIL[NUM_QUESTION - 1]:
                ANSWERS_USER += 1
            print(ANSWERS_USER)
            bot.send_message(message.chat.id, "Количество правильных ответов: " + str(ANSWERS_USER))
            bot.send_message(message.chat.id, "Правильные ответы: " + str(CORRECT_ANSWERS_LUKOIL1))
            quiz_end(message)
            ANSWERS_USER = 0
            QUIZE_STARTED = False
            TOPIC = ''
            NUM_QUESTION = 0
        elif not SEND_QUESTION:
            quize_lukoil(message)
        elif message.text not in ANSWERS_LUKOIL[NUM_QUESTION - 1]:
            pass
        else:
            ans = message.text
            if ans == CORRECT_ANSWERS_LUKOIL[NUM_QUESTION - 1]:
                ANSWERS_USER += 1
                SEND_QUESTION = False
                quize_lukoil(message)
            else:
                SEND_QUESTION = False
                quize_lukoil(message)

bot.polling()

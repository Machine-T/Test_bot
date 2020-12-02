import telebot
from telebot import types
#1464548661:AAF2mEOuy0rQ4HL8ABHq56fvZ0b2d23TpIA

validation_answer = ''
var1 = ''
var1_quantity = 0
var2 = ''
var2_quantity = 0
place = ''
person = ''
question = ''
action = ''


bot = telebot.TeleBot("1464548661:AAF2mEOuy0rQ4HL8ABHq56fvZ0b2d23TpIA")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте, я бот для решенния простых арифметических задач с фруктами")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text == 'Привет' or 'привет' or 'hi':
        bot.send_message(message.from_user.id, 'Хорошо, если хотите дать мне задачу то введите "да" или "нет"')
        bot.register_next_step_handler(message, validation_answer)

def validation_answer(message):

    global validation_answer
    validation_answer = message.text
    if validation_answer == 'да':
        bot.send_message(message.from_user.id, 'Для начала создадим условие задачи. '
                                               'В условии может быть несколько переменных, действующие лицо, '
                                               'место действия и ваш вопрос в условии.')

        bot.send_message(message.from_user.id, 'Введите название вашей переменной. Как она будет называться ?')
        bot.register_next_step_handler(message, reg_var1)

    elif validation_answer == 'нет':
        bot.send_message(message.from_user.id, "Ну как-нибудь в другой раз")


def reg_var1(message):
    global var1
    var1 = message.text
    bot.send_message(message.from_user.id, 'Замечательно, а теперь введите количество')
    bot.register_next_step_handler(message, reg_var1_quantity)

def reg_var1_quantity(message):
    global var1_quantity
    var1_quantity = int(message.text)
    bot.send_message(message.from_user.id, 'Хорошо у нас:' + ' ' + str(var1_quantity) + ' ' + var1)
    bot.send_message(message.from_user.id, 'Введите название следующей переменной')
    bot.register_next_step_handler(message, reg_var2)

def reg_var2(message):
    global var2
    var2 = message.text
    bot.send_message(message.from_user.id, 'Отлично, введите теперь количество')
    bot.register_next_step_handler(message, reg_var2_quantity)

def reg_var2_quantity(message):
    global var2_quantity
    var2_quantity = int(message.text)
    bot.send_message(message.from_user.id, 'Хорошо у нас:' + ' ' + str(var2_quantity)
                     + ' ' + var2 + ' ' + 'и' + ' ' + str(var1_quantity) + ' ' + var1)
    bot.send_message(message.from_user.id, 'Напишите где находились переменные')
    bot.register_next_step_handler(message, place_reg)

def place_reg(message):
    global place
    place = message.text
    bot.send_message(message.from_user.id, 'Напишите действующие лицо')
    bot.register_next_step_handler(message, person_reg)

def person_reg(message):
    global person
    person = message.text
    bot.send_message(message.from_user.id, 'Напишите, что сделало действующие лицо с предметами')
    bot.register_next_step_handler(message, action_reg)

def action_reg(message):

    global action
    action = message.text
    bot.send_message(message.from_user.id, 'Напишите ваш вопрос, он должен начинаться со слова "Сколько" ')
    bot.register_next_step_handler(message, question_reg)

def question_reg(message):

    global question
    question = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, place + ' '+'было' + ' ' + str(var2_quantity)+' ' + var2
    + ' '+'и'+' '+str(var1_quantity) + ' ' + var1 + '.' + person + ' ' + action + ' ' + str(var1_quantity)
    + ' ' + var1 + '.' + question + '\n Верно ли записано условие задачи ?', reply_markup=keyboard)
    @bot.callback_query_handler(func= lambda call: True)
    def callback_worker(call):
        if call.data == 'yes':
            bot.send_message(call.message.chat.id, 'Ответ: У нас осталось' + ' ' + str(var2_quantity)+' ' + 'фруктов')

        elif call.data == 'no':
            bot.send_message(call.message.chat.id, 'Попробуем ещё раз !')
            bot.send_message(call.message.chat.id, 'Введите название вашей переменной. Как она будет называться ?')
            bot.register_next_step_handler(call.message, reg_var1)

    #bot.reply_to(message, message.text)

bot.polling()
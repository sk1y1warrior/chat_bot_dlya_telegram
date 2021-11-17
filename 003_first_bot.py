import random
import telebot

token = 'xxxx:xxxxx' # здесь токен, который дают при регистрации
 # нового чат-бота в приложении telegram у юзера @BotFather
 # по этому номеру программа понимает, что это тот самый бот (мой)
 # команды как заводить чат-бота - там же будут выведены

bot = telebot.TeleBot(token)

RANDOM_TASKS = ['Записаться на курс в Нетологию', 'Написать Гвидо письмо',
                'Покормить кошку', 'Помыть машину']

# эти команды вводятся в отдельном чате телеграмм-бота, ссылка на него дается
# так же как и токен при регистрации нового бота у @BotFather
HELP = """
/help - вывести список доступных команд
/add - добавить задачу в список (название задачи
запрашиваем у пользователя).
/show - напечатать все добавленные задачи.
/random - добавить случайную задачу на дату Сегодня"""

tasks = {}

def add_todo(date, task):
    if date in tasks:
        # Дата есть в словаре
        # Добавляем в список задачу
        tasks[date].append(task)
    else:
        # Даты нет в словаре
        # Создаем дату с ключом date
        tasks[date] = []
        tasks[date].append(task)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=['add', 'todo'])
def add(message):
    command = message.text.split(maxsplit=2)
    date = command[1].lower()
    task = command[2]
    add_todo(date, task)
    text = 'Задача ' + task + ' добавлена на дату ' + date
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['random'])
def random_add(message):
    date = 'сегодня'
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    text = 'Задача ' + task + ' добавлена на дату ' + date
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['show', 'print'])
def show(message): # message.text = /print <date>
    command = message.text.split(maxsplit=1)
    date = command[1].lower()
    text = ''
    if date in tasks:
        text = date.upper() + '\n'
        for task in tasks[date]:
            text = text + '[] ' + task + '\n'
    else:
        text = 'Задач на эту дату нет'
    bot.send_message(message.chat.id, text)


# Постоянное обращение к серверам телеграм
bot.polling(none_stop=True)

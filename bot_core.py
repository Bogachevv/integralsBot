import sys
import telebot as tb

from funcBuilders import *
from parser import *
from calc import *

token = open("token.txt").readline()
bot = tb.TeleBot(token)
user_functions = {}


def generator(chat_id: int):
    bot.send_message(chat_id, "Input constants (name=value): ")
    inp = yield
    var_dict = {}
    while (inp != '.') and (inp.strip() != ""):
        name, val = inp.split('=')
        name.strip()
        val.strip()
        var_dict[name] = val
        bot.send_message(chat_id, "Input constants (name=value): ")
        inp = yield

    bot.send_message(chat_id, "Input function: ")
    s = yield
    s = f"({s})"
    bot.send_message(chat_id, "Left limit: ")
    a = yield
    a = str_to_float(var_dict)(a)
    bot.send_message(chat_id, "Right limit: ")
    b = yield
    b = str_to_float(var_dict)(b)
    print()
    polish = translate(s)
    print(polish)
    try:
        res = integral(build_fx(polish, var_dict), a, b)
        print(f"Integral(eps={0.001:.3f}) : {res:.3f}")
        bot.send_message(chat_id, f"Integral(eps={0.001:.3f}) : {res:.3f}")
    except ValueError as err:
        bot.send_message(chat_id, f"Incorrect data")
        print(err.args)


@bot.message_handler(commands=['start'])
def start_msg(message):
    uid = message.from_user.first_name
    bot.reply_to(message, f"Hello, {uid}")
    gen = generator(message.chat.id)
    next(gen)
    user_functions.update({message.chat.id: gen})


def calc_step(msg):
    print(f"Received message: {msg.text!r} from user: {msg.from_user.id}")
    if msg.chat.id not in user_functions:
        bot.send_message(msg.chat.id, "Please, use /start")
        return
    try:
        print(user_functions[msg.chat.id].send(msg.text))
    except StopIteration:
        user_functions.pop(msg.chat.id)


@bot.message_handler()
def receive(msg):
    try:
        calc_step(msg)
    except Exception as ex:
        print(repr(ex), file=sys.stderr)
        bot.send_message(msg.chat.id, "Unexpected error! Calculation process stopped.")
        if msg.chat.id in user_functions:
            user_functions.pop(msg.chat.id)


def run():
    bot.polling()

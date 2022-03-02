import os.path
import sys
import telebot as tb

from funcBuilders import *
from parser import *
from calc import *

token = open("token.txt").readline()
bot = tb.TeleBot(token)
user_functions = {}


def write_config(chat_id, case_sensitive: bool = True, custom_consts: bool = True):
    print(f"Writing {case_sensitive=}, {custom_consts=}")
    with open(f"userData\\{chat_id}.dat", mode="wb") as f:
        barr = bytes([case_sensitive, custom_consts])
        print(barr)
        f.write(barr)
        f.flush()


def get_config(chat_id):
    with open(f"userData\\{chat_id}.dat", mode="rb") as f:
        barr = f.read(2)
        print(barr)
        case_sensitive = bool(barr[0])
        custom_consts = bool(barr[1])
    print(f"Reading {case_sensitive=}, {custom_consts=}")
    return case_sensitive, custom_consts


def generator(chat_id: int):
    var_dict = {}
    case_sensitive, custom_consts = get_config(chat_id)
    if custom_consts:
        bot.send_message(chat_id, "Input constants (name=value): ")
        inp = yield
        while (inp != '.') and (inp.strip() != ""):
            name, val = inp.split('=')
            name.strip()
            name = name if case_sensitive else name.lower()
            val.strip()
            var_dict[name] = val
            bot.send_message(chat_id, "Input constants (name=value): ")
            inp = yield

    bot.send_message(chat_id, "Input function: ")
    s = yield
    s = f"({s})"
    s = s if case_sensitive else s.lower()
    bot.send_message(chat_id, "Left limit: ")
    a = yield
    a = a if case_sensitive else a.lower()
    a = str_to_float(var_dict)(a)
    bot.send_message(chat_id, "Right limit: ")
    b = yield
    b = b if case_sensitive else b.lower()
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


@bot.message_handler(commands=['start', 'run', 'calc'])
def start_msg(message):
    bot.reply_to(message, f"Hello, {message.from_user.first_name}")
    chat_id = message.chat.id
    if not os.path.isfile(f"userData\\{chat_id}.dat"):
        write_config(chat_id)
    gen = generator(chat_id)
    next(gen)
    user_functions.update({chat_id: gen})


def calc_step(msg):
    print(f"Received message: {msg.text!r} from user: {msg.from_user.id}")
    if msg.chat.id not in user_functions:
        bot.send_message(msg.chat.id, "Please, use /start")
        return
    try:
        print(user_functions[msg.chat.id].send(msg.text))
    except StopIteration:
        user_functions.pop(msg.chat.id)


@bot.message_handler(commands=['settings', 'config'])
def settings(msg):
    case_sensitive, custom_consts = get_config(msg.chat.id)
    response = f"Settings list: \n" \
               f"1) /register \n" \
               f"2) /customConsts \n" \
               f"\n" \
               f"Current settings: \n" \
               f"Case sensitive: {case_sensitive}\n" \
               f"Custom constants: {custom_consts}"
    bot.reply_to(msg, response)


@bot.message_handler(commands=['register'])
def register(msg):
    case_sensitive, custom_consts = get_config(msg.chat.id)
    case_sensitive = not case_sensitive
    bot.reply_to(msg, f"Case sensitive: {case_sensitive}")
    write_config(msg.chat.id, case_sensitive, custom_consts)


@bot.message_handler(commands=['customConsts'])
def custom_constants(msg):
    case_sensitive, custom_consts = get_config(msg.chat.id)
    custom_consts = not custom_consts
    bot.reply_to(msg, f"Custom constants: {custom_consts}")
    write_config(msg.chat.id, case_sensitive, custom_consts)


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

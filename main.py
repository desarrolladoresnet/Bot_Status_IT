#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import schedule
import time
import threading
import telebot
import os
import json

API_TOKEN = '6936260144:AAGxx5U4lMqmFpmF6FcHJgmaWZbm9Cgo4oM'
bot = telebot.TeleBot(API_TOKEN, parse_mode=None)

check_equipos = None
channel_id = '-1002107690050'


def send_automatic_status():
    global check_equipos

    if not check_equipos:
        check_equipos = buscar_equipos()

    msg = 'Busqueda automatica:\n'
    m = ''
    for e in check_equipos:
        m += do_ping2(e)

    if len(m) > 1 :
        msg += m
        bot.send_message(chat_id=channel_id, text=msg)


def do_ping(equipos):
    msg = ''
    for e in equipos:
        print(f"{e}")
        result = check_equipo(e)
        if result:
            msg += result
    if not msg:
        msg = "Sin cambios"
    return msg


def do_ping2(e):
    msg = ''
    print(f"{e}")
    result = check_equipo(e)
    if result:
        msg += result
    # if len(msg.strip()) <= 1:
    #     print("sin cambios")
    #     msg = "Sin cambios"
    return msg

def check_equipo(e):
    try:
        message = ''
        name = e["name"]
        ip = e['ip']
        if ping(ip):
            if 'state' not in e or e["state"] != True:
                message = f"{name} UP 🟩\n"
                e["state"] = True
                print(f"{e} Arriba")
        else:
            if 'state' not in e or e["state"] != False:
                message = f"{name} DOWN 🟥\n"
                e["state"] = False
                print(f"{e} Caido")
        return message
    except KeyError as ke:
        print(f"KeyError: {ke}")
        return ''
    except Exception as ex:
        print(f"Error: {ex}")
        return ''

def ping(host):
    response = os.system("ping -c 1 " + host)
    if response == 0:
        print(host, 'is up!')
        return True
    else:
        print(host, 'is down!')
        return False

def buscar_equipos():
    try:
        with open('equipos.json') as f:
            data = json.load(f)
        return data.get("equipos", [])
    except json.JSONDecodeError as jde:
        print(f"Error al cargar equipos (JSONDecodeError): {jde}")
        return []
    except Exception as ex:
        print(f"Error al cargar equipos: {ex}")
        return []

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    print(f"message {message}")
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

@bot.message_handler(commands=['status'])
def send_status1(message):
    global check_equipos

    if not check_equipos:
        check_equipos = buscar_equipos()

    bot.reply_to(message, "Buscando estado de los equipos, espere un momento.")
    msg = 'ESTADO:\n'
    msg += do_ping(check_equipos)
    bot.reply_to(message, msg)

@bot.channel_post_handler(['run'])
def send_status(message):
    global check_equipos

    if not check_equipos:
        check_equipos = buscar_equipos()

    bot.reply_to(message, "Buscando estado de los equipos, espere un momento.")
    msg = do_ping(check_equipos)
    bot.reply_to(message, msg)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.chat.type == 'channel':
        if '@echobot' in message.text:
            print(message.chat.id)
            bot.send_message(message.chat.id, message.text.replace('@echobot', ''))
    else:
        print(message.chat.id)
        bot.reply_to(message, message.text)

def job():
    threading.Thread(target=send_automatic_status).start()

def bot_polling():
    bot.infinity_polling()

def main():
    schedule.every(30).seconds.do(job)
    threading.Thread(target=bot_polling).start()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

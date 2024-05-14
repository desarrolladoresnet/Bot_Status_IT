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
bot = telebot.TeleBot(API_TOKEN,  parse_mode=None)

check_equipos = None
channel_id = '-1002107690050'

def ping(host):
    response = os.system("ping -c 1 " + host)
    if response == 0:
        print(host, 'is up!')
        return True
    else:
        print(host, 'is down!')
        return False


def buscar_equipos():
    with open('equipos.json') as f:
        data = json.load(f)

    return data.get("equipos", {})

def check_equipo(e, msj):
        # print(f"E = {e}")
        try:
            message = ''
            
            name = e["name"]
            ip = e['ip']
            if ping(ip):
                    if 'state' not in e or e["state"] != True or msj:
                        message = f"{name} UP 🟩\n"
                        e["state"] = True
                        print(e)
            else:
                    if 'state' not in e or e["state"] != False or msj:
                        message = f"{name} DOWN 🟥\n"
                        e["state"] = False
                        print(e)

            return message
        except Exception as e:
            print(e)
            pass


def do_ping(equipos, msj=False):
    while True:
        msg = '\n'
        for e in equipos:
            print(f"{e}")
            msg += check_equipo(e, msj)
            print(len(msg))
            if len(msg) <= 1:
                print("sin cambios")
                msg = "Sin cambios" 
        return msg
        # time.sleep(15)
        # print('-------------------------------\n')


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    print(f"message {message}")
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")
    
# Handle '/start' and '/help'
@bot.message_handler(commands=['status'])
def send_status1(message):
    global check_equipos

    if not check_equipos:
         check_equipos = buscar_equipos()

    bot.reply_to(message, "Buscando estado de los equipos, espere un momento.")
    msg = 'ESTADO:\n'
    msg += (do_ping(check_equipos, True))


    bot.reply_to(message, msg)


# Handle 'status'
# @bot.edited_channel_post_handler(['run'])
@bot.channel_post_handler(['run'])
def send_status(message):
    global check_equipos

    if not check_equipos:
         check_equipos = buscar_equipos()

    bot.reply_to(message, "Buscando estado de los equipos, espere un momento.")
    msg = (do_ping(check_equipos))
    bot.reply_to(message, msg)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    # print(message.chat.type)
    if message.chat.type == 'channel':
        if '@echobot' in message.text:
            print(message.chat.id)
            bot.send_message(message.chat.id, message.text.replace('@echobot', ''))
    else:
        print(message.chat.id)
        bot.reply_to(message, message.text)



def send_automatic_status():
    global check_equipos

    if not check_equipos:
         check_equipos = buscar_equipos()

    msg = 'Busqueda automatica:\n'
    msg += (do_ping(check_equipos))

    if "Sin cambios" in msg:
        print("no hubo cambios")
        pass
    
    else:
        bot.send_message(chat_id=channel_id, text=msg)


def job():
    threading.Thread(target=send_automatic_status).start()


def bot_polling():
    bot.infinity_polling()

def main():
    schedule.every(1).minutes.do(job)

    # Start bot polling in a separate thread
    threading.Thread(target=bot_polling).start()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
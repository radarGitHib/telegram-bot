import telebot
import random
from telebot import types

bot = telebot.TeleBot("8953043068:AAHVqLeMLXvt3yaNstFXZe0lTWljCtxqBdc")

balance = {}

def get_balance(uid):
    if uid not in balance:
        balance[uid] = 0
    return balance[uid]

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    get_balance(uid)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Баланс", "🎁 Бонус")
    bot.send_message(
        message.chat.id,
        "🎰 Добро пожаловать в Кубик-Казино!\n\n"
        "🎁 /bonus — получить 1000 валюты (1 раз)\n"
        "🎲 кубы чет 250\n"
        "🎲 кубы нечет 500\n\n"
        "Удачи, брат! 🍀",
        reply_markup=markup
    )

@bot.message_handler(commands=['bonus'])
def bonus(message):
    uid = message.from_user.id
    get_balance(uid)
    if balance[uid] > 0:
        bot.send_message(message.chat.id, "❌ Ты уже брал бонус!")
        return
    balance[uid] += 1000
    bot.send_message(message.chat.id, "🎁 Бонус получен: +1000 💰\n\n🎲 Играй: кубы чет 250")

@bot.message_handler(func=lambda m: m.text == "💰 Баланс")
def show_balance(message):
    uid = message.from_user.id
    bot.send_message(message.chat.id, f"💵 Твой баланс: {get_balance(uid)} 💰")

@bot.message_handler(func=lambda m: m.text == "🎁 Бонус")
def bonus_button(message):
    bonus(message)

@bot.message_handler(func=lambda m: m.text.lower().startswith("кубы"))
def cubes(message):
    uid = message.from_user.id
    get_balance(uid)

    parts = message.text.lower().split()
    if len(parts) != 3:
        bot.send_message(message.chat.id, "❌ Формат: кубы чет 250")
        return

    choice = parts[1]
    try:
        bet = int(parts[2])
    except:
        bot.send_message(message.chat.id, "❌ Ставка должна быть числом!")
        return

    if choice not in ["чет", "нечет"]:
        bot.send_message(message.chat.id, "❌ Выбери: чет или нечет")
        return

    if bet <= 0:
        bot.send_message(message.chat.id, "❌ Ставка должна быть больше 0!")
        return

    if bet > balance[uid]:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств!\n💵 Баланс: {balance[uid]}")
        return

    dice = random.randint(1, 6)
    is_even = dice % 2 == 0
    win = (choice == "чет" and is_even) or (choice == "нечет" and not is_even)

    if win:
        balance[uid] += bet
        bot.send_message(
            message.chat.id,
            f"🎲 Кубик: {dice}\n"
            f"🎉 ПОБЕДА! +{bet} 💰\n"
            f"💵 Баланс: {balance[uid]}"
        )
    else:
        balance[uid] -= bet
        bot.send_message(
            message.chat.id,
            f"🎲 Кубик: {dice}\n"
            f"😢 Проигрыш... -{bet} 💰\n"
            f"💵 Баланс: {balance[uid]}"
        )

bot.polling(none_stop=True)

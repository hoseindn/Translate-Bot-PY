from telebot import types
import telebot
from googletrans import Translator

# توکن ربات تلگرام
TOKEN = 'توکن ربات تلگرام شما'
bot = telebot.TeleBot(TOKEN)
translator = Translator()

user_lang_settings = {}

# لیست زبان‌ها
LANGUAGES = {
    'English': 'en',
    'Persian': 'fa',
    'French': 'fr',
    'German': 'de',
    'Spanish': 'es',
    'Arabic': 'ar',
    # می‌توانید زبان‌های بیشتری اضافه کنید
}


def generate_language_buttons(prefix):
    markup = types.InlineKeyboardMarkup()
    for lang_name, lang_code in LANGUAGES.items():
        button = types.InlineKeyboardButton(lang_name, callback_data=f"{prefix}:{lang_code}")
        markup.add(button)
    return markup


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    button_src = types.KeyboardButton("انتخاب زبان مبدأ")
    button_dest = types.KeyboardButton("انتخاب زبان مقصد")
    markup.add(button_src, button_dest)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! خوش آمدید🌻 به ربات مترجم [متن ؛ جمله و ...]",
                     reply_markup=main_keyboard())
    bot.send_message(message.chat.id, " لطفا زبان مبدأ و مقصد را انتخاب کنید:",
                     reply_markup=main_keyboard())


@bot.message_handler(func=lambda message: message.text == "انتخاب زبان مبدأ")
def choose_src_lang(message):
    bot.send_message(message.chat.id, "لطفا زبان مبدأ را انتخاب کنید:", reply_markup=generate_language_buttons("src"))


@bot.message_handler(func=lambda message: message.text == "انتخاب زبان مقصد")
def choose_dest_lang(message):
    bot.send_message(message.chat.id, "لطفا زبان مقصد را انتخاب کنید:", reply_markup=generate_language_buttons("dest"))


@bot.callback_query_handler(func=lambda call: call.data.startswith("src:") or call.data.startswith("dest:"))
def callback_query(call):
    if call.data.startswith("src:"):
        src_lang = call.data.split(":")[1]
        if call.message.chat.id not in user_lang_settings:
            user_lang_settings[call.message.chat.id] = {}
        user_lang_settings[call.message.chat.id]['src'] = src_lang
        bot.send_message(call.message.chat.id, f"زبان مبدأ به {src_lang} تنظیم شد.", reply_markup=main_keyboard())
    elif call.data.startswith("dest:"):
        dest_lang = call.data.split(":")[1]
        if call.message.chat.id not in user_lang_settings:
            user_lang_settings[call.message.chat.id] = {}
        user_lang_settings[call.message.chat.id]['dest'] = dest_lang
        bot.send_message(call.message.chat.id, f"زبان مقصد به {dest_lang} تنظیم شد.", reply_markup=main_keyboard())


@bot.message_handler(func=lambda message: True)
def translate_message(message):
    chat_id = message.chat.id
    if chat_id in user_lang_settings:
        settings = user_lang_settings[chat_id]
        if 'src' in settings and 'dest' in settings:
            translated = translator.translate(message.text, src=settings['src'], dest=settings['dest'])
            bot.reply_to(message, translated.text)
        else:
            bot.reply_to(message, "لطفا هر دو زبان مبدأ و مقصد را تنظیم کنید.")
    else:
        bot.reply_to(message, "لطفا ابتدا زبان مبدأ و مقصد را تنظیم کنید.")


bot.polling()

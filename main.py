import random
import GeneratqQuestion
import telebot
from telebot import types

class TrueWords:
    true = None
    chatid = None

class WordList:
    wordList = []

class Words:
    def __init__(self, ruTrans, enTrans):
        self.enTrans = enTrans
        self.ruTrans = ruTrans

def dolwodWords():
    with open('i.txt', 'r', encoding='utf-8') as file:
        content = file.readlines()  # file.read() # Или file.readline() / file.readlines()
    for i in range(len(content)):
        a = (content[i].replace(" ", "")).split("-")
        if len(a) == 2:
            WordList.wordList.append(Words(a[0], a[1][:len(a[1]) - 1]))
    print("")

def generatListWords(colChoice):
    chosenWords = []
    k = []
    for i in range(colChoice):
        indWord = random.randint(0, len(WordList.wordList)-1)
        while indWord in k:
            indWord = random.randint(0, len(WordList.wordList) - 1)
        k.append(indWord)
        chosenWords.append(WordList.wordList[indWord])
    return chosenWords

API_TOKEN = '7501771237:AAF9qQipemYKqHMlCJmAWnMDcOWjsf0xLQ4'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['manu', 'start'])
def startWorking(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    item1 = types.KeyboardButton('слова из бота')
    item2 = types.KeyboardButton('слова из своего файла')
    markup.add(item1, item2)  # Добавляем кнопки
    bot.send_message(message.chat.id, text="s", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "слова из бота" or message.text == "слова из своего файла")
def chuseVarians(message):
    if message.text == "слова из бота":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        item1 = types.KeyboardButton('учить')
        item2 = types.KeyboardButton('список всех слов')
        markup.add(item1, item2)  # Добавляем кнопки
        bot.send_message(message.chat.id, text="s ", reply_markup=markup)
    elif message.text == "слова из своего файла":
        bot.send_message(message.chat.id, text="отправьте файл с словами записанными в формате\n слово - перевод\n слово - перевод")

@bot.message_handler(func=lambda message: message.text == "учить")
def learnWords(message):
    if WordList.wordList == []:
        dolwodWords()
    colVarians = 4
    words = generatListWords(colVarians)
    true = words[random.randint(0, colVarians - 1)]
    TrueWords.true = true
    TrueWords.chatid = message.chat.id
    answers = types.InlineKeyboardMarkup()
    for i in range(len(words)):
        answer = types.InlineKeyboardButton(text=words[i].enTrans, callback_data=f"{words[i].ruTrans}")
        answers.add(answer)
    bot.send_message(message.chat.id, true.ruTrans, reply_markup=answers)

@bot.callback_query_handler(func=lambda call: call.data == f"{TrueWords.true.ruTrans}")
def giveAnsver(call):
    bot.send_message(TrueWords.chatid, "правильно")

@bot.callback_query_handler(func=lambda call: call.data != f"{TrueWords.true.ruTrans}")
def giveAnsver(call):
    bot.send_message(TrueWords.chatid, "неправильно")

bot.infinity_polling()

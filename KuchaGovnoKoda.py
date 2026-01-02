import random
import telebot
from telebot import types
import sqlite3

class TrueWords:
    true = None
    chatid = None

class WordList:
    wordList = []

class Words:
    def __init__(self, ruTrans, enTrans):
        self.enTrans = enTrans
        self.ruTrans = ruTrans

def dolwodWords(fileName, a):
    print("d1")
    content = None
    if a:
        with open(f'{fileName}', 'r', encoding='utf-8') as file:
            print("d2")
            content = file.read()  # file.read() # Или file.readline() / file.readlines()
        print(content, type(content), "d3")
        return content
    else:
        with open(f'{fileName}', 'r', encoding='utf-8') as file:
            print("d2")
            content = file.readlines()  # file.read() # Или file.readline() / file.readlines()
    words = []
    for i in range(len(content)):
        a = (content[i].replace(" ", "")).split("-")
        if len(a) == 2:
            words.append(Words(a[0], a[1][:len(a[1]) - 1]))
    print(words, "d4")
    return words

def generatListWords(colChoice, wordlist):
    print(wordlist)
    chosenWords = []
    k = []
    for i in range(colChoice):
        indWord = random.randint(0, len(wordlist)-1)
        while indWord in k:
            indWord = random.randint(0, len(wordlist) - 1)
        k.append(indWord)
        chosenWords.append(wordlist[indWord])
    return chosenWords

API_TOKEN = '7501771237:AAF9qQipemYKqHMlCJmAWnMDcOWjsf0xLQ4'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['manu', 'start'])
def startWorking(message):
    WordList.wordList = dolwodWords("i.txt", False)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    item1 = types.KeyboardButton('слова из бота')
    item2 = types.KeyboardButton('слова из своего файла')
    markup.add(item1, item2)  # Добавляем кнопки
    bot.send_message(message.chat.id, text="s", reply_markup=markup)
    print(WordList.wordList)

@bot.message_handler(func=lambda message: message.text == "слова из бота" or message.text == "слова из своего файла")
def chuseVarians(message):
    if message.text == "слова из бота":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        item1 = types.KeyboardButton('учить слова из бота')
        item2 = types.KeyboardButton('список всех слов')
        markup.add(item1, item2)  # Добавляем кнопки
        bot.send_message(message.chat.id, text="s ", reply_markup=markup)
    elif message.text == "слова из своего файла":
        bot.send_message(message.chat.id, text="отправьте файл(txt) с словами записанными в формате\n слово - перевод\n слово - перевод")
        bot.register_next_step_handler(message, getUserWordsFile)

def getUserWordsFile(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'D:/PythonProject/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        conn = sqlite3.connect("userWords.sql")
        cur =  conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS usersWordLists (chatId INT, words TEXT)')
        cur.execute("DELETE FROM usersWordLists WHERE chatid = ?",
                    (message.chat.id,))
        cur.execute("INSERT INTO usersWordLists (chatId, words) VALUES (?, ?)",
                    (message.chat.id, dolwodWords(f"{message.document.file_name}", True)))
        conn.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        item1 = types.KeyboardButton('учить слова из файла')
        item2 = types.KeyboardButton('список всех слов из файла')
        markup.add(item1, item2)  # Добавляем кнопки
        bot.send_message(message.chat.id,"продолжим", reply_markup=markup)
    except Exception:
        bot.reply_to(message,  "это не то что я хотел увидеть попробуй еще")

@bot.message_handler(func=lambda message: message.text == "список всех слов из файла")
def learnWordsUsers(message):
    bot.send_document(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "учить слова из файла")
def learnWords(message):
    colVarians = 4
    conn = sqlite3.connect("userWords.sql")
    cur = conn.cursor()
    cur.execute("SELECT * FROM usersWordLists")
    data = cur.fetchall()
    print("dsd", data)
    words = []
    wordlist = []
    print(message.chat.id, type(message.chat.id))
    for i in data:
        print(i)
        if str(message.chat.id) == i[0]:
            words = i[1].splitlines()
    print("w", words)
    for i in range(len(words)):
        a = (words[i].replace(" ", "")).split("-")
        print(a)
        if len(a) == 2:
            wordlist.append(Words(a[0], a[1][:]))
    print("wl", wordlist)
    for i in wordlist:
        print(i.ruTrans, i.enTrans)
    words = generatListWords(colVarians, wordlist)
    true = words[random.randint(0, colVarians - 1)]
    TrueWords.true = true
    TrueWords.chatid = message.chat.id
    answers = types.InlineKeyboardMarkup()
    for i in range(len(words)):
        answer = types.InlineKeyboardButton(text=words[i].enTrans, callback_data=f"{words[i].ruTrans}")
        answers.add(answer)
    bot.send_message(message.chat.id, true.ruTrans, reply_markup=answers)

@bot.message_handler(func=lambda message: message.text == "список всех слов")
def listWordsBot(message):
    bot.send_document(message.chat.id, open(r'i.txt', 'rb'))

@bot.message_handler(func=lambda message: message.text == "учить слова из бота")
def learnWordsBot(message):
    if WordList.wordList == []:
        WordList.wordList = dolwodWords("i.txt", False)
    print(WordList.wordList)
    colVarians = 4
    words = generatListWords(colVarians, WordList.wordList)
    true = words[random.randint(0, colVarians - 1)]
    TrueWords.true = true
    TrueWords.chatid = message.chat.id
    answers = types.InlineKeyboardMarkup()
    for i in range(len(words)):
        answer = types.InlineKeyboardButton(text=words[i].enTrans, callback_data=f"{words[i].ruTrans}")
        answers.add(answer)
    bot.send_message(message.chat.id, true.ruTrans, reply_markup=answers)

@bot.callback_query_handler(func=lambda call: True)
def giveAnsver(call):
    if call.data == f"{TrueWords.true.ruTrans}":
        bot.send_message(TrueWords.chatid, "правильно")
    else:
        bot.send_message(TrueWords.chatid, "неправильно")

bot.infinity_polling()

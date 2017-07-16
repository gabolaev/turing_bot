import datetime

import telebot
from telebot import *

import config
import dbUtils
import problemBuilding

bot = telebot.TeleBot(config.token)

# Главная клавиатура
main = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
main.row("🎲Случайная задача🎲", "🎓Буду ботать🎓")
main.row("🎭Буду читать мемесы🎭")

# ЕГЭ-Меню клавиатура
menuEge = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
menuEge.row('Вариант', 'II часть', 'Ларин')
menuEge.row(config.toBegin)

# Буду ботать клавиатура
typeOfBotka = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
typeOfBotka.row('ДВИ', 'ЕГЭ')
typeOfBotka.row(config.toBegin)

# II часть клавиатура
secondPart = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
secondPart.row('13', '14', '15', '16', '17', '18', '19')
secondPart.row(config.toBegin)

# ДВИ годы клавиатура
dviYears = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
dviYears.row('2017', '2016', '2015', '2014')
dviYears.row('2013', '2012', '2011', '2010')
dviYears.row('2009', '2008', '2007', '2006')
dviYears.row(config.toBegin)


def logging(msg=None, text=None):
    if (msg):
        logFormat = [msg.chat.id, msg.chat.username, msg.text] if (type(msg) is telebot.types.Message) else [msg.message.chat.id, msg.message.chat.username, msg.data]
        logLine = datetime.datetime.now().strftime("%H:%M:%S // %d.%m.%Y // ") + "{} ({}): {}".format(*logFormat)
    else:
        logLine = text
    with open(config.logFilePath, 'a+') as log:
        log.write("{}\n".format(logLine))
        log.close()
    print(logLine)


def whatTheFuckMan(msg):
    bot.send_message(msg.chat.id,
                     text=config.whatTheFuckMessage)


def sendProblemToUser(msg, egeNumber=None, year=None, variant=None):
    if (egeNumber):
        problemID, path, problemKeyboard, tags = problemBuilding.getEgeProblem(egeNumber)
        dbUtils.addUserProblemHistory(msg.chat.id, problemID)
    else:
        path, problemKeyboard, tags = problemBuilding.getDviProblem(year, variant)

    photo = open(path, 'rb')
    try:
        bot.send_photo(msg.chat.id, photo=photo, reply_markup=problemKeyboard, caption=tags)
    finally:
        photo.close()


def sendLarinVariant(msg, variantNumber):
    with open(config.bankPath + config.larinPathPattern.replace('*', str(variantNumber)), 'rb') as larinFile:
        bot.send_document(msg.chat.id, data=larinFile)


def showDVIVariants(msg, year):
    variants = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    llt = []

    for i in range(1, 5):
        llt.append(dict(text=str(i) + ' ({})'.format(year)))
    variants.keyboard = [llt]
    variants.row(config.toBegin)

    bot.send_message(msg.chat.id, text="Выберите вариант.", reply_markup=variants)


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    logging(msg=message)
    dbUtils.addUser(message)
    bot.send_message(message.chat.id,
                     parse_mode="HTML",
                     text="<b>NLog(N) Turing BOT</b>", reply_markup=main)
    bot.send_message(message.chat.id, parse_mode="HTML", text="<i>v1.2 (beta)</i>")
    bot.send_message(message.chat.id, parse_mode="HTML", text=config.helloMessage)

    mainlinks = types.InlineKeyboardMarkup(row_width=3)
    gitBookBtn = types.InlineKeyboardButton(text="GitBook",
                                            url="https://timyrik20.gitbooks.io/nlogn/")
    siteBtn = types.InlineKeyboardButton(text="Telegram-чат",
                                         url="https://t.me/joinchat/EvGqu0MpwttTiIWBl-rx7w")
    telegramChannelBtn = types.InlineKeyboardButton(text="Telegram-канал",
                                                    url="https://t.me/nlognege")

    mainlinks.add(gitBookBtn, siteBtn, telegramChannelBtn)
    bot.send_message(message.chat.id,
                     text="Timur Guev @timyrik20\n"
                          "George Gabolaev @gabolaev\n"
                          "Nelli Khlustova @nelli_snow", reply_markup=mainlinks)

    vkGroupsLinks = types.InlineKeyboardMarkup()
    egeBtn = types.InlineKeyboardButton(text="📓 ЕГЭ математика.", url="https://vk.com/nlognege")
    olympBtn = types.InlineKeyboardButton(text="🏆 Олимп. подготовка", url="https://vk.com/nlognolymp")
    csBtn = types.InlineKeyboardButton(text="💻 Комп. науки", url="https://vk.com/nlogncs")

    vkGroupsLinks.add(egeBtn, olympBtn, csBtn)
    bot.send_message(message.chat.id,
                     text=config.aboutVkMessage, reply_markup=vkGroupsLinks)


@bot.message_handler(regexp='ДВИ')
def wantDVIProblem(msg):
    logging(msg=msg)
    bot.send_message(msg.chat.id, text="Выберите год.", reply_markup=dviYears)


@bot.message_handler(regexp='Буду ботать')
def showTypesOfBotka(msg):
    bot.send_message(msg.chat.id, text='Выберите тип экзамена.', reply_markup=typeOfBotka)


@bot.message_handler(regexp='ЕГЭ')
def wantEgeProblem(msg):
    logging(msg=msg)
    bot.send_message(msg.chat.id, text="Выберите часть?", reply_markup=menuEge)


@bot.message_handler(regexp='Случайная задача')
def wantProblem(msg):
    logging(msg=msg)
    egeNumber = dbUtils.getRandomEgeNumber()
    sendProblemToUser(msg, egeNumber)


@bot.message_handler(regexp='Вариант')
def randomVariant(msg):
    logging(msg=msg)
    for i in range(13, 20):
        sendProblemToUser(msg, i)
        # time.sleep(1)


@bot.message_handler(regexp='II часть')
def partC(msg):
    logging(msg=msg)
    bot.send_message(msg.chat.id, text='Выберите номер задания.', reply_markup=secondPart)


@bot.message_handler(regexp='Ларин')
def larin(msg):
    logging(msg=msg)
    keyboard = problemBuilding.getLarinVariantsKeyboard()
    bot.send_message(msg.chat.id, text='Выберите вариант.', reply_markup=keyboard)


@bot.message_handler(regexp='В начало')
def beginning(msg):
    logging(msg=msg)
    bot.send_message(msg.chat.id, text='Возвращаемся', reply_markup=main)


@bot.message_handler(regexp='Буду читать мемесы')
def mem(msg):
    try:
        mem = dbUtils.getMem()
        bot.send_message(msg.chat.id, text=mem)
        logging(msg=msg)
    except(telebot.apihelper.ApiException):
        bot.send_message(msg.chat.id, text='Помедленнее, пожалуйста, {}. Я не выдерживаю.'.format(msg.chat.username))


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    logging(call)
    with open(call.data, "rb") as file:
        if call.data[11] == 'E':
            bot.send_photo(call.message.chat.id, photo=file)
        else:
            bot.send_document(call.message.chat.id, data=file)


@bot.message_handler(content_types=["text"])
def parseText(msg):
    logging(msg=msg)
    try:

        intValue = int(msg.text)
        if config.minEgeProblemNumber <= intValue <= config.maxEgeProblemNumber:  # ЕГЭ
            sendProblemToUser(msg=msg, egeNumber=intValue)
        elif config.minDVIYear <= intValue <= config.maxDVIYear:  # ДВИ
            showDVIVariants(msg, intValue)
        else:
            whatTheFuckMan(msg)
    except(Exception):
        try:
            if (msg.text[0:3] == 'Вар'):  # ЛАРИН
                sendLarinVariant(msg, msg.text[5::])
            else:
                sendProblemToUser(msg=msg, year=int(msg.text[3:7]), variant=int(msg.text[0]))  # ГОД ДВИ
        except Exception as ex:
            whatTheFuckMan(msg)
            logging(text=ex)


if __name__ == '__main__':
    logging(text="Enabling the bot in {}".format(datetime.datetime.now().strftime("%H:%M:%S // %d.%m.%Y // ")))
    bot.polling(none_stop=True)
    logging(text="\n Disabling the bot in {}".format(datetime.datetime.now().strftime("%H:%M:%S // %d.%m.%Y // ")))

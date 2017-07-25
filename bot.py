import random

import telebot

sys_random = random.SystemRandom()

from telebot import *
from config import *
import dbUtils
import problemBuilding

bot = telebot.TeleBot(token)

# Главная клавиатура
main = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
main.row("🎲Случайная задача🎲", "🎓Буду ботать🎓")
main.row("🎭Буду читать мемесы🎭")
main.row("📕Как оно работает?📕")

# ЕГЭ Меню клавиатура
menuEge = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
menuEge.row('Вариант', 'II часть', 'Ларин')
menuEge.row(toBegin)

# Буду ботать клавиатура
typeOfBotka = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
typeOfBotka.row('ДВИ', 'ЕГЭ')
typeOfBotka.row(toBegin)

# II часть клавиатура
secondPart = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
secondPart.row('13', '14', '15', '16', '17', '18', '19')
secondPart.row(toBegin)

# ДВИ годы клавиатура
dviYears = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
dviYears.row('2017', '2016', '2015', '2014')
dviYears.row('2013', '2012', '2011', '2010')
dviYears.row('2009', '2008', '2007', '2006')
dviYears.row(toBegin)


def logFromMsg(msg):
    log.info('{} ({}): {}'.format(msg.chat.id, msg.chat.username, msg.text))


def whatTheFuckMan(msg):
    bot.send_message(msg.chat.id, text=sys_random.choice(whatTheFuckMessage))


def sendProblemToUser(msg, egeNumber=None, year=None, variant=None, problemID=None):
    try:
        if egeNumber:
            problemID, path, problemKeyboard, tags = problemBuilding.getEgeProblem(
                dbUtils.getEgeProblem(msg, egeNumber=egeNumber))
            dbUtils.addUserProblemHistory(msg.chat.id, problemID)
        elif problemID:
            _, path, problemKeyboard, tags = problemBuilding.getEgeProblem(
                dbUtils.getEgeProblem(msg, problemID=problemID))
        else:
            path, problemKeyboard, tags = problemBuilding.getDviProblem(year, variant)

        photo = open(path, 'rb')
        bot.send_photo(msg.chat.id, photo=photo, reply_markup=problemKeyboard, caption=tags)
        photo.close()

    except(Exception):
        pass


def sendLarinVariant(msg, variantNumber):
    try:
        with open(bankPath + larinPathPattern.replace('*', str(variantNumber)), 'rb') as larinFile:
            bot.send_document(msg.chat.id, data=larinFile)
    except(Exception):
        bot.send_message(msg.chat.id, text="У меня возникли трудности с поиском этого варианта. А он точно есть?")


def showDVIVariants(msg, year):
    variants = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    variants.keyboard = [[dict(text=str(i) + ' ({})'.format(year)) for i in range(1, 5)]]
    variants.row(toBegin)

    bot.send_message(msg.chat.id, text="Выберите вариант.", reply_markup=variants)


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    logFromMsg(message)
    dbUtils.addUser(message)
    bot.send_message(message.chat.id,
                     parse_mode="HTML",
                     text="<b>NLog(N) Turing BOT</b>", reply_markup=main)
    bot.send_message(message.chat.id, parse_mode="HTML", text="<i>v1.3.3 (beta)</i>")
    bot.send_message(message.chat.id, parse_mode="HTML", text=helloMessage)

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
                     text=aboutVkMessage, reply_markup=vkGroupsLinks)


@bot.message_handler(regexp=dvi)
def wantDVIProblem(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text="Выберите год.", reply_markup=dviYears)


@bot.message_handler(regexp=issue)
def issue(msg):
    logFromMsg(msg)
    dbUtils.addIssue(msg.chat.id, msg.text)
    bot.send_message(msg.chat.id, text="Спасибо, скоро исправим.")
    bot.send_message(adminsGroup, text=aboutIssue.format(msg.chat.id, msg.chat.username, msg.text))


@bot.message_handler(regexp=thanks)
def parseLarinVariant(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id,
                     text='Если я не ошибся, ты хвалишь меня) Спасибо, {}! С тобой очень приятно работать.'.format(
                         msg.chat.username))


@bot.message_handler(regexp=tellMe)
def whoami(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text="Наверно, ты хочешь узнать про меня. Так вот...")
    bot.send_message(msg.chat.id, text=helloMessage)
    bot.send_message(msg.chat.id, text="А ещё в моей документации написано вот это.")
    bot.send_message(msg.chat.id, text=description)


@bot.message_handler(regexp=hello)
def sayHello(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text='Вроде здоровались, но я всегда рад тебе) Привет!')


@bot.message_handler(regexp=working)
def showTypesOfBotka(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text='Выбери тип экзамена.', reply_markup=typeOfBotka)


@bot.message_handler(regexp=documentation)
def documentation(msg):
    logFromMsg(msg)
    with open(docPath, 'rb') as doc:
        bot.send_document(msg.chat.id, data=doc, caption='Красивая инструкция.')


@bot.message_handler(regexp=ege)
def wantEgeProblem(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text="Как именно будем ботать ЕГЭ?", reply_markup=menuEge)


@bot.message_handler(regexp=random)
def wantProblem(msg):
    logFromMsg(msg)
    egeNumber = dbUtils.getRandomEgeNumber()
    sendProblemToUser(msg, egeNumber=egeNumber)


@bot.message_handler(regexp=part2)
def partC(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text='Выбери номер задания.', reply_markup=secondPart)


@bot.message_handler(regexp=back)
def beginning(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text='Возвращаемся', reply_markup=main)


@bot.message_handler(regexp=recourse)
def beginning(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text='Что?', reply_markup=main)


@bot.message_handler(regexp=mem)
def mem(msg):
    try:
        mem = dbUtils.getMem()
        bot.send_message(msg.chat.id, text=mem)
        logFromMsg(msg)
    except(telebot.apihelper.ApiException):
        bot.send_message(msg.chat.id, text='Помедленнее, пожалуйста, {}. Я не выдерживаю.'.format(msg.chat.username))


@bot.message_handler(regexp=variant)
def randomVariant(msg):
    logFromMsg(msg)
    for i in range(13, 20):
        sendProblemToUser(msg, egeNumber=i)


@bot.message_handler(regexp=var)
def parseLarinVariant(msg):
    logFromMsg(msg)
    sendLarinVariant(msg, msg.text[4::])


@bot.message_handler(regexp=larin)
def larin(msg):
    logFromMsg(msg)
    keyboard = problemBuilding.getLarinVariantsKeyboard()
    bot.send_message(msg.chat.id, text='Выбери вариант.', reply_markup=keyboard)


@bot.message_handler(regexp='get')
def getParse(msg):
    logFromMsg(msg)
    try:
        sendProblemToUser(msg, problemID=int(msg.text[4::]))
    except:
        whatTheFuckMan(msg)


@bot.message_handler(regexp='дай')
def getAlias(msg):
    getParse(msg)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    logger.info(call)
    with open(call.data, "rb") as file:
        if call.data[17] == 'E':
            bot.send_photo(call.message.chat.id, photo=file)
        else:
            bot.send_document(call.message.chat.id, data=file)


@bot.message_handler(content_types=["text"])
def parseText(msg):
    logFromMsg(msg)
    try:

        intValue = int(msg.text)
        if minEgeProblemNumber <= intValue <= maxEgeProblemNumber:  # Пришел номер ЕГЭ
            sendProblemToUser(msg, egeNumber=intValue)
        elif minDVIYear <= intValue <= maxDVIYear:  # Пришел год ДВИ
            showDVIVariants(msg, intValue)
        else:
            whatTheFuckMan(msg)
    except Exception:
        try:
            sendProblemToUser(msg, year=int(msg.text[3:7]), variant=int(msg.text[0]))  # ГОД ДВИ
        except Exception:
            whatTheFuckMan(msg)


if __name__ == '__main__':
    try:
        log.debug(botEnabling)
        bot.polling(none_stop=True)
        log.debug(botDisabling)
    except(Exception) as ex:
        log.error(ex)

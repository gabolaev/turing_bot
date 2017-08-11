import random

import telebot

sys_random = random.SystemRandom()
from config import *
import dbUtils
import problemBuilding

bot = telebot.TeleBot(token)


def logFromMsg(msg):
    form = '{} ({}) [{} {}] : {}'
    if msg.chat.id < 0:
        form = 'Из чата {} // '.format(msg.chat.id) + form
    log.info(form.format(msg.from_user.id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name, msg.text))


def whatTheFuckMan(msg):
    bot.send_message(msg.chat.id, text=sys_random.choice(whatTheFuckMessage))

def sendFileToUser(msg, path, problemKeyboard, tags):
    with open(path, 'rb') as file:
        bot.send_document(msg.chat.id, data=file, reply_markup=problemKeyboard, caption=tags)

def sendPhotoToUser(msg, path, problemKeyboard, tags):
    with open(path, 'rb') as file:
        bot.send_photo(msg.chat.id, photo=file, reply_markup=problemKeyboard, caption=tags)

def constructProblemBeforeSending(msg, egeNumber=None, year=None, problemID=None):
    try:
        if egeNumber:
            problemID, path, problemKeyboard, tags = problemBuilding.getEgeProblem(
                dbUtils.getEgeProblem(msg, egeNumber=egeNumber))
            dbUtils.addUserProblemHistory(msg.chat.id, problemID)
            sendPhotoToUser(msg, path, problemKeyboard, tags)
        elif problemID:
            _, path, problemKeyboard, tags = problemBuilding.getEgeProblem(
                dbUtils.getEgeProblem(msg, problemID=problemID))
            sendPhotoToUser(msg, path, problemKeyboard, tags)
        else:
            path, problemKeyboard, tags = problemBuilding.getDviProblem(year)
            sendFileToUser(msg, path, problemKeyboard, tags)

        log.info('FROM: ' + path)

    except(Exception):
        whatTheFuckMan(msg)


def sendLarinVariant(msg, variantNumber):
    try:
        with open(bankPath + larinPathPattern.replace('*', str(variantNumber)), 'rb') as larinFile:
            bot.send_document(msg.chat.id, data=larinFile)
    except(Exception):
        bot.send_message(msg.chat.id, text="У меня возникли трудности с поиском этого варианта. А он точно есть?")


def sendRealToUser(msg, year):
    try:
        with open(bankPath + realTaskPattern.format(year), 'rb') as doc:
            bot.send_document(msg.chat.id, data=doc)
    except(Exception):
        whatTheFuckMan(msg)


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    logFromMsg(message)
    dbUtils.addUser(message)
    bot.send_message(message.chat.id,
                     parse_mode="HTML",
                     text="<b>NLog(N) Turing BOT</b>", reply_markup=main)
    bot.send_message(message.chat.id, parse_mode="HTML", text="<i>v1.3.5 (beta)</i>")
    bot.send_message(message.chat.id, parse_mode="HTML", text=helloMessage)

    bot.send_message(message.chat.id,
                     text="Timur Guev @timyrik20\n"
                          "George Gabolaev @gabolaev\n"
                          "Nelli Khlustova @nelli_snow", reply_markup=mainlinks)

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


@bot.message_handler(regexp=books)
def getBook(msg):
    logFromMsg(msg)
    try:
        with open(bankPath + booksPath.format(msg.text), 'rb') as book:
            bot.send_document(msg.chat.id, data=book)
    except(Exception):
        whatTheFuckMan(msg)


@bot.message_handler(regexp=bookAlias)
def getBooksKeyboard(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text='Какую книжку хочешь?', reply_markup=booksKb)


@bot.message_handler(regexp=thanks)
def parseLarinVariant(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id,
                     text='Если я не ошибся, ты хвалишь меня) Спасибо, {}! С тобой очень приятно работать.'.format(
                         msg.chat.username))


@bot.message_handler(regexp=real)
def realVariants(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text='Выбери год ЕГЭ.', reply_markup=reals)


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
        bot.send_document(msg.chat.id, data=doc, caption='Документация моих возможностей.')


@bot.message_handler(regexp=ege)
def wantEgeProblem(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text="Как именно будем ботать ЕГЭ?", reply_markup=menuEge)


@bot.message_handler(regexp=random)
def wantProblem(msg):
    logFromMsg(msg)
    egeNumber = dbUtils.getRandomEgeNumber()
    constructProblemBeforeSending(msg, egeNumber=egeNumber)


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


@bot.message_handler(regexp=tellMe)
def whoami(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text="Наверно, ты хочешь узнать про меня. Так вот...")
    bot.send_message(msg.chat.id, text=helloMessage)
    bot.send_message(msg.chat.id, text="А ещё в моей документации написано вот это.")
    bot.send_message(msg.chat.id, text=description)


@bot.message_handler(regexp=variant)
def randomVariant(msg):
    logFromMsg(msg)
    for i in range(13, 20):
        constructProblemBeforeSending(msg, egeNumber=i)


@bot.message_handler(regexp=var)
def parseLarinVariant(msg):
    logFromMsg(msg)
    sendLarinVariant(msg, msg.text[4::])

@bot.message_handler(regexp="О нас")
def about(msg):
    logFromMsg(msg)
    bot.send_message(msg.chat.id, text="Скоро.")


@bot.message_handler(regexp=larin)
def larin(msg):
    logFromMsg(msg)
    keyboard = problemBuilding.getLarinVariantsKeyboard()
    bot.send_message(msg.chat.id, text='Выбери вариант.', reply_markup=keyboard)


@bot.message_handler(regexp='get')
def getParse(msg):
    logFromMsg(msg)
    try:
        constructProblemBeforeSending(msg, problemID=int(msg.text[4::]))
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


@bot.message_handler(regexp='даня')
def noRacism(msg):
    logFromMsg(msg)
    with open(no_racism, 'rb') as racism:
        bot.send_photo(msg.chat.id, photo=racism, caption='Be tolerant.')


@bot.message_handler(content_types=["text"])
def parseText(msg):
    logFromMsg(msg)
    try:
        intValue = int(msg.text)
        if minEgeProblemNumber <= intValue <= maxEgeProblemNumber:  # Пришел номер ЕГЭ
            constructProblemBeforeSending(msg, egeNumber=intValue)
        elif minDVIYear <= intValue <= maxDVIYear:  # Пришел год ДВИ
            constructProblemBeforeSending(msg, year=intValue)
        else:
            whatTheFuckMan(msg)
    except Exception:
        try:
            sendRealToUser(msg, year=msg.text[0:4])  # Пришёл год реального варианта
        except Exception as ex:
            whatTheFuckMan(msg)
            log.error(ex)


if __name__ == '__main__':
    try:
        log.info(botEnabling)
        bot.polling(none_stop=True)
        log.info(botDisabling)
    except Exception as ex:
        log.error(ex)

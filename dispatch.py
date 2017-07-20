import bot
import dbUtils

listOfUsers = dbUtils.getListOfUsers()


def sendToAll(text):
    for i in listOfUsers:
        try:
            bot.bot.send_message(i[2], text=text, reply_markup=bot.main)
            bot.logging(text='РАССЫЛКА:'+text)
        except bot.telebot.apihelper.ApiException as ex:
            bot.logging(text=ex)


while(1):
    sendToAll(input())

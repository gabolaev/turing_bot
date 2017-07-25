import bot
import dbUtils

listOfUsers = dbUtils.getListOfUsers()


def sendToAll(text):
    # for i in listOfUsers:
    #     try:
            bot.bot.send_message(83210918, text=text)
            # bot.logging(text='РАССЫЛКА:'+text)
        # except bot.telebot.apihelper.ApiException as ex:
        #     bot.logging(text=ex)
#

while(1):
    sendToAll(input())
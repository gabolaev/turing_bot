import bot
import dbUtils

listOfUsers = dbUtils.getListOfUsers()


def sendToAll(text):
    for i in listOfUsers:
        try:
            bot.bot.send_message(i[2], text=text)
            bot.log.info("{} ({}) : Доставлено".format(i[1],i[2]))
        except bot.telebot.apihelper.ApiException as ex:
            bot.log.error("{} ({}) : {}".format(i[1],i[2],ex))


sendToAll("""""")
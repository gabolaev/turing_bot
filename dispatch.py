import bot
import dbUtils
import time

listOfUsers = dbUtils.getListOfUsers()
def sendToAll(text):
    for i in listOfUsers:
        try:
            bot.bot.send_message(i[2], "Кстати про разбор...")
            time.sleep(1)
            bot.bot.send_message(i[2], """Над решениями работали:\nГуев Тимур\nГуссаова Рената\nГутнова Дзерасса\nПлиева Мадина\nТасоева Эсма\nЧшиев Аслан""")
            time.sleep(1)
            bot.bot.send_message(i[2], "АНТИХАЙП")
            bot.log.info("{} ({}) : Доставлено".format(i[1],i[2]))
            time.sleep(2)
        except bot.telebot.apihelper.ApiException as ex:
            bot.log.error("{} ({}) : {}".format(i[1], i[2], ex))

sendToAll("""Мы тут добавили разбор 202 варианта с сайта alexlarin.net. Он прям свежий.""")

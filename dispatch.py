import bot
import dbUtils
import time

listOfUsers = dbUtils.getListOfUsers()

def sendToAll(text):
    for i in listOfUsers:
        try:
            with open("/root/bot/botLocalFiles/missme.mp4", 'rb') as video:
                bot.bot.send_document(i[2], data=video, caption=text)
            bot.log.info("{} ({}) : Доставлено".format(i[1],i[2]))
            video.close()
            time.sleep(2)
        except bot.telebot.apihelper.ApiException as ex:
            bot.log.error("{} ({}) : {}".format(i[1], i[2], ex))

sendToAll("""Обновление 1.3.5 (beta)
    ✅ Небольшие изменения в структуре раздела ДВИ.""")

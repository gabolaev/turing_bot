import bot
import dbUtils
import time

listOfUsers = dbUtils.getListOfUsers()

def sendToAll(text):
    for i in listOfUsers:
        try:
            # with open("/root/bot/botLocalFiles/missme.mp4", 'rb') as video:
            bot.bot.send_message(i[2], text=text)
            bot.log.info("{} ({}) : Доставлено".format(i[1],i[2]))
            # video.close()j
            time.sleep(2)
        except bot.telebot.apihelper.ApiException as ex:
            bot.log.error("{} ({}) : {}".format(i[1], i[2], ex))

sendToAll("""Minor update 1.3.6 (beta)
    ✅ Обновлено содержимое раздела "О нас"
    ✅ Добавлена актуальная версия документации""")

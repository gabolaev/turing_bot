import bot
import dbUtils
import config
import time

listOfUsers = dbUtils.getListOfUsers()
listOfUsers = listOfUsers[8:]
def sendToAll(text):
    for i in listOfUsers:
        try:
            bot.sendLarinVariant(i[2], "201", text)
            bot.log.info("{} ({}) : Доставлено".format(i[1],i[2]))
            time.sleep(2)
        except bot.telebot.apihelper.ApiException as ex:
            bot.log.error("{} ({}) : {}".format(i[1], i[2], ex))

sendToAll("""Обновление 1.3.7 (beta)
✅ Мы начали добавлять разборы к решениям вариантов с сайта alexlarin.net.
Для получения нажмите на кнопку "Разбор" под сообщением.
Остальные в разделе:
🎓Буду ботать🎓/ЕГЭ/Ларин""")

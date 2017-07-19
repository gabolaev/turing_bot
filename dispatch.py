import bot
import dbUtils

listOfUsers = dbUtils.getListOfUsers()


# def sendToAll(text):
    # bot.bot.send_message(43903450, text=text)
    # for i in listOfUsers:
    #     try:
    #         bot.bot.send_message(i[2], text=text)
    #         bot.logging(text='РАССЫЛКА:'+text)
    #     except bot.telebot.apihelper.ApiException as ex:
    #         bot.logging(text=ex)
#
#
# sendToAll("""Обновление v1.3.1 (beta)
#
# ✅ Добавлена красивая :) инструкция. Для получения следует нажать кнопку "Как оно работает?" """)

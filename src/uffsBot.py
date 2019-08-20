import os
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import telegram
import RuBot, BusBot, CalendarBot, CanteenBot
from conf.settings import telegramToken

ruBot = RuBot.RuBot()
canteenBot = CanteenBot.CanteenBot()
busBot = BusBot.BusBot()
calendarBot = CalendarBot.CalendarBot()

def showStartMenu(bot, update):
    bot.send_message(
        chat_id = update.message.chat_id,
        text = 'Olá!\nSelecione uma opção para continuar...',
        reply_markup = getMainMenuMarkup()
    )

def showStartMenuInExistingMsg(bot, update):
    bot.editMessageText(
        message_id = update.callback_query.message.message_id,
        chat_id = update.callback_query.message.chat.id,
        text = 'Olá!\nSelecione uma opção para continuar...',
        reply_markup = getMainMenuMarkup()
    )

def getMainMenuMarkup():
    keyboard = [
        [
            telegram.InlineKeyboardButton('Cardápio RU', callback_data = 'menu-ru'),
            telegram.InlineKeyboardButton('Cardápio Cantina', callback_data = 'menu-canteen')
        ],
        [
            telegram.InlineKeyboardButton('Horário ônibus', callback_data = 'bus-schedules'),
            telegram.InlineKeyboardButton('Calendário acadêmico', callback_data = 'academic-calendar')
        ]
    ]
    return telegram.InlineKeyboardMarkup(keyboard)

def callHandler(bot, update):
    if update.callback_query.data == 'menu-ru':
        ruBot.selectCampus(bot, update)
    elif update.callback_query.data[:2] == 'RU':
        ruBot.showCardapio(bot, update, update.callback_query.data[3:])
    elif update.callback_query.data == 'menu-canteen':
        canteenBot.selectCampus(bot, update)
    elif update.callback_query.data[:7] == 'canteen':
        canteenBot.showCardapio(bot, update)
    elif update.callback_query.data == 'bus-schedules':
        busBot.selectCampus(bot, update)
    elif update.callback_query.data[:3] == 'bus':
        busBot.selectStartPoint(bot, update, update.callback_query.data[4:])
    elif update.callback_query.data[:13] == 'startPointBus':
        busBot.showSchedule(bot, update, update.callback_query.data[14:])
    elif update.callback_query.data == 'academic-calendar':
        calendarBot.getCalendar(bot, update)
    elif update.callback_query.data == 'main-menu':
        showStartMenuInExistingMsg(bot, update)

def main():
    updater = Updater(telegramToken)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', showStartMenu))
    dp.add_handler(CommandHandler('cal_academico', calendarBot.getCalendar))
    dp.add_handler(CallbackQueryHandler(callHandler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

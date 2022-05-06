from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from db_data import db_session
from db_data.__all_models import User
import requests


TOKEN = '5375409769:AAEVGJVIRF80jcYYr2DkWojMoGdR9wp8qCU'
REQUEST_KWARGS = {'proxy_url': 'socks5://ip:port'}

reply_keyboard = [['/site']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

group = 1


def start(update, context):
    update.message.reply_text('''Добро пожаловать в Голосовалку Школы №1357!)
Для получения уведомления о появлении новой голосовалки необходимо авторизоваться.
На первой строке введите почту, которую вы указывали при регистрации на сайте, на второй - пароль.''',
                              reply_markup=markup)


def site(update, context):
    update.message.reply_text('Ссылочка')


def authorization(update, context):
    if '\n' in update.message.text:
        if len(update.message.text.split('\n')) == 2:
            print(update.message.text.split('\n'))
            db_session.global_init('db/golosovalka.sqlite')
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == update.message.text.split('\n')[0]).first()
            if user and user.check_password(update.message.text.split('\n')[1]):
                update.message.reply_text('''
Вы успешно авторизованы. Теперь вы сможете получать уведомления о новых голосованиях!''')
            else:
                if not user:
                    update.message.reply_text('''Пользователь с такой почтой не найден. 
Возможно вы не зарегистрированы на нашем сервере или допустили ошибку при введении почты.''')
                elif not user.check_password(update.message.text.split('\n')[1]):
                    update.message.reply_text('''Неверный пароль.''')
        else:
            update.message.reply_text(
                'На первой строке введите почту, которую вы указывали при регистрации на сайте, на второй - пароль.')
    else:
        update.message.reply_text(
            'На первой строке введите почту, которую вы указывали при регистрации на сайте, на второй - пароль.')


# def newvote(context):
#     request = request_new_votes()
#     for i in request:
#
#     job = context.job
#     context.bot.send_message(job.context, text='Ура! Появилась новая голосовалка!')
#
#
# def set_timer(update, context):
#     chat_id = update.message.chat_id
#     try:
#         due = int(context.args[300])
#         context.job_queue.run_once(newvote, due, context=chat_id, name=str(chat_id))
#
#     except (IndexError, ValueError):
#         update.message.reply_text('Использование: /set <секунд>')


def request_new_votes():
    request = 'http://192.168.2.20:8000/api/newvotes'
    response = requests.get(request)
    request_json = response.json()
    return request_json


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("site", site))
    text_handler = MessageHandler(Filters.text, authorization)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

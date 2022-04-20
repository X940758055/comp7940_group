from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os
import logging

import uuid
import functions as func
import firebaseOperation as dbop
import cos as coscli



def main():

    # connection
    Region = (os.environ['COS_REGION'])
    bucket = (os.environ['COS_BUCKET'])
    secret_id = (os.environ['COS_SECRETID'])
    secret_key = (os.environ['COS_SECRETKEY'])
    global cos
    cos = coscli.tencent_cos(Region, bucket, secret_id, secret_key)
    updater = Updater(token=(os.environ['TELEGRAM_ACCESS_TOKEN']), use_context=True)
    global bot
    bot = Bot(os.environ['TELEGRAM_ACCESS_TOKEN'])
    global db
    db = dbop.init(os.environ['FIREBASE_SDK'])
    # db = dbop.init(host=(config['MYSQL']['HOST']),user=(config['MYSQL']['USER']), password=(config['MYSQL']['PASSWORD']), port=(config['MYSQL']['PORT']), database=(config['MYSQL']['DATABASE']))
    global uploadfile
    uploadfile = {}



    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("tv", tvHandler))
    dispatcher.add_handler(CommandHandler("hiking", hikingHandler))
    dispatcher.add_handler(CommandHandler("cookary", cookaryHandler))

    dispatcher.add_handler(MessageHandler(Filters.photo, photoHandler))
    dispatcher.add_handler(MessageHandler(Filters.video, videoHandler))


    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

def tvHandler(update: Update, context: CallbackContext) -> None:
    try:
        operation = context.args[0]
        tv_name = context.args[1]
        user_name = update.effective_user.full_name
        global db
        if operation == "write_review":
            comment = " ".join(context.args[2:])
            func.write_tv_review(db, tv_name, user_name , comment)
            update.message.reply_text('record success!')
        elif operation == "show_review":
            res = func.show_tv_review(db, tv_name)
            if len(res) == 0:
                update.message.reply_text("Sorry, no record about this.")
            else:
                for review in res:
                    update.message.reply_text('Written time:{}\nWriter:{}\nDescription:{}'.format(review["comment_time"], review["comment_name"], review["comment_description"]))
        else:
            pass
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /tv <operation> {tv_name} {option}')


def hikingHandler(update: Update, context: CallbackContext) -> None:
    try:
        operation = context.args[0]
        place = context.args[1]
        user_name = update.effective_user.full_name
        if operation == "write_routine":
            comment = " ".join(context.args[2:])
            func.write_hiking_routine(db, place, user_name, comment)
            update.message.reply_text('record success!')

        elif operation == "upload_photo":
            global uploadfile
            key = func.generate_upload_key("graph", user_name)
            uploadfile[key] = place
            update.message.reply_text('please upload photo')

        elif operation == "show_routine":
            res = func.show_hiking_routine(db, place)
            if len(res) == 0:
                update.message.reply_text("Sorry, no record about this.")
            else:
                for review in res:
                    update.message.reply_text(
                        'Commit time:{}\nSupporter:{}\nRoutine:{}'.format(review["comment_time"], review["comment_name"],
                                                               review["comment_description"]))

        elif operation == "show_photo":
            picts = func.show_hiking_photo(db, cos, place)
            sendGraphs(update, picts)
        else:
            pass

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hiking <operation> {place} {option}')





def cookaryHandler(update: Update, context: CallbackContext) -> None:
    try:
        operation = context.args[0]
        name = context.args[1]
        user_name = update.effective_user.full_name
        if operation == "upload_video":
            global uploadfile
            key = func.generate_upload_key("video", user_name)
            uploadfile[key] = name
            update.message.reply_text('please upload video')

        elif operation == "show_video":
            videos = func.show_cookary(db, cos, name)
            sendVideo(update, videos)
        else:
            pass

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hiking <operation> {place} {option}')



def sendGraphs(update, picts):
    try:
        global bot
        chat_id = update.effective_chat.id
        if len(picts) == 0:
            update.message.reply_text('Sorry, no record about this.')
        for pict in picts:
            # bot.send_photo(chat_id, photo=open(pict, 'rb'))
            bot.send_photo(chat_id, pict)
    except (IndexError, ValueError):
        update.message.reply_text('Internal server error')


def photoHandler(update: Update, context: CallbackContext):
    try:
        global uploadfile
        global bot
        global cos
        user_name = update.effective_user.full_name
        key = func.generate_upload_key("graph", user_name)
        if uploadfile.get(key, None) is not None:
            place = str(uploadfile[key])
            file = bot.getFile(update.message.photo.pop())
            # path = func.download_photo(file.file_path, str(uuid.uuid4()))
            path = func.save_file_on_cos(file.file_path, cos, str(uuid.uuid4()))
            func.write_hiking_photo(db, place, path, user_name)
            update.message.reply_text('saved')
            del uploadfile[key]
        else:
            update.message.reply_text('no title')
    except:
        update.message.reply_text('no title')


def videoHandler(update: Update, context: CallbackContext):

        global uploadfile
        global bot
        global cos
        user_name = update.effective_user.full_name
        key = func.generate_upload_key("video", user_name)
        if uploadfile.get(key, None) is not None:
            name = str(uploadfile[key])
            file = bot.getFile(update.message.video.file_id)
            # path = func.download_video(file.file_path, str(uuid.uuid4()))
            path = func.save_file_on_cos(file.file_path, cos, str(uuid.uuid4()))
            func.write_cookary(db, name, path, user_name)
            update.message.reply_text('saved')
            del uploadfile[key]
        else:
            update.message.reply_text('no title')


def sendVideo(update, videos):
    try:
        global bot
        chat_id = update.effective_chat.id
        if len(videos) == 0:
            update.message.reply_text('Sorry, no record about this.')
        for video in videos:
            # bot.send_video(chat_id, video=open(video, 'rb'))
            bot.send_video(chat_id, video)
    except (IndexError, ValueError):
        update.message.reply_text('Internal server error')

if __name__ == '__main__':
    main()

import os

import telegram
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.update import Update


class Init:
    def __init__(self, TOKEN):
        self.updater = Updater(TOKEN, use_context=True)
        self.bot = telegram.Bot(TOKEN)
        self.startCommand = CommandHandler('start', self.start)
        self.receivedPhoto = MessageHandler(Filters.photo, self.receivePhoto)
        self.receivedMessage = MessageHandler(Filters.text, self.receiveMessage)
        self.sendDocument = MessageHandler(Filters.document, self.senddocument)
        self.sendAudio = MessageHandler(Filters.voice, self.sendaudio)
        self.message = ""
        self.messageId = 0
        self.chat_id = 0
        self.groupId = os.environ.get("GROUPID")

    def start(self, update: Update, context: CallbackContext):
        self.bot.send_message(chat_id=update.message.chat_id,
                              text="مرحباً\nهذا البوت خاص بمادة البرمجة ٢ للسنة الثانية\nقم بارسال ما تريد من الاسئلة وسنقوم بالإجابة عنهم بأقرب وقت❤️\n#RBCsCAE \n#RBCsTeam\n#WeCarryYourO2")
        self.bot.send_message(chat_id=update.message.chat_id,
                              text="يرجى الانتباه ان يكون حسابك قابل لوصول الرسائل عليه\nو ذلك من خلال الذهاب الى الاعدادات و بعدها الى الخصوصية و النقر على الرسائل المحولة و تفعيل الخيار التالي:\n ملاحظة : اذا ارسلت رسالة قبل تعديل خصوصية حسابك لن نستطيع الرد عليك😌")
        self.bot.send_photo(chat_id=update.message.chat_id,
                            photo=open('IMG_20230207_211643.jpg', 'rb'))

    def receivePhoto(self, update: Update, context: CallbackContext):
        self.bot.send_message(chat_id=update.message.chat_id,
                              text="نعتذر منك لا تقبل الصور او الملفات \nرجاء ارسل سؤالك على شكل رسالة نصية من فضلك")

    def receiveMessage(self, update: Update, context: CallbackContext):
        try:
            self.message = update.message.text
            self.messageId = update.message.message_id
            self.chat_id = update.message.chat_id
            if update.message.chat.id != self.groupId:
                self.bot.forward_message(chat_id=self.groupId, from_chat_id=self.chat_id, message_id=self.messageId)
            else:
                self.bot.send_message(chat_id=update.message.reply_to_message['forward_from']['id'], text=self.message)
        except:
            self.bot.send_message(chat_id=self.groupId, text="لم تصله الرسالة")
            pass

    def senddocument(self, update: Update, context: CallbackContext):
        try:
            if update.message.chat_id == self.groupId:
                context.bot.get_file(update.message.document).download('temp.pdf')
                self.bot.send_document(chat_id=update.message.reply_to_message['forward_from']['id'],
                                       document=open("/home/obadakatma/RBCsbot/temp.pdf", 'rb'))
            else:
                self.bot.send_message(chat_id=update.message.chat_id, text="لا تستطيع ارسال الملفات")
        except:
            self.bot.send_message(chat_id=self.groupId, text="لم تصله الرسالة")
            pass

    def sendaudio(self, update: Update, context: CallbackContext):
        try:
            if update.message.chat_id == self.groupId:
                self.bot.get_file(update.message.voice.file_id).download('temp.mp3')
                self.bot.send_document(chat_id=update.message.reply_to_message['forward_from']['id'],
                                       document=open("/home/obadakatma/RBCsbot/temp.mp3", 'rb'))
            else:
                self.bot.send_message(chat_id=update.message.chat_id, text="لا تستطيع ارسال الاصوات")
        except:
            self.bot.send_message(chat_id=self.groupId, text="لم تصله الرسالة")
            pass

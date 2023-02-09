import os

from Init import Init

TOKEN = os.environ.get("TOKEN")
init = Init(TOKEN)

dp = init.updater.dispatcher
dp.add_handler(init.startCommand)
dp.add_handler(init.receivedPhoto)
dp.add_handler(init.receivedMessage)
dp.add_handler(init.sendDocument)
dp.add_handler(init.sendAudio)

init.updater.start_polling()

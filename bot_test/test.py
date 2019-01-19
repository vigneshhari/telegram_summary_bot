import os
import telepot
from pprint import pprint
bot = telepot.Bot(os.environ.get('BOT_TOKEN'))
print(bot.getUpdates())
pprint(bot.sendMessage('157202554', 'Hello My Nemesis'))


# https://api.telegram.org/bot783274283:AAFVieWerOW3qQZAQidxYhwQEe3oVFm9jPo/setWebhook?url={WEBHOOK_URL}

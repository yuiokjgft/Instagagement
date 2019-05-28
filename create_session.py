from telethon import TelegramClient, events, sync

telegram_api_id = input('Telegram API id: ')
telegram_api_hash = input('Telegram API hash: ')
session = input('Session name: ')
client = TelegramClient(session, int(telegram_api_id), str(telegram_api_hash))
client.start()
client.disconnect()
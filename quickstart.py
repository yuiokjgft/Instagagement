import json, random
from telethon import TelegramClient, events, sync

# Per day
max_likes_default = 750
max_follows_default = 500
max_unfollows_default = 500
delay_default = 5

# Config
session = ''
time_from = 0
time_to = 0
ig_username = ''
ig_password = ''
cookie_name = ''
telegram_api_id = 0
telegram_api_hash = 0
like_profile = ''
use_groups = ''
max_likes = 0
delay = 0
like_feed = 0

# Def. group range
username_req = [1, 12]
username_not_req = [13, 40]

# Get Telegram group list
with open('group_template.json') as load_groups:  
	group_list = json.load(load_groups)

print('When do you wish to use this script (e.g. from 8 to 16)? Machine time is used')
time_from = input('From: ')
time_to = input('To: ')
print()

print('Set up Instagram')
ig_username = input('Username: ')
ig_password = input('Password: ')
print()

# Telegram credentials
print('Set up Telegram')
telegram_api_id = input('Telegram API id: ')
telegram_api_hash = input('Telegram API hash: ')
session = 'telegram_'+ig_username+'_'+str(telegram_api_id)+'_'+str(random.randint(1,99))
client = TelegramClient(session, int(telegram_api_id), str(telegram_api_hash))
client.start()
print()

# Engagement profile
print('On which instagram profile you want to get likes on?')
print('[0] This profile (' + ig_username + ')')
print('[1] Different profile')
choice = input('Choose: ')
print()
if int(choice) != 0:
	print('(You wont be able to use groups that dont require username (e.g. Wolf global) - check documentation)')
	like_profile = input('Enter profile username: ')
	print()
	print('Select what engagement groups you want to use (some groups have follower restrictions - check documentation):')
	for i in range(username_req[0], username_req[1]+1):
		print('[' + str(i) + '] ' + group_list['available_groups'][str(i)])
	use_groups = input('Select groups (separate with comma): ')
	print()
else:
	print()
	like_profile = ig_username
	print('Select what engagement groups you want to use (some groups have follower restrictions - check documentation)')
	print()
	print('These groups require username:')
	for i in range(username_req[0], username_req[1]+1):
		print('[' + str(i) + '] ' + group_list['available_groups'][str(i)])
	print()
	print('These groups do not require username:')
	for i in range(username_not_req[0], username_not_req[1]+1):
		print('[' + str(i) + '] ' + group_list['available_groups'][str(i)])
	use_groups = input('Select groups (separate with comma): ')
	print()

max_likes = input('Set like limit per day (default ' + str(max_likes_default) + '): ')
if len(max_likes) == 0:
	max_likes = max_likes_default
print()

delay = input('Set like delay (default ' + str(delay_default) + '): ')
if len(delay) == 0:
	delay = delay_default
print()

print('Like recent feed (10-12 latest posts)?')
print('[0] Disable')
print('[1] Enable')
like_feed = input('Choose: ')
if len(like_feed) == 0:
	like_feed = 0
print()

print('Send errors/updates to your telegram (telegram username required)?')
print('[0] Disable')
print('[1] Enable')
telegram_username = int(input('Choose: '))
print()

if int(telegram_username) == 1:
	telegram_username = input('Telegram username: ')
	print()

config = {
	"session" : str(session),
	"time_from" : int(time_from),
	"time_to" : int(time_to),
	"ig_username" : str(ig_username),
	"ig_password" : str(ig_password),
	"cookie_name" : str(ig_username),
	"telegram_api_id" : int(telegram_api_id),
	"telegram_api_hash" : str(telegram_api_hash),
	"like_profile" : str(like_profile),
	"use_groups" : str(use_groups),
	"max_likes" : int(max_likes),
	"delay" : int(delay),
	"like_feed" : int(like_feed),
	"telegram_username" : telegram_username
}

print()
print("Saving config: " + json.dumps(config, indent=4, separators=(',', ': '), sort_keys=True))

with open(ig_username+'_config.json', 'w+') as config_file:
	json.dump(config, config_file, indent=4, separators=(',', ': '), sort_keys=True)

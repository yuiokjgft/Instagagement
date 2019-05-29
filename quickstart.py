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

print('When do you wish to use this script (e.g. from 8 to 16)? Machine time is used')
time_from = input('From: ')
time_to = input('To: ')
print()

print('Set up Instagram')
ig_username = input('Username: ')
ig_password = input('Password: ')
print()

if int(telegram_groups) == 1:
	# Telegram credentials
	print('Set up Telegram')
	telegram_api_id = input('Telegram API id: ')
	telegram_api_hash = input('Telegram API hash: ')
	session = 'telegram_'+ig_username+'_'+str(telegram_api_id)+'_'+str(random.randint(1,99))
	client = TelegramClient(session, int(telegram_api_id), str(telegram_api_hash))
	client.start()
	#print('Closing connection, please wait')
	#time.sleep(5)
	#client.disconnect()
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
		print('[1] Push 24h')
		print('[2] GainSpace | MASS Likes Dx5')
		print('[3] BoostGram Dx10')
		print('[4] BoostGram Dx20')
		print('[5] BoostGram Dx30')
		print('[6] InstaPro Dx20')
		print('[7] Wizard Dx30')
		print('[8] Like Dx30')
		use_groups = input('Select groups (separate with comma): ')
		print()
	else:
		print()
		like_profile = ig_username
		print('Select what engagement groups you want to use (some groups have follower restrictions - check documentation)')
		print()
		print('These groups require username:')
		print('[1] Push 24h')
		print('[2] GainSpace | MASS Likes Dx5')
		print('[3] BoostGram Dx10')
		print('[4] BoostGram Dx20')
		print('[5] BoostGram Dx30')
		print('[6] InstaPro Dx20')
		print('[7] Wizard Dx30')
		print('[8] Like Dx30')
		print()
		print('These groups do not require username:')
		print('[9] Wolf Onyx 24h')
		print('[10] Wolf Saphire 24h')
		print('[11] Wolf Emerald 24h')
		print('[12] Wolf Ruby 24h')
		print('[13] Wolf Amber 24h')
		print('[14] Wolf Quartz 24h')
		print('[15] Wolf 5K 24h')
		print('[16] Wolf 10K 24h')
		print('[17] Wolf 15K 24h')
		print('[18] Wolf | 5K Powerlikes Dx10')
		print('[19] Wolf | 1K Powerlikes Dx10')
		print('[20] Wolf | 3K Turbo Likes Dx50')
		print('[21] 50 Likes Pod')
		print('[22] Nest DX20')
		print('[23] Dx30 Engagement Group')
		print('[24] Den DX20')
		print('[25] Den DX50')
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
	"delay" : int(delay)
}

print()
print("Saving config: " + json.dumps(config, indent=4, separators=(',', ': '), sort_keys=True))

with open(ig_username+'_config.json', 'w+') as config_file:
	json.dump(config, config_file, indent=4, separators=(',', ': '), sort_keys=True)

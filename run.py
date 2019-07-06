import os, time, json, random
import instagagement
from datetime import datetime
from datetime import timedelta
from telethon import errors
import requests

# Settings
group_waittime = 20 	# Seconds between groups
loop_sleep = 30			# Minutes between loops (all groups)

# Placeholders
use_groups = []
group_list = []
config = []
like_end = datetime.now() - timedelta(minutes = loop_sleep)

print()
print()
print("|          |                                            |    ")
print("|,---.,---.|--- ,---.,---.,---.,---.,---.,-.-.,---.,---.|--- ")
print("||   |`---.|    ,---||   |,---||   ||---'| | ||---'|   ||    ")
print("``   '`---'`---'`---^`---|`---^`---|`---'` ' '`---'`   '`---'")
print("                     `---'     `---'                         ")
print()

# Get the name of preset
preset = input('Enter preset name or instagram username: ')
print()

def update_config():
	global config
	# Update config
	with open(preset + '_config.json') as config_file:
		config = json.load(config_file)

# Process config
update_config()

# Initialize and login
instagagement.init(preset)
user_info = instagagement.login()
print('Logged in as ' + config['ig_username'])
print('Followers: ' + str(user_info[0]))
print('Following: ' + str(user_info[1]))
print('Media count: ' + str(user_info[2]))
print('Getting likes for: ' + config['like_profile'])
print()

# Get Telegram group list
with open(str(config['telegram_api_id']) + '_groups.json') as load_groups:  
	group_list = json.load(load_groups)

# Run the progarm
while 1:
	if datetime.now().hour >= config['time_from'] and datetime.now().hour < config['time_to']:
		update_config()
		# Check if time between loops is big enough
		if (datetime.now() - like_end) / timedelta(minutes = 1) >= loop_sleep:
			# Engagement pods
			try:
				if config['use_groups'] != 0:
					instagagement.start_client()
					use_groups = config['use_groups'].split (",")
					for i in range(0, len(use_groups)):
						status = instagagement.start_groups(group_list['available_groups'][use_groups[i]])
						if status != -1:
							print('Waiting for ' + str(group_waittime) + ' seconds between groups')
							print()
							time.sleep(group_waittime)
						else:
							print()
							time.sleep(2)
					instagagement.disconnect_client()
					like_end = datetime.now()
			except ConnectionError:
				print('ConnectionError - check your internet connection')
			except requests.ConnectionError:
				print('requests ConnectionError - check your internet connection')

			# Like feed
			if config['like_feed'] == 1:
				instagagement.like_feed()
				like_end = datetime.now()
				print()

			print('Like loop ended at ' + str(datetime.now().strftime("%H:%M")) + ', continuing after ' + str(loop_sleep) + ' minutes')
			print()
		time.sleep(60)
	else:
		# Refresh values after every day
		update_config()
		time.sleep(random.randint(5*60,10*60))

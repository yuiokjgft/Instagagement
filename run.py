import os, time, json, random
import instagagement
from datetime import datetime

# Settings
sleep_time_loop = 30 * 60 	# x minutes between loops

# Placeholders
use_groups = []
group_list = []
config = []

# Get the name of preset
preset = input('Enter preset name (instagram username): ')

# Initialize and login
instagagement.init(preset)
instagagement.login()

def update_config():
	global config
	# Update config
	with open(preset + '_config.json') as config_file:
		config = json.load(config_file)

# Process config
# Get groups which will be used
update_config()
use_groups = config['use_groups'].split (",")

# Get Telegram group list
with open(str(config['telegram_api_id']) + '_groups.json') as load_groups:  
	group_list = json.load(load_groups)

# Run the progarm
while 1:
	update_config()
	if datetime.now().hour >= config['time_from'] and datetime.now().hour < config['time_to']:
		# Telegram engagement groups
		if config['telegram_groups'] == 1:
			instagagement.start_client()
			for i in range(0, len(use_groups)):
				try:
					instagagement.start_groups(group_list['available_groups'][use_groups[i]])
					time.sleep(60)
				except:
					print('Something went wrong')
			instagagement.disconnect_client()

		# Following competitor likers then unfollowing as FIFO after 24h
		if config['follow'] == 1:
			instagagement.start_follow()

		# Sleep x minutes
		time.sleep(sleep_time_loop)
	else:
		# Refresh values after every day
		update_config()
		time.sleep(random.randint(5*60,10*60))
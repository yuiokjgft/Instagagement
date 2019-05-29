import os, time, json, random
import instagagement
from datetime import datetime
from datetime import timedelta

# Settings
sleep_time_loop_like = 20		# x minutes between like loops
sleep_time_loop_follow = 60 	# x minutes between follow loops

# Placeholders
use_groups = []
group_list = []
config = []
like_end = datetime.now() - timedelta(minutes = sleep_time_loop_like)

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
	if datetime.now().hour >= config['time_from'] and datetime.now().hour < config['time_to']:
		update_config()
		# Check if time between loops is big enough
		if (datetime.now() - like_end) / timedelta(minutes = 1) >= sleep_time_loop_like:
			instagagement.start_client()
			for i in range(0, len(use_groups)):
				try:
					instagagement.start_groups(group_list['available_groups'][use_groups[i]])
					time.sleep(60)
				except:
					print('Something went wrong')
			instagagement.disconnect_client()
			like_end = datetime.now()
			print('Like loop ended at ' + str(datetime.now()) + ', continuing after ' + str(sleep_time_loop_like) + ' minutes')
		time.sleep(60)
	else:
		# Refresh values after every day
		update_config()
		time.sleep(random.randint(5*60,10*60))
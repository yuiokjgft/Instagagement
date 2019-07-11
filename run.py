import os, time, json, random, traceback
import instagagement
from datetime import datetime
from datetime import timedelta
from telethon import errors
import requests
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-c", "--config", dest="config", help="Bot preset - chooses config file (usually Instagram username)")
parser.add_argument("-l", "--links", dest="links",
					help="Choose links to which you want likes/comments on e.g. -l https://www.instagram.com/p/link1/, https://www.instagram.com/p/link2/ ; 'random' for picking random links")
parser.add_argument("-t", "--target", dest="target", help="Username on which you want to receive engagement")
parser.add_argument("-d", "--debug", dest="debug", help="Disable [0] (default) or enable [1] debug messages", default=0)
parser.add_argument("-f", "--feed", dest="feed", help="Disable [0] (default) or enable [1] feed like")
args = parser.parse_args()

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
if args.config == None:
	preset = input('Enter preset name or instagram username: ')
else:
	preset = args.config
print()

def update_config():
	global config
	# Update config
	with open(preset + '_config.json') as config_file:
		config = json.load(config_file)

# Process config
update_config()

if args.feed == None:
	feed_like = int(config['like_feed'])
else:
	feed_like = int(args.feed)

if args.target == None:
	target_user = config['like_profile']
else:
	target_user = args.target

# Initialize and login
instagagement.init(preset, args)
user_info = instagagement.login()
print()
print('Followers: ' + str(user_info[0]))
print('Following: ' + str(user_info[1]))
print('Media count: ' + str(user_info[2]))
print('Getting likes for: ' + target_user)
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
			try:
				# Engagement pods
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
				# Like feed
				if feed_like == 1:
					instagagement.like_feed()
					like_end = datetime.now()
					print()
			except Exception:
				print()
				instagagement.send_error(traceback.format_exc())

			print('Like loop ended at ' + str(datetime.now().strftime("%H:%M")) + ', continuing after ' + str(loop_sleep) + ' minutes')
			print()
		time.sleep(60)
	else:
		# Refresh values after every day
		update_config()
		time.sleep(random.randint(5*60,10*60))

# General
import os, sys
import json, time, math, datetime, random
import webbrowser, requests, pip
from datetime import datetime as datenow
# Instabot.py https://github.com/instabot-py/instabot.py
from instabot_py import InstaBot
from instabot_py.user_info import get_user_info
from instabot_py.user_feed import get_media_id_user_feed
# Telethon Telegram API by LonamiWebs https://github.com/LonamiWebs/Telethon
from telethon import TelegramClient, events, sync, errors, functions, types
from telethon.tl.functions.channels import JoinChannelRequest,LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest  

# Settings
group_template = 'group_template.json'
insta_string = '/p/' 			# To find instagram link in telegram message
insta_shortcode = 'shortcode'	# To find instagram link in user feed
group_list = []
settings = []
config = []
client = []
preset = ''
debug = 0						# Enables timing and other info

# Variables
first_array_full = False
new_message = False
client_started = False
compare_array = []
first_array = []
final_array = []
liked = []
liked_all = {}
add_liked = []
data = {}
group_name = ''
selected_group = ''
id_count = 0
likes_given = 0

# Instagram
instabot = []
link1 = ''
link2 = ''
link3 = ''

def init(preset_):
	global config, group_list, liked_all, preset
	preset = preset_

	# Print time after every print message
	if debug == 1:
		old_f = sys.stdout
		class F:
			def write(self, x):
				old_f.write(x.replace("\n", " [%s]\n" % str(datenow.now())))
		sys.stdout = F()

	# Load config
	update_config()

	# Load groups
	try:
		with open(str(config['telegram_api_id']) + '_groups.json', 'r') as load_groups:  
			group_list = json.load(load_groups)
		print('Group list loaded from ' + str(config['telegram_api_id']) + '_groups.json')
	except FileNotFoundError:
		print('File ' + str(config['telegram_api_id']) + '_groups.json' + ' does not exist, making for ' + config['ig_username'])
		try:
			groups = []
			with open(group_template, 'r') as from_temp:  
				groups = json.load(from_temp)
				group_list = groups
			with open(str(config['telegram_api_id']) + '_groups.json', 'w+') as make_groups:
				json.dump(groups, make_groups, indent=4, separators=(',', ': '), sort_keys=True)
		except FileNotFoundError:
			print('File ' + group_template + ' does not exist, get it from GitHub/Ewlbo')

	# Load likes
	try:
		with open(config['ig_username'] + '_liked.json', 'r') as json_file:
			if(os.stat(config['ig_username'] + '_liked.json').st_size == 0):
				json_file.close()
				os.remove(config['ig_username'] + '_liked.json')
			else:
				liked_all = json.load(json_file)
	except FileNotFoundError:
		print(config['ig_username'] + '_liked.json' + ' not found')

def update_config():
	global preset, config
	# Load config file
	try:
		with open(preset + '_config.json') as json_file:  
			config = json.load(json_file)
		print('Config loaded from ' + preset + '_config.json')
	except FileNotFoundError:
		print('File ' + preset + '_config.json' + ' does not exist, run quickstart.py!')
		print()
		sys.exit()

def get_last_posts():
	global instabot, link1, link2, link3
	# Get the posts from specified profile in config
	instabot.current_user = config['like_profile']
	get_media_id_user_feed(instabot)
	post_list = instabot.current_user_info["edge_owner_to_timeline_media"]["edges"]
	last_posts = str(post_list)
	# Find post 1
	post_start = findnth(last_posts, insta_shortcode, 0) + len(insta_shortcode)
	last_posts = last_posts[post_start:]
	post_start = findnth(last_posts, "'", 1) + 1
	last_posts = last_posts[post_start:]
	link1 = 'https://www.instagram.com/p/' + str(last_posts[:findnth(last_posts, "'", 0)]) + '/'
	# Find post 2
	last_posts = str(post_list)
	post_start = findnth(last_posts, insta_shortcode, 1) + len(insta_shortcode)
	last_posts = last_posts[post_start:]
	post_start = findnth(last_posts, "'", 1) + 1
	last_posts = last_posts[post_start:]
	link2 = 'https://www.instagram.com/p/' + str(last_posts[:findnth(last_posts, "'", 0)]) + '/'
	# Find post 3 (if ever needed?) If more needed, change 2nd line
	last_posts = str(post_list)
	post_start = findnth(last_posts, insta_shortcode, 2) + len(insta_shortcode) # change 2 to n+1 if more posts needed to be found (max 12 posts - n(max) = 11)
	last_posts = last_posts[post_start:]
	post_start = findnth(last_posts, "'", 1) + 1
	last_posts = last_posts[post_start:]
	link3 = 'https://www.instagram.com/p/' + str(last_posts[:findnth(last_posts, "'", 0)]) + '/'

def login():
	global instabot, client

	instabot = InstaBot(
		like_per_day = config['max_likes'],
		login = config['ig_username'],
		password = config['ig_password'],
		session_file = config['cookie_name'],
		log_mod = 2
		)

	# Telegram client
	client = TelegramClient(config['session'], config['telegram_api_id'], config['telegram_api_hash'])
	client.flood_sleep_threshold = 24 * 60 * 60  # Sleep always

# Get json from URL and get Media ID
def get_media_id(media_url):
	# Instagram api returning all the information about post
	url = 'https://api.instagram.com/oembed/?callback=&url=https://www.instagram.com/p/' + media_url
	response = requests.get(url)
	# If instagram responds with OK ([200]) - media exists
	http_r = str(response)
	if http_r.find('[200]') is not -1:
		try:
			# Get JSON from Instagram post      
			response = requests.get(url).json()
		except:
			print('Media not found')
			return -1
		# Typical media_id: 1966850165576277065_8559563219; ID after '_' is UserID; before - MediaID
		find_id = response['media_id'].find('_')  
		media_id = response['media_id'][:find_id]
		user_id = response['media_id'][find_id+1:]
		return media_id
	else:
		# Media not found
		return -1

# Needle in haystack - to find instagram links in telegram messages
def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)	

# Get just the id from full instagram link https://www.instagram.com/p/BtJx2Sal2hU/ -> BtJx2Sal2hU
def get_post_id(string):
	string = str(string)
	# Url ID is 11 chars, just in case it changes, range is set [10:12]
	url_id_length_min = 10
	url_id_length_max = 12
	# Typical link - https://www.instagram.com/p/BtJx2Sal2hU/
	# Atypical link - https://www.instagram.com/username/p/BtJx2Sal2hU/
	# Both are proper links; "/p/" is checked
	locate_start = findnth(string, insta_string, 0)
	# Offset of "/p/"
	offset = len(insta_string)
	# Check all the possible endings in message of telegram output
	find_end = []
	find_end.append(string[locate_start+offset:].find(","))
	find_end.append(string[locate_start+offset:].find(" "))
	find_end.append(string[locate_start+offset:].find("/"))
	find_end.append(string[locate_start+offset:].find("'"))
	find_end.append(string[locate_start+offset:].find("\\"))
	# Find the one that occurs earliest and use it as the end of link
	try:
		locate_end = min(int(s) for s in find_end if s > url_id_length_min)
	except ValueError:
		print('Broken Instagram link; end not found; ValueError (0)')
		return 'Fail'
	# Generate only the ID from Url
	url_id = string[locate_start+offset:locate_start+locate_end+offset]

	# Find second URL
	if group_list[selected_group]['max_links'] is 2:
		locate_start = findnth(string, insta_string, 1)
		if locate_start is not -1:
			# Check all the possible endings in message of telegram output
			find_end = []
			find_end.append(string[locate_start+offset:].find(","))
			find_end.append(string[locate_start+offset:].find(" "))
			find_end.append(string[locate_start+offset:].find("/"))
			find_end.append(string[locate_start+offset:].find("'"))
			find_end.append(string[locate_start+offset:].find("\\"))
			# Find the one that occurs earliest and use it as the end of link
			try:
				locate_end = min(int(s) for s in find_end if s > url_id_length_min)
			except ValueError:
				print('Broken Instagram link; end not found; ValueError (1)')
				return 'Fail'

			# Generate only the ID from Url
			url_id_2 = string[locate_start+offset:locate_start+locate_end+offset]
			# Check if ID fits (usually 11) - check only url1 as its the main one. Some might not attach url2, that has to be checked
			if len(url_id_2) >= url_id_length_min and len(url_id_2) <= url_id_length_max and str(url_id_2).find('abcdefgh') is -1:
				return url_id, url_id_2
			elif len(url_id) >= url_id_length_min and len(url_id) <= url_id_length_max and str(url_id).find('abcdefgh') is -1: 
				# Second link not found - not provided in the message
				return url_id,'false'
			else:
				return 'false', 'false'
		else:
			# Check if ID fits (usually 11)
			if len(url_id) >= url_id_length_min and len(url_id) <= url_id_length_max and str(url_id).find('abcdefgh') is -1:
				return url_id,'false'
			else:
				return 'false', 'false'
	else:
		# Check if ID fits (usually 11)
		if len(url_id) >= url_id_length_min and len(url_id) <= url_id_length_max and str(url_id).find('abcdefgh') is -1:
			return(url_id)
		else:
			return ('false')

# Check if you can post again in group
def check_group(group_to_check):
	global client, group_list, client_started, client_started
	message_count = 0

	print('Checking if link can be dropped again')

	# Join channel/group
	joined = join_channel(group_to_check)
	if joined == -1:
		return 'Fail'
	# Check the restriction
	if group_list[group_to_check]['restrictions']['post_amount'] is not 0:
		# Check messages if posted before
		if group_list[selected_group]['link_last']['link_posted'] is 1:
			for message in client.iter_messages(group_name):
				if str(message).find('instagram.com') is not -1:
					if str(get_post_id(message)).find(str(group_list[group_to_check]['link_last']['link_id'])) is not -1:
						print('Found last dropped link; links dropped in between: ' + str(message_count))
						print('Group check ended: ' + str(group_to_check))
						return message_count
					else:
						message_count += 1
					# If post is already over the restricted limit (e.g. 30 posts have to be in between posts, but in those 30 your post has not been found)
					if message_count >= group_list[group_to_check]['restrictions']['post_amount']:
						print('Could not find last link before set amount; safe to post')
						print('Group check ended: ' + str(group_to_check))
						return message_count
		else:
			print('First entrance in this group; safe to post')
			message_count = group_list[group_to_check]['restrictions']['post_amount'] * 2
			return message_count	
	else:
		# Get the minute difference from post time
		time_difference = (int(time.time()) - group_list[group_to_check]['link_last']['link_time']) / 60 
		return time_difference

		
# Get all messages
def check_messages():
	# Global variables
	global id_count, first_array_full, group_name, group_list
	# 24h ago (+30min for safety)
	time_24h = int(time.time()) - (24*60*60 + 30*60)
	time_limit = int(time.time())
	url_id = ""
	url_id_2 = ""
	# Get links from messages
	try:
		for message in client.iter_messages(group_name):
			if str(message).find('instagram.com') is not -1:
				# Convert Telegram output to string
				string = str(message)
				# Url ID is 11 chars, just in case it changes, range is set [10:12]
				url_id_length_min = 10
				url_id_length_max = 12
				# Check the type of group
				if str(group_list[selected_group]['group_type']).find('fixed') is not -1:
					# Fixed like groups
					if id_count < int(group_list[selected_group]['like_count']):
						# Get ID's
						if group_list[selected_group]['max_links'] is 2:
							url_id, url_id_2 = get_post_id(message)
							# Check first ID
							if len(url_id) >= url_id_length_min and len(url_id) <= url_id_length_max:
								# Check second ID
								if url_id_2 is not -1 and len(url_id_2) >= url_id_length_min and len(url_id_2) <= url_id_length_max:
									# Add to array and increase stored id count
									if first_array_full is False:
										first_array.append(url_id)          # Array made on first run
										first_array.append(url_id_2)          # Array made on first run
									else:
										compare_array.append(url_id)        # Array made on second run for comparison
										compare_array.append(url_id_2)        # Array made on second run for comparison
									id_count += 2
								else:
									# Add to array and increase stored id count
									if first_array_full is False:
										first_array.append(url_id)          # Array made on first run
									else:
										compare_array.append(url_id)        # Array made on second run for comparison
									id_count += 1
						else:
							url_id = get_post_id(message)
							# Check if ID fits (usually 11)
							if len(url_id) >= url_id_length_min and len(url_id) <= url_id_length_max:
								# Add to array and increase stored id count
								if first_array_full is False:
									first_array.append(url_id)          # Array made on first run
								else:
									compare_array.append(url_id)        # Array made on second run for comparison
								id_count += 1
					else:
						first_array_full = True
						print("Found " + str(id_count) + " links")
						id_count = 0
						break
				else:
					# 24H groups 
					# CHANGE IDS TO TIME
					if int(time_limit) > time_24h:
						# Get ID's
						if group_list[selected_group]['max_links'] is 2:
							url_id, url_id_2 = get_post_id(message)
							# Check first ID
							if len(url_id) >= url_id_length_min and len(url_id) <= url_id_length_max:
								# Check second ID
								if url_id_2 is not -1 and len(url_id_2) >= url_id_length_min and len(url_id_2) <= url_id_length_max:
									# Add to array and increase stored id count
									if first_array_full is False:
										first_array.append(url_id)          # Array made on first run
										first_array.append(url_id_2)          # Array made on first run
									else:
										compare_array.append(url_id)        # Array made on second run for comparison
										compare_array.append(url_id_2)        # Array made on second run for comparison
									# Find date of post
									start = findnth(string, 'date',0)
									start = string[start:].find('(') + start + 1
									end = findnth(string[start:], ',',4)
									time_limit = time.mktime(datetime.datetime.strptime(string[start:end+start], "%Y, %m, %d, %H, %M").timetuple())
									id_count += 2
								else:
									# Add to array and increase stored id count
									if first_array_full is False:
										first_array.append(url_id)          # Array made on first run
									else:
										compare_array.append(url_id)        # Array made on second run for comparison
									# Find date of post
									start = findnth(string, 'date',0)
									start = string[start:].find('(') + start + 1
									end = findnth(string[start:], ',',4)
									time_limit = time.mktime(datetime.datetime.strptime(string[start:end+start], "%Y, %m, %d, %H, %M").timetuple())
									id_count += 1
						else:
							url_id = get_post_id(message)
							# Check if ID fits (usually 11)
							if len(url_id) >= url_id_length_min and len(url_id) <= url_id_length_max:
								# Add to array and increase stored id count
								if first_array_full is False:
									first_array.append(url_id)          # Array made on first run
								else:
									compare_array.append(url_id)        # Array made on second run for comparison
								# Find date of post
								start = findnth(string, 'date',0)
								start = string[start:].find('(') + start + 1
								end = findnth(string[start:], ',',4)
								time_limit = time.mktime(datetime.datetime.strptime(string[start:end+start], "%Y, %m, %d, %H, %M").timetuple())
								id_count += 1
					else:
						first_array_full = True
						print("Found " + str(id_count) + " links")
						id_count = 0
						break
	except ValueError:
		print('Group does not exist')

# Check if new messages have been posted while liking pictures
def check_new_messages():
    global final_array, first_array, new_message, group_list, first_array_full, compare_array
    check_messages()
    final_array = list(set(compare_array) - set(first_array))
    first_array = compare_array
    if len(final_array) == 0:
        print("No new messages found while liking posts")
        new_message = False
        first_array_full = True
    else:
        new_message = True
        first_array_full = True      
        print("New message count: " + str(len(final_array)))
        like_posts()
        check_new_messages()

# Likes posts from array
def like_posts():
	global likes_given, group_list, liked
	# Check from which array to take posts
	if new_message is False:
		post_array = first_array
	else:
		post_array = final_array
	# Like all posts in array
	for post in post_array:
		# Check if already liked
		if str(liked_all).find(str(post)) is -1:
			instabot.like(get_media_id(post))
			add_liked.append(post)
			print('[' + str(likes_given+1) + '/' + str(len(post_array)) + '] Liked ' + post)
			# Delay
			if likes_given != len(post_array):
				if config['delay'] <= 0:
					time.sleep(1)
				else:
					time.sleep(random.randint(config['delay']-1,config['delay']+1))
		else:
			print('[' + str(likes_given+1) + '/' + str(len(post_array)) + '] Already liked, skipping ' + post)
		likes_given += 1
	likes_given = 0

# Post the link in telegram group
def post_link():
	global group_list, liked, liked_all, client
	
	# For updating liked.json with date
	date = str(datenow.now().year)+'-'+str(datenow.now().month)+'-'+str(datenow.now().day)

	# Get the array ready
	post_message = ""
	g_type = ""
	# Fixed or 24h (Dx30 or D24h)
	if str(group_list[selected_group]['group_type']).find('fixed') is not -1:
		g_type = 'Dx' + str(group_list[selected_group]['like_count'])
	else:
		g_type = 'D24h'
	# Check how many links to post
	if group_list[selected_group]['max_links'] is 1 or str(link2).find(insta_string) is -1:
		# Check if the group requires username
		if group_list[selected_group]['username_required'] is 1:
			post_message = g_type + " @" + config['ig_username'] + " " + link1
		else:
			post_message = g_type + " " + link1
	else:
		# Check if the group requires username
		if group_list[selected_group]['username_required'] is 1:
			post_message = g_type + " @" + config['ig_username'] + " " + link1 + " " + link2
		else:
			post_message = g_type + " " + link1 + " " + link2
	try:
		client.send_message(group_name, post_message, link_preview = False)
		print('Sent: ' + post_message)
	except:
		print("Can't send - might be banned from group or in general (check Telegram's Spam Info Bot)")
		return "Fail"
	# Write new data to groups.json
	try:
		with open(str(config['telegram_api_id']) + '_groups.json') as json_file:  
			group_list = json.load(json_file)
		with open(str(config['telegram_api_id']) + '_groups.json', 'w') as json_file:
			if str(group_list[selected_group]['group_type']).find('fixed') is -1:
				group_list[selected_group]['link_last']['link_id'] = get_post_id(link1)
			else:
				group_list[selected_group]['link_last']['link_id'] = get_post_id(link1)
			group_list[selected_group]['link_last']['link_time'] = int(time.time())
			group_list[selected_group]['link_last']['link_posted'] = 1
			json.dump(group_list, json_file, indent=4, separators=(',', ': '), sort_keys=True)
	except FileNotFoundError:
		print('File ' + str(config['telegram_api_id']) + '_groups.json' + ' does not exist')

	# Write new data to liked.json
	try:
		with open(config['ig_username'] + '_liked.json', 'r') as json_file:  
			try:
				liked = json.load(json_file)
				liked = liked[date]				
			except KeyError:
				print('No likes found for ' + str(date))
			json_file.close()
		with open(config['ig_username'] + '_liked.json', 'w+') as json_file:
			
			if len(liked) > 4:
				data[date] = liked + add_liked
			else:
				data[date] = add_liked
			json.dump(data, json_file, indent=4, separators=(',', ': '), sort_keys=True)
			json_file.close()
		with open(config['ig_username'] + '_liked.json', 'r') as json_file:  
			liked_all = json.load(json_file)
			json_file.close()

	except FileNotFoundError:
		with open(config['ig_username'] + '_liked.json', 'w+') as json_file:
			data[date] = add_liked 
			json.dump(data, json_file, indent=4, separators=(',', ': '), sort_keys=True)
			liked_all = add_liked
			json_file.close()

# Start the program
def start_groups(config_group):
	global client, first_array_full, new_message, compare_array, first_array, final_array, group_name, likes_given, add_liked, selected_group
	update_config()
	date = str(datenow.now().year)+'-'+str(datenow.now().month)+'-'+str(datenow.now().day) # returns e.g. 2019-1-29
	# Load likes
	liked_today = 0
	try:
		with open(config['ig_username'] + '_liked.json', 'r') as json_file:  
			try:
				liked_today = json.load(json_file)
				liked_today = len(liked_today[date])
				print('Already liked ' + str(liked_today) + ' posts today; max ' + str(config['max_likes']))
			except KeyError:
				print('No likes found for ' + str(date))
				liked_today = 0
	except FileNotFoundError:
		print(config['ig_username'] + '_liked.json' + ' not found')


	if int(liked_today) <= config['max_likes']:
		active = True

		# Get last links from posts
		try:
			get_last_posts()
		except AttributeError:
			print('Tried getting posts; AttributeError; Instabot.py')
			return 'Fail'

		# Check the conditions before starting

		# Check if your profile has enough followers
		#if group_list[selected_group]['restrictions']['followers'] < followers:
		# If group has no username requirement, user_id of selected post has to match Instagram user_id
		#if group_list[selected_group]['username_required'] is 1:
		selected_group = config_group
		if str(link1).find(insta_string) is -1:
			print('Link 1 not set or not properly formated (https://www.instagram.com/p/BtULbITlh7C/)')
		else:
			print()
			print("----------------------------------------------------------------")
			print('Starting group: ' + str(selected_group) + "; Time started " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute))
			print("----------------------------------------------------------------")
			print()

			# Join group and refresh it
			joined = join_channel(selected_group)
			if joined == -1:
				print("Could not join channel; Telethon")
				return 'Fail'
			try:
				result = client(functions.updates.GetChannelDifferenceRequest(
			        channel=group_name,
			        filter=types.ChannelMessagesFilter(
			            ranges=[types.MessageRange(
			                min_id=0,
			                max_id=1
			            )],
			            exclude_new_messages=False
			        ),
			        pts=42,
			        limit=100,
			        force=True
			    ))
			except:
				print("Channel not accesible; Telethon")
				return 'Fail'
			# Check the restriction
			if group_list[selected_group]['restrictions']['post_amount'] is not 0:
				#if group_list[selected_group]['link_last']['link_posted'] is 1 or 0:
				message_count = check_group(selected_group)
				if message_count >= group_list[selected_group]['restrictions']['post_amount']:
					# Check messages - find links
					check_messages()
					# Like posts from first_array and check new messages after
					like_posts()
					check_new_messages()
					# Post link to Telegram group
					post_link()
					# Reset all variables for next use
					first_array_full = False
					new_message = False
					first_array = []
					compare_array = []
					final_array = []
					add_liked = []
					likes_given = 0				
					print('Program ended: ' + str(selected_group))
					active = False
				else:
					print('Cant post; either too fast or post gap not reached (check restrictions)')
			else:
				time_difference = check_group(selected_group)
				if group_list[selected_group]['restrictions']['time_interval'] > time_difference:
					difference = group_list[selected_group]['restrictions']['time_interval'] - int(time_difference)
					print('Time interval is not met, wait ' + str(difference) + ' minutes (' + str(int(difference/60)) + ' hours)' ) 
				else:
					# Check messages - find links
					check_messages()
					# Like posts from first_array and check new messages after
					like_posts()
					check_new_messages()
					# Post link to Telegram group
					post_link()
					# Reset all variables for next use
					first_array_full = False
					new_message = False
					first_array = []
					compare_array = []
					final_array = []
					add_liked = []
					likes_given = 0
					# Make pop-up when done
					#sg.PopupOK('Done')
					print('Program ended: ' + str(selected_group))
					active = False
	else:
		print('Max like amount reached for today')

# Connect/start telegram client
def start_client():
	global client_started, client
	client.start()
	client_started = True
		
# Disconnect telegram client
def disconnect_client():
	global client_started, client
	client.disconnect()
	client_started = False

# Leave channel/group
def leave_channel(channel_name):
	global group_list, client
	# Check if client has joined this group
	if group_list[channel_name]['joined'] is 1:
		# Check if group is private - cant leave private with API (have to fix?)
		if group_list[channel_name]['private'] is 0:
			client(LeaveChannelRequest(group_list[channel_name]['group_id']))
			try:
				with open(str(config['telegram_api_id']) + '_groups.json') as json_file:  
					group_list = json.load(json_file)
				with open(str(config['telegram_api_id']) + '_groups.json', 'w') as json_file:
					group_list[channel_name]['joined'] = 0
					json.dump(group_list, json_file, indent=4, separators=(',', ': '), sort_keys=True)
			except FileNotFoundError:
				print('File ' + str(config['telegram_api_id']) + '_groups.json' + ' does not exist')

# Join channel/group
def join_channel(channel_name):
	global client, group_name, group_list
	try:
		# Check if client has joined this group
		if group_list[channel_name]['joined'] is 0:
			print('Joining group ' + str(channel_name))
			# Check if the channel is private
			if group_list[channel_name]['private'] is 0:
				client(JoinChannelRequest(group_list[channel_name]['group_id']))
				group_name = group_list[channel_name]['group_id']
			else:
				try:
					updates = client(ImportChatInviteRequest(group_list[channel_name]['group_id']))
					group_name = client.get_entity('telegram.me/joinchat/' + group_list[channel_name]['group_id'])
				except:
					group_name = client.get_entity('telegram.me/joinchat/' + group_list[channel_name]['group_id'])
			try:
				with open(str(config['telegram_api_id']) + '_groups.json') as json_file:  
					group_list = json.load(json_file)
				with open(str(config['telegram_api_id']) + '_groups.json', 'w') as json_file:
					group_list[channel_name]['joined'] = 1
					json.dump(group_list, json_file, indent=4, separators=(',', ': '), sort_keys=True)
			except FileNotFoundError:
				print('File ' + str(config['telegram_api_id']) + '_groups.json' + ' does not exist')
		else:
			if group_list[channel_name]['private'] is 0:
				group_name = group_list[channel_name]['group_id']
			else:
				group_name = client.get_entity('telegram.me/joinchat/' + group_list[channel_name]['group_id'])
	except:
		print('Cannot join group (perhaps does not exist/banned)')
		return -1
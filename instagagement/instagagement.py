# General
import os, sys
import json, time, datetime, random
import webbrowser, requests
from datetime import datetime as datenow
# Instabot https://github.com/instagrambot/instabot/
from instabot import API
# Telethon Telegram API by LonamiWebs https://github.com/LonamiWebs/Telethon
from telethon import TelegramClient, events, sync, errors, functions, types
from telethon.tl.functions.channels import JoinChannelRequest,LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest

# Settings
group_template = 'group_template.json'
insta_string = '/p/' 			# To find instagram link in telegram message
insta_shortcode = 'shortcode'	# To find instagram link in user feed
group_list = []
config = []
client = []
preset = ''
debug = 0						# Enables timing and other info
log_en = 1					# Logs data to .json
# For commenting
add_phrase = ['Keep posting!', 'Love it!', 'Keep it up!']
banned_phrases = ['check', 'Check', 'me', 'bio', 'follow', 'Follow', 'like', 'Like', 'profile', 'sale', 
					'discount', 'off', 'youtube', 'DM', 'hot', '#', '@', 'cheap', 'click', 'Click']
min_comment_length = 5

# Variables
first_array_full = False
new_message = False
client_started = False
profanity_imported = False
compare_array = []
first_array = []
final_array = []
group_name = ''
selected_group = ''

# Instagram
instabot = []
targeted_links = ['', '', '']

def init(preset_, args):
	global config, group_list, liked_all, preset, debug, targeted_links, target_user
	preset = preset_

	# Parse arguments
	debug = int(args.debug)
	if args.links != None:
		targeted_links = args.links.split(',')

	# Print time after every print message
	if debug == 1:
		old_f = sys.stdout
		class F:
			def write(self, x):
				old_f.write(x.replace("\n", " [%s]\n" % str(datenow.now())))
		sys.stdout = F()

	# Load config
	update_config()

	if args.target == None:
		target_user = config['like_profile']
	else:
		target_user = args.target

	# Load groups
	try:
		with open(str(config['telegram_api_id']) + '_groups.json', 'r') as load_groups:  
			group_list = json.load(load_groups)
		if debug == 1:
			print('Group list loaded from ' + str(config['telegram_api_id']) + '_groups.json')
	except FileNotFoundError:
		if debug == 1:
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
		if debug == 1:
			print(config['ig_username'] + '_liked.json' + ' not found')

def update_config():
	global preset, config, date
	date = str(datenow.now().year)+'-'+str(datenow.now().month)+'-'+str(datenow.now().day)
	# Load config file
	try:
		with open(preset + '_config.json') as json_file:  
			config = json.load(json_file)
		if debug == 1:
			print('Config loaded from ' + preset + '_config.json')
	except FileNotFoundError:
		print('File ' + preset + '_config.json' + ' does not exist, run quickstart.py!')
		print()
		sys.exit()

def get_last_posts():
	global instabot
	# Get the posts from specified profile in config
	# Stores links in user_links in range from 0 to 11 (12 posts)
	user_links = []

	instabot.search_username(target_user) 
	instabot.get_user_feed(instabot.last_json["user"]["pk"])
	for i in range(0, len(instabot.last_json['items'])):
		user_links.append(instabot.last_json['items'][i]['code'])

	return user_links

def login():
	global instabot, client, user_followers, user_following, user_media, user_id

	instabot = API()
	instabot.login(	username = config['ig_username'],
					password = config['ig_password'], 
					use_cookie = True, 
					cookie_fname = config['cookie_name'])

	# Telegram client
	client = TelegramClient(config['session'], config['telegram_api_id'], config['telegram_api_hash'])
	client.flood_sleep_threshold = 24 * 60 * 60

	# Get user info
	instabot.get_username_info(instabot.user_id)
	user_followers = instabot.last_json['user']['follower_count']
	user_following = instabot.last_json['user']['following_count']
	user_media = instabot.last_json['user']['media_count']
	user_id = instabot.user_id

	return [user_followers, user_following, user_media]

# Get json from URL and get Media ID
def get_media_id(media_url, mode):
	url = ''

	# Full link
	if mode == 0:
		url = 'https://api.instagram.com/oembed/?callback=&url=' + media_url 

	# Only shortcode of link
	if mode == 1:
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
		print('Broken Instagram link; end not found; ValueError (0). Given string: ' + string)
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
				print('Broken Instagram link; end not found; ValueError (1) Given string: ' + string)
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

	if debug == 1:
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
						print('Links dropped in between: ' + str(message_count) + ' - skipping group')
						if debug == 1:
							print('Group check ended: ' + str(group_to_check))
						return message_count
					else:
						message_count += 1
					# If post is already over the restricted limit (e.g. 30 posts have to be in between posts, but in those 30 your post has not been found)
					if message_count >= group_list[group_to_check]['restrictions']['post_amount']:
						print('Could not find last link before set amount - safe to post')
						if debug == 1:
							print('Group check ended: ' + str(group_to_check))
						return message_count
		else:
			print('First entrance in this group - safe to post')
			message_count = group_list[group_to_check]['restrictions']['post_amount'] * 2
			return message_count	
	else:
		# Get the minute difference from post time
		time_difference = (int(time.time()) - group_list[group_to_check]['link_last']['link_time']) / 60 
		return time_difference

		
# Get all messages
def check_messages():
	# Global variables
	global first_array_full, group_name, group_list
	# 24h ago (+30min for safety)
	time_24h = int(time.time()) - (24*60*60 + 30*60)
	time_limit = int(time.time())
	url_id = ""
	url_id_2 = ""
	link_count = 0
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
					if link_count < int(group_list[selected_group]['like_count']):
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
									link_count += 2
								else:
									# Add to array and increase stored id count
									if first_array_full is False:
										first_array.append(url_id)          # Array made on first run
									else:
										compare_array.append(url_id)        # Array made on second run for comparison
									link_count += 1
						else:
							url_id = get_post_id(message)
							# Check if ID fits (usually 11)
							if len(url_id) >= url_id_length_min and len(url_id) <= url_id_length_max:
								# Add to array and increase stored id count
								if first_array_full is False:
									first_array.append(url_id)          # Array made on first run
								else:
									compare_array.append(url_id)        # Array made on second run for comparison
								link_count += 1
					else:
						first_array_full = True
						if debug == 1:
							print("Found " + str(link_count) + " links")
						link_count = 0
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
									link_count += 2
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
									link_count += 1
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
								link_count += 1
					else:
						first_array_full = True
						if debug == 1:
							print("Found " + str(link_count) + " links")
						link_count = 0
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
        engage_with_posts()
        check_new_messages()

# Likes posts from array
def engage_with_posts():
	global group_list, instabot, current_post, profanity_imported
	add_liked = []

	liked_all = get_liked()

	# Check from which array to take posts
	if new_message is False:
		post_array = first_array
	else:
		post_array = final_array

	# Create progressbar
	progress = 0
	likes_given = 0
	printProgressBar(0, len(post_array), prefix = 'Progress:', suffix = '[' + str(likes_given+1) + '/' + str(len(post_array)) + '] ', bar_length = 25)
	# Like all posts in array
	for post in post_array:
		post_id = get_media_id(post, 1)
		current_post = post
		# Check if already liked
		if str(liked_all).find(str(post)) is -1:
			likes_given += 1
			printProgressBar(likes_given, len(post_array), prefix = 'Progress:', suffix = '[' + str(likes_given) + '/' + str(len(post_array)) + '] ' + post, bar_length = 25)
			if post_id != -1:
				# Like post
				is_liked = str(instabot.like(post_id))
				if is_liked == 0:
					print()					
					send_error('Post not liked, try changing cookie name in ' + config['ig_username'] + '_config.json')
					print()
					sys.exit()
			add_liked.append(post)	
			if likes_given != len(post_array):
				if config['delay'] <= 2:
					time.sleep(1 + random.randint(0, 5))
				else:
					time.sleep(random.randint(config['delay']-2,config['delay']+2))
		else:
			likes_given += 1
			printProgressBar(likes_given, len(post_array), prefix = 'Progress:', suffix = '[' + str(likes_given) + '/' + str(len(post_array)) + '] ' + post, bar_length = 25)
		# Post a comment
		if group_list[selected_group]['comment'] == 1 and post_id != -1:
			if profanity_imported == False:
				# Profanity predictor for commenting
				from profanity_check import predict_prob
				profanity_imported = True

			bad_comments = []
			good_comments = []
			comment = ' '
			instabot.get_media_comments(post_id)
			comment_json = instabot.last_json
			comments_disabled = False
			already_commented = False
			try:
				if comment_json['comments_disabled'] == True:
					comments_disabled = True
				else:
					comments_disabled = False
			except:
				comments_disabled = False

			if comments_disabled == False:
				# Find unwanted comments
				for i in range(0, len(instabot.last_json['comments'])):
					if int(instabot.last_json['comments'][i]['user_id']) == int(user_id):
						already_commented = True
					# Get all comments here
					good_comments.append(i)
					comment = instabot.last_json['comments'][i]['text']
					for phrase in banned_phrases:
						if phrase in comment or len(comment) < min_comment_length or instabot.last_json['comments'][i]['type'] != 0:
							bad_comments.append(int(i))
							break
				if already_commented == False:
					# Remove unwanted comments from found comments
					for i in range(0, len(bad_comments)):
						good_comments = list(filter(lambda a: a != bad_comments[i], good_comments))
					# Remove duplicates (if any)
					good_comments = list(set(good_comments))
					if len(good_comments) >= 1:
						#random_comment = int(random.randint(0, len(good_comments)-1))
						#comment = instabot.last_json['comments'][good_comments[random_comment]]['text'] + '! ' + add_phrase[random.randint(0, len(add_phrase)-1)]
						# Filter comments
						profanity = {}
						comment_list = []
						smallest = 1
						temp = 1
						good_comments = list(set(good_comments))
						for i in good_comments:
							comment = instabot.last_json['comments'][i]['text']
							comment_list.append(comment)
							prediction = str(predict_prob([comment])[0])
							profanity[prediction] = comment
							smallest = prediction
							if float(smallest) > float(temp):
								smallest = temp
							temp = smallest
						comment = profanity[smallest] + '! ' + add_phrase[random.randint(0, len(add_phrase)-1)]
						result = instabot.comment(post_id, comment)
						if 'feedback_required' in str(result):
							send_error('Could not comment, this feature might be blocked temporary; reduce commenting groups')
							sys.exit()
						# This is to check if comments are good enough and to find phrases to ban
						if log_en == 1:
							log_data(comment)
					else:
						result = instabot.comment(post_id, add_phrase[random.randint(0, len(add_phrase)-1)])
						if 'feedback_required' in str(result):
							send_error('Could not comment, this feature might be blocked temporary; reduce commenting groups')
							sys.exit()
			else:
				# Still try to comment
				result = instabot.comment(post_id, add_phrase[random.randint(0, len(add_phrase)-1)])
				if 'feedback_required' in str(result):
					send_error('Could not comment, this feature might be blocked temporary; reduce commenting groups')
					sys.exit()

	
	# Update liked posts (both .json and temporary hour counter)
	update_liked(add_liked)

# Post the link in telegram group
def post_link():
	global group_list, liked, liked_all, client
	
	# For updating liked.json with date
	date = str(datenow.now().year)+'-'+str(datenow.now().month)+'-'+str(datenow.now().day)

	# Get last links from selected user
	try:
		user_links = get_last_posts()
	except AttributeError:
		print('Tried getting posts; AttributeError; Instabot.py')
		return -1
	
	if 'random' in targeted_links:
		temp = user_links
		for i in range(0, len(user_links)-1):
			temp[i] = user_links[random.randint(0, len(user_links)-1)]
		user_links = temp
	else:
		# Check if link is added manually
		for i in range(0, len(targeted_links)):
			if len(targeted_links[i]) > 1:
				user_links[i] = get_post_id(targeted_links[i])

	# Get the array ready
	post_message = ""
	g_type = ""
	# Fixed or 24h (Dx30 or D24h)
	if str(group_list[selected_group]['group_type']).find('fixed') is not -1:
		g_type = 'Dx' + str(group_list[selected_group]['like_count'])
	else:
		g_type = 'D24h'
	# Check how many links to post
	if group_list[selected_group]['max_links'] == 1 or len(user_links[1]) <= 1:
		# Check if the group requires username
		if group_list[selected_group]['username_required'] is 1:
			post_message = g_type + " @" + config['ig_username'] + " " + 'https://instagram.com/p/' + user_links[0] + '/'
		else:
			post_message = g_type + " " + 'https://instagram.com/p/' + user_links[0] + '/'
	else:
		# Check if the group requires username
		if group_list[selected_group]['username_required'] is 1:
			post_message = g_type + " @" + config['ig_username'] + " " + 'https://instagram.com/p/' +  user_links[0] + "/\n" + 'https://instagram.com/p/' + user_links[1] + '/'
		else:
			post_message = g_type + " " + 'https://instagram.com/p/' + user_links[0] + "/\n" + 'https://instagram.com/p/' + user_links[1] + '/'
	try:
		client.send_message(group_name, post_message, link_preview = False)
		print('Sent: ' + post_message)
	except:
		print("Can't send - might be banned from group or in general (check Telegram's Spam Info Bot)")
		flag_group(selected_group)
		return "Fail"

	# Write new data to groups.json
	try:
		with open(str(config['telegram_api_id']) + '_groups.json') as json_file:  
			group_list = json.load(json_file)
		with open(str(config['telegram_api_id']) + '_groups.json', 'w+') as json_file:
			if str(group_list[selected_group]['group_type']).find('fixed') is -1:
				group_list[selected_group]['link_last']['link_id'] = user_links[0]
			else:
				group_list[selected_group]['link_last']['link_id'] = user_links[0]
			group_list[selected_group]['link_last']['link_time'] = int(time.time())
			group_list[selected_group]['link_last']['link_posted'] = 1
			json.dump(group_list, json_file, indent=4, separators=(',', ': '), sort_keys=True)
	except FileNotFoundError:
		print('File ' + str(config['telegram_api_id']) + '_groups.json' + ' does not exist')

# Start the program
def start_groups(config_group):
	global client, first_array_full, new_message, compare_array, first_array, final_array, group_name, likes_given, add_liked, selected_group
	update_config()
	selected_group = config_group

	# Get todays liked post amount
	try:
		liked_today = len(get_liked()[date])
	except:
		liked_today = 0

	print_header(config_group)

	if group_list[config_group]['blocked'] == 0:
		if int(liked_today) <= config['max_likes']:
			# Check this:
			# If group has no username requirement, user_id of selected post has to match Instagram user_id
			#if group_list[selected_group]['username_required'] is 1:

			if group_list[selected_group]['restrictions']['followers'] < user_followers:

				# Join group and refresh it
				joined = join_channel(selected_group)
				if joined == -1:
					print("Could not join channel - Telethon")
					return -1
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
					print("Channel not accesible - Telethon")
					return -1
				# Check the restriction
				if group_list[selected_group]['restrictions']['post_amount'] is not 0:
					#if group_list[selected_group]['link_last']['link_posted'] is 1 or 0:
					message_count = check_group(selected_group)
					if message_count >= group_list[selected_group]['restrictions']['post_amount']:
						# Check messages - find links
						check_messages()
						# Like posts from first_array and check new messages after
						engage_with_posts()
						check_new_messages()
						# Post link to Telegram group
						post_link()
						# Reset all variables for next use
						first_array_full = False
						new_message = False
						first_array = []
						compare_array = []
						final_array = []
						if debug == 1:			
							print('Program ended')
					else:
						print('Cant post - post gap not reached')
						return -1
				else:
					time_difference = check_group(selected_group)
					if group_list[selected_group]['restrictions']['time_interval'] > time_difference:
						difference = group_list[selected_group]['restrictions']['time_interval'] - int(time_difference)
						print('Time interval is not met, wait ' + str(difference) + ' minutes (' + str(int(difference/60)) + ' hours)' ) 
						return -1
					else:
						# Check messages - find links
						check_messages()
						# Like posts from first_array and check new messages after
						engage_with_posts()
						check_new_messages()
						# Post link to Telegram group
						post_link()
						# Reset all variables for next use
						first_array_full = False
						new_message = False
						first_array = []
						compare_array = []
						final_array = []
						if debug == 1:
							print('Program ended: ' + str(selected_group))
			else:
				print(str(group_list[selected_group]['restrictions']['followers']) + ' followers needed, skipping group')
				return -1
		else:
			print('Max like amount reached for today')
			return -1
	else:
		print('This group has been flagged, skipping')
		print('(could not post in group previously)')
		return -1

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
				with open(str(config['telegram_api_id']) + '_groups.json', 'w+') as json_file:
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
			if debug == 1:
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
				with open(str(config['telegram_api_id']) + '_groups.json', 'w+') as json_file:
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

def flag_group(channel_name):
	# If it was not possible to send message in group, you might be banned/blocked, therefore should be skipped next time
	with open(str(config['telegram_api_id']) + '_groups.json') as json_file:  
		group_list = json.load(json_file)
	with open(str(config['telegram_api_id']) + '_groups.json', 'w+') as json_file:
		group_list[channel_name]['blocked'] = 1
		json.dump(group_list, json_file, indent=4, separators=(',', ': '), sort_keys=True)

def get_liked():
	try:
		with open(config['ig_username'] + '_liked.json', 'r') as json_file:  
			liked_all = json.load(json_file)
			json_file.close()
			return liked_all
	except FileNotFoundError:
		return 0

def update_liked(new_likes):
	# Write new data to liked.json
	liked_all = {}
	liked_today = []
	data = {}
	try:
		with open(config['ig_username'] + '_liked.json', 'r') as json_file:  
			liked_all = json.load(json_file)
			try:
				liked_today = liked_all[date]	
			except KeyError:
				if debug == 1:
					print('No likes found for ' + str(date))
			json_file.close()
		with open(config['ig_username'] + '_liked.json', 'w+') as json_file:
			liked_all[date] = liked_today + new_likes
			json.dump(liked_all, json_file, indent=4, separators=(',', ': '), sort_keys=True)
			json_file.close()

	except FileNotFoundError:
		with open(config['ig_username'] + '_liked.json', 'w+') as json_file:
			data[date] = new_likes 
			json.dump(data, json_file, indent=4, separators=(',', ': '), sort_keys=True)
			liked_all = new_likes
			json_file.close()

	return liked_all

def log_data(data):
	logged_data = {}
	try:
		with open(config['ig_username'] + '_log.json', 'r') as json_file:  
			logged_data = json.load(json_file)
			json_file.close()
		with open(config['ig_username'] + '_log.json', 'w+') as json_file:
			logged_data[current_post] = data
			json.dump(logged_data, json_file, indent=4, separators=(',', ': '), sort_keys=True)
			json_file.close()
	except FileNotFoundError:
		with open(config['ig_username'] + '_log.json', 'w+') as json_file:
			logged_data[current_post] = data
			json.dump(logged_data, json_file, indent=4, separators=(',', ': '), sort_keys=True)
			json_file.close()

def print_header(name):
	# Get todays liked post amount
	try:
		liked_today = len(get_liked()[date])
	except:
		liked_today = 0

	start_message = ('[' + config['ig_username'] + "] '" + name + "' [" + str(datetime.datetime.now().strftime("%H:%M")) + '] ['
			+ str(liked_today) + '/' + str(config['max_likes'])+ ']')
	for x in range(1,len(start_message)+1):
		print('-', end = '')
	print()
	print(start_message)
	for x in range(1,len(start_message)+1):
		print('-', end = '')
	print()
	print()

# Like recent feed
def like_feed():
	update_config()
	add_liked = []
	# Print header
	print_header('Feed like')

	# Get todays liked post amount
	try:
		liked_today = len(get_liked()[date])
	except:
		liked_today = 0

	instabot.get_timeline_feed()

	if int(liked_today) <= int(config['max_likes']):
		feed_liked = 0
		try:
			timeline_posts = instabot.last_json['num_results']
		except:
			print('Could not get feed posts, trying again')
			feed_tries += 1
			like_feed()
		printProgressBar(0, timeline_posts, prefix = 'Progress:', suffix = '[' + str(feed_liked) + '/' + str(timeline_posts) + '] ', bar_length = 25)
		for i in range(0, timeline_posts):
			try:
				post = instabot.last_json['feed_items'][i]['media_or_ad']['code']
				# Check if its not own post
				if instabot.last_json['feed_items'][i]['media_or_ad']['id'].split('_')[1] != user_id:
					# Check if already liked
					if str(get_liked()).find(str(post)) is -1:
						instabot.like(get_media_id(post, 1))
						add_liked.append(post)
						time.sleep(config['delay'])
						instabot.get_timeline_feed()
			except:
				# Ad found
				pass
			feed_liked += 1
			printProgressBar(feed_liked, timeline_posts, prefix = 'Progress:', suffix = '[' + str(feed_liked) + '/' + str(timeline_posts) + '] ', bar_length = 25)
		update_liked(add_liked)
	else:
		print('Max like amount reached for today')

def send_error(error_message):
	print(error_message)
	try:
		error_message = error_message + '\n Group error ocurred: ' + selected_group
	except:
		pass
	try:
		error_message = error_message + '\n Post ID left on: ' + current_post
	except:
		pass
	if len(str(config['telegram_username'])) >= 4:
		time.sleep(5)
		if client_started == False:
			start_client()
			time.sleep(5)
		client.send_message(config['telegram_username'], "[" + config['ig_username'] + "] program error ocurred: \n\n" + error_message)

# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    if total <= 0:
    	total = 1
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    print('\r%s |%s| %s' % (prefix, bar, suffix), end = ''),

    if iteration >= total:
        print()
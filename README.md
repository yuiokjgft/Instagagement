# Instagagement

Python program that automates [Telegram engagement groups](https://medium.com/@violet.emily.xoxo/inside-instagram-pods-the-secret-trick-to-increase-your-engagement-55b0d9c3cee9) for Instagram such as Wolf Global by combining Instagram bot (Instabotpy) and Telegram API (Telethon).

This also runs on Raspberry Pi (tutorial will be added).

## Features

- Finds latest posts from profile you specify, gets links from them, joins Telegram group, finds all the links to engage with, engages, posts yours. That simple. Currently only supports likes.
- Intended for 24/7 use with limited hours during the day (e.g. 6.00 to 18.00).
- Supports basic Telegram engagement groups - post amount based and time based. All the available groups are found in group_template.json, more can be added. Currently 25 groups listed. Request any missing.

## Requirements

- [Python](https://www.python.org/downloads/)
- Telegram account with created [application](https://my.telegram.org/apps) from which API hash and ID will be used
- [Instabot.py](https://github.com/instabot-py/instabot.py) for handling likes and finding user feed last links (finds the links from specified profile which are needed in Telegram groups for posting)
- [Telethon](https://github.com/LonamiWebs/Telethon) for handling Telegram

## Installation

Until proper package is made, download the files and install following:

```
pip install instabot-py
pip install telethon
```
Should be ready to run the script.

## Usage

To get started and set everything up, run 'quickstart.py'. During quickstart you will be asked for your Instagram credentials and Telegram API keys which you can generate [here](https://my.telegram.org/apps). 

There is premade script for simple operation - 'run.py'.

If you exit python script while Telegram client is open, you will block Telegram's session file. To fix it, run 'create_session.py' and change the name of session file in config file of your account. Do not re-use old session name.

The groups go into 2 main categories: those, who require you to engage with the account that you want likes on (e.g. Wolf Global) and those who dont (e.g. Boostgram). Quickstart will guide you.

Some groups have minimum follower requirement. Use with care as currently there is nothing checking that (will add soon).

### Known bugs:
- After liking the posts that have been missed during first liking batch, it does not find the newly missed ones. Minor issue. Noticable in fast-pacing groups.
- Some useful features needed.
- Gets funny after midnight (dumb timing in run.py) - e.g. do not use with timing from 23 to 4 (it does not like day switch).
- Probably some other mess. Been stress-testing it for several weeks, no major issues.

### If you run multiple bots on 1 Telegram account:
- Do not overlap groups
- Run them in same location/folder

More details coming soon (maybe).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Software is quite messy due to inexperience with Python and time constraints. 

## License

Did not bother to add anything, do as you wish.

> **Disclaimer**: Please Note that this is a research project. I am by no means responsible for any usage of this tool. Use on your own behalf. I'm also not responsible if your Instagram account gets banned due to extensive use of this tool. If Telethon is outdated, your Telegram account most likely will get banned, update Telethon frequently. Check your Telegram frequently to see if any engagement has been missed (happens very rarely).

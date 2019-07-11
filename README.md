# Instagagement

Python program that automates [Telegram engagement groups](https://medium.com/@violet.emily.xoxo/inside-instagram-pods-the-secret-trick-to-increase-your-engagement-55b0d9c3cee9) for Instagram such as Wolf Global by combining Instagram bot ([Instabot](https://github.com/instagrambot/instabot)) and Telegram API ([Telethon](https://github.com/LonamiWebs/Telethon)).

This also runs on Raspberry Pi (requires Python 3.6 or higher; [here is a tutorial](https://github.com/Ewlbo/Instagagement/blob/master/RASPBERRY.md)).

GUI coming soon.

#### LATEST DEV.: Added [profanity-check](https://github.com/vzhou842/profanity-check) for commenting. Install it with 'pip install profanity-check'

#### NOTE: Web-based bot [InstaBot-Py 0.4.7](https://github.com/instabot-py/instabot.py) has been changed to mobile-based [Instabot](https://github.com/instagrambot/instabot). Release [0.1W](https://github.com/Ewlbo/Instagagement/releases/tag/0.1W) is the old version with InstaBot-Py 0.4.7 while release [0.2](https://github.com/Ewlbo/Instagagement/releases/tag/0.2) is the new release with Instabot.

## Features

- Finds latest posts from profile on which you want to get likes on, gets links from the posts, joins Telegram group, finds all the links to engage with, engages, posts yours. That simple. Supports likes and comments.
- As for commenting - it acquires other comments and chooses the one with least predicted [profanity](https://github.com/vzhou842/profanity-check), then adds random phrase and posts it
- Intended for 24/7 use with limited hours during the day (e.g. 6.00 to 18.00).
- Supports basic Telegram engagement groups - post amount based (e.g. Dx10) and 24h groups. Currently 41 groups are available and can be seen in 'group_template.json' (choosable during quickstart), more can be easily added. Request any missing.
- Optional: like latest posts from feed
- Optional: send errors/updates to your telegram

Argument list:

|   Argument  |                          Description                          |                                             Example                                             |
|:-----------:|:-------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------:|
| -c --config | Bot preset - chooses config file (usually Instagram username) | --config username                                                                               |
| -l --links  | Choose links to which you want likes/comments on              | --links https://www.instagram.com/p/link1/, https://www.instagram.com/p/link2/ ; --links random |
| -t --target | Username on which you want to receive engagement              | --target username                                                                               |
| -f --feed   | Disable [0] (default) or enable [1] feed like                 | --feed 1                                                                                            |
| -d --debug  | Disable [0] (default) or enable [1] debug messages            | --debug 1                                                                                            |

## Requirements

- [Python](https://www.python.org/downloads/) 3.6 or higher
- Telegram account with created [application](https://my.telegram.org/apps) from which API hash and ID will be used
- [Instabot](https://github.com/instagrambot/instabot) for handling likes and finding user feed last links (finds the links from specified profile which are needed in Telegram groups for posting)
- [Telethon](https://github.com/LonamiWebs/Telethon) for handling Telegram
- [Profanity check](https://github.com/vzhou842/profanity-check) for commenting

## Installation

Proper package will be made soon.

#### Windows

- Install [Python](https://www.python.org/downloads/)
- Download Instagagement and extract it somewhere
- Open Windows PowerShell or Command Prompt
- Run the following:
```elm
pip install instabot
pip install telethon
pip install profanity-check
(cd to where you extracted Instagagement e.g. cd ~/Desktop/Instagagement)
python quickstart.py
python run.py
```

#### Linux

```elm
pip install instabot
pip install telethon
pip install profanity-check
cd ~/Desktop
git clone https://github.com/Ewlbo/Instagagement/
cd Instagagement
python quickstart.py
python run.py
```

## Usage

To get started and set everything up, run 'quickstart.py'. During quickstart you will be asked for your Instagram credentials and Telegram API keys which you can generate [here](https://my.telegram.org/apps). 

There is premade program for simple operation - 'run.py'.

If you exit python program while Telegram client is open, you will block Telegram's session file. To fix it, run 'create_session.py' and change the name of session file in config file of your account. Do not re-use old session name.

The groups go into 2 main categories: those, who require you to engage with the account that you want likes on (e.g. Wolf Global) and those who dont (e.g. Boostgram). Quickstart will guide you. In first scenario you would use your main account for engagement (groups 1-25), in second scenario you would have alt account which does the engagement and posts link from main account (groups 1-8 only).

Some groups have minimum follower requirement. Use with care as currently there is nothing checking that (will add soon).

#### If you run multiple bots on 1 Telegram account:
- Do not overlap groups
- Run them in same location/folder

More details coming soon (maybe).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Did not bother to add anything, do as you wish.

> **Disclaimer**: Please Note that this is a research project. I am by no means responsible for any usage of this tool. Use on your own behalf. I'm also not responsible if your Instagram account gets banned due to extensive use of this tool. If Telethon is outdated, your Telegram account most likely will get banned, update Telethon frequently. Check your Telegram frequently to see if any engagement has been missed (happens very rarely).

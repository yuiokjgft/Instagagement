# Instagagement

Python script that automates [Telegram engagement groups](https://medium.com/@violet.emily.xoxo/inside-instagram-pods-the-secret-trick-to-increase-your-engagement-55b0d9c3cee9) for Instagram such as Wolf Global by combining Instagram bots (InstaPy and Instabot.py) and Telegram API (Telethon). Optionally you can enable function to follow Instagram profiles that have liked your competitor latest posts after which unfollow function is used (unfollows after 48h).

If you got fed up with manually engaging with posts through Telegram groups, then this is for you.

This also runs on Raspberry Pi. If I recall correctly, then it needed Python 3.7, but some features have been removed, thus 3.5 might be enough. If you wish to run this on Pi, turn off GUI that InstaPy requires in instagagement.py login function:

```
instapy = InstaPy(
  username = config['ig_username'], 
  password = config['ig_password'], 
  headless_browser = True,
  nogui = True,
  multi_logs = True
  )
```

## Features

- Intended for constant use with limited hours during the day (e.g. 6.00 to 18.00)
- Supports basic Telegram engagement groups - post amount based and time based. All the available groups are found in group_template.json, more can be added
- Takes latest links from specified Instagram profile

## Requirements

- Telegram account with created [application](https://my.telegram.org/apps) from which API hash and ID will be used
- [InstaPy](https://github.com/timgrossmann/InstaPy) for handling follow/unfollow
- [Instabot.py](https://github.com/instabot-py/instabot.py) for handling likes and finding user feed last links (finds the links from specified profile which are needed in Telegram groups for posting)
- [Telethon](https://github.com/LonamiWebs/Telethon) for handling Telegram

## Installation

Until proper package is made, download the files and install following:

```
pip install instapy
pip install instabot-py
pip install telethon
```
Should be ready to run the script.

## Usage

To get started and set everything up, run 'quickstart.py'

There is premade script for simple operation - run.py

More details coming soon.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Software is quite messy due to inexperience in Python and time constraints. Some features might be added.

## License

Did not bother to add anything, do as you wish.

> **Disclaimer**: Please Note that this is a research project. I am by no means responsible for any usage of this tool. Use on your own behalf. I'm also not responsible if your accounts get banned due to extensive use of this tool.

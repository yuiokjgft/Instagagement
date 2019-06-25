## Features to be added

#### General
- Telethon auto-update!
- ~~Check follower limit before joining group~~
- Adding groups dynamically to 'group_template.json' and 'quickstart.py'
- Fix bugs stated in README..

#### Reporting/control
- Start/stop by sending message in Telegram (either from another account or in 'Saved Messages')
- Daily report (sent to Telegram) - how many times each group was taken, which group failed etc.

#### Functionality/failsafes
- Catch the moment when there is no network (if network gets cut off mid program, session file is blocked and program throws you out)
- Arguments (silent mode, account, session name etc.)
- If blocked/banned from group - add to 'groups.json' to avoid entering the group
- ~~Check if login has been made on Instagram~~

#### Groups
- Comment groups. Example program: read comments from the post, pick one, check if it is not spam (links and spam phrases), add something and post comment (so it does not appear as spammy with pre-defined comments)
- Add functionality for groups which are doing 'rounds'


## Optional features

- Log follower count for analysis (alternative to Socialblade)
- GUI? In first phase this program was set up using PySimpleGUI, might be useful for some

## Other

- ~~Like feed posts~~
-- ~~Restrict from liking own post~~


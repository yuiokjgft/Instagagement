## Tested on:

- Raspbian Stretch Lite
- Raspberry Pi 3 Model A+ and Zero, will work on Model B/B+ as well, and might work for older ones as well

## Install

It's basically setting up Python 3.7.2 after which everything is the same as on PC. It will take time to get Python ready.

```elm
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt-get install -y git

sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
tar xf Python-3.7.2.tar.xz
cd Python-3.7.2
./configure --prefix=/usr/local/opt/python-3.7.2
make -j 4
sudo make altinstall
sudo ln -s /usr/local/opt/python-3.7.2/bin/pydoc3.7 /usr/bin/pydoc3.7
sudo ln -s /usr/local/opt/python-3.7.2/bin/python3.7 /usr/bin/python3.7
sudo ln -s /usr/local/opt/python-3.7.2/bin/python3.7m /usr/bin/python3.7m
sudo ln -s /usr/local/opt/python-3.7.2/bin/pyvenv-3.7 /usr/bin/pyvenv-3.7
sudo ln -s /usr/local/opt/python-3.7.2/bin/pip3.7 /usr/bin/pip3.7
ls /usr/bin/python*
cd ..
sudo rm -r Python-3.7.2
rm Python-3.7.2.tar.xz

sudo python3.7 -m pip install --upgrade pip

sudo python3.7 -m pip install telethon
sudo python3.7 -m pip install instabot-py==0.4.7

git clone https://github.com/Ewlbo/Instagagement/
cd Instagagement
sudo python3.7 quickstart.py
```

Optionally add 'screen' package to shutdown terminal if needed. Also 'dataplicity' could be useful for remote access.

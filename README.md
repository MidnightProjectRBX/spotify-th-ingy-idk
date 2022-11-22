# Features
 - New, minimalistic website
 - Automated upgrades
 - Customised list of countries
 - Get owner address
 - File Logging

# Instructions

1. Download [Python 3.5.4](https://www.python.org/downloads/release/python-354/) (Scroll to the bottom, where it says **Files**)
2. Edit the file that you're planning on running - either `windows.py` or `ubuntu.py`
2. Read the first few lines and modify them.
3. If you're planning on hosting the website on a domain, run this on a VPS, and change the last line of the file to `app.run(port=80, host="YOUR IP ADDRESS HERE")`
4. Open CMD or Shell and navigate to the folder.
5. Install the requirements: `python3.5 -m pip install -r requirements.txt`.
6. Run `python gen.py` and generate some tokens to give to your customers.
7. Run the right file using `python windows.py` or `python ubuntu.py`.
8. If you want a domain, setup an `A-NAME` DNS record for your domain pointing to your VPS.

# Installing Python 3.5.4 in SSH

```sudo apt-get install libssl-dev openssl
wget https://www.python.org/ftp/python/3.5.4/Python-3.5.4.tgz
tar xzvf Python-3.5.4.tgz
cd Python-3.5.4
./configure
make
sudo make install
```
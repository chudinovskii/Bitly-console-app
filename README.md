**URL shortener (URL to bitlink) and clicks counter console app**

Console app for URL to bitlink converting and counting clicks of bitlinks.

**Installation**

Python3 should be already installed. Then use pip to install dependencies:

```
pip install -r requirements.txt
```

**Usage**

It is necessary to have a Bitly Access Token. Generate it in your own Bitly account. Then put in .env file.

Create a bitlink:
```
$ main.py https://dvmn.org/
Bitlink: bit.ly/3eodNLB
```
Count the clicks:
```
$ main.py bit.ly/3eodNLB
Clicks sum: 1
```
**Project Goals**

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/)

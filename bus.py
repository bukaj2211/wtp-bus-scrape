import requests
import datetime
import bs4

# TODO 
# - line number as cli parameter
# - do not show buses thats already left
# - time interval as cli parameter

url = "https://www.wtp.waw.pl/rozklady-jazdy/"

now = datetime.datetime.now()
hour = now.hour

params = {"wtp_dt": now.strftime("%H-%M-%S"),
	"wtp_md": 5,
	"wtp_ln": 157,
	"wtp_st": 5155,
	"wtp_pt": "02",
	"wtp_dr": "B",
	"wtp_vr": 0,
	"wtp_lm": 1,
	"wtp_dy": 1}
page = requests.get(url, params=params)

soup = bs4.BeautifulSoup(page.content, 'html.parser')

ul = soup.find(attrs={"class": "timetable-line"})
lis = ul.find_all(attrs={"class": "timetable-time-hour"})

for li in lis:
    h = li.find("div", attrs={"class": "timetable-time-hour-name"})
    if h.string == str(hour) or h.string == str(hour+1):
        minutes = li.find_all("a")
        for m in minutes:
            print(m.get("aria-label")) 

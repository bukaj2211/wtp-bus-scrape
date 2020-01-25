#!/usr/bin/python3
import sys
import argparse
import requests
import datetime
import bs4

url = "https://www.wtp.waw.pl/rozklady-jazdy/"

params = {"wtp_dt": 0,
          "wtp_md": 5,
	  "wtp_ln": 157,
	  "wtp_st": 5155,
	  "wtp_pt": "02",
	  "wtp_dr": "B",
	  "wtp_vr": 0,
	  "wtp_lm": 1,
	  "wtp_dy": 1}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--line_num", help="Pass the line number (def 157)")
    parser.add_argument("-d", "--direction", help="Pass the direction: A-Żoliborz, B-Centre")
    parser.add_argument("-t", "--interval", help="The max hour difference from current time", 
                        type=int)
    args = parser.parse_args()
    
    # setup request parameters
    if args.line_num:
        params["wtp_ln"] = args.line_num
    if args.direction:
        params["wtp_dr"] = args.direction
    interval = args.interval if args.interval else 1

    now = datetime.datetime.now()
    hour = now.hour
    params["wtp_dt"] = now.strftime("%H-%M"),

    # extract the info from website
    page = requests.get(url, params=params)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    
    ul = soup.find(attrs={"class": "timetable-line"})
    lis = ul.find_all(attrs={"class": "timetable-time-hour"})
    
    time_table = []
    for li in lis:
        h = li.find("div", attrs={"class": "timetable-time-hour-name"})
        if int(hour) <= int(h.string) <= int(hour)+interval:
            minutes = li.find_all("a")
            for m in minutes:
                bus_time = m.get("aria-label")[:5]
                if now.strftime("%H:%M") < bus_time:
                    time_table.append(bus_time) 
    
    for i in time_table:
        print(i)

if __name__ == "__main__":
    main()

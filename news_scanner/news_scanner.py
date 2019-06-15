import re
import os
import requests
import urllib.request

def news_scanner():
    stringToMatch = ['Uber', 'Shravan']
    # news_line = ''
    for keyword in stringToMatch:
        with open('news.html', 'r') as file:
            for line in file:
            	if keyword in line:
                    news_line = line
                    start = 'href="'
                    end = '" target'
                    print(keyword + " : " + news_line[news_line.find(start)+len(start):news_line.rfind(end)])

news_scanner()
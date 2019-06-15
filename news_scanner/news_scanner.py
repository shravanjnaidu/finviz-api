import re
import os
import requests
import urllib.request

def download_news():
        os.system("curl https://finviz.com/news.ashx -o news.html")

def news_scanner():
    stringToMatch = ['Uber', 'Fed']
    # news_line = ''
    for keyword in stringToMatch:
        with open('news.html', 'r') as file:
            for line in file:
            	if keyword in line:
                    news_line = line
                    start = 'href="'
                    end = '" target'
                    print(keyword + " : " + news_line[news_line.find(start)+len(start):news_line.rfind(end)])

def delete_news():
        os.system("rm -rf news.html")

download_news()
news_scanner()
delete_news()
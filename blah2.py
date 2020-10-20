import csv
import time
import os
import glob
import pandas as pd
from urllib.request import Request, urlopen

home = os.getenv("HOME")
path = "./finviz-api/dailyreports"

def scrap_finviz(strategyNum, *url):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import pandas as pd
    from datetime import datetime
    import csv
    import urllib

    start_time = time.time()

    # if tuple is not empty
    if url:
        finviz_url = url[0]
        page = urlopen(finviz_url)
    # else use default url
    else:
        # input hard coded url here
        # finviz_url = "https://elite.finviz.com/screener.ashx?v=111&f=sh_curvol_o200,sh_price_u15&ft=4&o=-change&ar=10"
        finviz_url = "https://elite.finviz.com/screener.ashx?v=111&f=sh_curvol_o200,sh_price_u15&ft=4&o=-change&ar=10"
        # finviz_url = "https://finviz.com/screener.ashx?v=111&f=sh_curvol_o500,sh_price_u15&ft=4&o=-change"
        req = Request(finviz_url, headers={'User-Agent': 'Mozilla/5.0', 'username': '','password': ''})
        page = urlopen(req)

    hasNextPage = True
    firstPage = True
    # from page 2 onwards
    currentPageIndex = 0
    # collect all the text data in a list
    text_data = []

    while hasNextPage:
        if not firstPage:
            finviz_url += "&r=" + str(currentPageIndex)
            req = Request(finviz_url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req)
        soup = BeautifulSoup(page, "html.parser")

        # search all html lines containing table data about stock
        html_data = soup.find_all('td', class_="screener-body-table-nw")
        counter = 0
        for row in html_data:
            counter+= 1
            text_data.append(row.get_text())

        # toggle flag such that firstPage will be false after first run
        firstPage = False

        # advance to next page url
        if currentPageIndex == 0:
            currentPageIndex += 21
        else:
            currentPageIndex += 20
        # 220 is derrived from 20 stocks in a single page * 11 columns
        # anything lesser than 220 implies that page is not full (i.e. no next page)
        if counter < 220:
            hasNextPage = False

    # takes as input text_data array and outputs list of lists
    # each list contains information about one stock
    def helper(data):
        counter = 0
        list_of_lists = []
        temp_list = []
        for elem in data:
            # end of each stock
            if counter % 11 == 0:
                # add currently filled temp_list to list_of_lists if not empty
                if temp_list:
                    list_of_lists.append(temp_list)
                # reset to empty list
                temp_list = []
            # change from string to int for % change
            if elem[-1] == '%':
                elem = float(elem[:-1])
            temp_list.append(elem)
            counter += 1
        list_of_lists.append(temp_list)
        return list_of_lists

    stock_data = helper(text_data)
    stock_list = []
    for stock in stock_data:
        stock_list.append(stock[1])
    print(stock_list[:10])
    return stock_list[:10]
    


timestr = time.strftime("%Y-%m-%d_%H%M")
os.chdir(path)

scrap_finviz(timestr)



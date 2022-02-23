

import os
import requests
import json
import pandas as pd
import unicodedata
import pprint
import re
import matplotlib.pyplot as plt
import datetime
from words import words
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


TOKEN = os.getenv('TWIT_TOKEN')

header = {"Authorization" : f"Bearer {TOKEN}"}

#get fat string with 100 results
def search_twitter(query, bearer_token = TOKEN, max_id = None):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    max_results = "100"
    tweet_fields = "tweet.fields=text,id"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results={}".format(
        query, tweet_fields, max_results
    )
    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.content

def search_twitter_2(query, bearer_token = TOKEN, min_id = None):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    max_results = "100"
    tweet_fields = "tweet.fields=text,id"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results={}&until_id={}".format(
        query, tweet_fields, max_results, min_id
    )
    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.content

def getLowestID(str):
    res = re.findall('"id":"(\\d{19})"',str.decode("utf-8"))
    #print(f"min:",min(res))
    return min(res)

def getTweets(day, N=100):
    n = 0
    data = []
    initSearch = search_twitter(f"Wordle {day}")
    #print(initSearch)
    data.extend(parseData(initSearch,day))

    recentID = getLowestID(initSearch)
    while len(data) < N:
        newSearch = search_twitter_2(f"Wordle {day}", min_id=recentID)
        data.extend(parseData(newSearch,day))
        recentID = getLowestID(newSearch)
    #print(parseData(initSearch,day))
    #print(data)
    return data

def parseData(res, num):
    #data = res['data']
    x = re.findall(f"Wordle {num} ([1-6])/6", res.decode("utf-8")) #regex
    #print(x)
    x = list(map(int, x))
    misses = re.findall(f"Wordle {num} X/6", res.decode("utf-8")) #regex
    misses_l = [7 for miss in misses]
    x_nomiss = x
    x += misses_l
   # print(len(misses))
    #print(x)
    return x
#getTweets(243)

def printStats(data):
    print("_____STATS_____")
    print(f"Average: {sum(data)/len(data) :.2f}")
    print(f"Missed: {data.count(7)/len(data) *100:.2f}%")


def plotHist(day, dateString):
    data = getTweets(day, N=200)
    printStats(data)
    plt.hist(data, bins=7, range=(1,8))
    plt.title(f"{dateString} {words[day]}")
    plt.show()


DAY = 249

DAY1 = datetime.date(2021,6,19)
today = datetime.date.today()
delta = datetime.timedelta(days=DAY)
day = DAY1+delta #+ datetime.timedelta(days=1)
print(day)
plotHist(DAY, day.isoformat())

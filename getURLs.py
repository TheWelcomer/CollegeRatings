import requests
from faker import Faker
from lxml import html
from bs4 import BeautifulSoup
from googlesearch import search
from time import sleep
import asyncio
import grequests

with open('colleges.txt', 'r') as f, open('getURLs.txt', 'a') as r:
    colleges = f.readlines()
    for college in colleges:
        search_result_list = search(college.strip('\n') + ' niche reviews')
        URL = next(search_result_list)
        r.write(URL + '\n')
        print(URL)
        print(college.strip("\n") + " : " + "Error")
        r.write("Error" + '\n')
import requests
from faker import Faker
from lxml import html
from bs4 import BeautifulSoup
from googlesearch import search
from time import sleep
import asyncio
import grequests

fake = Faker()

async def all_parser(college):
    try:
        search_result_list = search(college.strip('\n') + ' niche reviews')
        page = await requests.get(next(search_result_list), headers={"User-Agent": fake.chrome()})
        soup = BeautifulSoup(page.content, 'html.parser')
        info = soup.find_all('div', class_='review__chart__item__total')
        for i in range(5):
            info[i] = int(info[i].get_text().strip().split(' ')[0].split('\xa0')[0])
        five_star, four_star, three_star, two_star, one_star = info
        rank = round((five_star * 5 + four_star * 4 + three_star * 3 + two_star * 2 + one_star * 1) / (five_star + four_star + three_star + two_star + one_star), 2)
        total = five_star + four_star + three_star + two_star + one_star
        print(college.strip("\n") + " : " + str(rank))
        return (college, rank, total, five_star, four_star, three_star, two_star, one_star)
    except:
        print(college.strip("\n") + " : " + "Error")
        return (college, "-1")

async def main():
    with open('colleges.txt', 'r') as f, open('result.txt', 'a') as r:
        colleges = f.readlines()
        tasks = []
        
        for college in colleges:
            tasks.append(all_parser(college))
        rankList = await asyncio.gather(*tasks)
        
        print(rankList)
        
        sorted_list = sorted(rankList, key=lambda x: x[1], reverse=True)
        for college, rank, total, five_star, four_star, three_star, two_star, one_star in sorted_list:
            r.write(college + ' ' + str(rank) + ' ' + str(total) + '\n' + str(five_star) + '; ' + str(four_star) + '; ' + str(three_star) + '; ' + str(two_star) + '; ' + str(one_star) + '\n')
            

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()
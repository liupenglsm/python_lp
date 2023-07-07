import json
import re

from Utils import *


def parse_join(soup):
    list = []
    for item in soup:
        list.append(item.string.strip())
    return ' / '.join(list)


def parse_result(soup):
    dev = soup.find(class_='subject clearfix').find(id='info')
    spanOne = dev.find('span', string='导演').next_sibling.next_sibling.find_all('a')
    spanTwo = dev.find('span', string='编剧').next_sibling.next_sibling.find_all('a')
    spanThree = dev.find('span', string='主演').next_sibling.next_sibling.find_all('a')
    spanFour = dev.find_all('span', property="v:genre")
    spanFive = dev.find('span', string=re.compile('语言')).next_sibling
    spanSix = dev.find('span', string=re.compile('片长')).next_sibling.next_sibling.string
    return {
        "director": parse_join(spanOne),
        "writer": parse_join(spanTwo),
        "start": parse_join(spanThree),
        "type": parse_join(spanFour),
        "language": spanFive.strip(),
        "time": re.match('^(\d+分钟)\S*$', spanSix.replace(' ', '').strip()).group(1),
        "test": None
    }


def handle(url):
    soup = request_soup(url)
    return parse_result(soup)


if __name__ == '__main__':
    for key, value in handle('https://movie.douban.com/subject/25662329/').items():
        if value:
            print(key + ':' + value)
        else:
            print(key + ': None')

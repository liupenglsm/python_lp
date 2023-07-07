from Utils import *
from DouBanTopDetail import handle as handleDetail
import xlwt


def parse_result(soup):
    items = soup.find(class_='grid_view').find_all('li')
    for item in items:
        link = item.find(class_='pic').find('a').get('href')

        detail = handleDetail(link)
        master = {
            'index': item.find('em').string,
            'name': item.find(class_='title').string,
            'score': item.find(class_='rating_num').string,
            'evaluate': item.find(class_='star').find_all('span')[3].string[0:-3],
            'img': item.find(class_='pic').find('img').get('src'),
            'link': item.find(class_='pic').find('a').get('href'),
            'quote': item.find(class_='inq').string if item.find(class_='inq') else '',
        }
        film = dict(**master, **detail)
        yield film




def handle(page):
    url = 'http://movie.douban.com/top250?start=' + str(page * 25) + '&filter='
    soup = request_soup(url)
    return parse_result(soup)


if __name__ == '__main__':
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    name_column = {'名称': 'name', '导演': 'director', '编剧': 'writer', '类型': 'type', '语言': 'language', '主演': 'start',
                   '时长': 'time', '评分': 'score', '评价': 'evaluate', '引用': 'quote', '头图': 'img', '链接': 'link'}

    for index, (key, value) in enumerate(name_column.items()):
        sheet.write(0, index, key)
        sheet.col(index).width = 256 * 12

    rowIndex = 1
    for i in range(0, 25):
        print('开始拉取第{}页'.format(i))
        print('进度条：', end='')
        result = handle(i)

        for item in result:
            for index, (key, value) in enumerate(name_column.items()):
                sheet.write(rowIndex, index, item[value])
            print(rowIndex, end='_')
            rowIndex += 1
        print('')

    book.save('豆瓣最受欢迎的250部电影.xlsx')

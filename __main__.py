import requests
import time
import os
import re
from apscheduler.schedulers.blocking import BlockingScheduler
from requests.exceptions import RequestException


def get_info():
    url = 'http://datanews.caixin.com/interactive/2020/pneumonia-h5/data/oversea.js'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    flag = 5
    while flag > 0:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                content = response.text
                flag = -1
                return content
        except RequestException:
            flag -= flag
    return None


def clear(content):
    """数据清洗"""
    reg = re.compile('(jQuery.*\()|\\\|\)|\n')
    content_1 = re.sub(reg, '', content)
    return content_1


def run():
    content = get_info()
    data_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    with open('res/' + data_time + '.js', 'w', encoding="UTF-8") as file:
        file.write(clear(content))


if __name__ == '__main__':
    if not os.path.exists('res'):
        os.mkdir('res')
    scheduler = BlockingScheduler()
    scheduler.add_job(run, 'interval', hours=12)
    try:
        scheduler.start()
    except(SystemExit, KeyboardInterrupt):
        pass

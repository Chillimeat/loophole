import requests
from lxml import etree
from pprint import pprint

ALL_URLS = []


def get_start_urls(url, headers):
    req = requests.get(url, headers=headers, verify=False, timeout=5)
    req.encoding = 'utf-8'
    text = req.text
    parse_html(text)
    save_json()


def parse_html(text):
    html = etree.HTML(text)
    inland_url_lst = html.xpath("""//div[@class="main-wrap"]/div/div[4]/div/div/div/div/a/@title""")
    foreign_url_lst = html.xpath("""//div[@class="main-wrap"]/div/div[5]/div/div/div/div/a/@title""")
    for inland_url in inland_url_lst:
        ALL_URLS.append(inland_url)
    for foreign_url in foreign_url_lst:
        ALL_URLS.append(foreign_url)
    # print(ALL_URLS, type(ALL_URLS))


def save_json():
    with open('urls.txt', 'w+', encoding='utf-8') as file:
        for url in ALL_URLS:
            file.write(url + '\n')


if __name__ == '__main__':
    url = "https://www.shentoushi.top/"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    get_start_urls(url, headers)

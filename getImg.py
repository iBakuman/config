import re
import string
import urllib.request
import random
import logging
import os
import time
from bs4 import BeautifulSoup
from progessBar import ShowProcess

file_handler = logging.FileHandler(os.path.join(os.getcwd(), 'log.txt'), encodings='utf-8')
logging.basicConfig(flevel=logging.INFO, handlers={file_handler})
# logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.INFO, filemode='a')


def install_opener():
    ua_pools = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36']
    cur_ua = random.choice(ua_pools)
    headers = ('User-Agent', cur_ua)
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    # 安装为全局
    urllib.request.install_opener(opener)


def save_image(src_url, save_dir=''):
    try:
        data = urllib.request.urlopen(src_url).read().decode('utf-8', 'ignore')
        pat = 'img1.wnacg.org/data/.*?.jpg'
        img_url_list = re.compile(pat).findall(data)
        count = 1
        total = len(img_url_list)
        print('Total: ' + str(total))
        process_bar = ShowProcess(total, 'OK')
        for img_url in img_url_list:
            img_url = 'http://' + img_url
            save_name = '%03d' % count + '.jpg'
            urllib.request.urlretrieve(img_url, filename=save_dir + '\\' + save_name)
            count += 1
            process_bar.show_process()
    except Exception as e:
        logging.error(e.__str__() + 'url = ' + src_url + ' in function save_image ')


def get_url_list(page_start, page_end):
    ret = {}
    for cur_page in range(page_start, page_end + 1):
        first_target = 'https://www.wnacg.org/albums-index-page-' + str(cur_page) + '-cate-9.html'
        first_data = urllib.request.urlopen(first_target).read().decode('utf-8', 'ignore')
        soup = BeautifulSoup(first_data, 'lxml')
        url_div_list = soup.find_all('div', class_='title')
        for each in url_div_list:
            try:
                tmp_url = each.a.attrs['href']
                title = each.a.attrs['title']
                # https://www.wnacg.org/photos-gallery-aid-40260.html
                act_url = 'https://www.wnacg.org' + tmp_url.replace('index', 'gallery')
                ret[title] = act_url
            except Exception as e:
                logging.error(logging.error(e.__str__() + ' in function get_url_list, cur_page = ' + str(cur_page)))
    return ret


if __name__ == '__main__':
    root_path = 'E:\\tmp\\'
    install_opener()
    url_list = get_url_list(228, 228)
    for key, value in url_list.items():
        dir_to_create = root_path + key
        if os.path.exists(dir_to_create):
            continue
        os.mkdir(dir_to_create)
        logging.info("create dir" + dir_to_create)
        print("create dir", dir_to_create)
        # 开始保存图片
        save_image(value, dir_to_create)
        # break

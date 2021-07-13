# -*- coding:utf-8 -*-
import os
import random
import ssl
import time
import urllib.request

from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
BASE_URL = "https://www.mzitu.com"
BASE_DIR = "../images"


def start_work(serial_id):
    picture_dir = BASE_DIR + os.sep + serial_id
    if not os.path.exists(picture_dir):
        os.mkdir(picture_dir)
    page_count = get_page_count(serial_id)
    print("%s 共%d个图片" % (serial_id, page_count))
    get_image_for_serial(picture_dir,serial_id,page_count)


def get_page_count(serial_id):
    header = {"user-agent": USER_AGENT}
    context = ssl._create_unverified_context()
    url = "%s/%s" % (BASE_URL, serial_id)
    req = urllib.request.Request(url, headers=header)
    resp = urllib.request.urlopen(req, context=context)
    content = resp.read()
    str_content = content.decode("utf-8")
    total_count = __get_counts(str_content)
    return total_count


def __get_counts(html_content):
    page_count = 0
    soup = BeautifulSoup(html_content, 'lxml')
    data = soup.select("body > div.main > div.content > div.pagenavi > a > span")
    if data and len(data) >= 3:
        page_count = int(data[-2].get_text())
    return page_count


def get_image_url(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    data = soup.select("body > div.main > div.content > div.main-image > p > a > img")
    url = None
    try:
        url = data[0].get("src")
    except Exception as ex:
        print("exception occur:%s" % ex)
    return url


def get_all_image_urls(serial_id, page_count):
    url_list=list()
    header = {"user-agent": USER_AGENT}
    context = ssl._create_unverified_context()
    if page_count <= 1:
        return

    for x in range(1,page_count+1):
        print("获取第%d张图片的地址" % x)
        url = "%s/%s/%s" % (BASE_URL, serial_id, x)
        req = urllib.request.Request(url, headers=header)
        resp = urllib.request.urlopen(req, context=context)
        content = resp.read()
        str_content = content.decode("utf-8")
        img_url = get_image_url(str_content)
        if img_url:
            url_list.append(img_url)
            print("第%d张图片地址是:%s" % (x, img_url))
        time.sleep(random.randint(1, 2))
    return url_list


def get_image_for_serial(dir_path, serial_id, total_count):
    for i in range(1, total_count + 1):
        print("开始获取第%d张图片" % i)
        get_image_for_index(dir_path, serial_id, i)
        sleep_seconds = random.randint(1, 10) /10
        time.sleep(sleep_seconds)


def get_image_for_index(dir_path, serial_id, page_index):
    header = {"user-agent": USER_AGENT}
    context = ssl._create_unverified_context()
    print("获取第%d张图片的地址" % page_index)
    ref_url = "%s/%s/%s" % (BASE_URL, serial_id, page_index)
    req = urllib.request.Request(ref_url, headers=header)
    resp = urllib.request.urlopen(req, context=context)
    content = resp.read()
    str_content = content.decode("utf-8")
    img_url = get_image_url(str_content)
    if img_url:
        print("第%d张图片地址是:%s" % (page_index, img_url))
        print("尝试保存图片%s" % img_url)
        save_img(dir_path, img_url, ref_url)


def save_imgs(dir_path, img_urls):
    for img_addr in img_urls:
        save_img(dir_path, img_addr)


def save_img(dir_path, img_url, ref_url):
    header = {
        "user-agent": USER_AGENT,
        "Referer": ref_url
    }
    context = ssl._create_unverified_context()
    req = urllib.request.Request(img_url, headers=header)
    resp = urllib.request.urlopen(req, context=context)
    content = resp.read()
    with open(dir_path+os.sep+img_url.split('/')[-1], 'wb') as f:
        f.write(content)
        f.close()
        print("已向目录:%s 保存文件:%s" % (dir_path, img_url.split('/')[-1]))
    time.sleep(random.randint(1, 2))


if __name__ == "__main__":
    vol_list = ["210713"]
    for serial_id in vol_list:
        start_work(serial_id)

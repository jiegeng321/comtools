#date：2020.5.25
#author:pmy
#aim:爬取google图片

from selenium import webdriver
import time
import os
import requests

import hashlib

# 使用代理的方法 ，可以直接windows使用代理，不用这么麻烦
# browserOptions = webdriver.ChromeOptions()
# browserOptions.add_argument('--proxy-server=10.57.241.119:7890')
# browser = webdriver.Chrome("/Users/td/Downloads/chromedriver",chrome_options=browserOptions)

#修改keyword便可以修改搜索关键词
keyword = '芬迪眼睛包'
save_path = "/data01/xu.fx/dataset/NEW_RAW_INCREASE_DATA/fendi_from_google/"
set_num = 1000
url = 'https://www.google.com.hk/search?q='+keyword+'&tbm=isch'


class Crawler_google_images:
    # 初始化
    def __init__(self):
        self.url = url

    # 获得Chrome驱动，并访问url
    def init_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        browser = webdriver.Chrome("/data01/xu.fx/comtools/get_img_from_google/chromedriver",chrome_options=chrome_options)
        # 访问url
        browser.get(self.url)
        # 最大化窗口，之后需要爬取窗口中所见的所有图片
        #browser.maximize_window()
        return browser
        

    #下载图片
    def download_images(self, browser,set_num=500,round=2000000):
        name = keyword
        picpath = os.path.join(save_path,name)
        # 路径不存在时创建一个
        if not os.path.exists(picpath): os.makedirs(picpath)
        # 记录下载过的图片地址，避免重复下载
        img_url_dic = []
        count = 0 #图片序号
        pos = 0
        for i in range(round):
            pos += 500
            # 向下滑动
            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            browser.execute_script(js)
            time.sleep(1)
            # 找到图片
            # html = browser.page_source#也可以抓取当前页面的html文本，然后用beautifulsoup来抓取
            #直接通过tag_name来抓取是最简单的，比较方便

            img_elements = browser.find_elements_by_tag_name('img')
            #遍历抓到的webElement
            for img_element in img_elements:
                img_url = img_element.get_attribute('src')
                # 前几个图片的url太长，不是图片的url，先过滤掉，爬后面的
                if isinstance(img_url, str):
                    if len(img_url) <= 200:
                        #将干扰的goole图标筛去
                        if 'images' in img_url:
                            #判断是否已经爬过，因为每次爬取当前窗口，或许会重复
                            #实际上这里可以修改一下，将列表只存储上一次的url，这样可以节省开销，不过我懒得写了···
                            if img_url not in img_url_dic:
                                try:
                                    img_url_dic.append(img_url)
                                    #下载并保存图片到当前目录下
                                    r = requests.get(img_url)
                                    md5_obj = hashlib.md5()
                                    md5_obj.update(r.content)
                                    hash_code = md5_obj.hexdigest()
                                    filename = os.path.join(picpath,"{}".format(hash_code) + ".jpg")

                                    with open(filename, 'wb') as f:
                                        f.write(r.content)
                                    f.close()
                                    count += 1
                                    print('this is '+str(count)+'/%s img'%set_num)
                                    if count>=set_num:
                                        return
                                    #防止反爬机制
                                    time.sleep(0.2)
                                except:
                                    print('failure')

    def run(self):
        self.__init__()
        browser = self.init_browser()
        self.download_images(browser,set_num)#可以修改爬取的页面数，基本10页是100多张图片
        browser.close()
        print("爬取完成")


if __name__ == '__main__':
    craw = Crawler_google_images()
    craw.run()

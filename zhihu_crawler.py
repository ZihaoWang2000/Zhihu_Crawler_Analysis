# -*- coding: utf-8 -*-

# 引入必要的库
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from data_admin import Database
import json
import time
import re
import random

def buffer(driver):
    for i in range(10):
        time.sleep(0.3)
        driver.execute_script('window.scrollBy(0,3000)', '')

def insert_content(data_list):
    Data_admin = Database()
    sql = 'insert into zhihu_it(question_num, question_title, is_full_video, answer_text, img_num, href_num, agree_num,' \
          'comment_num, reward_num, is_invite, is_profess, is_collect, first_post_time, last_revise_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    Data_admin.database(sql, data_list=data_list)

def get_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 前面设置的端口号
    chrome_options.add_argument("service_args = ['–ignore - ssl - errors = true', '–ssl - protocol = TLSv1']")
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)  # executable执行webdriver驱动的文件
    try:
        return driver
    except Exception as e:
        print(e)


# 得到登录的cookie
def login_cookie():
    driver = get_driver()
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    LOGIN_URL = 'https://www.zhihu.com/'
    driver.get(LOGIN_URL)
    time.sleep(5)
    input("请登录后按 Enter")
    cookies = driver.get_cookies()
    jsonCookies = json.dumps(cookies)
    #下面的文件位置需要自己改
    with open('/Users/elliott/Documents/校园/毕业论文/爬虫代码/zhihu.txt','w') as f:
        f.write(jsonCookies)
    driver.quit()

# 再次登录
def login():
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    LOGIN_URL = 'https://www.zhihu.com/'
    driver.get(LOGIN_URL)
    time.sleep(5)
    # 下面的文件位置需要自己改，与上面的改动一致
    f = open('/Users/elliott/Documents/校园/毕业论文/爬虫代码/zhihu.txt')
    cookies = f.read()
    jsonCookies = json.loads(cookies)
    for co in jsonCookies:
        driver.add_cookie(co)
    driver.refresh()
    time.sleep(5)

def isElementExist(driver,element):
    flag = True
    try:
        if element == 'a':
            driver.find_element_by_xpath('.//a[not(@class="css-1occaib")]')
        else:
            driver.find_element_by_tag_name(element)
        return flag
    except Exception as e:
        # print(e)
        flag = False
        return flag

def isFullVideo(driver):
    flag = True
    try:
        driver.find_element_by_xpath('.//div[@class="VideoAnswerPlayer"]')
        return flag
    except Exception as e:
        # print(e)
        flag = False
        return flag

def isInviteExist(driver):
    flag = True
    try:
        driver.find_element_by_xpath('.//div[@class="css-1p6warn"]')
        return flag
    except:
        flag = False
        return flag

def isProfessExist(driver):
    flag = True
    try:
        driver.find_element_by_xpath('.//a[@class="css-11028yi"]')
        return flag
    except:
        flag = False
        return flag

def isCollectExist(driver):
    flag = True
    try:
        driver.find_element_by_xpath('.//div[@class="css-1vse7nz"]')
        return flag
    except:
        flag = False
        return flag

def num_of_element(driver,element):
    try:
        if element == 'a':
            driver.find_elements_by_xpath('.//a[not(@class="css-1occaib")]')
            return len(driver.find_elements_by_xpath('.//a[not(@class="css-loccaib")]'))
        else:
            driver.find_elements_by_tag_name(element)
            return len(driver.find_elements_by_tag_name(element))
    except Exception as e:
        # print(e)
        return 0

# 爬取某问题下的所有答案
def get_answers(question_url,driver):
    driver.get(question_url)
    page = 0

    while True:
        page = page + 1
        # 滚动页面
        temp_height = 0
        while True:
            # 循环将滚动条下拉
            buffer(driver)
            # sleep一下让滚动条反应一下
            sleep = random.randint(3, 5)
            time.sleep(sleep)
            # 获取当前滚动条距离顶部的距离
            check_height = driver.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            # 如果两者相等说明到底了
            if check_height == temp_height:
                break
            temp_height = check_height

        try:
            question_xpath = '//*[@class="QuestionHeader-title"]'
            contents_xpath = '//*[@class="ContentItem AnswerItem"]'
            number = len(driver.find_elements_by_xpath(contents_xpath))

            question = driver.find_element_by_xpath(question_xpath).text
            print(question)

            answer_not_collected = []

            for k in range(number):
                data_list = []
                content_xpath = '/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[{}]/div/div'.format(k+1)
                # content_xpath = '/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div[{}]/div/div'.format(k+1)

                try:
                    element = driver.find_element_by_xpath(content_xpath)
                    agree = element.find_element_by_xpath('.//button[contains(@aria-label,"赞同")]').text
                    comment = element.find_element_by_xpath('.//button[contains(text(),"评论")]').text

                    if len(agree) != 2:  # 有赞同
                        agree_text = agree[3:]
                        if '万' in agree_text:
                            agree_nums = re.findall('[0-9]', agree_text)
                            agree_num = ''
                            for num in agree_nums:
                                agree_num = agree_num + str(num)
                            agree_num = int(agree_num) * 1000
                            num_of_agree = agree_num
                        else:
                            num_of_agree = int(agree_text)
                    else:
                        num_of_agree = 0

                    if len(comment) != 4:  # 有评论
                        comment_nums = re.findall('[0-9]', comment)
                        comment_num = ''
                        for num in comment_nums:
                            comment_num = comment_num + str(num)
                        num_of_comment = int(comment_num)
                    else:
                        num_of_comment = 0

                    try:
                        reward = element.find_element_by_xpath('.//p[@class="Reward-User-text"]').text
                        num_of_reward = reward[:-5]
                    except:
                        num_of_reward = 0

                    try:
                        label = element.find_element_by_xpath('.//div[contains(@class,"LabelContainer-wrapper")]')
                        if isInviteExist(label):
                            invite = True
                        else:
                            invite = False
                        if isProfessExist(label):
                            profess = True
                        else:
                            profess = False
                        if isCollectExist(label):
                            collect = True
                        else:
                            collect = False

                    except:
                        invite = False
                        profess = False
                        collect = False

                    if isFullVideo(element):  # 如果回答只有视频
                        video = True
                        num_of_img = 0
                        num_of_href = 0
                        first_post_time = element.find_element_by_xpath('.//span[contains(@data-tooltip,"发布于")]').get_attribute(
                            "data-tooltip")[4:]  # 发布回答的时间
                        last_revise_time = element.find_element_by_xpath('.//span[contains(@data-tooltip,"发布于")]').text[4:]  # 最后修改回答的时间

                        try:
                            answer = element.find_element_by_xpath('.//span[contains(@class,"RichText")]').text
                        except:
                            answer = ''

                    else:  # 回答不包括视频
                        video = False
                        element2 = element.find_element_by_xpath('.//span[contains(@class,"RichText")]')
                        answer = element2.text
                        first_post_time = element.find_element_by_xpath('.//span[contains(@data-tooltip,"发布于")]').get_attribute(
                            "data-tooltip")[4:]  # 发布回答的时间
                        last_revise_time = element.find_element_by_xpath('.//span[contains(@data-tooltip,"发布于")]').text[4:]  # 最后修改回答的时间

                        # 获取单个答案图片的个数
                        if isElementExist(element2,'img'):
                            num_of_img = num_of_element(element2,'img')
                        else:
                            num_of_img = 0

                        # 获取单个答案链接的个数
                        if isElementExist(element2, 'a'):
                            num_of_href = num_of_element(element2, 'a')
                        else:
                            num_of_href = 0

                    print('answer ' + str(k+1) + ' collected in page ' + str(page))
                    # print('视频：' + str(video))
                    # print('图片数：' + str(num_of_img), '链接数：' + str(num_of_href))
                    # print('赞同数：' + str(num_of_agree), '评论数：' + str(num_of_comment), '赞赏数：' + str(num_of_reward))
                    # print('邀请：' + str(invite), '专业：' + str(profess), '收录：'+ str(collect))
                    # print('发布时间：' + first_post_time, '修改时间：' + last_revise_time)
                    data_list.append((10, question, video, answer, num_of_img, num_of_href, num_of_agree, num_of_comment, num_of_reward, invite, profess, collect, first_post_time, last_revise_time))
                    insert_content(data_list)
                    time.sleep(1)

                except Exception as e:
                    print(e)
                    print('answer ' + str(k+1) + ' not collected in page ' + str(page))
                    answer_not_collected.append(k+1)
                    continue

            print('There are ' + str(len(answer_not_collected)) + ' answers not collected in page ' + str(page) + '! That is:')
            print(answer_not_collected)
            driver.find_element_by_xpath('//button[contains(@class,"PaginationButton-next")]').click()
            time.sleep(5)
            driver.refresh()
            time.sleep(5)

        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    # 设置你想要搜索的问题
    question_url = 'https://www.zhihu.com/question/24369601/answers' + '/updated?page=21'
    # login_cookie()
    driver = get_driver()
    # login()
    get_answers(question_url,driver)


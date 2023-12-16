from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from lxml.html import etree
from PIL import Image
from time import sleep
import re, requests
from urllib.request import urlretrieve
from bs4 import BeautifulSoup


def get_move_track(gap):
    track = []  # 移动轨迹
    current = 0  # 当前位移
    # 减速阈值
    mid = gap * 4 / 5  # 前4/5段加速 后1/5段减速
    t = 0.2  # 计算间隔
    v = 0  # 初速度
    while current < gap:
        if current < mid:
            a = 3  # 加速度为+3
        else:
            a = -3  # 加速度为-3
        v0 = v  # 初速度v0
        v = v0 + a * t  # 当前速度
        move = v0 * t + 1 / 2 * a * t * t  # 移动距离
        current += move  # 当前位移
        track.append(round(move))  # 加入轨迹
    return track


chrome_options = Options()  # 以后就可以设置无界面
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('blink-settings=imagesEnabled=false')
# prefs = {'profile.managed_default_content_settings.images': 2}
# chrome_options.add_experimental_option('prefs', prefs)

chromedriverPath = "F:\\Anaconda3\\Scripts\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriverPath)
driver.get("https://www.zhihu.com/signin?next=%2F,html")

driver.find_element(By.XPATH,
                    '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[1]/div[2]').click()
driver.find_element(By.XPATH, '//input[@name="username"]').send_keys("18361264919")
driver.find_element(By.XPATH, '//input[@name="password"]').send_keys("s374857303")
sleep(0.2)
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
sleep(2)
# /html/body/div[4]/iframe
fr = driver.find_element_by_tag_name("iframe")

# 切换iframe
driver.switch_to.frame(fr)
#
# # 获取滑动的箭头
#
ss = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div/div[1]/span[2]").text()
print(ss)
element = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/div[2]")
# # 拖住箭头
ActionChains(driver).click_and_hold(on_element=element).perform()
ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=157, yoffset=0).perform()
#
# tracks = get_move_track(50)
# for track in tracks:
#     ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
#
# sleep(0.8)
# ActionChains(driver).release().perform()


def get_geetest_image(self):  # 获取验证码图片
    # print(self.driver.page_source)
    gapimg = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
    sleep(2)
    gapimg.screenshot(r'./captcha1.png')  # 将class为geetest_canvas_bg的区域截屏保存
    # 通过js代码修改标签样式 显示图片2
    js = 'var change = document.getElementsByClassName("geetest_canvas_fullbg");change[0].style = "display:block;"'
    self.driver.execute_script(js)
    sleep(2)
    fullimg = self.wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_fullbg')))
    fullimg.screenshot(r'./captcha2.png')  # 将class为geetest_canvas_fullbg的区域截屏保存

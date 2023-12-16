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

from urllib import request
import cv2


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


def get_pos(imageSrc):
    img = cv2.imread(imageSrc)
    blurred = cv2.GaussianBlur(img, (5, 5), 0, 0)
    canny = cv2.Canny(blurred, 0, 100)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if 28 < area < 32:
        # 画出红色的矩形
            return x
            print(area)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imwrite('11.jpg', img)
        zhongchang = cv2.arcLength(contour, True)
        # 边长160的正方形 155，165
        if 24025 < area < 27225 and 620 < zhongchang < 660:
            # 要填的小矩形的坐标
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.imwrite('111.jpg',img)
            return x
    return 0



chrome_options = Options()  # 以后就可以设置无界面
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

chromedriverPath = "F:\\Anaconda3\\Scripts\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriverPath)
driver.get("https://accounts.douban.com/passport/login")

driver.find_element(By.XPATH,
                    '//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click()
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys("18361264919")
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("Ss374857303!")
sleep(1)
driver.find_element(By.XPATH, '//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click()

# ele = driver.find_elements_by_xpath('/html/body/div[4]/iframe')
# ele2 = driver.find_elements(By.TAG_NAME, "iframe")
# 重新获取页面
#
sleep(3)
driver.switch_to.frame(0)
# //*[@id="tcOperation"]/div[6]
# 获取滑动的箭头

element = driver.find_element(By.XPATH, '//*[@id="tcOperation"]/div[6]')

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'slideBg')))
bigImg = driver.find_element(By.ID, 'slideBg')
s = bigImg.get_attribute('style')
# print(s)
p = 'background-image: url\(\"(.*?)\"\);'
bigImgSrc = re.findall(p, s, re.S)[0]
if bigImgSrc.find("https")==-1:
    bigImgSrc = "https://t/captcha.qq.com"+bigImgSrc
# # print(bigImgSrc)
# # 得到大图片，保存到当前路径下
request.urlretrieve(bigImgSrc, '../bigImage.png')
dis = get_pos()
print(get_pos('bigImage.png'))















# 拖住箭头
# ActionChains(driver).click_and_hold(on_element=element).perform()
# ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=107, yoffset=0).perform()
#
# tracks = get_move_track(40)
# for track in tracks:
#     ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
#
# sleep(0.8)
# ActionChains(driver).release().perform()

"""
 " Created by PyCharm.
 " User: Devmc
 " Date: 2021/10/12
 " Time: 09:48
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import os

# 参数
# 用户名
USERNAME = "czq0320"
# 密码
PASSWORD = "czq0320"
# 要上传文件的路径
UPLOAD_PATH = r"F:\Projects\A-Outer\20210924-igem-AlphaLuco-13\resources\1-3 2个页面\MODEL"
# （不用修改）
UPLOAD_PATH = UPLOAD_PATH + r"\\"

# 配置
# 登录地址
LOGIN_URL = "https://igem.org/Login2"
# 上传地址
UPLOAD_URL = "https://2021.igem.org/Special:Upload"
# chrome位置（避免找不到Chrome Dev/Canary）
# CHROME_PATH = None
CHROME_PATH = r"C:\Program Files\Google\Chrome Dev\Application\chrome.exe"
# chromedriver位置
CHROMEDRIVER_PATH = r"chromedriver.exe"
# 文件类型
FILE_EXTENSION = {'.jpg', '.jpeg', '.png', '.mp4'}


def start():
    # 设置浏览器路径，避免找不到Chrome Dev等
    options = Options()
    if CHROME_PATH:
        options.binary_location = CHROME_PATH
    # 初始化driver
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

    # 登录
    driver.get(LOGIN_URL)
    login_account = driver.find_element_by_name("username")
    login_account.send_keys(USERNAME)
    login_password = driver.find_element_by_name("password")
    login_password.send_keys(PASSWORD)
    login_password = driver.find_element_by_name("Login")
    login_password.click()
    # 账号或密码错误
    while True:
        try:
            driver.find_element_by_id("login_error")
            print("账号或密码错误！")
            return
        except:
            break

    # 上传
    num = 0
    # 循环每个文件
    for item in os.listdir(UPLOAD_PATH):
        file_path = UPLOAD_PATH + item
        file_extension = os.path.splitext(file_path)[1]

        if file_extension.lower() in FILE_EXTENSION:
            # 打开地址
            driver.get(UPLOAD_URL)

            driver.find_element_by_id('wpUploadFile').send_keys(file_path)
            driver.find_element_by_id('wpDestFile').send_keys(item)
            driver.find_element_by_name("wpUpload").click()

            while True:
                try:
                    ignore = driver.find_element_by_name("wpUploadIgnoreWarning")
                    ignore.click()
                    break
                except:
                    break

            while True:
                try:
                    href = driver.find_element_by_css_selector(".filehistory-selected a")
                    print(href.get_attribute("href"))
                    num += 1
                    break
                except:
                    sleep(1)

    driver.quit()
    print("共上传了%d个文件！" % num)


start()

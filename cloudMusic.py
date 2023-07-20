import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # 修改这里

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait




def getMusicId(searchName):
    option = webdriver.ChromeOptions()
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/{}"
                        " (XHTML, like Gecko) Chrome/115.0.5790.98 Safari/{}")
    option.add_argument('headless')  # 设置option
    # 去除图片及css样式
    prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    option.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=option)  # 调用带参数的谷歌浏览器
    print('开始获取音乐id')
    try:
        url = 'https://music.163.com/#/search/m/?s=' + searchName
        driver.get(url)
        # time.sleep(1)
        # driver.switch_to.frame(0)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "contentFrame")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        row = soup.find_all("a", {"class": "ply"})[0].get('id')
        id = row.split('song_')[1]
        print(id)
        lyc = getMusicLyc(id,driver)
        return lyc
    except Exception as e:
        driver.quit()
        print('except:', e)
        return '歌曲id获取失败，请检查转发格式'

def getMusicLyc(musicId,driver):
    print('开始获取歌词')
    lyc_url = "https://music.163.com/#/song?id=" + musicId  # 根据歌曲的 ID 号拼接出下载的链接。歌曲直链获取的方法参考文前的注释部分。
    try:
        driver.get(lyc_url)
        # time.sleep(1)
        # driver.switch_to.frame(0)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "contentFrame")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for linebreak in soup.find_all('br'):
            linebreak.replace_with('\n\n')
        row = soup.find("div", {"id": "lyric-content"}).text
        lyc = row[0:len(row) - 2]
        print(lyc)
        return lyc
    except Exception as e:
        print('except:', e)
        return '歌词获取失败，请检查转发格式'
    finally:
        driver.quit()


# 测试使用
if __name__ == '__main__':
    MusicId = getMusicId('修炼爱情')

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # 修改这里

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait


# 根据搜索结果 获取歌曲id
def getMusicId(searchName, singer):
    if len(searchName) > 20:
        searchName = searchName[0:20]
    print(searchName)
    print(singer)
    option = webdriver.ChromeOptions()
    # 伪造请求头
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/{}"
                        " (XHTML, like Gecko) Chrome/115.0.5790.98 Safari/{}")
    # 隐藏浏览器窗口
    option.add_argument('headless')
    # 去除图片及css样式
    prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    option.add_experimental_option("prefs", prefs)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    # 调用带参数的谷歌浏览器
    driver = webdriver.Chrome(options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})

    print('开始获取音乐id')
    try:
        url = 'https://music.163.com/#/search/m/?s=' + searchName + '&type=1'
        driver.get(url)
        print(url)
        wait = WebDriverWait(driver, 1)
        # 切换到name =  contentFrame  的iframe中
        try:
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "contentFrame")))
        except TimeoutException:
            print("等待 iframe 超时，尝试重新加载页面")
            driver.refresh()
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "contentFrame")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        div_tags = soup.find_all('div', {'class': 'td w1'})
        # 是否为多歌手标识
        singers = singer.split('&')
        print(singers)
        isMoreSinger = False
        if len(singers) > 1:
            isMoreSinger = True
        # 比对歌手正确标识
        found = False
        # 索引标记
        index = 0
        for div in div_tags:
            if found:
                break
            text_div = div.find('div', {'class': 'text'})
            a_tags = text_div.find_all('a')
            print(a_tags)
            if a_tags is not None:
                i = 0
                for a in a_tags:
                    if isMoreSinger:
                        if a.text == singers[i]:
                            if i == len(singers)-1:
                                print("比对所有歌手完成")
                                # 修改标识以退出循环
                                found = True
                                break
                    i = i + 1
                    if not isMoreSinger:
                        if a.text == singer:
                            # 修改标识以退出循环
                            found = True
                            break
                        else:
                            index = index + 1
            else:
                if text_div.text == singer:
                    # 修改标识以退出循环
                    found = True
                    break
                else:
                    index = index + 1
        print(index)
        if index >= 20:
            return "网易云  只让我加载前20首 懒加载规则搞不懂 我是彩笔  我搞不定了"
        # 获取索引标记的id
        row = soup.find_all("a", {"class": "ply"})[index].get('id')
        id = row.split('song_')[1]
        print("歌曲id为： " + id)
        lyc = getMusicLyc(id, driver)
        return lyc
    except Exception as e:
        driver.quit()
        print('except:', e)
        return '歌曲id获取失败，请检查转发格式'


# 根据Id获取歌词
def getMusicLyc(musicId, driver):
    print('开始获取歌词')
    lyc_url = "https://music.163.com/#/song?id=" + musicId  # 根据歌曲的 ID 号拼接出下载的链接。歌曲直链获取的方法参考文前的注释部分。
    try:
        driver.get(lyc_url)
        wait = WebDriverWait(driver, 10)
        # 切换到name =  contentFrame  的iframe中
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "contentFrame")))
        # 获取网页元素
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # 替换 换行符
        for linebreak in soup.find_all('br'):
            linebreak.replace_with('\n\n')
        # 获取第一个id为lyric-content的div中的文本内容
        row = soup.find("div", {"id": "lyric-content"}).text
        # 去掉 歌词中带有的‘展开’
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
    MusicId = getMusicId('张韶涵&王赫野 篇章', '张韶涵&王赫野')

# Tutorial of PTT crawler
by slv ([Salas leVirve@Github](https://github.com/leVirve))
*Update: 2016/09/28*

＜Intro to crawler＞：
[Crawler / Spider](crawling.md) *Not complete yet...* :joy:

＜Python 實際演練＞：
在網路上養了一隻蟲，以下就用 PTT 的電影版文章作為我們的爬蟲目標囉！

# 相依套件
首先使用 `pip` 來安裝套件，
- `requests` 發送接收 HTTP 請求及回應
    - 官方標語：`HTTP for Humans`，這才是真正給人用的介面啊，建議不要直接使用內建的 `urllib` 模組！
- `beautifulsoup` 用來分析與抓取 html 中的元素
    - 簡單好用，沒有嚴格要求解析速度的話是個很好的選擇。

```bash
pip install requests
pip install beautifulsoup4
```
- (選用) `lxml` 用來解析 html/xml
    - 簡單好用(?)，解析速度快多了！不過想要直接透過 lxml 解需要先熟悉 `xpath` 語法，其實也挺容易學的～
    - 可在這邊找到好心人預編譯好的 wheel for Windows ([Unofficial pre-compiled lxml](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml))

```bash
# install through pip but need compile
pip install lxml

# if you have conda, congrats!
conda install lxml

# if on debain/ubuntu, you may install binary directly...
sudo apt-get install python3-lxml

# if on windows, install from lxml wheel
pip install lxml-3.6.4-cp35-cp35m-win_amd64.whl
```
# 第一步：所看即所抓
*What you see is what you retrieve, but all in text!*

使用 `requests.get()` 函式仿造 HTTP GET 方法來「瀏覽」網頁，並取得網址中的內容。
回傳結果是一個 `requests.Response` 包裝起來的物件，而我們現在的目標是取得頁面原始碼即可；而網頁原始碼就在 `response.text` 中。

```python
import requests

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)

print(response.text)  # result of setp-1
```

# 第二步：說說看你看到了什麼？
*Interpretate the retrieved text like a browser*

一版情況下瀏覽器拿到了網頁原始碼之後，會先解析然後把畫面顯示成我們平常看見的樣子；但這邊我們並不做顯示只想分析原始碼內的資訊。所以用 `Beautifulsoup` 來分析剛剛抓到的文字，在 `BeautifulSoup()` 的建構式第二個參數放入 `'lxml'` 讓他使用我們剛剛安裝的 lxml 來解析。
(p.s. 若剛剛未選擇安裝 `lxml`，則用 Python 內建的 `html.parser` 解析即可。)

而藉由我們打開瀏覽器查看網頁原始碼 (可用`F12` 開發者工具) 得知 PTT 網頁版中，每一篇文章的標題訊息皆放在 `class="r-ent"` 的 `div` 標籤裡。這裡我們使用到 `find_all()` 方法來操作 `BeautifulSoup` 物件並指定尋找目標，找到之後的結果是一串文章列表資訊。

```python
import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('div', 'r-ent')

print(articles)  # result of setp-2
```

# 第三步：所以我說那個標題資訊呢？
*Hey, here's some meta data*

剛剛說過 `find_all()` 回傳符合的結果，而這串結果是個 `list` 型態的東西，所以我們用 `for loop` 來一個一個印出來看看。

而因為 html 本來就是具有階層式的標記語言，所有的資料都是用 `觀察法` 判斷到底放在哪個標籤哪一階層裡，以下就不多加贅述！
示範內容抓出：推文數、標題名稱、作者、發文日期和文章網址。

```python
import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('div', 'r-ent')

for article in articles:
    meta = article.find('div', 'title').find('a')

    title = meta.getText().strip()
    link = meta.get('href')
    push = article.find('div', 'nrec').getText()
    date = article.find('div', 'date').getText()
    author = article.find('div', 'author').getText()

    print(push, title, date, author)  # result of setp-3
```

#### 執行結果 (此圖輸出經過特殊處理)
![crawler_3_snap](https://raw.github.com/leVirve/CrawlerTutorial/master/crawler_3_snap.png)

*特殊處理：* 沒事多寫點程式碼啊！把天賦通通點在美化上吧～

把這段程式碼貼到剛剛的 `crawler_3.py` 裡，並把 `print` 換成 `pretty_print`。漂亮的輸出就出現囉！

``` python
widths = [
        (126,    1), (159,    0), (687,     1), (710,   0), (711,   1),
        (727,    0), (733,    1), (879,     0), (1154,  1), (1161,  0),
        (4347,   1), (4447,   2), (7467,    1), (7521,  0), (8369,  1),
        (8426,   0), (9000,   1), (9002,    2), (11021, 1), (12350, 2),
        (12351,  1), (12438,  2), (12442,   0), (19893, 2), (19967, 1),
        (55203,  2), (63743,  1), (64106,   2), (65039, 1), (65059, 0),
        (65131,  2), (65279,  1), (65376,   2), (65500, 1), (65510, 2),
        (120831, 1), (262141, 2), (1114109, 1),
]


def calc_len(string):
    def chr_width(o):
        global widths
        if o == 0xe or o == 0xf:
            return 0
        for num, wid in widths:
            if o <= num:
                return wid
        return 1
    return sum(chr_width(ord(c)) for c in string)


def pretty_print(push, title, date, author):
    pattern = '%3s\t%s%s%s\t%s'
    padding = ' ' * (50 - calc_len(title))
    print(pattern % (push, title, padding, date, author))

```

# 第四步：現在 Data 分析時代欸，給我資料！
*Give me data!*

好，那就再用 `觀察法` 模式，去找找上一頁的連結在哪裡？
找到了嗎？不是問你頁面上的按鈕在哪裡喔！是看原始碼啊，同學！
相信都有發現了，關於頁面跳轉的超連結就放在 `<div class='btn-group-paging'>` 的 `<a class='btn'>` 裡，所以我們可以像這樣抓到他們：

```python
# 控制頁面選項: 最舊/上頁/下頁/最新
controls = soup.find('div', 'btn-group-paging').find_all('a', 'btn')
```

而我們需要的是`上一頁`的功能，為什麼呢？因為 PTT 是最新的文章顯示在前面啊～所以要挖資料必須往前翻。

那怎麼使用呢？先去抓出 `control` 中第二個(index: [1])的 `href`，然後他可能長這樣 `/bbs/movie/index3237.html`；而完整的網址(URL)必須要有 `https://www.ptt.cc/` 開頭，所以用 `urljoin()` 把 Movie 首頁連結和新的 link 比對合併成完整的 URL！

```python
link = controls[1].get('href')
page_url = urllib.parse.urljoin(INDEX, link)
```


另外，或許會發現怎麼前面的程式有時候會出錯啊？！看看網頁版發現原來當該頁面中有文章被刪除時，網頁上的 `＜本文已被刪除＞` 這個元素的原始碼 `結構` 和原本不一樣哇！所以我們用 `BeautifulSoup` 生一個 `<a>` 元素來替代，方便後面存取時使用 (避免 title 和 link 的地方對 `None` 存取，產生上述提到的錯誤)。

```python

NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

...

# meta = A or B，當前面 A 的 .find() 抓到的是空的，則讓 meta 等於 B
meta = article.find('div', 'title').find('a') or NOT_EXIST
```

現在我們將函式重新定義，讓：
- `get_posts_on_page(url)`:
抓取一頁中所有的文章的 metadata (很潮的`後設資料`)，並回傳一串 `key-value` 類型的資料，以及前一頁的 link。
- `get_pages(num)`:
抓取最新的 N 個頁面，並指派 `get_posts_on_page` 去抓每頁面中的資料，把每一串資料合併成一大串後回傳。

```python
# 每筆資料長這樣子，dict() 類型資料：key-value pairs data
{
    'title': meta.getText().strip(),
    'link': meta.get('href'),
    'push': article.find('div', 'nrec').getText(),
    'date': article.find('div', 'date').getText(),
    'author': article.find('div', 'author').getText(),
}
```

而 `get_posts_on_page(url)` 和 `get_pages(num)` 回傳的就是這樣的一串資料：
```python
[
{'push': '4', 'link': '/bbs/movie/M.1441633354.A.961.html', 'title': '[新聞] 侯孝賢：「一個導演，沒有自覺，就不用玩', 'date': ' 9/07', 'author': 'soulx'},
{'push': '', 'link': '/bbs/movie/M.1441636396.A.D64.html', 'title': '[請益] 倖存者（The Remaining)的結局', 'date': ' 9/07', 'author': 'Takuri'},
{'push': '', 'link': None, 'title': '本文已被刪除', 'date': ' 9/07', 'author': '-'},
{'push': '1', 'link': '/bbs/movie/M.1441637098.A.854.html', 'title': '[好雷] Hero電影版', 'date': ' 9/07', 'author': 'peichuan'},
{'push': '', 'link': '/bbs/movie/M.1441637150.A.DA1.html', 'title': '[新聞] 「夢想海洋」主題曲 魏德聖王大陸力挺', 'date': ' 9/07', 'author': 'fireguard119'},
{'push': '', 'link': '/bbs/movie/M.1441637513.A.14E.html', 'title': '[贈票] 未知之境 餘鬼狂歡～2015女性影展特映會', 'date': ' 9/07', 'author': 'epmt'},
{'push': '', 'link': '/bbs/movie/M.1441637531.A.E5A.html', 'title': '[問片] 問幾部港片/國片', 'date': ' 9/07', 'author': 'ogcxd'},
...
]
```


附上**crawler_4.py 完整程式碼**

另外要說明的是 `from utils import pretty_print`，把剛剛 **crawler_3.py** 那個漂亮的輸出功能數十行的程式碼放到同目錄底下的新檔案 `utils.py` 中(檔案名字你喜歡就好，只要記得 `from xxx import pretty_print` 要記得一起改)，然後在這邊 `import`(相當於 C語言中的 include )就能繼續沿用功能！

```python
import requests
import urllib.parse
from bs4 import BeautifulSoup

from utils import pretty_print

INDEX = 'https://www.ptt.cc/bbs/movie/index.html'
NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a


def get_posts_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    posts = list()
    for article in soup.find_all('div', 'r-ent'):
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        posts.append({
            'title': meta.getText().strip(),
            'link': meta.get('href'),
            'push': article.find('div', 'nrec').getText(),
            'date': article.find('div', 'date').getText(),
            'author': article.find('div', 'author').getText(),
        })

    next_link = soup.find('div', 'btn-group-paging').find_all('a', 'btn')[1].get('href')

    return posts, next_link


def get_pages(num):
    page_url = INDEX
    all_posts = list()
    for i in range(num):
        posts, link = get_posts_on_page(page_url)
        all_posts += posts
        page_url = urllib.parse.urljoin(INDEX, link)
    return all_posts



if __name__ == '__main__':
    pages = 5

    for post in get_pages(pages):
        pretty_print(post['push'], post['title'], post['date'], post['author'])

```

**上面的程式碼都在 `src/` 中可以找到！**

以上就是基本的爬蟲入門教學～

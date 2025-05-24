---
marp: true
theme: uncover
class: invert
---

# Python x Gradio

日文五十音大進擊 Day 2

[Colab Demo](https://colab.research.google.com/drive/1zOCkEO-rrN-AQNmslQZn4G27_zFvcMVQ)

---

## Python `with` 語法

----

### `with A as B:`

這是一種**上下文管理器 (Context Manager)** 語法
表示基於 A 的狀態下，進行某些行為
B 則是 A 的變數名稱

----

將 18 歲的 Person 命名為「高中生」
高中生會做以下這些事情：

```python
with Person(age=18) as 高中生:
    高中生.玩社團()
    高中生.談戀愛()
    高中生.唸書()
    高中生.考試()
    # ... AwA
```

----

將 28 歲的 Person 命名為「社畜」
社畜會做以下這些事情：

```python
with Person(age=28) as 社畜:
    社畜.找工作()
    社畜.賺錢()
    社畜.買房買車()
    社畜.結婚生小孩()
    # ... QAQ
```

---

## 使用 Gradio Blocks

----

### 元件宣告

將 `gr.Blocks()` 命名為 `app`
並且在 Blocks 裡面依序放入以下元件：

```python
with gr.Blocks() as app:
    name_text = gr.Textbox(label="名字")
    greet_btn = gr.Button("問候")
    farewell_btn = gr.Button("道別")
    message = gr.Textbox(label="訊息")
```

----

### 函式宣告

其實函式是不用宣告在 Blocks 裡面的

```python
def greet_fn(name):
    return f"{name}，你好！"

def farewell_fn(name):
    return f"{name}，再見！"

with gr.Blocks() as app:
    # ...
```

----

### 註冊事件

```python
# ... 函式宣告

with gr.Blocks() as app:
    # ... 元件宣告

    greet_btn.click(greet_fn, name_text, message)
    farewell_btn.click(farewell_fn, name_text, message)
```

----

```python
greet_btn.click(greet_fn, name_text, message)
```

當 `greet_btn` 被按下 (`click`) 時執行 `greet_fn` 函式
並且把 `name_text` 的內容傳入該函式
最後把該函式的輸出放到 `message` 裡面

----

### 處理多個輸入

```python
def greet_fn(name, n):
    return f"{name}，你好" + "！" * n

# ... 函式宣告

with gr.Blocks() as app:
    name_text = gr.Textbox(label="名字")
    num = gr.Number(label="驚嘆號數量")
    # ... 元件宣告

    greet_btn.click(greet_fn, [name_text, num], message)
    farewell_btn.click(farewell_fn, [name_text, num], message)

app.launch()
```

將輸入元件們以列表形式傳入

----

### 元件參數

- `gr.Number()` 有很多花花綠綠的參數可以修飾
  - `value` 為一開始呈現在網頁上的預設值
  - `minimum` 為使用者可以設定的最小值
  - `maximum` 為使用者可以設定的最大值
  - `step` 為每次調整的間距

```python
gr.Number(label="驚嘆號數量", value=10, minimum=5, maximum=50, step=5)
```

----

### 裝飾參數

- 其他元件也有很多參數可以設定：
  - `gr.Textbox()` 可以給 `placeholder` 提示訊息
  - `gr.Button()` 可以給 `icon` 設定按鈕圖案
  - 也能用 Emoji 直接在字串上做裝飾

----

### 打造花花綠綠的介面！

```python
with gr.Blocks() as app:
    name_text = gr.Textbox(label="😀 名字", placeholder="請輸入名字")
    num = gr.Number(label="⚠️ 驚嘆號數量", minimum=5, maximum=50, step=5, value=10)
    greet_btn = gr.Button("問候", icon="cherry-blossom.png")
    farewell_btn = gr.Button("道別", icon="tree.png")
    message = gr.Textbox(label="🗨️ 訊息")
```

---

## 版面配置

----

當我們想將兩個元件並排時
可以使用 `gr.Row()`

----

原本會由上而下排列：

```python
with gr.Blocks() as app:
    gr.Button("上面")
    gr.Button("下面")
    gr.Button("更下面")
```

----

在 `gr.Row()` 裡面會由左而右排列：

```python
with gr.Blocks() as app:
    with gr.Row():
        gr.Button("左邊")
        gr.Button("右邊")
    gr.Button("下面")
```

---

## Radio & Checkbox

----

透過 `gr.Radio()` 建立多個單選按鈕
透過 `gr.Checkbox()` 建立**單個**多選方塊
透過 `gr.CheckboxGroup()` 建立多個多選方塊

![Radio & Checkbox](https://i.imgur.com/zF8gbPy.png)

----

透過 `gr.Radio()` 元件
來改造溫度單位換算的應用

![Temperature Conversion with Radio](https://i.imgur.com/RFFNHOL.png)

----

### 密碼產生器

由使用者指定密碼長度
產生大小寫英文字母、數字或符號夾雜的一串密碼

可以透過 `random` 與 `string` 兩個內建套件來完成

----

### 概念驗證

----

在 `string` 套件底下，有預先定義好的字串

```python
import string

print(string.ascii_lowercase)  # 小寫 abcdefghijklmnopqrstuvwxyz
print(string.ascii_uppercase)  # 大寫 ABCDEFGHIJKLMNOPQRSTUVWXYZ
print(string.digits)           # 數字 0123456789
print(string.punctuation)      # 符號 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
```

----

透過字串加法將可能的字母串接起來

```python
candidates = ""
candidates += string.ascii_lowercase
candidates += string.ascii_uppercase
candidates += string.digits
candidates += string.punctuation  # Optional
```

----

透過 `random` 套件的 `choice()` 函式來隨機挑選字母

```python
import random

random.choice("abcde")
```

----

結合 `string` 與 `random.choice()` 來挑選字母

```python
random.choice(string.ascii_lowercase)
```

----

寫一個 `for` 迴圈來隨機挑選多個字母

```python
p = ""
for i in range(8):
    ch = random.choice(candidates)
    p += ch
print(p)
```

----

### 完整應用

----

透過 `gr.Checkbox()` 元件來建立密碼產生器

![Password Generator with Checkbox](https://i.imgur.com/NirZHIw.png)

----

### 進階寫法

----

透過 `gr.CheckboxGroup()` 元件
來精簡密碼產生器的寫法

![Password Generator with CheckboxGroup](https://i.imgur.com/UgXtQiZ.png)

<!--
To-Do List:
    - complex application => many variables, many functions
        - refactor as a class is more suitable
    - day 3 guess number => require state
    - day 3 case study - lyrics demo
-->

<style>
h1, h2, h3, h4, h5, h6 { color: #9AD; }
a {color: #9AD}
</style>

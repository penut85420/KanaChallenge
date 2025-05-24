---
marp: true
theme: uncover
class: invert
---

# Python x Gradio

日文五十音大進擊 Day 1

[Colab Demo](https://colab.research.google.com/drive/18kQcVKZRlnAMa4956wYljmUdW_R-NbU8)

---

## Python

[延伸閱讀：為什麼要學 Python 呢？](https://ithelp.ithome.com.tw/articles/10352210)

----

寫 Python 的方式主要分成兩種
**Notebook** & **Script**

----

**Notebook** 通常為 `.ipynb` 檔
可以拆解程式碼、逐步執行

混合搭配文件說明，適合報告與教學
但執行順序、版本控制是個問題

----

**Script** 通常為 `.py` 檔
適合版本控制
但除錯、反覆的細部測試較不容易

----

面對不熟悉的程式碼

先在 Notebook 探索基本用法
再整理成 Script 做系統化管理

---

## 開發環境

----

推薦 [Colab](https://colab.research.google.com/) 或 [Replit](https://replit.com)

Colab 為 Notebook
Replit 可以寫 Script

----

### Notebook 的構成元素

程式碼區塊 Code Cell
文件區塊 Markdown Cell
輸出區域 Output
執行核心 Kernel

貓貓、狗狗、螃蟹、爆炸（？

----

### 安裝 Gradio

在 Cell 內輸入 `%pip install gradio`
然後按下 `Ctrl + Enter` 執行安裝

延伸知識：什麼是 `%pip`？

---

## Gradio

----

### Gradio History

Gradio 是一份於 2019 年創立專案
由 Stanford 的 PhD Abubakar Abid 與室友們一同開發
在 2021 年 12 月加入 Hugging Face 家族

透過簡單的 Python 程式碼
就可以快速搭建一個簡潔的網頁小應用
讓使用者易於展示與操作

----

### 撰寫打招呼函式

```python
def greet(name, n):
    return "你好，" + name + "！" * n
```

----

### 原本我們這樣測試⋯

```python
def greet(name, n):
    return "你好，" + name + "！" * n

print(greet("花生", 3))
print(greet("土豆", 5))
```

----

### 這樣測試怎麼了？

主管看著黑底白字看到眼花
不懂程式的客戶不知道怎麽改

----

### 透過 Gradio 呈現圖形化介面

```python
import gradio as gr

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)
demo.launch()
```

----

### 匯入套件

```python
import gradio
```

透過 `import` 關鍵字匯入 `gradio` 套件

----

### 套件別名

```python
import gradio

gradio.Interface(...)
```

等價於

```python
import gradio as gr

gr.Interface(...)
```

透過 `as` 關鍵字縮短套件名稱
延長開發者的手指壽命

----

### 定義介面

`gr.Interface(fn=greet, ...)`

在幫 `greet` 這個函式定義**介面**

----

### 輸入輸出

`greet` 函式包含**兩個輸入**與**一個輸出**

第一個輸入 `name` 為文字
第二個輸入 `n` 為數字
輸出則為文字

----

### 元件

`text` 代表文字框
`slider` 代表數值滑桿

還有 `image`, `checkbox`, `number`, `markdown` 等元件

----

### 啟動

```python
demo = gr.Interface(...)
demo.launch()
```

在 Colab 裡面，預設會加上 `share=True` 參數

產生的網址 `https://xxx.gradio.live/`
可以分享給其他人使用

----

### 其他範例

大小寫轉換 (Checkbox)
灰階圖片轉換 (Image)
展示新聞連結 (Markdown)
BMI 計算器 (Number)
檔案大小計算器 (File)

----

### 自由發揮時間！

質因數分解
攝氏華氏溫度轉換
字串反轉
雜湊加密
密碼產生器
QRCode 產生器

[參考做法](https://colab.research.google.com/drive/1nr7GVXhV2qIFKyBGNjzjog0z8fLY7Lqz)

---

## Gradio Blocks

----

雖然 Gradio Interface 很方便
但是只支援單一函式
而且無法自訂排版

----

```python
with gr.Blocks() as app:
    name_text = gr.Textbox(label="名字")
    greet_btn = gr.Button("問候")
    farewell_btn = gr.Button("道別")
    message = gr.Textbox(label="訊息")

    def greet_fn(name):
        return f"{name}，你好！"

    def farewell_fn(name):
        return f"{name}，再見！"

    greet_btn.click(greet_fn, name_text, message)
    farewell_btn.click(farewell_fn, name_text, message)

app.launch()
```

----

### 版面配置

可以透過 `gr.Row` 跟 `gr.Column` 切版
使用 `gr.Group` 可以將元件放在同個群組

----

### 猜數字遊戲

練習使用 `gr.Blocks` 製作一個猜數字遊戲

透過 `random` 套件在 1~99 之間產生一個隨機數字
宣告 `upper` 與 `lower` 兩個全域變數紀錄猜測範圍

使用一個 `gr.Textbox` 告訴使用者目前的遊戲狀態
使用 `gr.Number` 接收使用者的猜測數字

[參考做法](https://colab.research.google.com/drive/1nr7GVXhV2qIFKyBGNjzjog0z8fLY7Lqz)

----

### 狀態錯亂

雖然單人使用起來沒有問題
但若開多個分頁同時猜測
情況會變得有些詭異

----

### 狀態管理

作為一個網頁應用
必須考慮多個使用者同時操作的情況

----

### 課程預告

透過 `gr.State` 來管理不同使用者的狀態

[五十音小測驗](https://huggingface.co/spaces/DaOppaiLoli/KanaQuiz)

<style>
h1, h2, h3, h4, h5, h6 { color: #9AD; }
a {color: #9AD}
</style>

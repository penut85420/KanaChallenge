---
marp: true
theme: uncover
class: invert
---

# Python x Gradio

日文五十音大進擊 Day 3

[Colab Demo](https://colab.research.google.com/drive/1zrn-X0GPtWG9C0gwjBEQnJfdHiTgoYBx)

---

## 猜數字遊戲

----

### 構成要素

1. 產生隨機數字
1. 得到使用者的輸入
1. 不斷檢查輸入是否正確

----

### 隨機數字

透過 `random.randint()` 產生一個隨機**整數**

```python
answer = random.randint(1, 99)
```

會隨機產生一個 1 到 99 之間（含）的整數

----

### 使用者輸入

透過 `input()` 取得使用者輸入

```python
n = input("請輸入一個數字：")
```

----

但是 `input()` 取得的資料型態是 `str` 字串型態
需要轉換成 `int` 整數型態才能進行運算

```python
n = input("...")  # 這時的 n 只是 str 字串
n = int(n)        # 這時的 n 才是 int 整數
```

----

### `while` 迴圈

`while ...` 表示某個條件未被滿足前
就不斷執行迴圈內的動作

----

### `while` 語法結構

```python
while 某個條件式:
    # 執行迴圈內的動作
```

----

```python
n = 0
while n < 5:
    print(n)
    n += 1
```

<!-- manim demo -->

----

### 基本的猜數字遊戲

```python
guess = None
answer = random.randint(1, 99)

while guess != answer:
    guess = input("猜一個數字：")
    guess = int(guess)

    if guess < answer:
        print("太小了！")
    elif guess > answer:
        print("太大了！")

print("答對了，遊戲結束！")
```

---

## 練習時間

----

### 可以給使用者更多提示嗎？

例如：
使用者最近猜的數字是什麼
可以猜測最大與最小的範圍

----

### 要如何把猜數字遊戲放進 Gradio 裡面？

需要一個輸入數字的 `gr.Number` 元件
需要一個顯示提示的 `gr.Textbox` 元件
使用全域變數紀錄目前的範圍？

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

### 使用 `gr.State`

將 `upper` 與 `lower` 兩個變數改成 `gr.State`

```python
# upper = 100
# lower = 0

upper = gr.State(100)
lower = gr.State(0)
```

把他們當成 Gradio 元件
放進輸入與輸出的參數裡面

----

### 還有什麼問題呢？

雖然產生的數字是隨機的
但大家的第一題數字卻都是一樣的

這是因為第一個數字在啟動時就已經產生了

----

### 被動初始化

可以先指定 `gr.State(None)`
等 `check_guess()` 被觸發時
再去產生隨機數字

----

### 額外補充

像是 `threading.Lock()` 這種 unpickable 的物件
是不能拿來初始化 `gr.State` 的

這時就可以在 `gr.State` 裡面放入 `None`
等後續觸發事件時再去初始化

---

## 花花綠綠小裝飾

----

### 佈景主題

除了預設的主題以外
Gradio 還提供了其他的佈景主題

在 `gr.Blocks()` 裡面
使用 `theme` 參數來指定主題名稱

```python
with gr.Blocks(theme="...") as app:
    # ...
```

----

![Base](https://i.imgur.com/iXFN0tr.png)

----

![Default](https://i.imgur.com/8PafG9y.png)

----

![Origin](https://i.imgur.com/P0ybGna.png)

----

![Monochrome](https://i.imgur.com/VaoP0l5.png)

----

![Glass](https://i.imgur.com/AV1ngzJ.png)

----

![Soft](https://i.imgur.com/YKso0DN.png)

----

![Citrus](https://i.imgur.com/srOnNSk.png)

----

![Ocean](https://i.imgur.com/Vi2RYU0.png)

----

### 標題與圖示

改變瀏覽器顯示的分頁標題與圖示：

```python
with gr.Blocks(title="這是你的帥氣標題") as app:
    # ...
app.launch(favicon_path="favicon.png")
```

![Tab](https://i.imgur.com/f31X8XU.png)

----

### （進階）自訂 CSS 樣式

例如要隱藏 `gr.Number` 的上下箭頭：

```python
css = """
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
"""

with gr.Blocks(css=css) as app:
    # ...
```

---

## 練習時間

----

### 精心製作的猜數字遊戲

使用者可以調整猜測範圍
增加猜測次數的限制
統計使用者的勝率
讓畫面更加美美的

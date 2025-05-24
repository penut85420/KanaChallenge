---
marp: true
theme: uncover
class: invert
---

# Python x Gradio

日文五十音大進擊 Day 4

[Colab Demo](https://colab.research.google.com/drive/1G1sM67Mj-AYuklpYpSTmmRbtEESzB1Cm)

----

## 基本五十音

平假名

```txt
あいうえお　はひふへほ
かきくけこ　まみむめも
さしすせそ　や　ゆ　よ
たちつてと　らりるれろ
なにぬねの　わ　　　を　ん
```

片假名

```txt
アイウエオ　ハヒフヘホ
カキクケコ　マミムメモ
サシスセソ　ヤ　ユ　ヨ
タチツテト　ラリルレロ
ナニヌネノ　ワ　　　ヲ　ン
```

----

## 濁音、半濁音、拗音

平假名

```txt
がぎぐげご　きゃきゅきょ　ぎゃぎゅぎょ
ざじずぜぞ　しゃしゅしょ　じゃじゅじょ
だぢづでど　ちゃちゅちょ　ぢゃぢゅぢょ
ばびぶべぼ　にゃにゅにょ
ぱぴぷぺぽ　ひゃひゅひょ　びゃびゅびょ　ぴゃぴゅぴょ
```

片假名

```txt
ガギグゲゴ　キャキュキョ　ギャギュギョ
ザジズゼゾ　シャシュショ　ジャジュジョ
ダヂヅデド　チャチュチョ　ヂャヂュヂョ
バビブベボ　ニャニュニョ
パピプペポ　ヒャヒュヒョ　ビャビュビョ　ピャピュピョ
```

----

## 發音

有些時候一個發音可能會有兩種拼寫方式

例如「ぢ」的發音可以拼成 `ji` 或 `di`

----

## 發音 vs 輸入法

有些時候發音和輸入法也不完全一樣

例如「ち」的發音是 `chi`
但輸入法可以是 `ti` 或 `chi`

----

## 檢查拼寫的方法

一開始我借助 `romkan` 套件來檢查
但發現有些發音有遺漏
所以最後還是選擇了正面表列

[GitHub Gist](https://gist.github.com/penut85420/5b383ee875f66cfba70c46ad0e2dd21b)

----

## JSON 結構

`category` 列出不同發音的類別
`hiragana` 列出每一排的平假名
`katakana` 列出每一排的片假名
`spell` 是假名對應的拼音

###### 清音 (Seion)、濁音 (Dakuon)、半濁音 (Handakuon)、拗音 (Youon)

----

## 版面設計

透過 `gr.Tabs` 和 `gr.Tab` 來區分「選題」與「作答」

```python
import gradio as gr

with gr.Blocks() as app:
    with gr.Tabs(selected=0) as tabs:
        with gr.Tab(label="設定", id=0):
            # 選擇要練習的假名

        with gr.Tab(label="測驗", id=1):
            # 測驗的內容
```

----

## 切換分頁

直接 `return` 一個新的 `gr.Tabs` 物件
就可以切換到新的分頁

```python
def start_test(...):

    # 取得要練習的假名

    return gr.Tabs(selected=1), ...
```

----

## 出題邏輯

先選擇要練習平假名、片假名
再選擇要練習哪幾排

把選出來的假名做個洗牌
透過 `gr.State` 紀錄測驗順序

----

## 錯誤訊息

如果使用者沒有選擇任何類別
可以透過 `raise gr.Error()` 來中斷函式進行
並顯示錯誤訊息

```python
def start_test(...):

    # 檢查使用者的選擇

    if not char_list:
        raise gr.Error("請至少選擇一個類別")
```

----

## 檢查作答

目前先透過 `gr.Info` 告訴使用者正確與否

```python
def check_answer(...):

    # 檢查使用者的答案

    if correct:
        return gr.Info("正確！")
    else:
        return gr.Info("錯誤，答案是 ...")
```

----

## Typing Hint

如果要確保函式參數的型別
通常會用 `var: type` 來標註
但這樣會讓參數列表看起來很長

```python
def foo(a: list, b: dict, c: str):
    a.pop()
    b.items()
    c.lower()
```

---

## Typing Hint 邪教寫法

可以不在參數列表上標註型別
改用 `cls.method(obj)` 的方式呼叫方法
維持參數列表的精簡

```python
def bar(a, b, c):
    list.pop(a)
    dict.items(b)
    str.lower(c)
```

----

## 觸發順序

多數的元件觸發時只會呼叫一個函式
但 `txt_input` 會分別觸發「檢查假名」與「顯示下一題」
可以用 `txt_input.submit(...).then(...)` 來處理觸發順序

----

## 選個有趣的字體

[Google Fonts](https://fonts.google.com/?lang=ja_Jpan) 上面很多有趣的日文字體

例如 [DotGothic16](https://fonts.google.com/specimen/DotGothic16) 是像素風格

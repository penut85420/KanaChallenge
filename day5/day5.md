---
marp: true
theme: uncover
class: invert
---

# Python x Gradio

日文五十音大進擊 Day 5

[Colab Demo](https://colab.research.google.com/drive/1ABh2sU7lOn2Qm1X_1GkYSvvcT7Qnf420)

---

## 應用收尾

再加上幾個元件來完善整體應用：

1. 提示資訊
2. 計算正確題數 & 正確率
3. 答錯的歷史紀錄
4. (Optional) 重構

---

# 提示欄位

----

## 增加提示元件

用來提示使用者正確、錯誤以及答案是什麼：

```python
with gr.Row():
    txt_test = gr.Textbox(label="題目", interactive=False)
    txt_info = gr.Textbox(label="資訊", interactive=False)
txt_input = gr.Textbox(label="作答", submit_btn=True)
```

----

在檢查答案時，回傳相關的提示資訊：

```python
def check_answer(...):
    # ...
    if txt_input in spell[txt_test]:
        # ...
        txt_info = "正確！"
    else:
        # ...
        answer = ", ".join(spell[txt_test])
        txt_info = f"錯誤，正確答案為 {answer}"
    # ...
    return ..., txt_info, ...
```

---

# 正確率

----

增加**答對題數**、**總答題數**和**答對比率**的元件：

```python
n_correct = gr.Number(label="答對題數", interactive=False)
n_total = gr.Number(label="總答題數", interactive=False)
txt_accuracy = gr.Textbox("100.00%", label="答對比率", interactive=False)
```

設定 `interactive=False` 避免被使用者竄改
因為答對比率要顯示 `%` 所以要是 `gr.Textbox` 元件

----

在 `check_answer()` 時順便統計正確率：

```python
def check_answer(..., n_correct, n_total):
    # ...

    if txt_input in spell[txt_test]:
        n_correct += 1
        # ...

    n_total += 1
    accuracy = n_correct / n_total

    return ..., n_correct, n_total, f"{accuracy:.2%}"
```

---

# 歷史紀錄

----

放一個 `gr.TextArea` 在新的分頁：

```python
with gr.Tab(label="紀錄", id=2):
    txt_records = gr.TextArea(show_label=False, interactive=False)
    btn_again = gr.Button("再次測驗")
    btn_back = gr.Button("回到設定")
```

在這個分頁順便放上**再次測驗**與**回到設定**兩個按鈕
方便使用者跳轉到不同分頁進行行動

----

在使用者答錯時記錄下來：

```python
def check_answer(..., txt_records):
    if txt_input in spell[txt_test]:
        # ...
    else:
        answer = ", ".join(spell[txt_test])
        txt_info = f"錯誤，正確答案為 {answer}"
        txt_records += f"題目：{txt_test}、正解：{answer}、輸入：{txt_input}\n"
    # ...
    return ..., txt_records
```

----

在測驗結束時，計算正確率並跳轉到紀錄分頁：

```python
def next_char(st_queue, n_correct, n_total, txt_record):
    if not st_queue:
        gr.Info("測驗結束！")
        accuracy = n_correct / n_total
        txt_record += f"正確率 {accuracy:.2%} ({n_correct}/{n_total})"
        return None, None, None, txt_record, gr.Tabs(selected=2)

    # ...
```

----

當使用者點擊**再次測驗**時
其實與點擊第一個分頁的**開始測驗**按鈕一樣

```python
btn_start.click(...)
btn_again.click(...)
```

----

點擊**回到設定**時，只要跳轉分頁即可：

```python
def back():
    return gr.Tabs(selected=0)

btn_back.click(back, outputs=tabs)
```

----

在重新進行測驗時，記得重置狀態紀錄：

```python
def reset():
    return 0, 0, "100.00%", None, None

btn_again.click(
    reset, outputs=[n_correct, n_total, txt_accuracy, txt_info, txt_records]
).then(...)
```

---

# 重構

----

Gradio 的事件註冊往往有很多重複性的參數
這時很適合進行簡單的重構

----

宣告一個取得 Keyword Arguments 的函式：

```python
def gr_args(fn=None, inputs=None, outputs=None, show_progress="hidden", **kwargs):
    return dict(
        fn=fn,
        inputs=inputs,
        outputs=outputs,
        show_progress=show_progress,
        **kwargs,
    )
```

----

將輸入、輸出、參數各自獨立成變數：

```python
reset_outputs = [n_correct, n_total, txt_accuracy, txt_info, txt_records]
reset_args = gr_args(reset, outputs=reset_outputs)

start_inputs = [chk_kana, chk_seion, chk_dakuon, chk_handakuon, chk_youon]
start_outputs = [txt_test, st_queue, debug, tabs]
start_args = gr_args(start_test, start_inputs, start_outputs)
```

----

這樣就能對重複或相似的事件做大幅度的精簡：

```python
btn_start.click(**reset_args).then(**start_args)
btn_again.click(**reset_args).then(**start_args)
```

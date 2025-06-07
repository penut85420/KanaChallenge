---
marp: true
theme: uncover
class: invert
---

# Python x Gradio

日文五十音大進擊 Day X

[Space Demo](https://huggingface.co/spaces/PenutChen/KanaQuizDemo)

---

## 重構

----

在 Gradio 裡面，常常需要使用 `with` 區塊來排版

----

![h:500 IndentMeme](https://hackmd.io/_uploads/SkEbwDZQxe.png)

----

將 Gradio App 重構為 Class
是個減少縮排的好方法

----

```python
# 基本框架

class App:
    def __init__(self):
        self.__init_app()

    def __init_app(self):
        with gr.Blocks() as self.app:
            self.__init_layout()

    def __init_layout(self):
        with gr.Tabs(selected=0) as self.tabs:
            with gr.Tab(id=0, label="Setting"):
                self.__init_setting_tab()

            with gr.Tab(id=1, label="Quiz"):
                self.__init_quiz_tab()

            with gr.Tab(id=2, label="Record"):
                self.__init_record_tab()

    def __init_setting_tab(self):
        # ...

    def __init_quiz_tab(self):
        # ...

    def __init_record_tab(self):
        # ...
```

----

```python
# 註冊事件

class App:
    def __init__(self):
        self.__init_app()

    def __init_app(self):
        with gr.Blocks() as self.app:
            self.__init_layout()
            self.__register_events()

    def __init_layout(self):
        # ...

    def __register_events(self):
        reset_outputs = [self.n_correct, self.n_total, self.txt_accuracy]
        reset_outputs += [self.txt_info, self.txt_records]
        reset_args = gr_args(self.reset, outputs=reset_outputs)

        start_inputs = [self.chk_kana, self.chk_seion, self.chk_dakuon]
        start_inputs += [self.chk_handakuon, self.chk_youon]
        start_outputs = [self.txt_test, self.st_queue, self.debug, self.tabs]
        start_args = gr_args(self.start_test, start_inputs, start_outputs)

        self.btn_start.click(**reset_args).then(**start_args)

    def reset(self):
        return 0, 0, "100.00%", None, None

    def start_test(self, kana, seion, dakuon, handakuon, yoon):
        # ...
        return char, char_list, char_list, gr.Tabs(selected=1)
```

---

# Hugging Face 🤗 Space

----

[HF Space](https://huggingface.co/spaces) 可以免費讓 Gradio App 在上面運作

----

先[註冊](https://huggingface.co/join)一個 HF 帳號

![h:550 Sign Up](https://hackmd.io/_uploads/HkseOdZmll.png)

----

新增一個 Space 專案

![New Space](https://hackmd.io/_uploads/SJo-u_W7ee.png)

----

Space SDK 選 Gradio

![h:550 Space Initialize](https://hackmd.io/_uploads/HJFmddWXgl.png)

----

建立好 Space 後，前往 Files 分頁

![Files](https://hackmd.io/_uploads/Byi4dd-Xxe.png)

----

右上角的 Contribute 可以建立新檔案或上傳檔案

![Upload](https://hackmd.io/_uploads/Sk9HOdbQeg.png)

先上傳 `kana-spell.json`
再建立 `app.py`

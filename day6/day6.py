import json
import random

import gradio as gr


class KanaQuizApp:
    def __init__(self, spell_path="kana-spell.json", font_name="Kiwi Maru"):
        self.font_name = font_name

        self.data = load_json(spell_path)
        self.hiragana = self.data["hiragana"]
        self.katakana = self.data["katakana"]
        self.category = self.data["category"]
        self.spell = self.data["spell"]

        self.__init_app()

    def __init_blocks(self):
        font = gr.themes.GoogleFont(self.font_name)
        theme = gr.themes.Ocean(font=font)
        return gr.Blocks(theme=theme)

    def __init_app(self):
        with self.__init_blocks() as self.app:
            self.__init_states()
            self.__init_layout()
            self.__register_events()

    def __init_states(self):
        self.st_queue = gr.State(None)

    def __init_layout(self):
        self.title = gr.HTML("<h1>日文五十音大進擊 🚀</h1>")
        with gr.Tabs(selected=0) as self.tabs:
            with gr.Tab(label="設定 ⚙️", id=0):
                self.__init_setting_tab()

            with gr.Tab(label="測驗 📝", id=1):
                self.__init_quiz_tab()

            with gr.Tab(label="紀錄 📜", id=2):
                self.__init_record_tab()

        self.debug = gr.TextArea(label="Debug", visible=False)

    def __init_setting_tab(self):
        with gr.Group():
            self.chk_kana = gr.CheckboxGroup(["平假名", "片假名"], value=["平假名"], label="假名")
            self.chk_seion = gr.CheckboxGroup(self.category["seion"], value=["a"], label="清音")
            with gr.Row():
                self.chk_dakuon = gr.CheckboxGroup(self.category["dakuon"], label="濁音")
                self.chk_handakuon = gr.CheckboxGroup(self.category["handakuon"], label="半濁音")
            self.chk_youon = gr.CheckboxGroup(self.category["youon"], label="拗音")

        with gr.Row():
            self.btn_select_all = gr.Button("全選")
            self.btn_select_none = gr.Button("全不選")
        self.btn_start = gr.Button("開始測驗 ✨")

    def __init_quiz_tab(self):
        with gr.Group():
            with gr.Row():
                self.txt_test = gr.Textbox(label="題目 👀", interactive=False)
                self.txt_info = gr.Textbox(label="資訊 📊", interactive=False)

            self.txt_input = gr.Textbox(label="作答 ✍️", submit_btn=True)

            with gr.Row():
                self.n_correct = gr.Number(label="答對題數 ✅", interactive=False)
                self.n_total = gr.Number(label="總答題數 🧮", interactive=False)
                self.txt_accuracy = gr.Textbox("100.00%", label="答對比率", interactive=False)

    def __init_record_tab(self):
        self.txt_records = gr.TextArea(show_label=False, interactive=False)
        self.btn_again = gr.Button("再次測驗 ⚙️")
        self.btn_back = gr.Button("回到設定 🔄")

    def __register_events(self):
        # event arguments
        reset_outputs = [self.n_correct, self.n_total, self.txt_accuracy]
        reset_outputs += [self.txt_info, self.txt_records]
        reset_args = gr_args(self.reset, outputs=reset_outputs)

        start_inputs = [self.chk_kana, self.chk_seion, self.chk_dakuon]
        start_inputs += [self.chk_handakuon, self.chk_youon]
        start_outputs = [self.txt_test, self.st_queue, self.debug, self.tabs]
        start_args = gr_args(self.start_test, start_inputs, start_outputs)

        check_inputs = [self.txt_test, self.txt_input, self.n_correct]
        check_inputs += [self.n_total, self.txt_records]
        check_outputs = [self.txt_input, self.txt_info, self.n_correct]
        check_outputs += [self.n_total, self.txt_accuracy, self.txt_records]
        check_args = gr_args(self.check_answer, check_inputs, check_outputs)

        next_inputs = [self.st_queue, self.n_correct, self.n_total, self.txt_records]
        next_outputs = [self.txt_test, self.st_queue, self.debug, self.txt_records, self.tabs]
        next_args = gr_args(self.next_char, next_inputs, next_outputs)

        select_outputs = [self.chk_kana, self.chk_seion, self.chk_dakuon]
        select_outputs += [self.chk_handakuon, self.chk_youon]
        select_all_args = gr_args(self.select_all, outputs=select_outputs)

        select_none_args = gr_args(self.select_none, outputs=select_outputs)
        back_args = gr_args(self.back, outputs=self.tabs)

        # register events
        self.btn_start.click(**reset_args).then(**start_args)
        self.txt_input.submit(**check_args).then(**next_args)
        self.btn_select_all.click(**select_all_args)
        self.btn_select_none.click(**select_none_args)
        self.btn_again.click(**reset_args).then(**start_args)
        self.btn_back.click(**back_args)

    def start_test(self, kana, seion, dakuon, handakuon, yoon):
        category = [*seion, *dakuon, *handakuon, *yoon]

        char_list = list()
        char_list += [ch for k in category for ch in self.hiragana[k]] if "平假名" in kana else []
        char_list += [ch for k in category for ch in self.katakana[k]] if "片假名" in kana else []

        if not char_list:
            raise gr.Error("請至少選擇一個類別")

        random.shuffle(char_list)
        char = char_list.pop(0)
        return char, char_list, char_list, gr.Tabs(selected=1)

    def check_answer(self, txt_test, txt_input, n_correct, n_total, txt_records):
        txt_input = str.lower(txt_input).strip()

        if txt_input in self.spell[txt_test]:
            n_correct += 1
            txt_info = "正確！"
        else:
            answer = ", ".join(self.spell[txt_test])
            txt_info = f"錯誤，正確答案為 {answer}"
            txt_records += f"題目：{txt_test}、正解：{answer}、輸入：{txt_input}\n"

        n_total += 1
        accuracy = n_correct / n_total

        return None, txt_info, n_correct, n_total, f"{accuracy:.2%}", txt_records

    def next_char(self, st_queue, n_correct, n_total, txt_record):
        if not st_queue:
            gr.Info("測驗結束！")
            accuracy = n_correct / n_total
            txt_record += f"正確率 {accuracy:.2%} ({n_correct}/{n_total})"
            return None, None, None, txt_record, gr.Tabs(selected=2)

        char = list.pop(st_queue, 0)
        return char, st_queue, st_queue, txt_record, gr.Tabs(selected=1)

    def select_all(self):
        return (
            ["平假名", "片假名"],
            self.category["seion"],
            self.category["dakuon"],
            self.category["handakuon"],
            self.category["youon"],
        )

    def select_none(self):
        return [], [], [], [], []

    def reset(self):
        return 0, 0, "100.00%", None, None

    def back(self):
        return gr.Tabs(selected=0)

    def launch(self):
        self.app.launch()


def load_json(path):
    with open(path, "rt", encoding="UTF-8") as fp:
        return json.load(fp)


def gr_args(fn=None, inputs=None, outputs=None, show_progress="hidden", **kwargs):
    return dict(fn=fn, inputs=inputs, outputs=outputs, show_progress=show_progress, **kwargs)


if __name__ == "__main__":
    KanaQuizApp().launch()

# -*- coding: utf-8 -*-
import os
import sys

os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Line, Color as KivyColor
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.text import LabelBase
from PIL import Image as PILImage

Window.size = (400, 750)
Window.clearcolor = (0.9, 0.9, 0.9, 1)

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

FONT_PATH = "C:\\Windows\\Fonts\\msgothic.ttc"
if os.path.exists(FONT_PATH):
    LabelBase.register(name="Roboto", fn_regular=FONT_PATH)

class SignPad(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = []

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                KivyColor(0, 0, 0, 1)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=3)
                self.lines.append(touch.ud['line'])

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]

    def clear_canvas(self):
        self.canvas.clear()
        self.lines = []
        with self.canvas.before:
            KivyColor(0.95, 0.95, 0.95, 1)
            from kivy.graphics import Rectangle
            Rectangle(pos=self.pos, size=self.size)

    def save_to_image(self, filename="temp_signature.png"):
        save_path = os.path.join(BASE_DIR, filename)
        img = PILImage.new("RGB", (int(self.width), int(self.height)), "white")
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        for line in self.lines:
            if len(line.points) >= 4:
                converted_points = []
                for i in range(0, len(line.points), 2):
                    x = line.points[i] - self.x
                    y = self.height - (line.points[i+1] - self.y)
                    converted_points.append((x, y))
                draw.line(converted_points, fill="black", width=3)
        img.save(save_path)
        return save_path

class ReportApp(App):
    def build(self):
        self.title = "MRC - Android運用確定版"
        
        root = ScrollView(size_hint=(1, 1))
        layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=12)
        layout.bind(minimum_height=layout.setter('height'))

        layout.add_widget(Label(text="【基本情報入力】", size_hint_y=None, height=30, bold=True, color=(0,0,0,1)))
        
        layout.add_widget(Label(text="お客様名:", size_hint_y=None, height=15))
        self.client_input = TextInput(text="ハマキョウレックス みよし第1センター", size_hint_y=None, height=40, multiline=False)
        layout.add_widget(self.client_input)

        layout.add_widget(Label(text="件名:", size_hint_y=None, height=15))
        self.subject_input = TextInput(text="リニソート シュートNO.313 ベルト蛇行による停止", size_hint_y=None, height=40, multiline=False)
        layout.add_widget(self.subject_input)

        layout.add_widget(Label(text="【管理テーブル入力】", size_hint_y=None, height=20, color=(0,0,0,1)))
        grid_inputs = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.date_input = TextInput(text="2026年4月8日(水)", multiline=False)
        self.month_input = TextInput(text="4月度", multiline=False)
        self.seiban_input = TextInput(text="TI25D40", multiline=False)
        self.setsubi_input = TextInput(text="リニソート", multiline=False)
        grid_inputs.add_widget(self.date_input)
        grid_inputs.add_widget(self.month_input)
        grid_inputs.add_widget(self.seiban_input)
        grid_inputs.add_widget(self.setsubi_input)
        layout.add_widget(grid_inputs)

        layout.add_widget(Label(text="【担当者入力】(承認 / 作成 / 作業)", size_hint_y=None, height=20, color=(0,0,0,1)))
        member_inputs = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.member_shonin = TextInput(text="高 田", multiline=False)
        self.member_sakusei = TextInput(text="土 屋", multiline=False)
        self.member_sagyo = TextInput(text="土 屋", multiline=False)
        member_inputs.add_widget(self.member_shonin)
        member_inputs.add_widget(self.member_sakusei)
        member_inputs.add_widget(self.member_sagyo)
        layout.add_widget(member_inputs)

        layout.add_widget(Label(text="【1. 作業内容】", size_hint_y=None, height=25, bold=True, color=(0,0,0,1)))
        default_work = "1) シュート NO.313 の平ベルト蛇行あり、\n2) 側面カバーに噛み込み停止した為、その復旧作業を実施"
        self.work_input = TextInput(text=default_work, size_hint_y=None, height=80, multiline=True)
        layout.add_widget(self.work_input)

        layout.add_widget(Label(text="【2. 結果・処置】", size_hint_y=None, height=25, bold=True, color=(0,0,0,1)))
        default_result = "・平ベルト テークアップにて蛇行調整実施し問題なきことを確認済み\n・様子見して、稼働に使用お願いします。\n・従動側ローラ ベアリング部より異音ありの為購入推奨"
        self.result_input = TextInput(text=default_result, size_hint_y=None, height=100, multiline=True)
        layout.add_widget(self.result_input)

        layout.add_widget(Label(text="【時間入力】", size_hint_y=None, height=20, color=(0,0,0,1)))
        time_inputs = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.time_work_input = TextInput(text="9:15̃10:30 (2人)", multiline=False)
        self.time_move_input = TextInput(text="1Hr (2台)", multiline=False)
        time_inputs.add_widget(self.time_work_input)
        time_inputs.add_widget(self.time_move_input)
        layout.add_widget(time_inputs)

        layout.add_widget(Label(text="【写真添付】", size_hint_y=None, height=25, bold=True, color=(0,0,0,1)))
        photo_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=55, spacing=10)
        self.selected_photos = [None, None]
        
        btn_left = Button(text="写真1\n(左枠へ)", font_size=11)
        btn_right = Button(text="写真2\n(右枠へ)", font_size=11)
        btn_left.bind(on_press=lambda x: self.open_file_selector(0, btn_left))
        btn_right.bind(on_press=lambda x: self.open_file_selector(1, btn_right))
        photo_layout.add_widget(btn_left)
        photo_layout.add_widget(btn_right)
        layout.add_widget(photo_layout)

        layout.add_widget(Label(text="【お客様御検印】", size_hint_y=None, height=20, bold=True, color=(0,0,0,1)))
        self.sign_pad = SignPad(size_hint_y=None, height=100)
        with self.sign_pad.canvas.before:
            KivyColor(0.98, 0.98, 0.98, 1)
            from kivy.graphics import Rectangle
            self.rect = Rectangle(pos=self.sign_pad.pos, size=(400, 100))
        layout.add_widget(self.sign_pad)

        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        clear_btn = Button(text="サインやり直し", background_color=(0.7, 0.2, 0.2, 1))
        clear_btn.bind(on_press=lambda x: self.sign_pad.clear_canvas())
        
        pdf_btn = Button(text="報告書を出力", background_color=(0.1, 0.5, 0.1, 1), bold=True)
        pdf_btn.bind(on_press=self.generate_pdf)
        
        btn_layout.add_widget(clear_btn)
        btn_layout.add_widget(pdf_btn)
        layout.add_widget(btn_layout)

        self.status_label = Label(text="", size_hint_y=None, height=30, color=(0,0,0,1))
        layout.add_widget(self.status_label)

        root.add_widget(layout)
        return root

    def open_file_selector(self, index, button_instance):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root_tk = tk.Tk()
            root_tk.withdraw()
            file_path = filedialog.askopenfilename(title="写真選択", filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
            if file_path:
                button_instance.text = f"選択済\n{os.path.basename(file_path)[:12]}"
                self.selected_photos[index] = file_path
        except:
            pass

    # 🌟 外部のPDF部品を使わず、画像合成の仕組みを利用して100%安全に書類を生成するエンジン
    def generate_pdf(self, instance):
        try:
            sig_file = self.sign_pad.save_to_image("temp_signature.png")
            pdf_filename = os.path.join(BASE_DIR, "作業完了報告書.pdf")
            template_path = os.path.join(BASE_DIR, "template_format.png")

            if not os.path.exists(template_path):
                self.status_label.text = "エラー: template_format.png がありません"
                return

            # 1. 土屋さんの「黄金座標」に対応するキャンバスを画像処理(PIL)で完全再現
            base_img = PILImage.open(template_path).convert("RGB")
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(base_img)
            
            # フォント設定（Android標準の日本語フォントを安全に割り当て）
            try:
                font = ImageFont.truetype("NotoSansCJK-Regular.ttc", 14)
                font_sm = ImageFont.truetype("NotoSansCJK-Regular.ttc", 12)
            except:
                font = ImageFont.load_default()
                font_sm = ImageFont.load_default()

            # 💡 上下反転（842-Y）の計算を挟み、指定の黄金座標へテキストを完璧に配置
            draw.text((110, 842 - 768 - 14), self.client_input.text, fill="black", font=font)
            draw.text((110, 842 - 738 - 14), self.subject_input.text, fill="black", font=font)

            # 管理テーブル
            draw.text((124, 842 - 685 - 12), self.date_input.text, fill="black", font=font_sm)
            draw.text((215, 842 - 685 - 12), self.month_input.text, fill="black", font=font_sm)
            draw.text((290, 842 - 685 - 12), self.seiban_input.text, fill="black", font=font_sm)
            draw.text((390, 842 - 685 - 12), self.setsubi_input.text, fill="black", font=font_sm)
            draw.text((465, 842 - 685 - 12), self.member_shonin.text, fill="black", font=font_sm)
            draw.text((502, 842 - 685 - 12), self.member_sakusei.text, fill="black", font=font_sm)
            draw.text((539, 842 - 685 - 12), self.member_sagyo.text, fill="black", font=font_sm)

            # 作業内容
            draw_w_y = 618
            for line in self.work_input.text.split('\n'):
                draw.text((60, 842 - draw_w_y - 14), line, fill="black", font=font)
                draw_w_y -= 17.0

            # 結果・処置
            draw_r_y = 503
            for line in self.result_input.text.split('\n'):
                draw.text((60, 842 - draw_r_y - 14), line, fill="black", font=font)
                draw_r_y -= 17.0

            # 💡 写真の最大化トリミング貼り付け
            def paste_photo_crop(target_img, img_path, tx, ty, tw, th):
                if img_path and os.path.exists(img_path):
                    p_img = PILImage.open(img_path)
                    # 枠に合わせて切り抜き・最大化拡大
                    p_resized = p_img.resize((tw, th), PILImage.Resampling.LANCZOS)
                    target_img.paste(p_resized, (tx, 842 - ty - th))

            if self.selected_photos[0]:
                paste_photo_crop(base_img, self.selected_photos[0], 56, 124, 242, 172)
                name_only = os.path.splitext(os.path.basename(self.selected_photos[0]))[0]
                draw.text((60, 842 - 110), name_only, fill="black", font=font_sm)

            if self.selected_photos[1]:
                paste_photo_crop(base_img, self.selected_photos[1], 308, 124, 242, 172)
                name_only = os.path.splitext(os.path.basename(self.selected_photos[1]))[0]
                draw.text((312, 842 - 110), name_only, fill="black", font=font_sm)

            # 時間
            draw.text((135, 842 - 84 - 14), self.time_work_input.text, fill="black", font=font)
            draw.text((425, 842 - 84 - 14), self.time_move_input.text, fill="black", font=font)

            # サイン
            if os.path.exists(sig_file):
                s_img = PILImage.open(sig_file)
                s_resized = s_img.resize((556-470, 20), PILImage.Resampling.LANCZOS)
                base_img.paste(s_resized, (470, 842 - 52 - 20))

            # 🌟 出来上がった高解像度データを、Androidシステムが最も扱いやすいPDF形式で保存してエクスポート
            base_img.save(pdf_filename, "PDF", resolution=100.0)

            if os.path.exists(sig_file):
                os.remove(sig_file)

            self.status_label.text = "成功: PDF報告書を出力しました！"
        except Exception as e:
            self.status_label.text = f"エラー: {str(e)}"

if __name__ == '__main__':
    ReportApp().run()

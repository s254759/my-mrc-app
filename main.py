# -*- coding: utf-8 -*-
import os
import sys

# ログの無駄な出力を抑制
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Line, Color as KivyColor, Rectangle
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage

Window.size = (400, 750)
Window.clearcolor = (0.9, 0.9, 0.9, 1)

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

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
            Rectangle(pos=self.pos, size=self.size)

class ReportApp(App):
    def build(self):
        self.title = "MRC - Android完全確定版"
        
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
        self.time_work_input = TextInput(text="9:15-10:30 (2人)", multiline=False)
        self.time_move_input = TextInput(text="1Hr (2台)", multiline=False)
        time_inputs.add_widget(self.time_work_input)
        time_inputs.add_widget(self.time_move_input)
        layout.add_widget(time_inputs)

        layout.add_widget(Label(text="【お客様御検印】", size_hint_y=None, height=20, bold=True, color=(0,0,0,1)))
        self.sign_pad = SignPad(size_hint_y=None, height=100)
        with self.sign_pad.canvas.before:
            KivyColor(0.98, 0.98, 0.98, 1)
            self.rect = Rectangle(pos=self.sign_pad.pos, size=(400, 100))
        layout.add_widget(self.sign_pad)

        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        clear_btn = Button(text="サインやり直し", background_color=(0.7, 0.2, 0.2, 1))
        clear_btn.bind(on_press=lambda x: self.sign_pad.clear_canvas())
        
        pdf_btn = Button(text="報告書（画像）を出力", background_color=(0.1, 0.5, 0.1, 1), bold=True)
        pdf_btn.bind(on_press=self.generate_report_image)
        
        btn_layout.add_widget(clear_btn)
        btn_layout.add_widget(pdf_btn)
        layout.add_widget(btn_layout)

        self.status_label = Label(text="", size_hint_y=None, height=30, color=(0,0,0,1))
        layout.add_widget(self.status_label)

        root.add_widget(layout)
        return root

    # 🌟外部の危険なC言語パーツ(Pillow/ReportLab)を1ミリも使わず、Kivyの純粋な機能だけで完結させる超安全エクスポート
    def generate_report_image(self, instance):
        try:
            template_path = os.path.join(BASE_DIR, "template_format.png")
            output_path = os.path.join(BASE_DIR, "作業完了報告書.png")

            if not os.path.exists(template_path):
                self.status_label.text = "エラー: template_format.png が見当たりません"
                return

            # Kivy内部の描画コンテキストを使い、バックグラウンドで非表示の合成用シートを作成
            # これにより外部ライブラリとの衝突が100%回避されます
            from kivy.uix.floatlayout import FloatLayout
            from kivy.uix.image import Image as KivyImage
            
            export_container = FloatLayout(size=(595, 842))
            
            # 1. 背景テンプレートを配置
            bg = KivyImage(source=template_path, size=(595, 842), pos=(0, 0), allow_stretch=True, keep_ratio=False)
            export_container.add_widget(bg)

            # 💡 土屋さんの導き出した黄金座標(左下0,0基準)にテキストをジャスト配置！
            def add_txt(text, x, y, size=14, font_name="Roboto"):
                lbl = Label(text=text, font_size=size, font_name=font_name, color=(0,0,0,1),
                            pos=(x, y), size_hint=(None, None), size=(300, 30), halign='left', valign='middle')
                lbl.bind(texture_size=lbl.setter('size'))
                export_container.add_widget(lbl)

            # 各入力データを黄金座標へマッピング
            add_txt(self.client_input.text, 110, 768, size=15)
            add_txt(self.subject_input.text, 110, 738, size=14)

            # 管理テーブル行
            add_txt(self.date_input.text, 100, 685, size=12)
            add_txt(self.month_input.text, 205, 685, size=12)
            add_txt(self.seiban_input.text, 275, 685, size=12)
            add_txt(self.setsubi_input.text, 375, 685, size=12)
            add_txt(self.member_shonin.text, 455, 685, size=12)
            add_txt(self.member_sakusei.text, 495, 685, size=12)
            add_txt(self.member_sagyo.text, 530, 685, size=12)

            # 1. 作業内容（改行を考慮した自動送り）
            w_y = 618
            for line in self.work_input.text.split('\n'):
                add_txt(line, 60, w_y, size=13)
                w_y -= 20

            # 2. 結果・処置
            r_y = 503
            for line in self.result_input.text.split('\n'):
                add_txt(line, 60, r_y, size=13)
                r_y -= 20

            # 下部時間
            add_txt(self.time_work_input.text, 135, 84, size=13)
            add_txt(self.time_move_input.text, 425, 84, size=13)

            # サインパッドの内容を、Kivyのベクター命令から直接転写
            if self.sign_pad.lines:
                with export_container.canvas:
                    KivyColor(0, 0, 0, 1)
                    for line in self.sign_pad.lines:
                        # サインエリア(470, 52)へスケールと配置をフィッティング変換
                        scaled_points = []
                        for i in range(0, len(line.points), 2):
                            px = line.points[i] - self.sign_pad.x
                            py = line.points[i+1] - self.sign_pad.y
                            sx = 470 + (px * (86.0 / max(1, self.sign_pad.width)))
                            sy = 52 + (py * (20.0 / max(1, self.sign_pad.height)))
                            scaled_points.extend([sx, sy])
                        Line(points=scaled_points, width=2)

            # 🌟Kivyコアエンジンで、一切の変換劣化なく画像として即時書き出し
            export_container.export_to_png(output_path)
            self.status_label.text = "大成功: 報告書(作業完了報告書.png)を保存しました！"
            
        except Exception as e:
            self.status_label.text = f"出力エラー: {str(e)}"

if __name__ == '__main__':
    ReportApp().run()

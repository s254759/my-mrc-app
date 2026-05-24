# -*- coding: utf-8 -*-
import os
import sys

# Kivyの環境ログを非表示にして起動をスッキリさせます
os.environ["KIVY_NO_CONSOLELOG"] = "1"

# --- Kivyの基本部品を読み込む ---
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

# --- PDF生成と画像処理の部品を読み込む ---
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from PIL import Image as PILImage

# --- スマホ画面シミュレート ---
Window.size = (400, 750) # 担当者枠追加に伴い画面の高さを少し広げました
Window.clearcolor = (0.9, 0.9, 0.9, 1)

# 実行中のフォルダーの住所を自動取得
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

# --- Windows標準の日本語フォント「MSゴシック」を登録 ---
FONT_PATH = "C:\\Windows\\Fonts\\msgothic.ttc"
if os.path.exists(FONT_PATH):
    LabelBase.register(name="Roboto", fn_regular=FONT_PATH)

# --- 手書きサイン用キャンバス ---
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


# --- メインアプリケーション UI ---
class ReportApp(App):
    def build(self):
        self.title = "Mobile Report Creator (MRC) - 運用改善版"
        
        root = ScrollView(size_hint=(1, 1))
        layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=12)
        layout.bind(minimum_height=layout.setter('height'))

        # 1. 基本情報入力
        layout.add_widget(Label(text="【基本情報入力】", size_hint_y=None, height=30, bold=True, color=(0,0,0,1)))
        
        layout.add_widget(Label(text="お客様名:", size_hint_y=None, height=15))
        self.client_input = TextInput(text="ハマキョウレックス みよし第1センター", size_hint_y=None, height=40, multiline=False)
        layout.add_widget(self.client_input)

        layout.add_widget(Label(text="件名:", size_hint_y=None, height=15))
        self.subject_input = TextInput(text="リニソート シュートNO.313 ベルト蛇行による停止", size_hint_y=None, height=40, multiline=False)
        layout.add_widget(self.subject_input)

        # 2. 管理用テーブル項目入力（★文字サイズを通常サイズへ大きく統一）
        layout.add_widget(Label(text="【管理テーブル入力】(実施日 / 月度 / 製番 / 設備)", size_hint_y=None, height=20, color=(0,0,0,1)))
        grid_inputs = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        
        # font_sizeをデフォルトの大きさに戻しました
        self.date_input = TextInput(text="2026年4月8日(水)", multiline=False)
        self.month_input = TextInput(text="4月度", multiline=False)
        self.seiban_input = TextInput(text="TI25D40", multiline=False)
        self.setsubi_input = TextInput(text="リニソート", multiline=False)
        
        grid_inputs.add_widget(self.date_input)
        grid_inputs.add_widget(self.month_input)
        grid_inputs.add_widget(self.seiban_input)
        grid_inputs.add_widget(self.setsubi_input)
        layout.add_widget(grid_inputs)

        # ★追加項目：承認・作成・作業の担当者入力枠
        layout.add_widget(Label(text="【担当者入力】(承認 / 作成 / 作業)", size_hint_y=None, height=20, color=(0,0,0,1)))
        member_inputs = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.member_shonin = TextInput(text="高 田", multiline=False)
        self.member_sakusei = TextInput(text="土 屋", multiline=False)
        self.member_sagyo = TextInput(text="土 屋", multiline=False)
        member_inputs.add_widget(self.member_shonin)
        member_inputs.add_widget(self.member_sakusei)
        member_inputs.add_widget(self.member_sagyo)
        layout.add_widget(member_inputs)

        # 3. 作業内容 ＆ 結果・処置
        layout.add_widget(Label(text="【1. 作業内容】", size_hint_y=None, height=25, bold=True, color=(0,0,0,1)))
        default_work = (
            "1) シュート NO.313 の平ベルト蛇行あり、\n"
            "2) 側面カバーに噛み込み停止した為、その復旧作業を実施"
        )
        self.work_input = TextInput(text=default_work, size_hint_y=None, height=80, multiline=True)
        layout.add_widget(self.work_input)

        layout.add_widget(Label(text="【2. 結果・処置】", size_hint_y=None, height=25, bold=True, color=(0,0,0,1)))
        default_result = (
            "・平ベルト テークアップにて蛇行調整実施し問題なきことを確認済み\n"
            "・様子見して、稼働に使用お願いします。\n"
            "・従動側ローラ ベアリング部より異音ありの為購入推奨"
        )
        self.result_input = TextInput(text=default_result, size_hint_y=None, height=100, multiline=True)
        layout.add_widget(self.result_input)

        # 4. 【時間入力】(位置を結果・処置の真下に配置)
        layout.add_widget(Label(text="【時間入力】(作業時間 / 移動時間)", size_hint_y=None, height=20, color=(0,0,0,1)))
        time_inputs = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.time_work_input = TextInput(text="9:15̃10:30 (2人)", multiline=False)
        self.time_move_input = TextInput(text="1Hr (2台)", multiline=False)
        time_inputs.add_widget(self.time_work_input)
        time_inputs.add_widget(self.time_move_input)
        layout.add_widget(time_inputs)

        # 5. 写真添付欄
        layout.add_widget(Label(text="【写真添付】(タップして現場写真を選択)", size_hint_y=None, height=25, bold=True, color=(0,0,0,1)))
        photo_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=55, spacing=10)
        self.selected_photos = [None, None]
        
        # ★左右逆転を防ぐため、ボタンの配列構造を直観的に整理
        btn_left = Button(text="写真1\n(左枠へ)", font_size=11)
        btn_right = Button(text="写真2\n(右枠へ)", font_size=11)
        btn_left.bind(on_press=lambda x: self.open_file_selector(0, btn_left))
        btn_right.bind(on_press=lambda x: self.open_file_selector(1, btn_right))
        photo_layout.add_widget(btn_left)
        photo_layout.add_widget(btn_right)
        layout.add_widget(photo_layout)

        # 6. お客様サイン欄（バグ修正・完全復活）
        layout.add_widget(Label(text="【お客様御検印】(白枠内にサインを受領してください)", size_hint_y=None, height=20, bold=True, color=(0,0,0,1)))
        self.sign_pad = SignPad(size_hint_y=None, height=100)
        with self.sign_pad.canvas.before:
            KivyColor(0.98, 0.98, 0.98, 1)
            from kivy.graphics import Rectangle
            self.rect = Rectangle(pos=self.sign_pad.pos, size=(400, 100))
        layout.add_widget(self.sign_pad)

        # ボタンエリア
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        clear_btn = Button(text="サインをやり直す", background_color=(0.7, 0.2, 0.2, 1))
        clear_btn.bind(on_press=lambda x: self.sign_pad.clear_canvas())
        
        pdf_btn = Button(text="サイン完了・PDFを出力", background_color=(0.1, 0.5, 0.1, 1), bold=True)
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
            file_path = filedialog.askopenfilename(
                title="挿入する現場写真を選択してください",
                filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
            )
            if file_path:
                filename_only = os.path.basename(file_path)
                button_instance.text = f"選択済\n{filename_only[:12]}..." 
                button_instance.background_color = (0.2, 0.5, 0.8, 1)
                self.selected_photos[index] = file_path
        except Exception as e:
            print(f"ファイル選択エラー: {e}")

    # ==========================================
    # 🚀 【改善反映版】PDF生成流し込みエンジン
    # ==========================================
    def generate_pdf(self, instance):
        try:
            sig_file = self.sign_pad.save_to_image("temp_signature.png")
            pdf_filename = os.path.join(BASE_DIR, "作業完了報告書.pdf")
            template_path = os.path.join(BASE_DIR, "template_format.png")

            if not os.path.exists(template_path):
                self.status_label.text = "エラー: template_format.png が見つかりません"
                return

            c = canvas.Canvas(pdf_filename, pagesize=(595, 842))
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
            
            # 1階：背景画像を全面に敷く
            c.drawImage(template_path, 0, 0, width=595, height=842)

            # 2階：割り出した正確な座標（黄金座標）にデータを流し込みます
            # A. 基本情報
            c.setFont('HeiseiKakuGo-W5', 11)
            c.drawString(110, 768, self.client_input.text)  # お客様名 (Y768)
            c.drawString(110, 738, self.subject_input.text) # 件名 (Y738)

            # B. 管理グリッドテーブル (すべて Y685 に美しく一列配置)
            c.setFont('HeiseiKakuGo-W5', 9.5)
            c.drawCentredString(124, 685, self.date_input.text)     # 実施日
            c.drawCentredString(215, 685, self.month_input.text)    # 月度
            c.drawCentredString(290, 685, self.seiban_input.text)   # 製番
            c.drawCentredString(390, 685, self.setsubi_input.text)  # 設備
            c.drawCentredString(465, 685, self.member_shonin.text)  # 承認 (アプリから取得)
            c.drawCentredString(502, 685, self.member_sakusei.text) # 作成 (アプリから取得)
            c.drawCentredString(539, 685, self.member_sagyo.text)   # 作業 (アプリから取得)

            # C. 1. 作業内容 (ノート罫線ピッチ Y17.0)
            c.setFont('HeiseiKakuGo-W5', 10)
            draw_w_y = 618
            for line in self.work_input.text.split('\n'):
                c.drawString(60, draw_w_y, line)
                draw_w_y -= 17.0

            # D. 2. 結果・処置 (ノート罫線ピッチ Y17.0)
            draw_r_y = 503
            for line in self.result_input.text.split('\n'):
                c.drawString(60, draw_r_y, line)
                draw_r_y -= 17.0

            # 💡 ★大幅改善：画像を歪ませず、指定枠いっぱいにトリミング拡大(最大化)して描画する高度な関数
            def draw_photo_crop_fill(canvas_obj, img_path, tx, ty, tw, th):
                if img_path and os.path.exists(img_path):
                    with PILImage.open(img_path) as pil_img:
                        iw, ih = pil_img.size
                    
                    # 枠を完全に満たすための拡大率を計算 (maxを使用)
                    ratio = max(float(tw) / iw, float(th) / ih)
                    fw, fh = iw * ratio, ih * ratio
                    
                    # 枠の中心に合わせるためのオフセット
                    ox = tx + (tw - fw) / 2.0
                    oy = ty + (th - fh) / 2.0
                    
                    # 描画範囲をその枠だけに固定（はみ出しをカットするマスクをかける）
                    canvas_obj.saveState()
                    p = canvas_obj.beginPath()
                    p.rect(tx, ty, tw, th)
                    canvas_obj.clipPath(p, stroke=0, fill=0)
                    
                    # 画像を描画
                    canvas_obj.drawImage(img_path, ox, oy, width=fw, height=fh)
                    canvas_obj.restoreState()

            # --- E. 写真＆ファイル名の流し込み (左右反転バグを修正) ---
            c.setFont('HeiseiKakuGo-W5', 7.5)
            
            # 左写真枠 (X56〜298、Y124〜296) -> 写真1をトリミングいっぱいに拡大貼り付け
            if self.selected_photos[0]:
                draw_photo_crop_fill(c, self.selected_photos[0], 56, 124, (298-56), (296-124))
                # 拡張子を除去してファイル名を印字 (Y106〜120の範囲)
                name_without_ext = os.path.splitext(os.path.basename(self.selected_photos[0]))[0]
                c.drawString(60, 110, name_without_ext)

            # 右写真枠 (X308〜550、Y124〜296) -> 写真2をトリミングいっぱいに拡大貼り付け
            if self.selected_photos[1]:
                draw_photo_crop_fill(c, self.selected_photos[1], 308, 124, (550-308), (296-124))
                # 拡張子を除去してファイル名を印字 (Y106〜120の範囲)
                name_without_ext = os.path.splitext(os.path.basename(self.selected_photos[1]))[0]
                c.drawString(312, 110, name_without_ext)

            # F. 最下部：時間 (Y84へ配置)
            c.setFont('HeiseiKakuGo-W5', 10)
            c.drawString(135, 84, self.time_work_input.text)
            c.drawString(425, 84, self.time_move_input.text)

            # G. お客様御検印（新指定枠：X470〜556、Y52〜72 に完全格納）
            if os.path.exists(sig_file):
                c.drawImage(sig_file, 470, 52, width=(556-470), height=(72-52))

            # --- PDFを確定・保存 ---
            c.showPage()
            c.save()

            if os.path.exists(sig_file):
                os.remove(sig_file)

            self.status_label.text = "成功: フォーマット完全一致のPDFを出力しました！"
            
        except Exception as e:
            self.status_label.text = f"エラー: {str(e)}"

if __name__ == '__main__':
    ReportApp().run()
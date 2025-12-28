import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
import threading
import os
import sys

# 1. exe化した時に画像を見失わないため
def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class KairuAssistant:
    def __init__(self):
        self.root = tk.Tk()
        
        # --- ウィンドウの設定 ---
        self.root.overrideredirect(True)      # 枠を消す
        self.root.wm_attributes("-topmost", True)  # 常に最前面
        self.root.wm_attributes("-transparentcolor", "black") # 黒を透明にする
        
        # --- 音声エンジンの初期化 ---
        self.engine = pyttsx3.init()
        
        # --- 画像（Kairu.png）の読み込み ---
        try:
            self.img_path = get_path("Kairu.png") # ここをKairu.pngに変更済み
            self.img = Image.open(self.img_path).convert("RGBA")
            self.photo = ImageTk.PhotoImage(self.img)
        except Exception as e:
            print(f"画像が見つかりません: {e}")
            # 画像がない場合、代わりに小さな文字を表示
            self.photo = tk.PhotoImage(width=1, height=1)
            tk.Label(self.root, text="Kairu.png not found").pack()

        # キャラクターを表示するラベル
        self.label = tk.Label(self.root, image=self.photo, bg="black", bd=0)
        self.label.pack()

        # --- マウス操作の設定 ---
        self.label.bind("<Button-1>", self.on_left_click)  # 左クリック
        self.label.bind("<Button-3>", self.show_menu)      # 右クリック
        self.label.bind("<B1-Motion>", self.on_drag)       # ドラッグ移動

        # --- 右クリックメニュー（カイル君仕様） ---
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="挨拶する", command=self.say_hello)
        self.menu.add_command(label="お前を消す方法", command=self.vanishing_joke)
        self.menu.add_command(label="鉄道運行情報(仮)", command=lambda: self.speak("ダイヤは平常通りです。出発進行！"))
        self.menu.add_separator()
        self.menu.add_command(label="カイル君を終了", command=self.root.destroy)

    # --- 動作メソッド ---
    def speak(self, text):
        """別スレッドでしゃべる（画面をフリーズさせない）"""
        def _target():
            self.engine.say(text)
            self.engine.runAndWait()
        threading.Thread(target=_target, daemon=True).start()

    def say_hello(self):
        self.speak("こんにちは！何かお困りですか？")

    def vanishing_joke(self):
        self.speak("お前を消す方法…？ そんなことより、一緒に電車の旅にでも行きませんか？")

    def on_left_click(self, event):
        self.speak("はい、何でしょうか！")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def on_drag(self, event):
        # キャラクターの真ん中を掴んで動かせるように計算
        x = self.root.winfo_pointerx() - (self.photo.width() // 2)
        y = self.root.winfo_pointery() - (self.photo.height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KairuAssistant()
    app.run()

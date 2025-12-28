import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
import threading
import os
import sys

# 1.（exe化した時に画像を見失わないため）
def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class DesktopAssistant:
    def __init__(self):
        self.root = tk.Tk()
        
        # --- ウィンドウの設定 ---
        self.root.overrideredirect(True) # 枠を消す
        self.root.wm_attributes("-topmost", True) # 常に最前面
        self.root.wm_attributes("-transparentcolor", "black") # 黒を透明化
        
        # --- 音声エンジンの初期化 ---
        self.engine = pyttsx3.init()
        
        # --- 画像の読み込み ---
        try:
            self.img_path = get_path("character.png")
            self.img = Image.open(self.img_path).convert("RGBA")
            self.photo = ImageTk.PhotoImage(self.img)
        except Exception as e:
            print(f"画像が見つかりません: {e}")
            # 画像がない場合、代わりに赤い四角を表示（エラー落ち防止）
            self.photo = tk.PhotoImage(width=100, height=100)

        # キャラクターを表示するラベル
        self.label = tk.Label(self.root, image=self.photo, bg="black", bd=0)
        self.label.pack()

        # --- イベントの設定 ---
        self.label.bind("<Button-1>", self.on_left_click)  # 左クリ
        self.label.bind("<Button-3>", self.show_menu)      # 右クリ
        self.label.bind("<B1-Motion>", self.on_drag)       # ドラッグ

        # --- 右クリックメニューの内容 ---
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="挨拶する", command=lambda: self.speak("出発進行！"))
        self.menu.add_command(label="運行状況(開発中)", command=lambda: self.speak("ダイヤは正常です。"))
        self.menu.add_separator()
        self.menu.add_command(label="終了", command=self.root.destroy)

    # --- 動作メソッド ---
    def speak(self, text):
        """別スレッドでしゃべる（アプリをフリーズさせない）"""
        def _target():
            self.engine.say(text)
            self.engine.runAndWait()
        threading.Thread(target=_target, daemon=True).start()

    def on_left_click(self, event):
        self.speak("なにか御用ですか？")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def on_drag(self, event):
        # マウスの位置に合わせてウィンドウを動かす
        x = self.root.winfo_pointerx() - (self.photo.width() // 2)
        y = self.root.winfo_pointery() - (self.photo.height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DesktopAssistant()
    app.run()

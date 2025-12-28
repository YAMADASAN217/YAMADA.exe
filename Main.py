import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
import threading
import os
import sys
import datetime

def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class KairuAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "black")

        self.engine = pyttsx3.init()

        # --- 1. 画像の読み込み（指定のファイル名に変更！） ---
        try:
            # ファイル
            self.img_name = "20200307093104.png"
            self.img_path = get_path(self.img_name)
            self.img = Image.open(self.img_path).convert("RGBA")
            self.photo = ImageTk.PhotoImage(self.img)
        except Exception as e:
            print(f"画像読み込みエラー: {e}")
            self.photo = tk.PhotoImage(width=100, height=100)

        self.label = tk.Label(self.root, image=self.photo, bg="black", bd=0)
        self.label.pack()

        # --- 2. 字幕ウィンドウの作成 ---
        self.msg_win = tk.Toplevel(self.root)
        self.msg_win.overrideredirect(True)
        self.msg_win.wm_attributes("-topmost", True)
        self.msg_win.wm_attributes("-transparentcolor", "black")
        
        # 黄色い太文字でカイル君らしさを演出
        self.msg_label = tk.Label(self.msg_win, text="", font=("MS UI Gothic", 14, "bold"), 
                                  fg="#FFFF00", bg="black", wraplength=200)
        self.msg_label.pack()
        self.msg_win.withdraw() # 最初は隠しておく

        # --- 3. イベント登録 ---
        self.label.bind("<Button-1>", self.on_left_click)
        self.label.bind("<Button-3>", self.show_menu)
        self.label.bind("<B1-Motion>", self.on_drag)

        # --- 4. 右クリックメニュー ---
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="挨拶する", command=self.say_hello)
        self.menu.add_command(label="時刻と運行状況", command=self.check_rail_time)
        self.menu.add_command(label="お前を消す方法", command=self.vanishing_joke)
        self.menu.add_separator()
        self.menu.add_command(label="カイル君を片付ける", command=self.root.destroy)

    def speak(self, text):
        """字幕を表示しながらしゃべる"""
        self.msg_label.config(text=text)
        self.msg_win.deiconify()
        # カイル君の少し上に字幕を表示
        self.msg_win.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y() - 40}")
        
        def _target():
            self.engine.say(text)
            self.engine.runAndWait()
            # 3秒後に字幕を消す
            self.root.after(3000, self.msg_win.withdraw)
            
        threading.Thread(target=_target, daemon=True).start()

    def say_hello(self):
        self.speak("こんにちは！何かお手伝いしましょうか？")

    def check_rail_time(self):
        now = datetime.datetime.now()
        msg = f"現在は{now.hour}時{now.minute}分。ダイヤは非常に正確です！"
        self.speak(msg)

    def vanishing_joke(self):
        self.speak("お前を消す方法？ そんな悲しいこと言わないでくださいよ。")

    def on_left_click(self, event):
        self.speak("はい！準備はできています！")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def on_drag(self, event):
        x = self.root.winfo_pointerx() - (self.photo.width() // 2)
        y = self.root.winfo_pointery() - (self.photo.height() // 2)
        self.root.geometry(f"+{x}+{y}")
        # ドラッグ中も字幕を隠す（位置がズレるのを防ぐため）
        self.msg_win.withdraw()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KairuAssistant()
    app.run()

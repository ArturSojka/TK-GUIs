import os
import json
import tkinter as tk
import math
from wallpapers import Wallpaper, Wallpapers, WallpaperFactory


class DisplayFrame(tk.Frame):

    def __init__(self, master, master_w, master_h, wallpapers: Wallpapers):
        super().__init__(master, bg='red')
        self._wallpapers: Wallpapers = wallpapers
        self.current_bbox: list[int] = Wallpaper.default_bbox()
        self.current_tk_image = None

        img_width, img_height = Wallpaper.default_size()
        ratio = min(master_w / img_width, master_h / img_height)
        self.re_size = (math.ceil(img_width * ratio), math.ceil(img_height * ratio))
        self.canvas_center: tuple[float, float] = (master_w / 2, master_h / 2)
        self.speed = 1
        self.notif_sprites = []
        self.sprite = None

        self.canvas: tk.Canvas = tk.Canvas(self, width=master_w, height=master_h, highlightthickness=0, bg='blue')
        self.canvas.pack()
        self.change_image()
        self.bind_keys()

    def initial_render(self, reset=False):
        if reset:
            self.current_bbox = Wallpaper.default_bbox()
        else:
            self.current_bbox = self._wallpapers.current_wallpaper.bbox.copy()
        self.current_tk_image = self._wallpapers.crop_current_image(self.current_bbox, self.re_size)
        prev = self.sprite
        self.sprite = self.canvas.create_image(*self.canvas_center, image=self.current_tk_image)
        if prev is not None:
            self.canvas.delete(prev)

    def render_image(self, delta_x=1):
        self.current_bbox[0] = max(0, min(self.current_bbox[0] + self.speed * delta_x, 935))
        self.current_bbox[2] = max(2905, min(self.current_bbox[2] + self.speed * delta_x, 3840))
        self.current_tk_image = self._wallpapers.crop_current_image(self.current_bbox, self.re_size)
        prev = self.sprite
        self.sprite = self.canvas.create_image(*self.canvas_center, image=self.current_tk_image)
        self.canvas.delete(prev)

    def change_image(self):
        if self._wallpapers.current_wallpaper is not None:
            self._wallpapers.current_wallpaper.bbox = self.current_bbox
        self._wallpapers.next_wallpaper()
        self.initial_render()

    def change_speed(self, delta):
        self.speed = max(self.speed + delta, 0)
        self.show_notif(f"speed={self.speed}")

    def show_notif(self, message):
        x, y = self.canvas_center
        self.notif_sprites.append(self.canvas.create_rectangle(x * 2 - 200, y * 2 - 100, x * 2, y * 2, fill='black'))
        self.notif_sprites.append(self.canvas.create_text((x * 2 - 100, y * 2 - 50), text=message, fill='white', font=('Consolas', 18)))

    def hide_notif(self):
        self.canvas.delete(*self.notif_sprites)
        self.notif_sprites.clear()

    def bind_keys(self):
        self.master.bind("<Escape>", lambda e: (self._wallpapers.save_json(), e.widget.withdraw(), e.widget.quit()))
        self.master.bind("<Left>", lambda e: self.render_image(-1))
        self.master.bind("<KeyPress-Right>", lambda e: self.render_image(1))
        self.master.bind("<KeyPress-Up>", lambda e: self.change_speed(1))
        self.master.bind("<KeyRelease-Up>", lambda e: self.master.after(50, self.hide_notif))
        self.master.bind("<KeyPress-Down>", lambda e: self.change_speed(-1))
        self.master.bind("<KeyRelease-Down>", lambda e: self.master.after(50, self.hide_notif))
        self.master.bind("<KeyPress-Tab>", lambda e: (self.initial_render(reset=False), self.show_notif("Cofnięto zmiany")))
        self.master.bind("<KeyRelease-Tab>", lambda e: self.master.after(50, self.hide_notif))
        self.master.bind("<KeyPress-space>", lambda e: (self.initial_render(reset=True), self.show_notif("Wyśrodkowano")))
        self.master.bind("<KeyRelease-space>", lambda e: self.master.after(50, self.hide_notif))
        self.master.bind("<Return>", lambda e: self.change_image())


def main():
    if not os.path.isdir('raw'):
        os.mkdir('raw')

    if not os.path.isdir('edited'):
        os.mkdir('edited')

    if not os.path.isfile('wallpapers.json'):
        with open('wallpapers.json', 'w') as f:
            json.dump(dict(), f)

    raw_w = WallpaperFactory.from_raw()
    try:
        bookmarks_w = WallpaperFactory.from_bookmarks()
    except FileNotFoundError:
        bookmarks_w = []
    json_w = WallpaperFactory.from_json()
    wallpapers = Wallpapers(*raw_w, *bookmarks_w, *json_w)

    window = tk.Tk()
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.overrideredirect(True)
    window.geometry(f"{w}x{h}+0+0")
    frame = DisplayFrame(window, w, h, wallpapers)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    frame.grid(row=0, column=0, sticky='nsew')

    window.mainloop()


if __name__ == '__main__':
    main()

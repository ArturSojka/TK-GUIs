import os
from dataclasses import dataclass
from typing import Optional
import json
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import aiofiles
from PIL import Image, ImageTk


@dataclass
class Wallpaper:
    file_name: str
    file_path: str
    bbox: list[int]
    site_url: Optional[str] = None
    image_url: Optional[str] = None

    @property
    def frame(self) -> tuple[int, int, int]:
        season = int(self.file_name[-13:-12])
        episode = int(self.file_name[-11:-9])
        frame = int(self.file_name[-8:-4])
        return (season, episode, frame)

    @staticmethod
    def default_bbox() -> list[int]:
        return [468, 263, 3373, 1897]

    @staticmethod
    def default_size() -> tuple[int, int]:
        return (2905, 1634)


class WallpaperFactory:

    @staticmethod
    def from_raw() -> list[Wallpaper]:
        files = os.listdir('raw')
        result = []
        for file_name in files:
            if file_name.endswith('.jpg'):
                result.append(Wallpaper(
                    file_name=os.path.basename(file_name),
                    file_path=os.path.join('raw', file_name),
                    bbox=Wallpaper.default_bbox()
                ))
        return result

    @staticmethod
    def from_json() -> list[Wallpaper]:
        with open('wallpapers.json', 'r') as f:
            wallpapers: list[Wallpaper] = [Wallpaper(
                    file_path=w['file_path'],
                    file_name=w['file_name'],
                    bbox=w['bbox'],
                    site_url=w['site_url'],
                    image_url=w['image_url']
                ) for w in json.load(f).values()]
        return wallpapers

    @staticmethod
    def from_bookmarks() -> list[Wallpaper]:
        if not os.path.isfile('bookmarks.html'):
            raise FileNotFoundError('bookmarks.html not found')
        site_links: list[str] = []
        with open('bookmarks.html', 'r') as f:
            bs4: BeautifulSoup = BeautifulSoup(f, 'html.parser')
        for tag in bs4.find_all('a'):
            href = tag.get('href')
            if href.startswith('https://www.cap-that.com'):
                site_links.append(href)
        result = []
        for link in site_links:
            file_name = link.split('=')[-1]
            result.append(Wallpaper(
                file_name=file_name,
                file_path=os.path.join('raw', file_name),
                bbox=Wallpaper.default_bbox(),
                site_url=link
            ))
        return result


class Wallpapers:
    def __init__(self, *wallpapers: Wallpaper):
        self.wallpapers = {w.file_name: w for w in wallpapers}
        self._fix_site_urls()
        self._fix_image_urls()
        asyncio.run(self._download_images())

        self.current_wallpaper: Wallpaper | None = None
        self.current_image: Image.Image | None = None
        self.wallpaper_generator = (w for w in self.wallpapers.values())

    def save_json(self):
        with open('wallpapers.json', 'w') as file:
            json.dump(self.wallpapers, file, indent=2, default=vars)

        for wallpaper in self.wallpapers.values():
            image = Image.open(wallpaper.file_path).crop(wallpaper.bbox)
            image.save(os.path.join("edited", wallpaper.file_name), quality=95)

    def crop_current_image(self, bbox, size) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(self.current_image.crop(bbox).resize(size))

    def next_wallpaper(self) -> None:
        try:
            w = next(self.wallpaper_generator)
            self.current_wallpaper = w
            self.current_image = Image.open(w.file_path)
        except StopIteration:
            pass

    def _fix_site_urls(self) -> None:
        for w in self.wallpapers.values():
            if w.site_url is None:
                url = f"https://www.cap-that.com/starwars/the-bad-batch/{w.frame[0]}{w.frame[1]:02d}"
                if w.frame[0] == 1:
                    url += f"/2160/index.php?image={w.file_name}"
                else:
                    url += f"/index.php?image={w.file_name}"
                w.site_url = url

    def _fix_image_urls(self) -> None:
        for w in self.wallpapers.values():
            if w.image_url is None:
                url = f"https://s3.us-west-1.wasabisys.com/cap-that.com/tv/star-wars/the-bad-batch/{w.frame[0]}{w.frame[1]:02d}"
                if w.frame[0] == 1:
                    url += f"/2160-optimised/images/{w.file_name}"
                else:
                    url += f"/images-optimised/{w.file_name}"
                w.image_url = url

    async def _download_image(self, session: aiohttp.ClientSession, w: Wallpaper) -> None:
        async with session.get(w.image_url) as response:
            if response.status == 200:
                img = await response.read()
                async with aiofiles.open(w.file_path, 'wb') as f:
                    await f.write(img)

    async def _download_images(self) -> None:
        to_download = []
        for w in self.wallpapers.values():
            if not os.path.isfile(w.file_path):
                to_download.append(w)

        async with aiohttp.ClientSession() as session:
            tasks = [self._download_image(session, w) for w in to_download]
            await asyncio.gather(*tasks)


def main():
    raw_w = WallpaperFactory.from_raw()
    try:
        bookmarks_w = WallpaperFactory.from_bookmarks()
    except FileNotFoundError:
        bookmarks_w = []
    json_w = WallpaperFactory.from_json()
    wallpapers = Wallpapers(
        *raw_w,
        *bookmarks_w,
        *json_w
    )
    wallpapers.save_json()

    print(wallpapers.wallpapers)


if __name__ == '__main__':
    main()

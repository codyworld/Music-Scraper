import curses
import urllib.request

from scrapy.crawler import CrawlerProcess

from music_scrapper.gui import GUI
from music_scrapper.threads import GuiThread
from music_scrapper.spiders.music_spider import MusicSpider


def start_gui(process):
    def create_ui(screen):
        GUI.screen = screen
        GUI.strings = []
        GUI.init_display()
        GUI.update_on_key()

    curses.wrapper(create_ui)
    process.stop()


def main():
    process = CrawlerProcess({'LOG_ENABLED': False})
    message = ''
    while message == '':
        message = input("Give me something to start with - (Example: senjittale song download ) : ")
    s = urllib.request.quote(message)
    MusicSpider.start_urls = [
        "http://www.google.com/search?q=" + s,
    ]
    process.crawl(MusicSpider)
    thread = GuiThread(process, start_gui)
    thread.start()
    process.start()
    if len(GUI.strings) == 0:
        GUI.box.erase()
        GUI.box.addstr(0, 0, "No Results Found... Try with Some other keywords.", GUI.high_light_text)
        GUI.box.addstr(curses.LINES - 1, 0, "ESC:Exit", GUI.high_light_text)
        GUI.box.addstr(curses.LINES - 1, curses.COLS // 2, "ENTR:Download", GUI.high_light_text)
        GUI.screen.refresh()
        GUI.box.refresh()
from extension import Extension
from seleniumbase import Driver

import os, time


class Browser():
    def __init__(self,
                 target_url: str,
                 headless: bool=False,
                 bypass: bool=False,
                 proxy: str=None) -> None:


        self.target_url = target_url
        self.headless = headless
        self.bypass = bypass
        self.proxy = proxy
        self.extension_dir = os.getcwd() + '\\1.9.9_0'
        self.session = self.spawn_browser()
        self.ext = Extension(self.session)

    def spawn_browser(self):
        driver = Driver(
            browser = 'chrome',
            headless = False,
            headless2 = self.headless,
            incognito = True,
            dark_mode = True,
            devtools = False,
            uc = True,
            extension_dir=self.extension_dir
        )
        driver.open(self.target_url)
        return driver

    def open_page(self, url: str) -> None:
        self.session.open(url)
        
    def refresh(self) -> None:
        self.session.refresh()
        
    def get_page_source(self) -> str:
        return self.session.page_source
    
    def get_current_url(self) -> str:
        return self.session.current_url
    
    def get_page_title(self) -> str:
        return self.session.title.lower()

    def quit_browser(self) -> None:
        print('Quitting browser...')
        self.session.quit()








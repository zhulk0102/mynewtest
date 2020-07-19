# -*- coding: utf-8 -*-
"""
@Time ： 2019/12/26 11:53
@Auth ： zhulk

"""

import time
from selenium import webdriver
from config.settings import driverPath,DRIVER_MODE,DRIVER_URL,DRIVER_PORT,reportPath
from common.ownerror import UnSupportBrowserTypeError,UnSupportDriverModeError,UrlError
from common.log import Log
import os
from utils import page_utils


PhantomjsPath = driverPath + r'\phantomjs.exe'
FireFoxPath = driverPath + r'\geckodriver.exe'
ChromedriverPath = driverPath + r'\chromedriver.exe'
EdgedriverPath = driverPath + r'\MicrosoftWebDriver.exe'
IeDriverPath = driverPath + r'\IEDriverServer.exe'

TYPES = {'phantomjs': webdriver.PhantomJS,
         'firefox': webdriver.Firefox,
         'chrome': webdriver.Chrome,
         'edge': webdriver.Edge,
         'ie': webdriver.Ie}

OPTIONS_PATH = {'firefox': webdriver.FirefoxOptions,
                'chrome': webdriver.ChromeOptions,
                'ie': webdriver.IeOptions,
                }

EXECUTABLE_PATH = {'phantomjs': PhantomjsPath,
                   'firefox': FireFoxPath,
                   'chrome': ChromedriverPath,
                   'edge': EdgedriverPath,
                   'ie': IeDriverPath}

chrome_arguments = [
    '--disable-gpu',  # 谷歌文档提到需要加上这个属性来规避bug
    'disable-infobars',  # 隐藏"Chrome正在受到自动软件的控制"
    'lang=zh_CN.UTF-8',  # 设置成中文
    #'blink-settings=imagesEnabled=false',  # 提升速度
    'window-size=1920x3000'  # 指定浏览器分辨率
    # '--hide-scrollbars'        # 隐藏滚动条, 应对一些特殊页面
]


OPTIONS = {
    'chrome_options': {
        'arguments': chrome_arguments,
    },
}

log =Log()
class Browser(object):
    def __init__(self,browser_type='chrome'):
        self.type = browser_type.lower()
        if self.type in TYPES:
            self.browser = TYPES[self.type]
        else:
            raise UnSupportBrowserTypeError('仅支持: %s!' % ', '.join(TYPES.keys()))
        self.driver = None
        self.options = None
        self.browser_type = browser_type

    def _set_driver(self):
        if self.type == 'chrome':
            self.set_options(OPTIONS)
            if DRIVER_MODE == 'local':
                self.driver = self.browser(executable_path=EXECUTABLE_PATH[self.type], chrome_options=self.options, )
            elif DRIVER_MODE == 'remote':
                self.driver = webdriver.Remote(
                    command_executor='%s:%s/wd/hub' % (DRIVER_URL,DRIVER_PORT),
                    desired_capabilities={
                        'platform': 'ANY',
                        'browserName': self.type,
                        'version': '',
                        'javascriptEnabled': True,
                    }
                )
            else:
                raise UnSupportDriverModeError(
                '%s,错误的驱动模式，请在setting中配置DRIVER_MODE的值为remote或者local!' % DRIVER_MODE)
        elif self.type == 'firefox':
            self.driver = self.browser(executable_path=EXECUTABLE_PATH[self.type], firefox_options=self.options, )
        elif self.type == 'ie':
            self.driver = self.browser(executable_path=EXECUTABLE_PATH[self.type], ie_options=self.options, )
        else:
            self.driver = self.browser(executable_path=EXECUTABLE_PATH[self.type], )

    def set_options(self, options):
        if self.options is None:
            if self.type in OPTIONS_PATH:
                self.options = OPTIONS_PATH[self.type]()
        else:
            raise UnSupportBrowserTypeError('提供配置支持的浏览器: %s!' % ', '.join(OPTIONS_PATH.keys()))
        if self.type == 'chrome':
            _browser = "%s_%s" % (self.type, 'options')
            # 添加参数
            [self.options.add_argument(argument) for argument in options[_browser]['arguments']]

    #调用此方法后可继续调用其他方法
    def to(self,url, maximize_window=True, implicitly_wait=30):
        self._set_driver()
        if page_utils.is_valid_url:
            self.driver.get(url)
            if maximize_window:
                self.driver.maximize_window()
            self.driver.implicitly_wait(implicitly_wait)
            log.info("open the default page: %s" % self.current_url)
            return self
        else:
            raise UrlError("this url is error")

    @property
    def current_url(self):
        current_url = self.driver.current_url
        return current_url

    @property
    def title(self):
        title = self.driver.title
        log.info("get current page title: %s" % title)
        return title

    def wait(self, seconds=1):
        time.sleep(seconds)
        log.info("wait %f seconds" % seconds)

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()
        log.info("quit browser")

    def close(self):
        self.driver.close()
        log.info("close the current page: %s" % self.current_url)

    def refresh(self):
        self.driver.refresh()
        log.info("page refresh: %s" % self.current_url)

    def forward(self):
        self.driver.forward()
        log.info("page forward to the: %s" % self.current_url)

    def back(self):
        self.driver.back()
        log.info("page back to the: %s" % self.current_url)

    def get_source(self):
        log.info("page soure to the: %s" % self.current_url)
        return self.driver.page_source

    def get_title(self):
        log.info("page title to the: %s" % self.current_url)
        return self.driver.title

    @property
    def current_window(self):
        handle = self.driver.current_window_handle
        log.info("get current page handle: %s" % handle)
        return handle

    def switch_to_window(self, partial_url='', partial_title=''):
        """切换窗口
            如果窗口数<3,不需要传入参数，切换到当前窗口外的窗口；
            如果窗口数>=3，则需要传入参数来确定要跳转到哪个窗口
        """
        all_windows = self.driver.window_handles
        if len(all_windows) == 1:
            log.warning('只有1个window!')
        elif len(all_windows) == 2:
            other_window = all_windows[1 - all_windows.index(self.current_window)]
            self.driver.switch_to.window(other_window)
        else:
            for window in all_windows:
                self.driver.switch_to.window(window)
                if partial_url in self.current_url or partial_title in self.title:
                    break
        log.info("switch window to the: %s" % self.current_url)

    def save_screen_shot(self, name='screen_shot'):
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        screenshot_path = reportPath + r'\screenshot_%s' % day
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        tm = time.strftime('%H%M%S', time.localtime(time.time()))
        self.driver.save_screenshot(screenshot_path + '\\%s_%s.png' % (name, tm))
        log.info("capture page images: %s" % screenshot_path + '\\%s_%s.png' % (name, tm))
        return screenshot_path + r'\%s_%s.png' % (name, tm)


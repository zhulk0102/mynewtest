# -*- coding: utf-8 -*-
"""
@Time ： 2019/12/27 11:02
@Auth ： zhulk

"""
from selenium.webdriver.common.by import By
from common.browser import Browser
from common.log import Log
from config.settings import TIMEOUT,JSCHECK,TEXT_XPATH,INTERVAL_TIME
from common.ownerror import SendKeysNoneError
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException,NoSuchElementException, StaleElementReferenceException
from utils import page_utils
from selenium.webdriver.remote.command import Command
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import win32con
import win32gui

log =Log()
class basePage(Browser):

    def find_elements(self,selector,by=By.CSS_SELECTOR,timeout=TIMEOUT,js_check = JSCHECK):
        if js_check:
            self.judge_js_error()
        _selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        log.debug("find elements:(%s, %s)" % (by, selector))
        try:
            self.driver_wait(selector, timeout, by)
        except Exception as e:
            log.error('find elements:(%s, %s) error, info: %s.' % (by, selector, e))
            return False
        web_elements = self.driver.find_elements(by, selector)
        if len(web_elements) == 1:
            self.execute("arguments[0].focus();", web_elements[0])
            if 'iframe' not in _selector:
                self.alter_attribute('style', 'border: 2px solid red;', web_elements[0])
            return web_elements[0]
        else:
            return web_elements

    def __recalculate_selector(self, selector, by):
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
            return selector, by
        elif page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
            return selector, by
        elif page_utils.is_partial_link_text_selector(selector):
            selector = page_utils.get_partial_link_text_from_selector(selector)
            by = By.PARTIAL_LINK_TEXT
            return selector, by
        elif page_utils.is_name_selector(selector):
            name = page_utils.get_name_from_selector(selector)
            selector = '[name="%s"]' % name
            by = By.CSS_SELECTOR
            return selector, by
        elif page_utils.is_tag_selector(selector):
            tag = page_utils.get_tag_name_from_selector(selector)
            selector = tag
            by = By.TAG_NAME
            return selector, by
        elif by == By.LINK_TEXT or by == By.PARTIAL_LINK_TEXT:
            if self.browser == "safari" and selector.lower() != selector:
                selector = ("""//a[contains(translate(.,"ABCDEFGHIJKLMNOPQR"""
                            """STUVWXYZ","abcdefghijklmnopqrstuvw"""
                            """xyz"),"%s")]""" % selector.lower())
                by = By.XPATH
                return selector, by
        # 现在仅支持#和.开头的CSS检索
        elif not page_utils.is_css_selector(selector):
            selector = TEXT_XPATH % selector
            by = By.XPATH
            return selector, by
        else:
            return selector, by

    def __unpack(self, *args):
        if isinstance(args[0], WebElement):
            web_element = args[0]
        else:
            web_element = self.find_elements(*args)
        return web_element

    def judge_js_error(self):
        self.wait(0.5)
        try:
            browser_logs = self.driver.get_log('browser')
        except (ValueError, WebDriverException) as e:
            log.debug("Could not get browser logs for driver due to exception: %s" %e)
            return []
        errors = []
        for entry in browser_logs:
            if entry['level'] == 'SEVERE':
                errors.append(entry)
        if len(errors) > 0:
            raise Exception(
                "JavaScript errors found on %s => %s" % (self.current_url, errors))
        return errors

    def driver_wait(self, selector, timeout=TIMEOUT, by=By.CSS_SELECTOR, ):
        WebDriverWait(self.driver, timeout).until(expected_conditions.presence_of_element_located((by, selector)))

    def execute(self, js, *args):
        self.driver.execute_script(js, *args)
        log.debug("execute javascript: %s" % js)

    def alter_attribute(self, name, value, web_element):
        if name == 'style':
            js = "arguments[0].setAttribute('style', '%s');" % value
        else:
            js = "arguments[0].%s = '%s';" % (name, value)
        self.execute(js, web_element)

    def click(self, selector, by=By.CSS_SELECTOR, timeout=TIMEOUT, js_check=JSCHECK):
        web_elements = self.__unpack(selector, by, timeout, js_check)
        if not web_elements:
            raise TimeoutError('find element error!')
        if isinstance(web_elements, list):
            web_element = web_elements[0]
        else:
            web_element = web_elements
        if self.type == "ie":
            self.driver.execute(Command.W3C_CLEAR_ACTIONS)
            self.execute("arguments[0].click();", web_element)
        else:
            try:
                self.wait(0.5)
                web_element.click()
            except Exception as e:
                self.execute("arguments[0].click();", web_element)
                log.info('click error %s.' % e)
        log.info("click element: %s" % selector)

    def js_click(self, selector, by=By.CSS_SELECTOR, timeout=TIMEOUT, js_check=JSCHECK):
        web_elements = self.__unpack(selector, by, timeout, js_check)
        if not web_elements:
            raise TimeoutError('find element error!')
        if isinstance(web_elements, list):
            web_element = web_elements[0]
        else:
            web_element = web_elements
        self.wait(1)
        self.execute("arguments[0].click();", web_element)
        log.info("click element: %s" % selector)

    def get(self,url):
        log.info("get to page {}".format(url))
        self.driver.get(url)

    def move_to(self, selector, by=By.CSS_SELECTOR, timeout=TIMEOUT, js_check=JSCHECK):
        web_elements = self.__unpack(selector, by, timeout, js_check)
        if not web_elements:
            raise TimeoutError('find element error!')
        if isinstance(web_elements, list):
            web_element = web_elements[0]
        else:
            web_element = web_elements
        action = ActionChains(self.driver)
        action.reset_actions()
        if self.type == 'ie':
            x = web_element.location['x']
            y = web_element.location['y']
            action.move_by_offset(x, y).perform()
        else:
            action.move_to_element(web_element).perform()
        log.info("click element: %s" % selector)


    def send_keys(self, selector, text, by=By.CSS_SELECTOR, timeout=TIMEOUT, js_check=JSCHECK):
        if text is None:
            raise SendKeysNoneError('Please input your text.')
        web_elements = self.__unpack(selector, by, timeout, js_check)
        if not web_elements:
            raise TimeoutError('find element error!')
        if isinstance(web_elements, list):
            web_element = web_elements[0]
        else:
            web_element = web_elements
        if self.is_displayed(web_element):
            try:
                web_element.clear()
            except Exception:
                self.click(selector)
                action_sendkeys = ActionChains(self.driver).click(self.find_elements(selector))
                action_sendkeys.send_keys(Keys.HOME).perform()
                action_sendkeys.send_keys(text).perform()
                return
        if self.type == "ie":
            text = str(text)
            for i in text:
                web_element.send_keys(i)
        else:
            web_element.send_keys(str(text))
        self.wait(0.5)
        log.info("send keys to element: %s value: %s" % (selector, text))

    def js_send_keys(self, selector, text, by=By.CSS_SELECTOR, timeout=TIMEOUT, js_check=JSCHECK):
        if text is None:
            raise SendKeysNoneError('Please input your text.')
        web_elements = self.__unpack(selector, by, timeout, js_check)
        if not web_elements:
            raise TimeoutError('find element error!')
        if isinstance(web_elements, list):
            web_element = web_elements[0]
        else:
            web_element = web_elements
        if self.is_displayed(web_element):
            web_element.clear()
        if self.type == "ie":
            text = str(text)
            for i in text:
                web_element.send_keys(i)
        else:
            js = "arguments[0].setAttribute('value', '%s');" % text
            self.execute(js,web_element)
        self.wait(0.5)
        log.info("send keys to element by js: %s value: %s" % (selector, text))


    def is_displayed(self, web_element):
        return web_element.is_displayed()

    def is_enabled(self, web_element):
        return web_element.is_enabled()

    def is_selected(self, web_element):
        return web_element.is_selected()

    def switch_to_frame(self, selector, by=By.CSS_SELECTOR, timeout=TIMEOUT):
        web_element = self.__unpack(selector, by, timeout)
        self.driver.switch_to.frame(web_element)
        log.info("switch to frame: {}".format(selector))

    def switch_to_parent_frame(self):
        self.driver.switch_to.parent_frame()
        log.info("switch to parent frame.")

    def switch_to_alert(self):
        return self.driver.switch_to.alert

    def get_attribute(self, selector, attr, by=By.CSS_SELECTOR):
        log.debug("get attributes to element:(%s, %s) name: %s" % (by, selector, attr))
        try:
            web_element = self.__unpack(selector, by)
            return getattr(web_element, attr) if hasattr(web_element, attr) else web_element.get_attribute(attr)
        except Exception:
            return ''

    def get_attributes(self, selector, attr, by=By.CSS_SELECTOR):
        values = []
        log.debug("get attributes to element:(%s, %s) name: %s" % (by, selector, attr))
        web_elements = self.__unpack(selector, by)
        for web_element in web_elements:
            try:
                values.append(
                    getattr(web_element, attr) if hasattr(web_element, attr) else web_element.get_attribute(attr))
            except Exception:
                values.append('')
        return values

    # 等待元素消失
    def wait_element_disapper(self, selector, interval_time=INTERVAL_TIME,by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        log.info('wait (%s, %s) begin.' % (by, selector))
        all_time = 0
        try:
            while self.driver.find_element(by, selector):
                self.wait(interval_time)
                all_time = all_time + interval_time
                if all_time >= 4:
                    log.info('wait (%s, %s, %f) timeout.' % (by, selector, all_time))
                    break
        except NoSuchElementException:
            log.info('wait (%s, %s) end.' % (by, selector))
        except StaleElementReferenceException:
            log.info('wait (%s, %s) end.' % (by, selector))


    # 元素没有消失，等待元素的display值由True变为False,或者由False变为True
    def wait_element_change_display(self, selector, interval_time=INTERVAL_TIME,by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        log.info('wait (%s, %s) begin.' % (by, selector))
        all_time = 0
        self.wait(0.5)
        self.driver_wait(selector=selector, by=by, timeout=5)
        if self.is_displayed(self.driver.find_element(by, selector)) is True:
            while self.is_displayed(self.driver.find_element(by, selector)) is True:
                self.wait(interval_time)
                all_time = all_time + interval_time
                if all_time >= 5:
                    log.info('wait (%s, %s, %f) true timeout.' % (by, selector, all_time))
                    break
        else:
            while self.is_displayed(self.driver.find_element(by, selector)) is False:
                self.wait(interval_time)
                all_time = all_time + interval_time
                if all_time >= 5:
                    log.info('wait (%s, %s, %f) false timeout.' % (by, selector, all_time))
                    break
        log.info('wait (%s, %s) end.' % (by, selector))

    # 元素没有消失，等待元素的属性值改变,默认获取元素的文本属性值
    def wait_element_change_attr(self, selector, attr_value, interval_time=INTERVAL_TIME,by=By.CSS_SELECTOR, attr='text' ):
        selector, by = self.__recalculate_selector(selector, by)
        log.info('wait (%s, %s, %s) begin.' % (by, selector, attr_value))
        all_time = 0
        self.driver_wait(selector=selector, by=by, timeout=5)
        while self.get_attribute(selector=self.driver.find_element(by, selector), attr=attr) in attr_value:
            self.wait(interval_time)
            all_time = all_time + interval_time
            if all_time >= 5:
                log.info('wait (%s, %s, %f) timeout.' % (by, selector, all_time))
                break
        log.info('wait (%s, %s, %s) end.' % (by, selector, attr_value))

    def upload_file(self, path):
        """上传附件"""
        self.wait(0.5)
        dialog = win32gui.FindWindow('#32770', u'打开')  # 识别对话框句柄
        combo_box_ex32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        combo_box = win32gui.FindWindowEx(combo_box_ex32, 0, 'ComboBox', None)
        edit = win32gui.FindWindowEx(combo_box, 0, 'Edit', None)  # 找到输入框Edit对象的句柄
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 找到按钮Button
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, path)  # 往输入框输入绝对地址
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
        self.wait(2.5)
        log.info("upload file: %s" % path)

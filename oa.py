import time
from selenium import webdriver
from selenium.webdriver.chrome import options as chrome_options
from selenium.webdriver.firefox import options as firefox_options
from selenium.webdriver.edge import options as edge_options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class OAConfig:
    def __init__(self, username: str, password: str,
                 timeout=60, headless=False, driver_path='auto',
                 browser_type='chrome', browser_path='auto') -> None:
        self._valid_config = True
        self.username = username.strip()
        self.password = password
        self.timeout = timeout

        self.headless = headless
        self.driver_path = driver_path

        b = browser_type.strip().lower()
        if (b != 'chrome' and b != 'firefox' and b != 'edge'):
            print('Unsupported browser')
            self.valid_config = False
            return
        self.browser_type = b
        del b

        self.browser_path = browser_path


class OA:
    def __init__(self, config: OAConfig) -> None:
        if not config._valid_config:
            print('Invalid config')
            return

        self.config = config
        self.is_logged_in = False
        print('Init for user', self.config.username)

    def _wait(self, by, locator) -> None:
        WebDriverWait(self.browser, self.config.timeout).until(
            EC.presence_of_element_located((by, locator)))

    def launch(self) -> None:
        "启动浏览器"

        print('Launching', self.config.browser_type)

        options = ''
        if (self.config.browser_type == 'chrome'):
            options = chrome_options.Options()
        elif (self.config.browser_type == 'firefox'):
            options = firefox_options.Options()
        elif (self.config.browser_type == 'edge'):
            options = edge_options.Options()

        if (self.config.browser_path != 'auto'):
            options.binary_location = self.config.browser_path
        if (self.config.headless):
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

        if (self.config.driver_path == 'auto'):
            if (self.config.browser_type == 'chrome'):
                self.browser = webdriver.Chrome(options=options)
            elif (self.config.browser_type == 'firefox'):
                self.browser = webdriver.Firefox(options=options)
            elif (self.config.browser_type == 'edge'):
                self.browser = webdriver.Edge(options=options)
        else:
            if (self.config.browser_type == 'chrome'):
                self.browser = webdriver.Chrome(
                    self.config.driver_path, options=options)
            elif (self.config.browser_type == 'firefox'):
                self.browser = webdriver.Firefox(
                    self.config.driver_path, options=options)
            elif (self.config.browser_type == 'edge'):
                self.browser = webdriver.Edge(
                    self.config.driver_path, options=options)

        self.browser.set_window_size(900, 920)

    def quit(self) -> None:
        "退出浏览器"

        self.browser.quit()
        print('Quited', self.config.browser_type)

    def update_config(self, config: OAConfig) -> None:
        "更新配置 (仅更新用户名和密码)"

        self.config.username = config.username
        self.config.password = config.password
        print('Updated config: username =', self.config.username)

    def login(self) -> None:
        "执行用户登录"

        print('Logging in')
        self.browser.get('https://id.sspu.edu.cn/cas/login')
        try:
            self.browser.find_element_by_class_name('success')
        except NoSuchElementException:
            self.is_logged_in = False
        else:
            print('Already logged in')
            self.is_logged_in = True
            return

        self._wait(By.CLASS_NAME, 'submit_button')

        # 用户名
        cur = self.browser.find_element_by_id('username')
        cur.send_keys(self.config.username)
        # 密码
        cur = self.browser.find_element_by_id('password')
        cur.send_keys(self.config.password)
        # 登录
        cur = self.browser.find_element_by_class_name('submit_button')
        cur.click()

        # 检查是否登录成功
        try:
            self.browser.find_element_by_class_name('success')
        except NoSuchElementException:
            print('Login failed')
            self.is_logged_in = False
            return
        print('Login success')
        self.is_logged_in = True

    def logout(self) -> None:
        "执行用户登出"

        self.browser.get('https://id.sspu.edu.cn/cas/login')

        try:
            self.browser.find_element_by_class_name('success')
        except NoSuchElementException:
            self.is_logged_in = False
            print('Not logged in')
            return

        self._wait(By.XPATH, '//*[@id="msg"]/p[3]/a[3]')
        cur = self.browser.find_element_by_xpath('//*[@id="msg"]/p[3]/a[3]')
        cur.click()
        print('Logged out')
        self.is_logged_in = False

    def apply(self) -> None:
        "申请出校"

        today = time.localtime(time.time())
        time_str = '00:00-12:00'
        if (today.tm_hour >= 12):
            time_str = '12:00-00:00'

        print('Jumping to apply page')
        # 跳转到申请页面
        url = 'https://oa.sspu.edu.cn/workflow/request/AddRequest.jsp?workflowid=2382'
        self.browser.get('https://oa.sspu.edu.cn/wui/main.jsp')
        self.browser.get(url)
        self._wait(By.ID, 'bodyiframe')

        print('Checking')
        # 切换 iFrame
        iframe = self.browser.find_element_by_id('bodyiframe')
        self.browser.switch_to.frame(iframe)
        self._wait(By.ID, 'field11237span')
        self._wait(By.ID, 'field11250browser')
        self._wait(By.ID, 'field11304_browserbtn')

        # 学生类型
        cur = self.browser.find_element_by_id('field11404')
        Select(cur).select_by_visible_text('本专科生')
        time.sleep(0.5)
        self.browser.execute_script(
            "changeshowattr('11404_0', 0, -1, 2382, 9047, false);")

        # 是否离沪
        cur = self.browser.find_element_by_id('field12523')
        Select(cur).select_by_visible_text('否')
        time.sleep(0.5)
        self.browser.execute_script(
            "changeshowattr('12523_0', 1, -1, 2382, 9047, false);")

        # 出校事由
        cur = self.browser.find_element_by_id('field11663')
        Select(cur).select_by_visible_text('其他')
        time.sleep(0.5)
        self.browser.execute_script(
            "changeshowattr('11663_0', 6, -1, 2382, 9047, false);")

        # 具体事由
        cur = self.browser.find_element_by_id('field11683')
        cur.clear()
        cur.send_keys('吃饭')

        # 出校日期
        cur = self.browser.find_element_by_id('field11250browser')
        cur.click()

        self._wait(By.XPATH, '//*[@id="_my97DP"]/iframe')
        iframe = self.browser.find_element_by_xpath(
            '//*[@id="_my97DP"]/iframe')
        self.browser.switch_to.frame(iframe)

        cur = self.browser.find_element_by_id('dpTodayInput')
        cur.click()

        self.browser.switch_to.parent_frame()
        date_str = self.browser.find_element_by_id('field11250span').text

        # 出校时间段
        cur = self.browser.find_element_by_id('field11251')
        Select(cur).select_by_visible_text(time_str)

        # 出校去向
        cur = self.browser.find_element_by_id('field11241')
        cur.clear()
        cur.send_keys('宝龙城市广场')

        # 出行交通工具
        cur = self.browser.find_element_by_id('field11304_browserbtn')
        cur.click()

        self.browser.switch_to.parent_frame()

        self._wait(
            By.XPATH, '/html/body/div[10]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/iframe')
        iframe = self.browser.find_element_by_xpath(
            '/html/body/div[10]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/iframe')
        self.browser.switch_to.frame(iframe)

        self._wait(By.ID, 'main')
        iframe = self.browser.find_element_by_id('main')
        self.browser.switch_to.frame(iframe)

        self._wait(
            By.XPATH, '//*[@id="e8_src_table"]/tbody/tr[4]/td[3]/div[1]')
        cur = self.browser.find_element_by_xpath(
            '//*[@id="e8_src_table"]/tbody/tr[4]/td[3]/div[1]')
        cur.click()

        self._wait(By.ID, 'singleArrowTo')
        cur = self.browser.find_element_by_id('singleArrowTo')
        cur.click()

        self._wait(By.ID, 'btnok')
        cur = self.browser.find_element_by_id('btnok')
        cur.click()

        self.browser.switch_to.parent_frame()
        self.browser.switch_to.parent_frame()
        iframe = self.browser.find_element_by_id('bodyiframe')
        self.browser.switch_to.frame(iframe)

        # 返校日期
        cur = self.browser.find_element_by_id('field13063browser')
        cur.click()

        self._wait(By.XPATH, '//*[@id="_my97DP"]/iframe')
        iframe = self.browser.find_element_by_xpath(
            '//*[@id="_my97DP"]/iframe')
        self.browser.switch_to.frame(iframe)

        cur = self.browser.find_element_by_id('dpTodayInput')
        cur.click()

        self.browser.switch_to.parent_frame()

        # 返校时间段
        cur = self.browser.find_element_by_id('field11255')
        Select(cur).select_by_visible_text(time_str)

        # 目前健康状况
        cur = self.browser.find_element_by_id('field11259')
        Select(cur).select_by_visible_text('良好')

        # 承诺信息属实
        cur = self.browser.find_element_by_xpath(
            '//*[@id="flowbody"]/form/div[1]/table/tbody/tr/td/table/tbody/tr[21]/td/div/span[1]/span/span')
        cur.click()

        # 承诺做好防护
        cur = self.browser.find_element_by_xpath(
            '//*[@id="flowbody"]/form/div[1]/table/tbody/tr/td/table/tbody/tr[22]/td/div/span[1]/span/span')
        cur.click()

        # 切换 iFrame
        self.browser.switch_to.parent_frame()

        print('Submitting')
        # 提交
        cur = self.browser.find_element_by_xpath(
            '//*[@id="null_box"]/input[1]')
        cur.click()

        time.sleep(3)

        print('Apply success')
        print('You can eat out at: ' + date_str + ' ' + time_str)

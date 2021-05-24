import time
import requests
from bs4 import BeautifulSoup
import json
import data


class OAConfig:
    def __init__(self, username: str, password: str, timeout=60) -> None:
        self.username = username
        self.password = password


class OA:
    def __init__(self, config: OAConfig) -> None:
        self.config = config
        self.s = requests.Session()
        self.is_logged_in = False
        print('Init for user', self.config.username)
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0)' + \
            ' Gecko/20100101 Firefox/88.0'
        self.s.headers.update({'User-Agent': ua})
        self.xmid = '-1'

    def update_config(self, config: OAConfig) -> None:
        "更新配置"

        self.logout()
        self.config = config
        print('Updated config: username =', self.config.username)

    def login(self) -> None:
        "执行用户登录"

        print('Logging in')
        url = 'https://id.sspu.edu.cn/cas/login'
        r = self.s.get(url)

        soup = BeautifulSoup(r.text, features='lxml')
        if len(soup.find_all(attrs={'class': 'success'})) > 0:
            print('Already logged in')
            self.is_logged_in = True
            return
        else:
            self.is_logged_in = False

        # 登录
        lt = soup.find('input', attrs={'name': 'lt'}).attrs['value']
        data = {
            'username': self.config.username,
            'password': self.config.password,
            # 'imageCodeName': '',
            'errors': '0',
            'lt': lt,
            '_eventId': 'submit'
        }
        r = self.s.post(url=url, data=data)

        # 检查是否登录成功
        soup = BeautifulSoup(r.text, features='lxml')
        if len(soup.find_all(attrs={'class': 'success'})) > 0:
            print('Login success')
            self.is_logged_in = True
        else:
            print('Login failed')
            self.is_logged_in = False

    def login_oa(self) -> None:
        self.s.get('https://oa.sspu.edu.cn/login/Login.jsp')
        self.xmid = self.s.cookies.get('loginidweaver')
        if len(self.xmid) == 0:
            print('Login OA failed')
            return
        print('Login OA success')

    def logout(self) -> None:
        "执行用户登出"

        if not self.is_logged_in:
            print('Not logged in')
            return

        self.xmid = '-1'
        self.s.cookies.clear()
        print('Logged out')
        self.is_logged_in = False

    def get_info(self) -> dict:
        if self.xmid == '-1':
            print('Not logged in OA')
            return {}
        data_url = 'https://oa.sspu.edu.cn/msdev/jsp/databand/DataBand.jsp'
        r = self.s.get(data_url + '?xmid=' + self.xmid)
        oa_info = json.loads(r.text)
        return oa_info

    def apply(self) -> None:
        "申请出校"

        print('Checking')

        oa_info = self.get_info()
        if len(oa_info) == 0:
            print('Can not get info')
            return

        now = time.time()
        form_data = data.gen_data(oa_info, self.xmid, now)

        print('Now: ' + time.asctime(time.localtime(now)))

        url = 'https://oa.sspu.edu.cn/workflow/request/RequestOperation.jsp'
        r = self.s.post(url=url, data=form_data,
                        headers={'host': 'oa.sspu.edu.cn'})

        # success: len = 12871, fail: len = 11879
        if len(r.text) < 12000:
            print('Apply failed')
            return
        print('Apply success')

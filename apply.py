from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from time import sleep
import config

today = time.localtime(time.time())

browser = webdriver.Chrome()
browser.set_window_size(900, 920)
browser.get('https://id.sspu.edu.cn/cas/login')
sleep(1)

# 用户名
cur = browser.find_element_by_id('username')
cur.send_keys(config.username)

# 密码
cur = browser.find_element_by_id('password')
cur.send_keys(config.password)

# 登录
cur = browser.find_element_by_class_name('submit_button')
cur.click()
sleep(1)

# 检查是否登录成功
try:
    browser.find_element_by_class_name('success')
except:
    print('Login Failed')
    exit(1)
print('Login Success')

# 跳转到申请页面
url = 'https://oa.sspu.edu.cn/workflow/request/AddRequest.jsp?workflowid=2382'
browser.get('https://oa.sspu.edu.cn/wui/main.jsp')
browser.get(url)
sleep(2)

# 切换 iFrame
iframe = browser.find_element_by_id('bodyiframe')
browser.switch_to.frame(iframe)
sleep(1)

# 学生类型
cur = browser.find_element_by_id('field11404')
Select(cur).select_by_visible_text('本专科生')

# 是否离沪
cur = browser.find_element_by_id('field12523')
Select(cur).select_by_visible_text('否')

# 出校事由
cur = browser.find_element_by_id('field11663')
Select(cur).select_by_visible_text('其他')

# 具体事由
cur = browser.find_element_by_id('field11683')
cur.clear()
cur.send_keys('吃饭')

# 出校日期
cur = browser.find_element_by_id('field11250browser')
cur.click()
sleep(0.5)

iframe = browser.find_element_by_xpath('//*[@id="_my97DP"]/iframe')
browser.switch_to.frame(iframe)

cur = browser.find_element_by_id('dpTodayInput')
cur.click()

browser.switch_to.parent_frame()

# 出校时间段
cur = browser.find_element_by_id('field11251')
if (today.tm_hour < 12):
    Select(cur).select_by_visible_text('00:00-12:00')
else:
    Select(cur).select_by_visible_text('12:00-00:00')

# 出校去向
cur = browser.find_element_by_id('field11241')
cur.clear()
cur.send_keys('宝龙城市广场')

# 出行交通工具
cur = browser.find_element_by_id('field11304_browserbtn')
cur.click()
sleep(2)

browser.switch_to.parent_frame()
iframe = browser.find_element_by_xpath(
    '/html/body/div[10]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/iframe')
browser.switch_to.frame(iframe)
iframe = browser.find_element_by_id('main')
browser.switch_to.frame(iframe)

cur = browser.find_element_by_xpath(
    '//*[@id="e8_src_table"]/tbody/tr[4]/td[3]/div[1]')
cur.click()
cur = browser.find_element_by_id('singleArrowTo')
cur.click()
cur = browser.find_element_by_id('btnok')
cur.click()

browser.switch_to.parent_frame()
browser.switch_to.parent_frame()
iframe = browser.find_element_by_id('bodyiframe')
browser.switch_to.frame(iframe)

# 返校日期
cur = browser.find_element_by_id('field13063browser')
cur.click()
sleep(0.5)

iframe = browser.find_element_by_xpath('//*[@id="_my97DP"]/iframe')
browser.switch_to.frame(iframe)

cur = browser.find_element_by_id('dpTodayInput')
cur.click()

browser.switch_to.parent_frame()

# 返校时间段
cur = browser.find_element_by_id('field11255')
if (today.tm_hour < 12):
    Select(cur).select_by_visible_text('00:00-12:00')
else:
    Select(cur).select_by_visible_text('12:00-00:00')

# 目前健康状况
cur = browser.find_element_by_id('field11259')
Select(cur).select_by_visible_text('良好')

# 承诺信息属实
cur = browser.find_element_by_xpath(
    '//*[@id="flowbody"]/form/div[1]/table/tbody/tr/td/table/tbody/tr[21]/td/div/span[1]/span/span')
cur.click()

# 承诺做好防护
cur = browser.find_element_by_xpath(
    '//*[@id="flowbody"]/form/div[1]/table/tbody/tr/td/table/tbody/tr[22]/td/div/span[1]/span/span')
cur.click()

# 切换 iFrame
browser.switch_to.parent_frame()

# 提交
cur = browser.find_element_by_xpath('//*[@id="null_box"]/input[1]')
cur.click()

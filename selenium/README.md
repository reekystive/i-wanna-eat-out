# I Wanna Eat Out

SSPU automatic applying for leaving school

## 我要出去吃饭

这是一个用 Python 和 Selenium 实现的自动申请出校工具，它可以帮助你快速出校吃饭。

通过内置的定时器，可以实现让你在任意时间出校。

## 功能特性

* 单次运行
* 定时运行
* API

## 使用方法

### 单次运行

* 修改 `config.py`
* 运行 `apply.py`

### 定时运行

* 修改 `config.py`
* 运行 `scheduler.py`

### API

* 运行 `api.py`
* `GET` request to `http://ip:6991/apply?username=123&password=123`

## 浏览器支持

* Google Chrome
* Firefox _(Not tested)_
* Microsoft Edge _(Not tested)_

## 依赖

## 浏览器 Driver

* [Chrome Driver](https://chromedriver.chromium.org/downloads)
* [Firefox Driver](https://github.com/mozilla/geckodriver/releases)
* [Edge Driver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

### pip 包依赖

* `selenium`
* `Flask` _(for API)_
* `schedule` _(for scheduler)_

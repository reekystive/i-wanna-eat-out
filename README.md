# I Wanna Eat Out

SSPU automatic applying for leaving school

本项目于 2021 年 5 月 24 日完成。2021 年 5 月 25 日，接学校通知，出校无需再进行申请。

项目终。

## 我要出去吃饭

这是一个用 Python 和 requests 实现的自动申请出校工具，它可以帮助你快速出校吃饭。

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

* 运行 `api.py` (API 模式下不使用 `config.py`)
* `GET` request to `http://ip:6991/apply?username=123&password=123`

## 依赖

### pip 包依赖

* `requests`
* `beautifulsoup4`
* `Flask` _(for API)_
* `schedule` _(for scheduler)_

from oa import OAConfig

users = [
    # The first one is main config
    # the others only require 'username' and 'password'
    OAConfig(
        username='20201234567',
        password='123456',
        timeout=10,  # seconds
        headless=False,
        driver_path='auto',
        browser_type='chrome',  # 'chrome', 'firefox', 'edge'
        browser_path='auto'
    ),
    OAConfig(
        username='20201234567',
        password='123456'
    )
]

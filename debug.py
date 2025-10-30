import time

from browser import get_driver

driver = get_driver(False)
URL = "https://treehole.pku.edu.cn/web/"
driver.get(URL)
time.sleep(10000000)  # 等待初始加载

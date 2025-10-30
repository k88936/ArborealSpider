import time
import random
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import test
from browser import get_driver
from record import parse_entry, save_entry

driver = get_driver(False)

URL = "https://treehole.pku.edu.cn/web/"
driver.get(URL)
time.sleep(10)  # 等待初始加载（随机10-30秒）

while (True):
    try:
        # Wait for the element to be clickable and then click it
        xpath = '//*[@id="eagleMapContainer"]/div[1]/div[3]/div/div[1]/div/a[1]'
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        sleep(random.uniform(10, 30))

        # Collect all elements matching dynamic XPaths
        parent_xpath = '//*[@id="table_list"]/div/div'
        try:
            parent_elements = driver.find_elements(By.XPATH, parent_xpath)
            print(f"Found {len(parent_elements)} parent div elements:")
            for i, parent in enumerate(parent_elements):
                # Get all child elements of each parent
                children = parent.find_elements(By.XPATH, './*')
                print(f"Parent {i + 1} has {len(children)} children")
                for j, child in enumerate(children):
                    print(f"  Child {j + 1}: {child.text}")
                    marked = test.test(child.text)
                    entry = parse_entry(child.text,marked)
                    save_entry(entry)

        except Exception as e:
            print(f"Error collecting elements from {parent_xpath}: {e}")
        sleep(random.uniform(10, 30))
    except Exception as e:
        print(e)

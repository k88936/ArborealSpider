from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver(headless=True):
    # 初始化headless chromedriver
    # user_data_dir = f"./chrome_config"
    user_data_dir = f"C:/temp/restart"
    chrome_options = Options()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    if headless:
        chrome_options.add_argument(f'--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        '''
    })
    return driver

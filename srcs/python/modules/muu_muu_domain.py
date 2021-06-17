import re
import datetime
import configparser
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from fake_useragent import UserAgent

# Logger setting
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

### functions ###
def parse_expiration_date(text):
    match = re.search(r'あと [-\d]+ 日', text)
    if match:
        day_left = int(re.search(r'[-\d]+', match.group()).group())
        now = datetime.datetime.now()
        expiration_date = now + datetime.timedelta(days=day_left)
        return expiration_date.strftime('%Y/%m/%d')
    else:
        return '-'

def parse_contents(conpane_cards):
    for element in conpane_cards:
        text = element.get_text()
        match = re.search(r'期限切れ間近|期限切れ|自動更新中', text)
        if match:
            if match.group() == "期限切れ":
                continue
            elif match.group() == "自動更新中":
                autorenew = 1
            else:
                autorenew = 0
        else:
            autorenew = 0
        match = re.search(r'\d{4}/\d{2}/\d{2}', text)
        if match:
            expiration_date = match.group()
        else:
            expiration_date = parse_expiration_date(text)
        start = re.search(r'契約期間', text).start()
        domain_name = text[:start].replace(' ', '').replace('\n', '')
        yield [domain_name, "ムームー", expiration_date, autorenew]

def get_domain_info():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    url = "https://muumuu-domain.com/checkout/login"
    login = config["MUU_MUU_DOMAIN"]["Id"]
    password = config["MUU_MUU_DOMAIN"]["Password"]
    webdriverPath = config["WEBDRIVER"]["Path"]
    
    ua = UserAgent()
    logger.debug(f'muu_muu_domain: UserAgent: {ua.chrome}')

    options = Options()
    options.add_argument('--headless')
    options.add_argument(ua.chrome)
    
    try:
        driver = webdriver.Chrome(executable_path=webdriverPath, chrome_options=options)
        
        driver.get(url)
        
        driver.find_element_by_id("session_muu_id").send_keys(login)
        driver.find_element_by_id("session_password").send_keys(password)
        driver.find_element_by_name("button").send_keys(Keys.ENTER)
        
        logger.debug('muu_muu_domain: login')
        sleep(10)
        
        driver.find_element_by_link_text("ドメイン一覧(すべて)へ").send_keys(Keys.ENTER)
        
        logger.debug('muu_muu_domain: go to all-domain-list')
        sleep(10)
        
        dropdown = driver.find_element_by_name("limit")
        select = Select(dropdown)
        select.select_by_value('1000')
        
        logger.debug('muu_muu_domain: select 1000')
        sleep(30)
        
        contents = BeautifulSoup(driver.page_source, "lxml")
        domain_info = list(parse_contents(contents.find_all(class_="conpane-card")))
        logger.debug(f'muu_muu_domain: total_list_number: {len(domain_info)}')

        driver.close()
        driver.quit()

        return domain_info
    except Exception as err:
        logger.debug(f'Error: muu_muu_domain: get_domain_info: {err}')
        return None

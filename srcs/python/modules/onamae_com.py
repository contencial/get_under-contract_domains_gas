import re
import datetime
import configparser
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException 
from fake_useragent import UserAgent
from modules.by_pass_captcha import by_pass_captcha

# Logger setting
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

### functions ###
def check_exists_by_name(driver, name):
    try:
        driver.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_class_name(driver, class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

def parse_expiration_date(text):
    match = re.search(r'残り[\d]+日', text)
    if match:
        day_left = int(re.search(r'[\d]+', match.group()).group())
        now = datetime.datetime.now()
        expiration_date = now + datetime.timedelta(days=day_left)
        return expiration_date.strftime('%Y/%m/%d')
    else:
        return '-'

def parse_contents(tblFixed, tblwrap):
    tblFixedSize = len(tblFixed)
    tblwrapSize = len(tblwrap)
    logger.debug(f'tblFixed: {tblFixedSize}, tblwrap: {tblwrapSize}')
    if tblFixedSize != tblwrapSize:
        logger.debug(f'pop: {tblFixed.pop(0)}')
    for i in range(len(tblFixed)):
        attr = tblwrap[i].find_all("td")
        text = attr[1].get_text()
        match = re.search(r'\d{4}/\d{2}/\d{2}', text)
        if match:
            expiration_date = match.group()
        else:
            expiration_date = parse_expiration_date(text)
        edate = datetime.datetime.strptime(expiration_date, "%Y/%m/%d")
        if datetime.date(edate.year, edate.month, edate.day) < datetime.date.today():
            continue
        text = attr[2].get_text()
        match = re.search(r'設定', text)
        if match:
            autorenew = 0
        else:
            autorenew = 1
        domain_name = tblFixed[i].get_text()
        yield [domain_name, "お名前", expiration_date, autorenew]

def get_domain_info():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    url = "https://navi.onamae.com/domain"
    login = config["ONAMAE_COM"]["Id"]
    password = config["ONAMAE_COM"]["Password"]
    webdriverPath = config["WEBDRIVER"]["Path"]

    ua = UserAgent()
    logger.debug(f'onamae_com: UserAgent: {ua.chrome}')

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--mute-audio")
    options.add_argument(ua.chrome)
    options.add_argument('--headless')
    
    try:
        driver = webdriver.Chrome(executable_path=webdriverPath, options=options)
        
        driver.get(url)
        driver.set_window_size(1200, 1053)
        
        driver.find_element_by_name("loginId").send_keys(login)
        driver.find_element_by_name("loginPassword").send_keys(password)
        driver.find_element_by_tag_name("button").click()
        sleep(15)

        logger.debug("onamae_com: check if g-recaptcha exists")
        if check_exists_by_class_name(driver, "g-recaptcha"):
            ret = by_pass_captcha(driver)
            if ret == False:
                exit(1)
            sleep(10)

        logger.debug('onamae_com: login')

        if not check_exists_by_name(driver, "select1"):
            driver.find_element_by_link_text("TOP").click()
            sleep(5)
            driver.find_element_by_xpath('//button[@data-gtmvalue="usagesituation_domain"]').click()
            sleep(10)

        dropdown = driver.find_element_by_name("select1")
        select = Select(dropdown)
        select.select_by_value('100')
        
        logger.debug('onamae_com: select 100')
        sleep(30)

        nav = driver.find_element_by_xpath('//ul[@class="nav-Pagination"]')
        paging = nav.find_elements_by_tag_name("a")
        logger.debug(f'paging: {len(paging) - 2}')
        
        contents = BeautifulSoup(driver.page_source, "html.parser")
        domain_info = list(parse_contents(contents.find_all("tr", target="tblFixed"), contents.find_all("tr", target="tblwrap")))
        logger.debug(f'page: 1: {len(domain_info)}')

        for i in range(len(paging)):
            if i == 0 or i == 1 or i == len(paging) - 1:
                continue
            paging[i].click()
            sleep(20)
            contents = BeautifulSoup(driver.page_source, "html.parser")
            domain_chunk = list(parse_contents(contents.find_all("tr", target="tblFixed"), contents.find_all("tr", target="tblwrap")))
            logger.debug(f'page: {i}: {len(domain_chunk)}')
            domain_info.extend(domain_chunk)

        logger.debug(f'onamae_com: total_list_number: {len(domain_info)}')

        driver.close()
        driver.quit()

        return domain_info
    except Exception as err:
        logger.debug(f'Error: onamae_com: get_domain_info: {err}')
        return None

import re
import datetime
import gspread
import configparser
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from fake_useragent import UserAgent
from oauth2client.service_account import ServiceAccountCredentials

# Logger setting
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

### functions ###
def write_domain_list(config, registered_domain_list):
    spreadsheet_id = config["SPREADSHEET"]["Id"]
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('登録中ドメイン（123サーバー）')

    sheet.clear()
    cell_list = sheet.range(1, 1, len(registered_domain_list) + 1, 3)
    i = 0
    for cell in cell_list:
        if (i == 0):
            cell.value = "サーバ番号"
        elif (i == 1):
            cell.value = "#"
        elif (i == 2):
            cell.value = "ドメイン名"
        elif (i % 3 == 0):
            cell.value = registered_domain_list[int(i / 3) - 1][0]
        elif (i % 3 == 1):
            cell.value = registered_domain_list[int(i / 3) - 1][1]
        elif (i % 3 == 2):
            cell.value = registered_domain_list[int(i / 3) - 1][2]
        i += 1
    sheet.update_cells(cell_list)

    cell_list = sheet.range('D1:E1')
    cell_list[0].value = 'Size'
    cell_list[1].value = len(domain_info)
    sheet.update_cells(cell_list)

def parse_contents(contents):
    tbody = contents.find_all("tbody")
    server_no = tbody[0].find("td").get_text()
    domain_list = tbody[1].find_all("a")
    domain_no = 0
    for element in domain_list:
        domain_no += 1
        domain_name = element.get_text()
        yield [server_no, domain_no, domain_name]

def button_click(driver, button_text):
    buttons = driver.find_elements_by_tag_name("button")

    for button in buttons:
        if button.text == button_text:
            button.click()
            break

def get_domain_info(config):
    url = "https://member.123server.jp/members/login/"
    login = config["SERVER_123"]["Id"]
    password = config["SERVER_123"]["Password"]
    webdriverPath = config["WEBDRIVER"]["Path"]
    
    ua = UserAgent()
    logger.debug(f'123_server: UserAgent: {ua.chrome}')

    options = Options()
    #options.add_argument('--headless')
    options.add_argument(ua.chrome)
    
    try:
        driver = webdriver.Chrome(executable_path=webdriverPath, options=options)
        
        driver.get(url)

        driver.find_element_by_id("MemberContractId").send_keys(login)
        driver.find_element_by_id("MemberPassword").send_keys(password)
        button_click(driver, "ログイン")
        
        logger.debug('123_server: login')
        sleep(3)
        
        driver.find_element_by_xpath('//a[@href="/servers/"]').click()
        
        logger.debug('123_server: go to server_list')
        sleep(3)

        paging = driver.find_element_by_xpath('//ul[@class="pagination"]').find_elements_by_tag_name("a")
        
        registered_domain_list = list()
        for i in range(len(paging)):
            if i < 1 or i > 3:
                continue
            logger.debug(f'123_server: page: {i}')
            driver.find_element_by_link_text(str(i)).click()
            sleep(10)
            for index in range(100):
                domain_list_button = driver.find_elements_by_link_text("ドメイン一覧")
                domain_list_button[index].click()
                server_no = 100 * (i - 1) + index + 1
                sleep(5)
                contents = BeautifulSoup(driver.page_source, "lxml")
                domain_chunk = list(parse_contents(contents))
                logger.debug(f'123_server: No {server_no}: {len(domain_chunk)}')
                registered_domain_list.extend(domain_chunk)
                driver.find_element_by_xpath('//a[@href="/servers/"]').click()
                sleep(5)

        logger.debug(f'123_server: total_list_number: {len(registered_domain_list)}')

        driver.close()
        driver.quit()

        return registered_domain_list
    except Exception as err:
        logger.debug(f'Error: 123_server: get_domain_info: {err}')
        exit(1)

def scrape_123server():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    try:
        logger.debug("123_server: start get_domain_info")
        registered_domain_list = get_domain_info(config)
        logger.debug("123_server: start write_domain_list")
        write_domain_list(config, registered_domain_list)
        return True
    except Exception as err:
        logger.debug(f'123_server: {err}')
        return False

scrape_123server()

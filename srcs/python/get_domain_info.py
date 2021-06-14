import re
import os
import gspread # to manipulate spreadsheet
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from oauth2client.service_account import ServiceAccountCredentials # to access Google API

# Logger setting
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

### functions ###
def num2alpha(num):
    if num <= 26:
        return chr(64 + num)
    elif num % 26 == 0:
        return num2alpha(num//26 - 1) + chr(90)
    else:
        return num2alpha(num//26) + chr(64 + num % 26)

def parse_contents(conpane_list):
    for element in conpane_list:
        text = element.get_text()
        match = re.search(r'\d{4}/\d{2}/\d{2}', text)
        if match:
            expiration_date = match.group()
        else:
            expiration_date = '-'
        match = re.search(r'あと [-\w]+ 日', text)
        if match:
            day_left = match.group()
        else:
            day_left = '-'
        match = re.search(r'期限切れ|自動更新中', text)
        if match:
            status = match.group()
        else:
            status = '-'
        yield [expiration_date, day_left, status]

def write_domain_list(domainList, domainInfo):
    SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('契約中ドメイン（ムームー）')

    sheet.clear()
    cell_list = sheet.range(1, 1, len(domainList) + 1, 5)
    i = 0;
    for cell in cell_list:
        if (i == 0):
            cell.value = 'No'
        elif (i == 1):
            cell.value = 'ドメイン名'
        elif (i == 2):
            cell.value = '有効期限'
        elif (i == 3):
            cell.value = '残り契約期間'
        elif (i == 4):
            cell.value = '状態'
        elif (i % 5 == 0):
            cell.value = int(i / 5)
        elif (i % 5 == 1):
            cell.value = domainList[int(i / 5) - 1]
        elif (i % 5 == 2):
            cell.value = domainInfo[int(i / 5) - 1][0]
        elif (i % 5 == 3):
            cell.value = domainInfo[int(i / 5) - 1][1]
        elif (i % 5 == 4):
            cell.value = domainInfo[int(i / 5) - 1][2]
        i += 1
    sheet.update_cells(cell_list)

### main_script ###
if __name__ == '__main__':

    url = "https://muumuu-domain.com/checkout/login"
    login = "contencial"
    password = "kashi911"
    webdriverPath = "/Users/kefujiwa/Documents/webdriver/chromedriver"
    
    options = Options()
    options.add_argument('--headless')
    
    try:
        driver = webdriver.Chrome(executable_path=webdriverPath, chrome_options=options)
        
        driver.get(url)
        
        driver.find_element_by_id("session_muu_id").send_keys(login)
        driver.find_element_by_id("session_password").send_keys(password)
        driver.find_element_by_name("button").send_keys(Keys.ENTER)
        
        logger.debug('Login')
        sleep(10)
        
        driver.find_element_by_link_text("ドメイン一覧(すべて)へ").send_keys(Keys.ENTER)
        
        logger.debug('Go to All-Domain-List')
        sleep(10)
        
        dropdown = driver.find_element_by_name("limit")
        select = Select(dropdown)
        select.select_by_value('1000')
        
        logger.debug('Select 1000')
        sleep(30)
        
        contents = BeautifulSoup(driver.page_source, "lxml")
        domainList = [c.get_text().replace(' ', '').replace('\n', '') for c in contents.find_all(class_="conpane-card__heading")]
        domainInfo = list(parse_contents(contents.find_all(class_="conpane-list")))
        write_domain_list(domainList, domainInfo)
        logger.debug('Finish')
    except Exception as err:
        logger.debug(err)

    driver.close()
    driver.quit()

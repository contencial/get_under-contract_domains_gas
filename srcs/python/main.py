import modules
import os
import gspread # to manipulate spreadsheet
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
def write_domain_list(domain_info):
    SPREADSHEET_KEY = os.environ['SPREADSHEET_KEY']
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('契約中ドメイン一覧')

    sheet.clear()
    cell_list = sheet.range(1, 1, len(domain_info) + 1, 5)
    i = 0
    for cell in cell_list:
        if (i == 0):
            cell.value = 'No'
        elif (i == 1):
            cell.value = 'ドメイン名'
        elif (i == 2):
            cell.value = '取得先'
        elif (i == 3):
            cell.value = '有効期限'
        elif (i == 4):
            cell.value = '自動更新\nフラグ'
        elif (i % 5 == 0):
            cell.value = int(i / 5)
        elif (i % 5 == 1):
            cell.value = domain_info[int(i / 5) - 1][0]
        elif (i % 5 == 2):
            cell.value = domain_info[int(i / 5) - 1][1]
        elif (i % 5 == 3):
            cell.value = domain_info[int(i / 5) - 1][2]
        elif (i % 5 == 4):
            cell.value = domain_info[int(i / 5) - 1][3]
        i += 1
    sheet.update_cells(cell_list)
    
    cell_list = sheet.range('F1:J1')
    cell_list[0].value = 'Size'
    cell_list[1].value = len(domain_info)
    cell_list[2].value = '=HYPERLINK("https://www.value-domain.com/login.php", "Go to バリュー")'
    cell_list[3].value = '=HYPERLINK("https://muumuu-domain.com/?mode=conpane", "Go to ムームー")'
    cell_list[4].value = '=HYPERLINK("https://navi.onamae.com/domain", "Go to お名前")'
    sheet.update_cells(cell_list, value_input_option='USER_ENTERED')

### main_script ###
if __name__ == '__main__':

    try:
        domain_info = modules.value_domain.get_domain_info()
        logger.debug(f'main: add value_domain: {len(domain_info)}')
        if not domain_info:
            logger.debug("Error: value_domain: get_domain_info")
            exit(1)
        domain_chunk = modules.muu_muu_domain.get_domain_info()
        if not domain_chunk:
            logger.debug("Error: muu_muu_domain: get_domain_info")
            exit(1)
        domain_info.extend(domain_chunk)
        logger.debug(f'main: add muu_muu_domain: {len(domain_info)}')
        domain_chunk = modules.onamae_com.get_domain_info()
        if not domain_chunk:
            logger.debug("Error: onamae_com: get_domain_info")
            exit(1)
        domain_info.extend(domain_chunk)
        logger.debug(f'main: add onamae_com: {len(domain_info)}')
        write_domain_list(domain_info)
        logger.debug('Finish')
    except Exception as err:
        logger.debug(f'main: {err}')

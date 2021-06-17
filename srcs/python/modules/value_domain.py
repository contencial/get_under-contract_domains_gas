import json
import pathlib        
import datetime
import requests
import configparser

# Logger setting
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

### functions ###
def parse_body(results):
    for domain in results:
        expiration_date = domain["expirationdate"].replace('-', '/')
        edate = datetime.datetime.strptime(expiration_date, "%Y/%m/%d")
        if datetime.date(edate.year, edate.month, edate.day) < datetime.date.today():
            continue
        yield [domain["domainname"], "バリュー", expiration_date, domain["autorenew"]]

def get_list_number(value_domain_url, headers):
    try:
        req = requests.get(value_domain_url, headers=headers)
        body = req.json()
        list_number = body["paging"]["max"]
        logger.debug(f'value_domain: list_number: {list_number}')
        return list_number
    except Exception as err:
        logger.debug(f'Error: value_domain: get_list_number: {err}')
        return None

def get_domain_info():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    value_domain_url = "https://api.value-domain.com/v1/domains"
    api_key = config["VALUE_DOMAIN"]["Api_Key"]
    headers = {'Authorization': f'Bearer {api_key}'}
    list_number = get_list_number(value_domain_url, headers)
    if not list_number:
        return None
    try:
        req = requests.get(f'{value_domain_url}?limit={list_number}', headers=headers)
        body = req.json()
        domain_info = list(parse_body(body['results']))
        logger.debug(f'value_domain: total_list_number: {len(domain_info)}')
        return domain_info
    except Exception as err:
        logger.debug(f'Error: value_domain: get_domain_info: {err}')
        return None

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import os, sys
import time,requests
import random
from bs4 import BeautifulSoup

# Logger setting
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

### functions ###
def audio_to_text(driver, mp3Path, audioToTextDelay):
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])

    googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'
    driver.get(googleIBMLink)

    # Upload file 
    time.sleep(1)
    root = driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(mp3Path)

    # Audio to text is processing
    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements_by_tag_name('span')
    result = " ".join( [ each.text for each in text ] )

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result

def request_audio_file(href, filename):
    logger.debug(f'by_pass_captcha: href: {href}')
    response = requests.get(href, stream=True)
    logger.debug(f'by_pass_captcha: request_audio_file: {response.status_code}')
    if response.status_code != 200:
        logger.debug(f'by_pass_captcha: request_audio_file: try again')
        request_audio_file(href, filename)
    with open(filename, "wb") as handle:
        for data in response.iter_content():
            handle.write(data)

def by_pass_captcha(driver):
    delayTime = 5
    audioToTextDelay = 10
    filename = 'test.mp3'

    allIframesLen = driver.find_elements_by_tag_name('iframe')
    audioBtnFound = False
    audioBtnIndex = -1
    
    logger.debug("by_pass_captcha: find iframe")
    for index in range(len(allIframesLen)):
        driver.switch_to.default_content()
        iframe = driver.find_elements_by_tag_name('iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element_by_id('recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass

    logger.debug("by_pass_captcha: proceed to audio authenticate")
    if audioBtnFound:
        try:
            while True:
                href = driver.find_element_by_id('audio-source').get_attribute('src')
                request_audio_file(href, filename)
                response = audio_to_text(driver, os.getcwd() + '/' + filename, audioToTextDelay)
                logger.debug(response)
    
                driver.switch_to.default_content()
                iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
                driver.switch_to.frame(iframe)
                time.sleep(random.randint(5, 10))
    
                inputbtn = driver.find_element_by_id('audio-response')
                inputbtn.send_keys(response)
                inputbtn.send_keys(Keys.ENTER)
                logger.debug("by_pass_captcha: send audio answer")
                time.sleep(random.randint(8, 11))

                driver.switch_to.default_content()
                contents = BeautifulSoup(driver.page_source, "html.parser")

                if contents.find("title", text="お名前.com Navi"):
                    logger.debug("by_pass_captcha: Success")
                    return True

                driver.switch_to.frame(iframe)
        except Exception as err:
            with open("error_page_source.txt", "w") as handle:
                handle.write(driver.page_source)
            logger.debug(f'by_pass_captcha: {err}')
            logger.debug('by_pass_captcha: Caught. Need to change proxy now')
            return False
    else:
        logger.debug('by_pass_captcha: Button not found. This should not happen.')
        return False

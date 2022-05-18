from selenium import webdriver
import time


options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless')


def pars_main(driver):
    driver.set_window_size(1500, 2000)
    driver.find_element_by_class_name(name='fix-btn-active').click()
    time.sleep(3)
    chat_container = driver.find_element_by_class_name('chat-container')
    scroll_line = driver.find_element_by_class_name('bscroll-vertical-scrollbar')
    driver.execute_script('arguments[0].style.maxHeight = "none";', chat_container)
    driver.execute_script('arguments[0].style.display = "none";', scroll_line)
    container_message = driver.find_elements_by_class_name('message-all')[1]
    time.sleep(3)
    container_message.screenshot('screen.png')
    print('Скрін зроблено!')

def pars_while(link, value, minute):
    old_date = None
    print(f'Начало роботи.\nTTН - {value}')
    while 1:
        try:
            print(f'Начало цикла в {minute} минут')
            driver = webdriver.Chrome(executable_path='chromedriver.exe',
                                      options=options)
            driver.get(link)
            paste_ttn = driver.find_element_by_id(id_='en')
            paste_ttn.send_keys(value)
            driver.find_element_by_id(id_='np-number-input-desktop-btn-search-en').click()
            time.sleep(3)
            driver.find_elements_by_class_name(name='v-btn__content')[6].click()
            time.sleep(3)
            date = driver.find_element_by_class_name('np-message__header').text
            print(date)
            if old_date != date:
                print('Знайдено змінення!')
                pars_main(driver)
            old_date = date
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
            time.sleep(minute * 60)


if __name__ == '__main__':
    value = '20400280961157'
    link = f'https://tracking.novaposhta.ua/#/uk'
    minute = 20
    pars_while(link=link, value=value, minute=minute)

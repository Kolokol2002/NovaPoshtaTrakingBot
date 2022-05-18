import pickle

import undetected_chromedriver
import time

value = '20450533054505'
link = f'https://tracking.novaposhta.ua/#/uk/'

def pars():
    driver.get(link)
    driver.set_window_size(1500, 2000)
    #строка пошуку
    paste_ttn = driver.find_element_by_id(id_='en')
    paste_ttn.send_keys(value)
    #кнопка пошуку
    driver.find_element_by_id(id_='np-number-input-desktop-btn-search-en').click()
    time.sleep(1)
    #прокуск підсказки
    driver.find_elements_by_class_name(name='v-btn__content')[6].click()
    time.sleep(1)
    #кнопка "детальніше"
    driver.find_element_by_class_name(name='fix-btn-active').click()
    time.sleep(1)
    chat_container = driver.find_element_by_class_name('chat-container')
    scroll_line = driver.find_element_by_class_name('bscroll-vertical-scrollbar')
    driver.execute_script('arguments[0].style.maxHeight = "none";', chat_container)
    driver.execute_script('arguments[0].style.display = "none";', scroll_line)
    container_message = driver.find_elements_by_class_name('message-all')[1]
    time.sleep(2)
    container_message.screenshot('screen.png')
if __name__ == '__main__':
        try:
            driver = undetected_chromedriver.Chrome()
            pars()
        except Exception as ex:
            print(ex)
            pars()
        finally:
            driver.close()
            driver.quit()
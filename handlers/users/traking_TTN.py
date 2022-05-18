import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from selenium import webdriver
import time

from keyboards.default import def_kb
from loader import dp
from aiogram.dispatcher.filters import Text

from keyboards.inline import inline_back

from states import TTN


@dp.message_handler(Text(equals=['✅Трекінг по ТТН'], ignore_case=True))
async def traking(message: types.Message):
    try:
        await message.answer('Напишіть ваш TTН:', reply_markup=inline_back)
        await TTN.ttn.set()
    except:
        await message.reply('Це не ціле число!!!', reply_markup=inline_back)

@dp.message_handler(state=TTN.ttn)
async def ttn(message: types.Message, state: FSMContext):
    try:
        await state.update_data(ttn=message.text)
        await message.answer('З яким інтервалом перевіряти інформацію?', reply_markup=inline_back)
        await TTN.next()
    except:
        await message.reply('Це не ціле число!!!', reply_markup=inline_back)

@dp.message_handler(state=TTN.minute)
async def minute(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ttn = data.get('ttn')
    minute = float(message.text)

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')

    async def pars_main(driver):
        driver.set_window_size(1500, 2000)
        driver.find_element_by_class_name(name='fix-btn-active').click()
        time.sleep(3)
        chat_container = driver.find_element_by_class_name('chat-container')
        scroll_line = driver.find_element_by_class_name('bscroll-vertical-scrollbar')
        driver.execute_script('arguments[0].style.maxHeight = "none";', chat_container)
        driver.execute_script('arguments[0].style.display = "none";', scroll_line)
        container_message = driver.find_elements_by_class_name('message-all')[1]
        time.sleep(2)
        container_message.screenshot('screen.png')
        print('Скрін зроблено!')
        photo = open('screen.png', 'rb')
        await message.answer_photo(photo=photo, reply_markup=inline_back)

    async def pars_while(link, value, minute):
        old_date = None
        print(f'Начало роботи.\nTTН - {value}')
        while 1:
            try:
                print(f'Начало цикла в {minute} минут')
                driver = webdriver.Chrome(executable_path='C:/Users/maksk/Desktop/Project on python/NovaPoshtaTrakingBot/chromedriver.exe',
                                          options=options)
                driver.get(link)
                paste_ttn = driver.find_element_by_id(id_='en')
                paste_ttn.send_keys(value)
                driver.find_element_by_id(id_='np-number-input-desktop-btn-search-en').click()
                time.sleep(3)
                driver.find_elements_by_class_name(name='v-btn__content')[6].click()
                time.sleep(3)
                date = driver.find_element_by_class_name('np-message__header').text

                if old_date != date:
                    print('Знайдено змінення!')
                    await pars_main(driver)
                    print(date)
                    old_date = date
                else:
                    print('Змінення не знайдено!')
            except Exception as ex:
                print(ex)
            finally:
                driver.close()
                driver.quit()
            await asyncio.sleep(minute * 60)


    link = f'https://tracking.novaposhta.ua/#/uk'
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(pars_while(link=link, value=ttn, minute=minute))
    loop.run_forever()

@dp.callback_query_handler(text='back', state='*')
async def next_keyboard(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text='🔙Назад', reply_markup=def_kb)

    await state.finish()


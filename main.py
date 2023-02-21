from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

bot = Bot("Token")
dp = Dispatcher(bot)


# команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await bot.send_message(message.chat.id, "Добрый день! Я бот с поиском информации википедии!")

@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    url = "https://ru.wikipedia.org/w/index.php?go=Перейти&search=" + message.text
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    links = soup.find_all("div", class_="mw-search-result-heading")

    if len(links) > 0:
        url = "https://ru.wikipedia.org" + links[0].find("a")["href"]

    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    driver = webdriver.Chrome(options=option)
    driver.get(url)

    driver.execute_script("window.scrollTo(0, 200)")
    driver.save_screenshot("img.png")
    driver.close()

    photo = open("img.png", 'rb')
    await bot.send_photo(message.chat.id, photo=photo, caption=f'Ссылка на статью: <a href="{url}">тык</a>', parse_mode="HTML")


executor.start_polling(dp)
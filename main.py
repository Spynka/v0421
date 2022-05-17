# Телеграм-бот v.004
import json
from gettext import find
from io import BytesIO
import telebot  # pyTelegramBotAPI	4.3.1
import random
import html
import logging
from telegram import ParseMode

from telebot import types
import requests
import bs4   #beautifulsoup4
import BotGames  # бот-игры, файл BotGames.py
from menuBot import Menu  # в этом модуле есть код, создающий экземпляры классов описывающих моё меню
import DZ  # домашнее задание от первого уро

bot = telebot.TeleBot('5285865621:AAHtiMAGGb4VRe-CLCtHFpR4cTTJENbzZRk')  # Создаем экземпляр бота
game21 = None  # класс игры в 21, экземпляр создаём только при начале игры


# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message, res=False):
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(message.chat.id, text=txt_message, reply_markup=Menu.getMenu("Главное меню").markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global game21

    chat_id = message.chat.id
    ms_text = message.text

    result = goto_menu(chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if result == True:
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    if Menu.cur_menu != None and ms_text in Menu.cur_menu.buttons:  # проверим, что команда относится к текущему меню

        if ms_text == "Помощь":
            send_help(chat_id)

        elif ms_text == "Прислать лисичку":
            bot.send_photo(chat_id, photo=getImgFox(), caption="Вот тебе лисичка, фыр-фыр!")

        elif ms_text == "Прислать идею стартапа":
            bot.send_message(chat_id, text=get_startup(chat_id), parse_mode='html')

        elif ms_text == "Прислать цитату на Eng":
            get_quote(chat_id)
 #           bot.send_message(chat_id, text=get_quote(), parse_mode=ParseMode.HTML)

        elif ms_text == "Прислать геймпад":
            Catalog(chat_id)
            parser(chat_id,ms_text)



        elif ms_text == "Угадай кто?":
            get_ManOrNot(chat_id)

        elif ms_text == "Карту!":
            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                goto_menu(chat_id, "Выход")
                return

        elif ms_text == "Стоп!":
            game21 = None
            goto_menu(chat_id, "Выход")
            return

        elif ms_text == "Задание-1":
            DZ.dz1(bot, chat_id)

        elif ms_text == "Задание-2":
            DZ.dz2(bot, chat_id)

        elif ms_text == "Задание-3":
            DZ.dz3(bot, chat_id)

        elif ms_text == "Задание-4":
            DZ.dz4(bot, chat_id)

        elif ms_text == "Задание-5":
            DZ.dz5(bot, chat_id)

        elif ms_text == "Задание-6":
            DZ.dz6(bot, chat_id)

    else:  # ...........................................................................................................
       bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
       goto_menu(chat_id, "Главное меню")


# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать параметр или несколько параметров в обработчик кнопки, использовать методы Menu.getExtPar() и Menu.setExtPar()
    pass
    # if call.data == "ManOrNot_GoToSite": #call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    #
    #     # После обработки каждого запроса нужно вызвать метод answer_callback_query, чтобы Telegram понял, что запрос обработан.
    #     bot.answer_callback_query(call.id)

# -----------------------------------------------------------------------

#------------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    if name_menu == "Выход" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            global game21
            game21 = BotGames.Game21()  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        return True
    else:
        return False


# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias


# -----------------------------------------------------------------------
def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Ксения Spynka Смирнова")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/Spunka")
    markup.add(btn1)
    img = open('AVA.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)
#---------------------------------------------------------------------
def Catalog(chat_id):
    bot.send_message(chat_id, """
                       Привет! Смотри какие геймпады классные на Е-каталоге нашел""",
                        parse_mode="html")


def parser(chat_id, ms_text):

    url = "https://kz.e-katalog.com/ek-list.php?katalog_=200&pr_[]=841&sb_=Геймпад"
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.text, "html.parser")

    all_links = soup.find_all("a", class_="model-short-title")
    for link in all_links:
        url = "https://kz.e-katalog.com/" + link["href"]
        request = requests.get(url)
        soup = bs4.BeautifulSoup(request.text, "html.parser")

        name = soup.find("div", class_="fix-menu-name")
        price = name.find("a").text
        name.find("a").extract()
        name = name.text

        img = soup.find("div", class_="img200")
        img = img.findChildren("img")[0]
        img = "https://kz.e-katalog.com/" + img["src"]

        bot.send_photo(chat_id, img,
                    caption="<b>" + name + "</b>\n<i>" + price + f"</i>\n<a href='{url}'>Ссылка на сайт</a>",
                    parse_mode='HTML')

        if all_links.index(link) == 3:
            break
#---------------------------------------------------------------------


# -----------------------------------------------------------------------
#def send_film(chat_id):
#    film = get_randomFilm()
#    info_str = f"<b>{film['Наименование']}</b>\n" \
#               f"Год: {film['Год']}\n" \
#               f"Страна: {film['Страна']}\n" \
#               f"Жанр: {film['Жанр']}\n" \
#               f"Продолжительность: {film['Продолжительность']}"
#    markup = types.InlineKeyboardMarkup()
#    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
#    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
#    markup.add(btn1, btn2)
#    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)






# -----------------------------------------------------------------------
@bot.message_handler(content_types=['text'])
def get_quote(chat_id):
#    array_anekdots = []
#    req_anek = requests.get('http://anekdotme.ru/random')
#    if req_anek.status_code == 200:
#        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
#        result_find = soup.select('.anekdot_text')
#        for result in result_find:
#            array_anekdots.append(result.getText().strip())
#    if len(array_anekdots) > 0:
#        return array_anekdots[0]
#    else:
#        return ""
#    array_quotes = []
    answer = requests.get('https://zenquotes.io/api/random')
    if answer.status_code == 200:
        soup = bs4.BeautifulSoup(answer.text, "html.parser")
#        soup = soup.text
#        soup_new = soup.replace('[{"q":', '').strip()
#        return soup
        bot.send_message(chat_id, soup,parse_mode="html")

#def get_anekdot(author, work, begin: str = "", end: str = ""):
#     answer = requests.get('https://zenquotes.io/api/random')
#     if answer.status_code == 200:
 #       soup = bs4.BeautifulSoup(answer.text, "html.parser")
        #if author not in list(lib.keys()):
        #        return HTTPException(404)
        #if work not in list(lib[author]):
        #        return HTTPException(404)
        #words = str(poems[work])
        #if begin == "" or end == "":
#            return soup(content=words, media_type="text/plain")
	    #begin = words.find(begin)
	    #end = words.rfind(end) + 1
	    #if begin != -1 and end != 0 and begin <= end:
		#        return answer(content=words[begin:end]+"\n", media_type="text/plain")
	    #else:
		#        return answer(content=words, media_type="text/plain")
#          result_find = soup.select('')
#          for result in result_find:
#         return soup.getText().strip()
#     if len(array_quotes) > 0:
#         return array_quotes[0]
#     else:
#         return ""

# -----------------------------------------------------------------------
import os
import requests as rq
from random import randint

def getImgFox():
    img = rq.get("https://randomfox.ca/floof/")
    if img.status_code != 200:
        return img
    img = img.json()["image"]
    res = rq.get(img)
    if res.status_code != 200:
        return res
    bImg = res.content
    if not os.path.isdir("foxsImg"):
        os.mkdir("foxsImg")
    with open("foxsImg/" + str(randint(0, 2048)) + ".jpg", "wb") as f:
        f.write(bImg)
        f.close()
        return bImg
getImgFox()
     # making a GET request to the endpoint.
#     resp = requests.get("https://some-random-api.ml/animal/cat")
     # checking if resp has a healthy status code.
#     if 300 > resp.status_code >= 200:
#         content = resp.json()  # We have a dict now.
#     else:
#         content = f"Recieved a bad status code of {resp.status_code}."
#     return content
#    url = ""
#    req = requests.get('https://randomfox.ca/floof')
#    req = requests.get('https://aws.random.cat/meow')
#    from requests import get
#    num = random.randint(1,1600)
#    source = get(f'https://aws.random.cat/view/{num}').text
#    if "id=\"cat" in source:
#        print(source.split("src=\"")[1].split("\"")[0])
#    else:
#        print("Incorrect id")
#    if req.status_code == 200:
#        r_json = req.json()
#        url = r_json['url']
        # url.split("/")[-1]
#    return url
#    img = (requests.get("https://randomfox.ca/floof/").json())["file"]
#    res = requests.get(img)
#    return res.content
#     url = ""
#    req = requests.get('https://aws.random.cat/meow')
#    r_json = req.json()
#    url = r_json['url']
        # url.split("/")[-1]
#    return url

#    querystring = {"top":"Top Text","bottom":"Bottom Text","meme":"Condescending-Wonka","font_size":"50","font":"Impact"}

#    headers = {
#	    "X-RapidAPI-Host": "ronreiter-meme-generator.p.rapidapi.com",
#	    "X-RapidAPI-Key": "SIGN-UP-FOR-KEY"
#}

#     response = requests.request("GET", url, headers=headers, params=querystring)

#    return response
# ---------------------------------------------------------------------

# --------------------------------------------------------------------

def get_startup(chat_id):
     global bot
     bot.send_message(chat_id, text="генерирую новые идеи с помощью двух случайных параметров на Eng")
     startup = requests.get('http://itsthisforthat.com/api.php?json')
     soup = bs4.BeautifulSoup(startup.text, "html.parser")
     return  soup


#     array_startup = []
#     startup = requests.get('http://itsthisforthat.com/api.php?json')
 #    if startup.status_code == 200:
  #       soup1 = bs4.BeautifulSoup(startup.text, "html.parser")
  #       result_find = soup1.select('this')
  #       for result in result_find:
 #            array_startup.append(result.getText().strip())
 #    if len(array_startup) > 0:
 #        return array_startup[0]
    # else:
   #      return ""


# -----------------------------------------------------------------------
def get_ManOrNot(chat_id):
    global bot

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить", url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")

# ---------------------------------------------------------------------
#def get_randomFilm():
#    url = 'https://randomfilm.ru/'
#    infoFilm = {}
#    req_film = requests.get(url)
#    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
#    result_find = soup.find('div', align="center", style="width: 100%")
#    infoFilm["Наименование"] = result_find.find("h2").getText()
#    names = infoFilm["Наименование"].split(" / ")
#    infoFilm["Наименование_rus"] = names[0].strip()
#    if len(names) > 1:
#        infoFilm["Наименование_eng"] = names[1].strip()

#    images = []
#    for img in result_find.findAll('img'):
#        images.append(url + img.get('src'))
#    infoFilm["Обложка_url"] = images[0]

#    details = result_find.findAll('td')
#    infoFilm["Год"] = details[0].contents[1].strip()
#    infoFilm["Страна"] = details[1].contents[1].strip()
#    infoFilm["Жанр"] = details[2].contents[1].strip()
#    infoFilm["Продолжительность"] = details[3].contents[1].strip()
#    infoFilm["Режиссёр"] = details[4].contents[1].strip()
#    infoFilm["Актёры"] = details[5].contents[1].strip()
#    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
#    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

#    return infoFilm
#    return url_block

# ---------------------------------------------------------------------


bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()

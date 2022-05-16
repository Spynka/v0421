from aiogram import types, executor, Dispatcher, Bot
import requests
import bs4

@bot.message_handler(content_types=['text'])
def parser(message):
    url= "https://kz.e-katalog.com/ek-list.php?search_=" + message.text
    request=requests.get(url)
    soup = bs4.BeautifulSoup(request.text, "html.parser")

    all_links = soup.find_all("a", class_="model-short-title")
    for link in all_links:
        url = "https://kz.e-katalog.com/"+ link["href"]
        request = requests.get(url)
        soup = bs4.BeautifulSoup(request.text, "html.parser")

        name = soup.find("div", class_="fix-menu-name")
        price = name.find("a").text
        name.find("a").extract()
        name = name.text

        img = soup.find("div",class_="img200")
        img = img.findChildren("img")[0]
        img = "https://kz.e-katalog.com/"+ img["src"]

        bot.send_photo(chat_id,img, caption="<b>" + name + "</b>\n<i>"+price + f"</i>\n<a href='{url}'>Ссфлка на сайт</a>",
        parse_mode='HTML')

        if all_links.index(link)==2:
            break
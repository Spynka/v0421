#from aiogram import types, executor, Dispatcher, Bot
#import requests
#import bs4

#@bot.message_handler(content_types=['text'])
#def parser(message):
#    url= "https://kz.e-katalog.com/ek-list.php?search_=" + message.text
#    request=requests.get(url)
#    soup = bs4.BeautifulSoup(request.text, "html.parser")

#    all_links = soup.find_all("a", class_="model-short-title")
#    for link in all_links:
#       url = "https://kz.e-katalog.com/"+ link["href"]
 #       request = requests.get(url)
 #       soup = bs4.BeautifulSoup(request.text, "html.parser")

 #       name = soup.find("div", class_="fix-menu-name")
 #       price = name.find("a").text
#        name.find("a").extract()
 #       name = name.text

#        img = soup.find("div",class_="img200")
 #       img = img.findChildren("img")[0]
 #       img = "https://kz.e-katalog.com/"+ img["src"]

   #     bot.send_photo(chat_id,img, caption="<b>" + name + "</b>\n<i>"+price + f"</i>\n<a href='{url}'>Ссфлка на сайт</a>",
  #      parse_mode='HTML')

 #       if all_links.index(link)==2:
  #          break

from aiogram import types, executor, Dispatcher, Bot
import requests
import bs4

@bot.message_handler(content_types=['text'])
def parser(message):
    url= "https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search=" + message.text
    request=requests.get(url)
    soup = bs4.BeautifulSoup(request.text, "html.parser")

    all_links = soup.find_all("a", class_="product-card__main j-card-link")
    for link in all_links:
        url =link["href"]
        request = requests.get(url)
        soup = bs4.BeautifulSoup(request.text, "html.parser")

        Brand_name = soup.find("div", class_="product-card__brand")
        price = Brand_name.findChildren("div")[0].text

        Bname = soup.find("div", class_="product-card__brand-name")
        name = Bname.find("span").text

        img = soup.find("div",class_="product-card__img-wrap img-plug j-thumbnail-wrap")
        img = img.findChildren("img")[0]
        img = img["src"]

        bot.send_photo(chat_id,img, caption="<b>" + name + "</b>\n<i>"+price + f"</i>\n<a href='{url}'>Ссылка на сайт</a>",
        parse_mode='HTML')

        if all_links.index(link)==2:
            break
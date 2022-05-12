import requests
import json
import html
#answer = requests.get('https://zenquotes.io/api/random')
#b=(json.loads(answer.text))
#print (html.unescape(b))
req = requests.get('http://anekdotme.ru/random')
print (json.loads(req.text))
import requests
import json
import html
#answer = requests.get('https://zenquotes.io/api/random')
#b=(json.loads(answer.text))
#print (html.unescape(b))
req = requests.get('https://api.thecatapi.com/v1/images/search')
print (req.status_code)
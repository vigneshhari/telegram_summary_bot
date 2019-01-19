from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import telepot
import json
import os

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import requests
from bs4 import BeautifulSoup
import os

import json
import urllib
from urllib.request import urlopen
import urllib.parse
from pprint import pprint

def url_fix(s, charset='utf-8'):
    #if isinstance(s, unicode):
    #    s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(s)
    path = urllib.parse.quote(path, '/%')
    qs = urllib.parse.quote_plus(qs, ':&=')
    return urllib.parse.urlunsplit((scheme, netloc, path, qs, anchor))


def search(request):
    q=request
    r = requests.get('https://duckduckgo.com/html/?q={}'.format(q))
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('a', attrs={'class':'result__a'}, href=True)
    link = results[0]
    url = link['href']
    o = urllib.parse.urlparse(url)
    d = urllib.parse.parse_qs(o.query)
    url = (d['uddg'][0])
    """url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyDgiTjHdPpuICe6erDCbnsXtXLHRsFVirA&cx=000472016662631019324:xexwwqkpope&q="+q
    print(url)
    url = url_fix(url)
    print(url)
    response = requests.get(url)
    if(response.ok):
        data = json.loads(response.content.decode('utf-8'))
    url = data['items'][0]['link']
    print(url)
    """
    print(url)
    LANGUAGE = "english"
    SENTENCES_COUNT = 100
    out=[]
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        out.append(str(sentence))
    r = requests.get(url)
    test = url.split("/")
    urlval = str('/'.join(test[:3]))
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    temp = []
    for link in soup.find_all('img'):
        image = link.get("src")
        temp.append(image)
        break
    for loc,i in enumerate(temp):
        if(i[0] == "/"):
            temp[loc] =   urlval + temp[loc]
    print("Content Returned")
    return ({'content' : str("\n".join(out)) + '  '.join(temp)  })


@csrf_exempt
def webhook(request):
    received_json_data=json.loads(str(request.body,"UTF-8"))
    pprint(received_json_data)
    chat_id = received_json_data["message"]["from"]["id"]
    message = received_json_data["message"]["text"]
    bot = telepot.Bot(os.environ.get('BOT_TOKEN'))
    out =  "." + search(message)["content"]
    lim = 4095
    for i in range((len(out) // lim) ):
        bot.sendMessage(chat_id, out[(i*lim) : ((i+1) * lim)] )
    #print("out" , out)
    if((len(out) // lim) == 0):bot.sendMessage(chat_id, out)
    return JsonResponse({})

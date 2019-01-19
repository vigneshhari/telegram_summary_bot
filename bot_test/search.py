from __future__ import absolute_import
from __future__ import division, print_function


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


def url(request):
    if(request.GET.get('url','url').lower() not in  ['url','image']):
        url = request.GET.get('url','url')
        print(url)
        LANGUAGE = "english"
        SENTENCES_COUNT = 5
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
        for loc,i in enumerate(temp):
            if(i[0] == "/"):
                temp[loc] =   urlval + temp[loc]
        return ({'content' : str("\n".join(out)) + '  '.join(temp)  })


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
    return ({'content' : str("\n".join(out)) + '  '.join(temp)  })


pprint(search("hacktool"))

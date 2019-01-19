from bs4 import BeautifulSoup
import urllib.parse
import requests

r = requests.get('https://duckduckgo.com/html/?q=troj_malkryp')
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all('a', attrs={'class':'result__a'}, href=True)
link = results[0]
url = link['href']
o = urllib.parse.urlparse(url)
d = urllib.parse.parse_qs(o.query)
print(d['uddg'][0])

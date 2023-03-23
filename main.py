import requests
from bs4 import BeautifulSoup 
import re
from pprint import pprint

#r = requests.get('http://books.toscrape.com/')
#print(r.content)



#pageOrder = soup.find_all("li", class_="current")[0].text.strip()
##currentPage = re.search(r'Page (.*?) of', pageOrder).group(1)
#maxPageRange = re.search(r'(?<=of ).*', pageOrder)[0]

fivestar_href_List = []
#print(maxPageRange)
for i in range(1, 10):
    r = requests.get('https://books.toscrape.com/catalogue/page-{0}.html'.format(i))
    soup = BeautifulSoup(r.content, 'html.parser')
    pageRange = soup.find_all("li", class_="current")[0].text.strip()
    currentPage = re.search(r'Page (.*?) of', pageRange).group(1)
    for item in soup.find_all("p", class_="star-rating Five"):
        parentContainer = item.parent
        itemHref = "http://books.toscrape.com/catalogue/{0}".format(parentContainer.find("h3").find("a")['href'])
        fivestar_href_List.append([currentPage, itemHref])

pprint(fivestar_href_List)

f = open("test.html", "w")
f.write(r.text)
f.close()
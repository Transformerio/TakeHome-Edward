import requests
from bs4 import BeautifulSoup 
import re
from pprint import pprint
import csv

#r = requests.get('http://books.toscrape.com/')
#print(r.content)



#pageOrder = soup.find_all("li", class_="current")[0].text.strip()
##currentPage = re.search(r'Page (.*?) of', pageOrder).group(1)
#maxPageRange = re.search(r'(?<=of ).*', pageOrder)[0]

def writeToFile(content):
    f = open("test.html", "w", encoding="utf-8")
    f.write(content)
    f.close()

def WriteToCSV(filename, header, data):
    """
    - data must be an array of dicts
    - elements must not contain nested dicts
    - data keys = header
    """
    
    with open(filename + '.csv', 'w') as csvfile:
        print("[WriteToCSV] {0}.csv has been opened and is currently being written ...".format(filename))
        csvwriter = csv.DictWriter(csvfile, fieldnames = header)
        csvwriter.writeheader()
        csvwriter.writerows(data)
        print("[WriteToCSV] {0}.csv has successfully been written to.".format(filename))


def GetFiveStarBooks():
    fivestar_href_List = []
    headers = [
        "Title", 
        "Price", 
        "UPC", 
        "Product Type", 
        "Price (excl. tax)", 
        "Price (incl. tax)", 
        "Tax", 
        "Availability", 
        "Number of reviews"
    ]
    ##TODO: FIX THIS RANGE
    for i in range(1, 10):
        r = requests.get('https://books.toscrape.com/catalogue/page-{0}.html'.format(i))
        soup = BeautifulSoup(r.content, 'html.parser')
        page_range = soup.find_all("li", class_="current")[0].text.strip()
        page_current = re.search(r'Page (.*?) of', page_range).group(1)
        # Iterates through all the books in the page with a 5 star rating
        for book in soup.find_all("p", class_="star-rating Five"):
            book_parent_container = book.parent
            book_href = "http://books.toscrape.com/catalogue/{0}".format(book_parent_container.find("h3").find("a")['href'])
            book_detail = requests.get(book_href)
            bookSoup = BeautifulSoup(book_detail.content, 'html.parser')
            productmain_container = bookSoup.find_all("div", class_="col-sm-6 product_main")
            book_title = productmain_container[0].find("h1").text
            book_price = productmain_container[0].find("p", class_="price_color").text

            product_information_table = bookSoup.find("table", class_="table table-striped")
            product_details = {
                "Title": book_title,
                "Price": book_price,
                "UPC": None,
                "Product Type": None,
                "Price (excl. tax)": None,
                "Price (incl. tax)": None,
                "Tax": None,
                "Availability": None,
                "Number of reviews": None
            }

            for row in product_information_table.find_all("tr"):
                product_details[row.find("th").text] = row.find("td").text

            fivestar_href_List.append(product_details)
        print(page_range)
    return headers, fivestar_href_List

def GetHistoricalFictionBooks():
    ### Gettomg HistoricalFictionBooks over $30 in price
    fivestar_href_List = []
    headers = [
        "Title", 
        "Price", 
        "UPC", 
        "Product Type", 
        "Price (excl. tax)", 
        "Price (incl. tax)", 
        "Tax", 
        "Availability", 
        "Number of reviews"
    ]
    ##TODO: FIX THIS RANGE
    for i in range(1, 10):
        r = requests.get('https://books.toscrape.com/catalogue/page-{0}.html'.format(i))
        soup = BeautifulSoup(r.content, 'html.parser')
        page_range = soup.find_all("li", class_="current")[0].text.strip()
        page_current = re.search(r'Page (.*?) of', page_range).group(1)
        # Iterates through all the books in the page with a 5 star rating
        for price in soup.find_all("p", class_="price_color"):
            if (float(str(price.text)[1:]) > 30.00):
                book_parent_container = price.parent.parent
                book_href = "http://books.toscrape.com/catalogue/{0}".format(book_parent_container.find("h3").find("a")['href'])
                book_detail = requests.get(book_href)
                bookSoup = BeautifulSoup(book_detail.content, 'html.parser')
                productmain_container = bookSoup.find_all("div", class_="col-sm-6 product_main")
                book_title = productmain_container[0].find("h1").text
                book_price = productmain_container[0].find("p", class_="price_color").text

                product_information_table = bookSoup.find("table", class_="table table-striped")
                product_details = {
                    "Title": book_title,
                    "Price": book_price,
                    "UPC": None,
                    "Product Type": None,
                    "Price (excl. tax)": None,
                    "Price (incl. tax)": None,
                    "Tax": None,
                    "Availability": None,
                    "Number of reviews": None
                }

                for row in product_information_table.find_all("tr"):
                    product_details[row.find("th").text] = row.find("td").text

                fivestar_href_List.append(product_details)
            
    return headers, fivestar_href_List

#book_fivestar_data = GetFiveStarBooks()
book_overprice_data = GetHistoricalFictionBooks()
#pprint(book_overprice_data[1])
WriteToCSV("test", book_overprice_data[0], book_overprice_data[1])



